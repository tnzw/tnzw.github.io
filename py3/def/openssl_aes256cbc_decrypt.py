# openssl_aes256cbc_decrypt.py Version 1.1.0-1
# Copyright (c) 2020-2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def openssl_aes256cbc_decrypt():

  def openssl_aes256cbc_decrypt(message, password, with_salt=None, iv=None):
    # message = "..." or b"..." or [uint8..]
    # password = "..." or b"..." or [uint8..]
    # with_salt = bool  (optional)
    #   None -> extract salt if any
    #   True -> extract salt, fail if none is found
    #   False -> do not extract salt
    # iv = b"16 bytes" or [uint8 x16]  (optional)
    res = []
    for _ in _iter(message, password, with_salt, iv): res.append(_)
    return b"".join(res)

  def _iter(message, password, with_salt=None, iv=None):

    def iter_block(iterable, block_size):
      block = [None]*block_size
      i = 0
      for _ in iterable:
        block[i] = _
        i += 1
        if i == block_size:
          yield block
          i = 0

    def transcode_uint8_to_uint32_bigendian(bytes_data):
      return [uint32_bigendian_frombytes(_) for _ in iter_block(bytes_data, 4)]

    def iter(iterable):
      for _ in iterable:
        yield _

    def iter_slice(iterable, end):
      for _ in iterable:
        yield _
        end -= 1
        if end <= 0:
          break

    def iter_n(*iterables):
      for it in iterables:
        for _ in it:
          yield _

    if isinstance( message, str):  message =  message.encode("UTF-8")
    if isinstance(password, str): password = password.encode("UTF-8")

    if iv and len(iv) != 16:
      raise ValueError("invalid iv length (!= 16 and != 0)")

    key, generated_iv = [0]*32, [0]*16
    salt = b""

    try:
      L = len(message)
      if L: message[0]
    except TypeError: L = None

    if with_salt in (None, True):
      if L is None:
        message = iter(message)
        extract = bytes(_ for _ in iter_slice(message, 16))
        if len(extract) == 16 and extract[:8] == b"Salted__":
          salt = extract[8:16]
        else:
          if with_salt: raise ValueError("no salt found")  # salt desired but not found
          message = iter_n(extract, message)
      else:
        extract = message[:16]
        if len(extract) == 16 and extract[:8] == b"Salted__":
          salt = extract[8:16]
          message = message[16:]
        elif with_salt: raise ValueError("no salt found")  # salt desired but not found

    OPENSSL_EVP_BytesToKey(sha256_sumbytes, 32, salt, password, 1, key, 32, generated_iv, 16)
    #OPENSSL_EVP_BytesToKey(md5_sumbytes, 16, salt, password, 1, key, 32, generated_iv, 16)
    return aes_cbc_pkcs7_decryptbytes.iter(message, transcode_uint8_to_uint32_bigendian(key), transcode_uint8_to_uint32_bigendian(iv if iv else generated_iv))

  openssl_aes256cbc_decrypt.iter = _iter
  return openssl_aes256cbc_decrypt

openssl_aes256cbc_decrypt = openssl_aes256cbc_decrypt()
openssl_aes256cbc_decrypt._required_globals = [
  "OPENSSL_EVP_BytesToKey",
  "aes_cbc_pkcs7_decryptbytes",
  "uint32_bigendian_frombytes",
  #"md5_sumbytes",
  "sha256_sumbytes",
]
