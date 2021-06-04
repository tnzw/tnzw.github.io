# OpensslAes256CbcDecoder.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class OpensslAes256CbcDecoder(object):
  """\
OpensslAes256CbcDecoder(key, iv, **opt)

Decodes/decrypts from OpenSSL AES-256-CBC like stream.

password => bytes()
         => str()
opt:
  salt => None      : (default) get the salt from stream.
          bytes(8)  : use specific salt.
          b""       : no salt.
  iv   => None      : (default) generate iv from password.
       => [uint32]*4: use specific iv.
  cast => bytes     : (default) cast the returned transcoded values to bytes.
       => None      : do not cast, returns transcoded byte iterator instead.
  cache             : internal use only.
  decoder           : internal use only.

Interfaces:
- copyable (ie. `copy()`)
- transcoder (ie. `transcode(iterable=None, *, stream=False)`)
"""
  @staticmethod
  def uint32_bigendian_decode(bb): return tuple((b4[3] | (b4[2] << 8) | (b4[1] << 16) | (b4[0] << 24)) for b4 in iter_blocks(bb, 4, errors="strict"))
  def copy(self): return self.__class__(**{k: getattr(v, "copy", lambda: v)() for k, v in self.__dict__.items()})
  def __init__(self, password, *, salt=None, iv=None, cast=bytes, cache=b"", decoder=None):
    if isinstance(password, str): password = password.encode("UTF-8")
    self.password = password
    self.salt = salt
    self.cast = cast
    self.cache = cache
    self.iv = iv
    self.decoder = decoder
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
      it = iterable
      salt = self.salt
      decoder = self.decoder
      if decoder is None:
        if salt is None:
          # no salt extracted, please extract
          it = (_ for _ in it)
          salt = bytes(b for _, b in zip(range(16), iter_chain(self.cache, it)))
          if len(salt) != 16:
            if stream:
              self.cache = salt  # + bytes(it) ← useless 'cause len(salt) < 16
              return
            raise ValueError("EOF reached before getting salt")  # error reading input file
          if salt[:8] == b"Salted__": salt = salt[8:]
          else: raise ValueError("invalid salt prefix")  # bad magic number
        key, iv = [0]*32, [0]*16
        OPENSSL_EVP_BytesToKey(sha256_sumbytes, 32, salt, self.password, 1, key, 32, iv, 16)
        #OPENSSL_EVP_BytesToKey(md5_sumbytes, 16, salt, self.password, 1, key, 32, iv, 16)
        key = self.uint32_bigendian_decode(key)
        if self.iv is None: iv = self.uint32_bigendian_decode(iv)
        else: iv = self.iv
        decoder = AesCbcPkcs7Decoder(key, iv, cast=None)
        yield from decoder.transcode(it, stream=stream)
        self.cache = b""
        self.salt = salt
        self.decoder = decoder
      else:
        yield from decoder.transcode(iter_chain(self.cache, it), stream=stream)
    return it() if self.cast is None else self.cast(it())
  decode = transcode
OpensslAes256CbcDecoder._required_globals = [
  "AesCbcPkcs7Decoder",
  "OPENSSL_EVP_BytesToKey",
  "iter_blocks",
  "iter_chain",
  "sha256_sumbytes",
]
