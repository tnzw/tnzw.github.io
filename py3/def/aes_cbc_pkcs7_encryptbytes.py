# aes_cbc_pkcs7_encryptbytes.py Version 1.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def aes_cbc_pkcs7_encryptbytes(bytes_data, key, iv):
  # pad with PKCS#7

  # bytes_data = [..]
  #   an array of uint8 or a byte string
  # key = [..]
  #   an array of 4/6/8 uint32
  # iv = [..]
  #   an array of 4 uint32

  def iter_with_padding(iterable):
    L = 0
    for _ in iterable:
      yield _
      L += 1
    L16 = L % 16
    if L16:
      n = 16 - L16
      for _ in range(n):
        yield n

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

  def transcode_uint32_to_uint8_bigendian(block):
    return [_ for uint32 in block for _ in uint32_bigendian_tobytes(uint32)]

  cipher_bytes = b""
  aes = Aes(key)

  for block in iter_block(iter_with_padding(bytes_data), 16):
    block = transcode_uint8_to_uint32_bigendian(block)
    for i in range(4): block[i] = block[i] ^ iv[i]
    iv = aes.encrypt(block)
    cipher_bytes += bytes(transcode_uint32_to_uint8_bigendian(iv))

  return cipher_bytes
aes_cbc_pkcs7_encryptbytes._required_globals = [
  "Aes",
  "uint32_bigendian_frombytes",
  "uint32_bigendian_tobytes",
]
