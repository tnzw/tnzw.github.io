# sealedlist.py Version 1.0.1
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class sealedlist(list):
  """\
A sealedlist is a list that cannot be resized.
"""
  # methods that return new object
  for _ in ("__add__", "__mul__", "__rmul__"):
    exec(f"def {_}(self, *a, **k): return self.__class__(bytearray.{_}(self, *a, **k))", {}, locals())
  # methods that resizes the object
  for _ in ("__delitem__", "__iadd__", "__imul__",
            "append", "clear", "extend", "insert", "pop", "remove"):
    exec(f"def {_}(self, *a, **k): raise ValueError('sealedlist cannot be resized')", {}, locals())
  del _
  def __repr__(self): return f"{self.__class__.__name__}({list.__repr__(self)})"
  def __setitem__(self, index, value):
    if isinstance(index, slice):
      indices = index.indices(len(self))
      # check valid unpack
      ilen = len(range(*indices))
      if not hasattr(value, "__len__"):
        value = list(v for i, v in zip(range(ilen + 1), value))
      vlen = len(value)
      if ilen != vlen: raise ValueError(f"{self.__class__.__name__} assignment: lvalue and rvalue have different structures")
      # END check valid unpack
      it = iter(value)
      for i in range(*indices):
        for _ in it:
          self[i] = _
          break
        else: return
      return
    return list.__setitem__(self, index, value)
  def copy(self): return sealedlist(self)
