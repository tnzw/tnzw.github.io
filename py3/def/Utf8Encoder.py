# Utf8Encoder.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class Utf8Encoder(object):
  """\
Utf8Encoder(**opt)

opt:
  errors => "strict"       : raise on invalid or reserved code.
         => "ignore"       : ignore the malformed data and continue.
         => "surrogatepass": allow encoding of surrogate codes.
         => "replace"      : replace malformed data with a sequence of bytes.
  replacement => b"?": the replacement sequence on errors="replace"
  replacer => callable: (defaults None) returns the replacement sequence on errors="replace"
  cast => bytes: (default) cast the returned transcoded values to bytes.
       => None : do not cast, returns transcoded byte iterator instead.

Interfaces:
- copyable (ie. `copy()`)
- transcoder (ie. `transcode(iterable=None, *, stream=False)`)
"""
  def copy(self): return self.__class__(**{k: v for k, v in self.__dict__.items()})
  def __init__(self, *, errors="strict", cast=bytes, replacer=None, replacement=b"?"):
    self.errors = errors
    self.cast = cast
    self.replacer = replacer
    self.replacement = replacement
  def transcode(self, iterable=None, *, stream=False):
    """\
transcode(iterable, **opt)

iterable: an unicode uint32 iterable or str value (defaults to None)
opt:
  stream => False: tells the transcoder that it is the last transcode operation
         => True
"""
    if iterable is None: iterator = ()
    elif isinstance(iterable, str): iterator = (ord(_) for _ in iterable)
    else: iterator = iter(iterable)
    def it():
      errors, replacer, replacement = self.errors, self.replacer, self.replacement
      for code in iterator:
        if code <= 0x7F: yield code
        elif code <= 0x7FF:
          yield 0xC0 | ((code >> 6) & 0x1F)
          yield 0x80 | (code & 0x3F)
        elif code <= 0xFFFF:
          if 0xD800 <= code <= 0xDFFF:
            if errors == "strict": raise ValueError("surrogates not allowed")
            elif errors == "ignore": code = 0
            elif errors == "surrogatepass": pass
            elif errors == "replace":
              if replacer is not None: yield from replacer(code)
              else: yield from replacement
              code = 0
            else: raise LookupError(f"unknown error handler name {errors!r}")
          if code > 0:  # continue encoding
            yield 0xE0 | ((code >> 12) & 0xF)
            yield 0x80 | ((code >> 6) & 0x3F)
            yield 0x80 | (code & 0x3F)
        elif code <= 0x10FFFF:
          yield 0xF0 | ((code >> 18) & 0x7)
          yield 0x80 | ((code >> 12) & 0x3F)
          yield 0x80 | ((code >> 6) & 0x3F)
          yield 0x80 | (code & 0x3F)
        else:
          raise ValueError("code not in range(0x110000)")
    return it() if self.cast is None else self.cast(it())
  encode = transcode
