# Base64Decoder.py Version 1.1.0-2
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class Base64Decoder(object):
  """\
Base64Decoder(**opt)

opt:
  errors => "strict"          : (default) raise on any error
         => "pad"             : add base64 padding before EOF if necessary (eg b"RS" → b"RS==")
         => "ignore"          : ignore unexpected characters
                                ex: b"R=K==A=B=L~OZ" → b"RK==ABLO"
  scheme : The scheme to use bytes(256)
         => (default) "standard" (or STANDARD_SCHEME)
         => "url" (or URL_SCHEME)
         => <CUSTOM_SCHEME> (`compute_scheme(codes, padding, ignored)`)
  cast => bytes: (default) cast the returned transcoded values to bytes.
       => None : do not cast, returns transcoded byte iterator instead.
  cache    : internal use only.
  state    : internal use only.

Interfaces:
- copyable (ie. `copy()`)
- transcoder (ie. `transcode(iterable=None, *, stream=False)`)
"""
  STANDARD_CODES = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
  URL_CODES = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
  @staticmethod
  def compute_scheme(codes=b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/', padding=b"=", ignored=b" \n\r\t"):
    """\
opt:
  codes   => bytes(64) : the list of code to use for decoding
  ignored => b" \n\r\t": ignores each one of these bytes from input
  padding => b"="      : each one of these bytes may be concidered as padding
"""
    struct = bytearray([255] * 256)
    for _ in ignored: struct[_] = 65
    for _ in padding: struct[_] = 64
    for i, _ in enumerate(codes): struct[_] = i
    return bytes(struct)
  STANDARD_SCHEME = b'\xff\xff\xff\xff\xff\xff\xff\xff\xffAA\xff\xffA\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffA\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff>\xff\xff\xff?456789:;<=\xff\xff\xff@\xff\xff\xff\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\xff\xff\xff\xff\xff\xff\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
  URL_SCHEME = b'\xff\xff\xff\xff\xff\xff\xff\xff\xffAA\xff\xffA\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffA\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff>\xff\xff456789:;<=\xff\xff\xff@\xff\xff\xff\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\xff\xff\xff\xff?\xff\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
  def copy(self): return self.__class__(**{k: v for k, v in self.__dict__.items()})
  def __init__(self, *, errors="strict", scheme="standard", cast=bytes, cache=0, state=0):
    self.errors = errors
    self.scheme = {"standard": self.STANDARD_SCHEME, "url": self.URL_SCHEME}.get(scheme, scheme)
    self.cast = cast
    self.cache = cache
    self.state = state
  def transcode(self, iterable=None, *, stream=False):
    """\
transcode(iterable, **opt)

iterable: a byte iterable value (defaults to None)
opt:
  stream => False: tells the transcoder that it is the last transcode operation
         => True
"""
    if iterable is None: iterable = ()
    # states are:
    # 0 => [?...]
    # 1 => [A?..]
    # 2 => [AB?.]
    # 3 => [ABC?]
    # 4 => [AB=?]

    def check_errors(errors):
      if errors in ("strict", "pad", "ignore"): return errors
      raise LookupError(f"unknown error handler name {errors!r}")

    def it():
      #errors, scheme, ignored, padding = self.errors, self.scheme[:64], self.ignored, self.padding
      errors, scheme = self.errors, self.scheme
      cache, state = self.cache, self.state

      for b in iterable:
        code = scheme[b]

        if code != 65:

          if code == 64:  # is padding
            if state in (3, 4): state = 0  # [ABC=] [AB==]
            elif state in (2,): state = 4  # [AB=.]
            else:  # [=...] [A=..]
              if errors != "ignore":
                check_errors(errors)
                raise ValueError("unexpected padding")
          else:
            if code < 64:
              if state == 0: pass  # [A...]
              elif state == 1: yield (cache << 2) | (code >> 4)  # [AB..]
              elif state == 2: yield ((cache & 0xF) << 4) | (code >> 2)  # [ABC.]
              elif state == 3: yield ((cache & 0x3) << 6) | code  # [ABCD]
              cache = code
              state = (state + 1) % 4
            elif errors != "ignore":
              check_errors(errors)
              raise ValueError("invalid code")

      if stream:
        self.cache, self.state = cache, state
        return

      if state == 0: pass
      elif errors == "ignore": state = 0
      elif errors == "pad":
        if state == 1: raise ValueError("unexpected end of data")
        state = 0
      else:
        check_errors(errors)
        raise ValueError("unexpected end of data")

      self.cache, self.state = cache, state
    return it() if self.cast is None else self.cast(it())
  decode = transcode
