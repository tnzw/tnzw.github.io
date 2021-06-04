# sealedarray_setitem.py Version 1.0.1
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def sealedarray_setitem(array, key, item, setter=None):
  """\
A __setitem__ implementation that avoids changing the size of the array.

Requires `array` to have a `__len__` method.

Does not prevent inconsistencies (like concurrency issues eg. `item`
changes his size during the setitem), to avoid them, array.__setitem__()
must not be written (commit) if the write process raises (transaction
failure). bytearray() and list() builtins already have such a
transaction mechanism. However, you can easily prevent this by copying
`item` before calling setitem:

    sealedarray_setitem(mutable, slice(None), list(untrusted_data))

Usage:

    ba = bytearray(b"test")
    sealedarray_setitem(ba, slice(1, 3), item)

    Or

    class o(bytearray):
      def __setitem__(self, key, item):
        return sealedarray_setitem(self, key, item, bytearray.__setitem__)
"""
# Exemple of inconsistencies:
#     class InconsistentObject():
#       def __iter__(self):
#         yield 2
#         yield 3
#       def __len__(self):
#         return 1
#     l = [0]
#     sealedarray_setitem(l, slice(None), InconsistentObject())  # raises ValueError
#     # l -> [0]: `l` is not modified as list() has transaction mechanism.
  if isinstance(key, slice):
    def unpack(it, length):
      i = -1
      for i, v in zip(range(length), it): yield v
      if i + 1 != length: raise ValueError(f"not enough values to unpack (expected {length}, got {length - i - 2})")
      for _ in it: raise ValueError(f"too many values to unpack (expected {length})")
    ilen = len(range(*key.indices(len(array))))
    if hasattr(item, "__len__"):
      if ilen != len(item): raise ValueError(f"{array.__class__.__name__} assignment: lvalue and rvalue have different structures")
    #if not hasattr(item, "__len__"): item = list(v for i, v in zip(range(ilen + 1), item))
    #if ilen != len(item): raise ValueError(f"{array.__class__.__name__} assignment: lvalue and rvalue have different structures")
    item = unpack(iter(item), ilen)
  if setter is None:
    array[key] = item
    return
  return setter(array, key, item)
