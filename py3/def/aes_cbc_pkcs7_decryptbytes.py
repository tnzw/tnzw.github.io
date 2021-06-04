# aes_cbc_pkcs7_decryptbytes.py Version 1.1.0
# Copyright (c) 2020-2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def aes_cbc_pkcs7_decryptbytes():

  def aes_cbc_pkcs7_decryptbytes(bytes_data, key, iv):
    res = []
    for _ in _iter(bytes_data, key, iv): res.append(_)
    return b"".join(res)

  def _iter(iterable_bytes, key, iv):
    # checks PKCS#7 padding

    # iterable_bytes = [..]
    #   an array of uint8 or a byte string
    # key = [..]
    #   an array of 4/6/8 uint32
    # iv = [..]
    #   an array of 4 uint32

    def iter_block(iterable, block_size):
      block = [None]*block_size
      i = 0
      for _ in iterable:
        block[i] = _
        i += 1
        if i == block_size:
          yield block
          i = 0
      if i: raise ValueError("invalid length")
      #if i:
      #  block[:] = block[:i]
      #  yield block

    def transcode_uint8_to_uint32_bigendian(iterable_bytes):
      return [uint32_bigendian_frombytes(_) for _ in iter_block(iterable_bytes, 4)]

    def transcode_uint32_to_uint8_bigendian(block):
      return [_ for uint32 in block for _ in uint32_bigendian_tobytes(uint32)]

    aes = Aes(key)

    if type(iterable_bytes) in (bytes, bytearray) and len(iterable_bytes) % 16:
      # avoid to iterate to the hole iterable_bytes
      raise ValueError("invalid length")  # Cannot decrypt: invalid input length

    uncipher_bytes = b""
    for block in iter_block(iterable_bytes, 16):
      if uncipher_bytes: yield uncipher_bytes
      # The raise below has been moved to iter_block
      #if len(block) != 16: raise ValueError("invalid length")  # Cannot decrypt: invalid input length
      block = transcode_uint8_to_uint32_bigendian(block)
      out = aes.decrypt(block)
      for i in range(4): out[i] = out[i] ^ iv[i]
      uncipher_bytes = bytes(transcode_uint32_to_uint8_bigendian(out))
      iv = block

    n = uncipher_bytes[-1]
    if n > 16 or n == 0: raise ValueError("invalid padding")  # Cannot decrypt: invalid padding
    for i in range(2, n + 1):
      if uncipher_bytes[-i] != n:
        raise ValueError("invalid padding")  # Cannot decrypt: invalid padding
    if n != 16: yield uncipher_bytes[:-n]
  aes_cbc_pkcs7_decryptbytes.iter = _iter
  return aes_cbc_pkcs7_decryptbytes
aes_cbc_pkcs7_decryptbytes = aes_cbc_pkcs7_decryptbytes()
aes_cbc_pkcs7_decryptbytes._required_globals = [
  "Aes",
  "uint32_bigendian_frombytes",
  "uint32_bigendian_tobytes",
]
