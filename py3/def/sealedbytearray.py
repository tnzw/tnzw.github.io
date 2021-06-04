# sealedbytearray.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class sealedbytearray(bytearray):
  """\
A sealedbytearray is a bytearray that cannot be resized.
"""
  # methods that return new object
  for _ in ("__add__", "__mod__", "__mul__", "__rmod__", "__rmul__",
            "capitalize", "center", "expandtabs", "join", "ljust", "lower",
            "lstrip", "removeprefix", "removesuffix", "replace",
            "rjust", "rstrip", "strip", "swapcase", "title", "translate",
            "upper", "zfill"):
    exec(f"def {_}(self, *a, **k): return self.__class__(bytearray.{_}(self, *a, **k))", {}, locals())
  # methods that returns tuple of new object
  for _ in ("partition", "rpartition"):
    exec(f"def {_}(self, *a, **k): return tuple(sealedbytearray(_) for _ in bytearray.{_}(self, *a, **k))", {}, locals())
  # methods that resizes the object
  for _ in ("__delitem__", "__iadd__", "__imul__",
            "append", "clear", "extend", "insert", "pop", "remove"):
    exec(f"def {_}(self, *a, **k): raise ValueError('sealedbytearray cannot be resized')", {}, locals())
  del _
  def __setitem__(self, index, value):
    if isinstance(index, slice):
      indices = index.indices(len(self))
      # check valid unpack
      ilen = sealedlist.indices_len(indices)  # ilen = sum(1 for _ in range(*indices))
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
    return bytearray.__setitem__(self, index, value)
  def copy(self): return sealedbytearray(self)
  @staticmethod
  def indices_len(indices):
    # indices_len(slice(0, 20, 2).indices(10)) -> 5
    start, stop, step = indices
    if step < 0:
      delta = start - stop
      if step < -1:
        d,m = divmod(delta, -step)
        delta = d + (1 if m else 0)
    else:
      delta = stop - start
      if step > 1:
        d,m = divmod(delta, step)
        delta = d + (1 if m else 0)
    return delta if delta > 0 else 0
