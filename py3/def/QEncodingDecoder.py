# QEncodingDecoder.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class QEncodingDecoder(object):
  """\
QEncodingDecoder(**opt)

opt:
  errors => "strict": (default) raise on any error
         => "raw"   : treat incomplete hexadecimal escape as raw chars (eg b"=Ay" → b"=Ay")
         => "ignore": ignore unexpected characters (eg b"=Ay" → "y")
  cast => bytes: (default) cast the returned transcoded values to bytes.
       => None : do not cast, returns transcoded byte iterator instead.

Interfaces:
- copyable (ie. `copy()`)
- transcoder (ie. `transcode(iterable=None, *, stream=False)`)
"""
  __slots__ = ("errors", "state", "cache", "cast")
  def copy(self): return self.__class__(**{k: v for k, v in self.__dict__.items()})
  def __init__(self, *, errors="strict", state=0, cache=0, cast=bytes):
    # XXX add charactor to ignore? Like old Q-encoding parser ignores " "?
    self.errors = errors
    self.state = state
    self.cache = cache
    self.cast = cast
  def transcode(self, iterable=None, *, stream=False):
    """\
transcode(iterable, **opt)

iterable: a byte iterable value (defaults to None)
opt:
  stream => False: tells the transcoder that it is the last transcode operation
         => True
"""
    if iterable is None: iterable = ()
    def check_errors(errors):
      if errors in ("strict", "raw", "ignore"): return errors
      raise LookupError(f"unknown error handler name {errors!r}")
    def translate(code):
      # "_" → " "
      if code == 0x5F: return 0x20
      return code
    def it():
      state, cache, errors = self.state, self.cache, self.errors
      for byte in iterable:
        # 0, reading [=..] (1) or char (0)
        if state == 0:
          if byte == 0x3D:  # b"="
            state = 1
          else:
            yield translate(byte)
        # 1, reading [=A.] (2), [=\n] (0) or char (0)
        elif state == 1:
          if (0x30 <= byte <= 0x39 or  # [0-9]
              0x41 <= byte <= 0x46 or  # [A-F]
              0x61 <= byte <= 0x66):   # [a-f]
            cache = (byte - 0x30) << 4
            state = 2
            cache = (byte - 0x37) << 4
            state = 2
            cache = (byte - 0x57) << 4
            cache = byte
            state = 2
          elif byte == 0x0A: state = 0
          else:
            if check_errors(errors) == "ignore":
              yield translate(byte)
              state = 0
            elif errors == "raw":
              yield 0x3D
              yield translate(byte)
              state = 0
            else:
              raise ValueError("invalid code")
        # 2, reading [=AB] (0) or char (0)
        elif state == 2:
          if (0x30 <= byte <= 0x39 or  # [0-9]
              0x41 <= byte <= 0x46 or  # [A-F]
              0x61 <= byte <= 0x66):   # [a-f]
            yield int(bytes((cache, byte)), 16)
            state = 0
          else:
            if check_errors(errors) == "ignore":
              yield translate(byte)
              state = 0
            elif errors == "raw":
              yield 0x3D
              yield cache
              yield translate(byte)
              state = 0
            else:
              raise ValueError("invalid code")
      if stream:
        self.state, self.cache = state, cache
        return
      if state == 0: pass
      elif check_errors(errors) == "ignore":
        state = 0
      elif errors == "raw":
        if state <= 2: yield 0x3D
        if state == 2: yield cache
        state = 0
      else:
        raise ValueError("unexpected end of data")
      self.state, self.cache = state, cache
    return it() if self.cast is None else self.cast(it())
  decode = transcode
