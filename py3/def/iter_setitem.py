# iter_setitem.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def iter_setitem(buffer):
  """\
Allow to iter through a buffer in order to set its item in this
way `setter[key_or_index] = value`.

Examples:

buffer = bytearray(b"abc")
for byte, index, setter in iter_setitem(buffer):
  setter[index] = (byte + 1) % 256
print(buffer)  # bytearray(b"bcd")

mapping = {"a": 1, "b": 2}
for value, key, setter in iter_setitem(mapping):
  setter[key] = value + 1
print(mapping)  # {'a': 2, 'b': 3}

mag = [[1, 2], [3]]
class Magic():
  def __iter_setitem__(self):
    for b in mag:
      for j, v in enumerate(b):
        yield v, j, b
for v, i, s in iter_setitem(Magic()):
  s[i] = v + 1
print(mag)  # [[2, 3], [4]]
"""
  if hasattr(buffer, "__iter_setitem__"): return iter(buffer.__iter_setitem__())  # should be O(1)
  #if hasattr(buffer, "__js_foreach__"): return iter(buffer.__js_foreach__())  # could not be O(1)
  # class Mapping():
  #   def keys(self): yield key
  #   def __getitem__(self, key): return value
  #   def __setitem__(self, key, value): pass
  if hasattr(buffer, "keys"):
    it = buffer.keys()
    def __iter__():
      for k in it: yield buffer[k], k, buffer
    return __iter__()
  if not hasattr(buffer, "__getitem__"):
    raise TypeError(f"{buffer.__class__.__qualname__!r} object is not a buffer or a mapping")
  # class Buffer():
  #   def __getitem__(self, index): return value or raise IndexError
  #   def __setitem__(self, index, value): pass
  def __iter__():
    i = 0
    while True:
      try: v = buffer[i]
      except IndexError: break
      yield v, i, buffer
      i += 1
  return __iter__()
