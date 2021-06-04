# OpensslAes256CbcEncoder.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class OpensslAes256CbcEncoder(object):
  """\
OpensslAes256CbcEncoder(key, iv, **opt)

Encodes/encrypts to OpenSSL AES-256-CBC like stream.

password => bytes()
         => str()
salt     => bytes(8): example: os.urandom(8)
         => b""     : no salt.
opt:
  iv   => None      : (default) generate iv from password.
       => [uint32]*4: use specific iv.
  cast => bytes     : (default) cast the returned transcoded values to bytes.
       => None      : do not cast, returns transcoded byte iterator instead.
  encoder           : internal use only.

Interfaces:
- copyable (ie. `copy()`)
- transcoder (ie. `transcode(iterable=None, *, stream=False)`)
"""
  @staticmethod
  def uint32_bigendian_decode(bb): return tuple((b4[3] | (b4[2] << 8) | (b4[1] << 16) | (b4[0] << 24)) for b4 in iter_blocks(bb, 4, errors="strict"))
  def copy(self): return self.__class__(**{k: getattr(v, "copy", lambda: v)() for k, v in self.__dict__.items()})
  def __init__(self, password, salt, *, iv=None, cast=bytes, encoder=None):
    if isinstance(password, str): password = password.encode("UTF-8")
    self.password = password
    self.salt = salt  # ex: os.urandom(8)
    self.cast = cast
    self.iv = iv
    self.encoder = encoder
  def transcode(self, iterable=None, *, stream=False):
    """\
transcode(iterable, **opt)

iterable: a byte iterable value (defaults to None)
opt:
  stream => False: tells the transcoder that it is the last transcode operation
         => True
"""
    if iterable is None: iterable = ()
    def it():
      encoder = self.encoder
      if encoder is None:
        key, iv = [0]*32, [0]*16
        OPENSSL_EVP_BytesToKey(sha256_sumbytes, 32, self.salt, self.password, 1, key, 32, iv, 16)
        #OPENSSL_EVP_BytesToKey(md5_sumbytes, 16, self.salt, self.password, 1, key, 32, iv, 16)
        key = self.uint32_bigendian_decode(key)
        if self.iv is None: iv = self.uint32_bigendian_decode(iv)
        else: iv = self.iv
        encoder = AesCbcPkcs7Encoder(key, iv)
        if self.salt:
          yield from b"Salted__"
          yield from bytes(self.salt)
        yield from encoder.transcode(iterable, stream=stream)
        self.encoder = encoder
      else:
        yield from encoder.transcode(iterable, stream=stream)
    return it() if self.cast is None else self.cast(it())
  encode = transcode
OpensslAes256CbcEncoder._required_globals = [
  "AesCbcPkcs7Encoder",
  "iter_blocks",
  "sha256_sumbytes",
]
