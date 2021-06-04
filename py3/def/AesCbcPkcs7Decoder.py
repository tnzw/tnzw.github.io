# AesCbcPkcs7Decoder.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class AesCbcPkcs7Decoder(object):
  """\
AesCbcPkcs7Decoder(key, iv, **opt)

Decodes/decrypts from AES CBC with PKCS#7 padding.

key => [uint32]*4
    => [uint32]*6
    => [uint32]*8
iv  => [uint32]*4
opt:
  cast => bytes  : (default) cast the returned transcoded values to bytes.
       => None   : do not cast, returns transcoded byte iterator instead.
  cache          : internal use only.
  last_unciphered: internal use only.

Interfaces:
- copyable (ie. `copy()`)
- transcoder (ie. `transcode(iterable=None, *, stream=False)`)
"""
  @staticmethod
  def uint32_bigendian_decode(bb): return tuple((b4[3] | (b4[2] << 8) | (b4[1] << 16) | (b4[0] << 24)) for b4 in iter_blocks(bb, 4, errors="strict"))
  @staticmethod
  def uint32_bigendian_encode(u32b): return bytes(b for u32 in u32b for b in ((u32 >> 24) & 0xFF, (u32 >> 16) & 0xFF, (u32 >> 8) & 0xFF, u32 & 0xFF))
  def copy(self): return self.__class__(**{k: v for k, v in self.__dict__.items()})
  def __init__(self, key, iv, *, cast=bytes, cache=(), last_unciphered=b""):
    self.key = key
    self.iv = iv
    self.cast = cast
    self.cache = cache
    self.last_unciphered = last_unciphered
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
    def it():
      iv = self.iv
      unciphered = self.last_unciphered
      for block in iter_blocks(iter_chain(self.cache, iterable), 16, errors="truncate" if stream else "strict"):
        if unciphered:
          yield from unciphered
          unciphered = b""
        if len(block) != 16:
          self.last_unciphered = unciphered
          self.cache = tuple(block)
          self.iv = iv
          return
        block = self.uint32_bigendian_decode(block)
        out = aes.decrypt(block)
        for i in range(4): out[i] = out[i] ^ iv[i]
        unciphered = self.uint32_bigendian_encode(out)
        iv = block  # block is tuple here
      if stream:
        self.last_unciphered = unciphered
        self.cache = ()
        self.iv = iv
        return
      n = unciphered[-1]
      if n > 16 or n == 0:
        raise ValueError("invalid padding")  # Cannot decrypt: invalid padding
      for i in range(2, n + 1):
        if unciphered[-i] != n:
          raise ValueError("invalid padding")  # Cannot decrypt: invalid padding
      if n != 16:
        yield from unciphered[:-n]
      self.last_unciphered = b""
      self.cache = ()
      self.iv = iv
    return it() if self.cast is None else self.cast(it())
  decode = transcode
AesCbcPkcs7Decoder._required_globals = [
  "Aes",
  "iter_blocks",
  "iter_chain",
]
