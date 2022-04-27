# Base64Encoder.py Version 1.0.1
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

# could be easily python codec compatible
# see https://docs.python.org/3/library/codecs.html#incremental-encoding-and-decoding
class Base64Encoder(object):
  """\
Base64Encoder(**opt)

opt:
  scheme : The scheme to use bytes(64 or more)
         => (default) "standard" (or STANDARD_SCHEME)
         => "url" (or URL_SCHEME)
         => <CUSTOM_SCHEME> (`compute_scheme(codes, padding)`)
  cast => bytes : (default) cast the returned transcoded values to bytes.
       => None  : do not cast, returns transcoded byte iterator instead.
  state : internal use only.

Interfaces:
- copyable (ie. `copy()`)
- transcoder (ie. `transcode(iterable=None, *, stream=False)`)
"""
  STANDARD_CODES = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
  URL_CODES = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
  @staticmethod
  def compute_scheme(codes=b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/', padding=b"="):
    """\
opt:
  codes   => bytes(64) : the list of code to use for decoding
  padding => b"="      : each one of these bytes may be concidered as padding
"""
    return codes + padding
  STANDARD_SCHEME = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
  URL_SCHEME = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_='
  def copy(self): return self.__class__(**{k: v for k, v in self.__dict__.items()})
  def __init__(self, *, errors="strict", scheme="standard", cast=bytes, state=0):
    self.scheme = {"standard": self.STANDARD_SCHEME, "url": self.URL_SCHEME}.get(scheme, scheme)
    self.cast = cast
    self.state = state
  def transcode(self, iterable=None, *, stream=False):
    """\
transcode(iterable, **opt)

iterable: a byte iterable value (defaults to None)
opt:
  stream => False: tells the transcoder that it is the last transcode operation
         => True
"""
    if iterable is None: iterator = ()
    else: iterator = iter(iterable)
    # states are:
    # 0 => [?..]
    # 1 => [A?.]
    # 2 => [AB?]

    def it():
      scheme = self.scheme
      state = self.state
      cache, state = state >> 8, state & 0xFF

      for b in iterator:
        if state == 0:  # [?..]
          yield scheme[b >> 2]
          cache, state = b, 1
        elif state == 1:  # [A?.]
          yield scheme[((cache & 0x3) << 4) | (b >> 4)]
          cache, state = b, 2
        else:  # [AB?]
          yield scheme[((cache & 0xF) << 2) | (b >> 6)]
          yield scheme[b & 0x3F]
          cache, state = 0, 0

      if stream:
        self.state = ((cache & 0xFF) << 8) | state
        return

      if state == 0: pass
      elif state == 1:
        yield scheme[(cache & 0x3) << 4]
        if scheme[64:65]: yield scheme[64]; yield scheme[64]
      else:
        yield scheme[(cache & 0xF) << 2]
        if scheme[64:65]: yield scheme[64]
      cache, state = 0, 0
      self.state = ((cache & 0xFF) << 8) | state
    return it() if self.cast is None else self.cast(it())
  encode = transcode
