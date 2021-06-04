# AesCbcPkcs7Encoder.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class AesCbcPkcs7Encoder(object):
  """\
AesCbcPkcs7Encoder(key, iv, **opt)

Encodes/encrypts to AES CBC with PKCS#7 padding.

key => [uint32]*4
    => [uint32]*6
    => [uint32]*8
iv  => [uint32]*4
opt:
  cast => bytes  : (default) cast the returned transcoded values to bytes
       => None   : do not cast, returns transcoded byte iterator instead
  cache          : internal use only

Interfaces:
- copyable (ie. `copy()`)
- transcoder (ie. `transcode(iterable=None, *, stream=False)`)
"""
  @staticmethod
  def uint32_bigendian_decode(bb): return list((b4[3] | (b4[2] << 8) | (b4[1] << 16) | (b4[0] << 24)) for b4 in iter_blocks(bb, 4, errors="strict"))
  @staticmethod
  def uint32_bigendian_encode(u32b): return (b for u32 in u32b for b in ((u32 >> 24) & 0xFF, (u32 >> 16) & 0xFF, (u32 >> 8) & 0xFF, u32 & 0xFF))
  def copy(self): return self.__class__(**{k: v for k, v in self.__dict__.items()})
  def __init__(self, key, iv, *, cast=bytes, cache=()):
    self.key = key
    self.iv = iv
    self.cast = cast
    self.cache = cache
  def transcode(self, iterable=None, *, stream=False):
    """\
transcode(iterable, **opt)

iterable: a byte iterable value (defaults to None)
opt:
  stream => False: tells the transcoder that it is the last transcode operation
         => True
"""
    if iterable is None: iterable = ()
    aes = Aes(self.key)
    def encrypt(block, iv):
      block = self.uint32_bigendian_decode(block)
      for i in range(4): block[i] = block[i] ^ iv[i]
      return aes.encrypt(block)
    def it():
      iv = self.iv
      for block in iter_blocks(iter_chain(self.cache, iterable), 16, errors="truncate"):
        len_block = len(block)
        if len_block != 16:
          if stream:
            self.cache = bytes(block)
            self.iv = tuple(iv)
            return
          delta = 16 - len_block
          block.extend([delta] * delta)
          iv = encrypt(block, iv)
          yield from self.uint32_bigendian_encode(iv)
          self.cache = b""
          self.iv = tuple(iv)
          return
        iv = encrypt(block, iv)
        yield from self.uint32_bigendian_encode(iv)
      if not stream:
        iv = encrypt([16] * 16, iv)
        yield from self.uint32_bigendian_encode(iv)
      self.cache = b""
      self.iv = tuple(iv)
    return it() if self.cast is None else self.cast(it())
  encode = transcode
AesCbcPkcs7Encoder._required_globals = [
  "Aes",
  "iter_blocks",
  "iter_chain",
]
