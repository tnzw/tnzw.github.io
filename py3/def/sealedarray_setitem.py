# sealedarray_setitem.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def sealedarray_setitem(array, key, item, setter=None):
  # a __setitem__ implementation that avoids changing the size of the array
  # usage:
  #   class o(bytearray):
  #     def __setitem__(self, key, item): return sealedarray_setitem(self, key, item, bytearray.__setitem__)
  def unpack(iterable, expected):
    count = expected
    for _ in iterable:
      if count:
        yield _
        count -= 1
      else:   raise ValueError(f"too many values to unpack (expected {expected})")
    if count: raise ValueError(f"not enough values to unpack (expected {expected}, got {expected - count})")
  if isinstance(key, slice):
    alen = len(array)
    klen = indices_len(key.indices(alen))
    if hasattr(item, "__len__"):
      ilen = len(item)
      d = klen - ilen
      if d < 0: raise ValueError(f"too many values to unpack (expected {klen})")
      if d > 0: raise ValueError(f"not enough values to unpack (expected {klen}, got {ilen})")
    else:
      # XXX it assigns some values even if raising... no other way? without doing several iterations?
      item = unpack(item, klen)
  if setter is None: array[key] = item
  else: return setter(array, key, item)
sealedarray_setitem._required_globals = ["indices_len"]
