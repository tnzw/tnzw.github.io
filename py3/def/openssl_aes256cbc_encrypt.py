# openssl_aes256cbc_encrypt.py Version 1.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def openssl_aes256cbc_encrypt(message, password, salt=None, iv=None):
  # message = "..." or b"..." or [uint8..]
  # password = "..." or b"..." or [uint8..]
  # salt = b"0 or 8 bytes" or [] or [uint8 x8]  (optional)
  #   None -> salt automatically generated
  #   b"...x8" -> with salt
  #   b"" -> no salt (no salt written in the output)
  # iv = b"16 bytes" or [uint8 x16]  (optional)

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

  if isinstance( message, str):  message =  message.encode("UTF-8")
  if isinstance(password, str): password = password.encode("UTF-8")

  if salt is None:
    salt = os.urandom(8)
  if iv and len(iv) != 16:
    raise ValueError("invalid iv length (!= 16 and != 0)")

  key, generated_iv = [0]*32, [0]*16
  #OPENSSL_EVP_BytesToKey(XXXsha256_sumbytes, 32, salt, password, 1, key, 32, generated_iv, 16)
  OPENSSL_EVP_BytesToKey(md5_sumbytes, 16, salt, password, 1, key, 32, generated_iv, 16)
  message = aes_cbc_pkcs7_encryptbytes(message, transcode_uint8_to_uint32_bigendian(key), transcode_uint8_to_uint32_bigendian(iv if iv else generated_iv))
  #if message is None: return None  # XXX possible ?
  if not salt: return message
  return b"Salted__" + bytes(salt) + message
openssl_aes256cbc_encrypt._required_globals = [
  "os",
  "OPENSSL_EVP_BytesToKey",
  "aes_cbc_pkcs7_encryptbytes",
  "uint32_bigendian_frombytes",
  "md5_sumbytes",
]
