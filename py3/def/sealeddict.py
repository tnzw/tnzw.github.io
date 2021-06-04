# sealeddict.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class sealeddict(dict):
  """\
A sealeddict is a dict that cannot be resized.
"""
  # methods that resizes the object
  for _ in ("__delitem__",
            "clear", "pop", "popitem"):
    exec(f"def {_}(self, *a, **k): raise ValueError('sealeddict cannot be resized')", {}, locals())
  del _
  @classmethod
  def fromkeys(cls, keys, value=None):
    return cls({k: value for k in keys})
  def __ior__(self, other):
    if hasattr(other, "keys"):
      for k in other.keys(): self[k] = other[k]
    else:
      for k, v in other: self[k] = v
  def __or__(self, other):
    self = self.copy()
    if hasattr(other, "keys"):
      for k in other.keys(): self[k] = other[k]
    else:
      for k, v in other: self[k] = v
    return self
  def __repr__(self): return f"{self.__class__.__name__}({dict.__repr__(self)})"
  def __setitem__(self, key, value):
    if key in self: return dict.__setitem__(self, key, value)
    raise ValueError("sealeddict cannot be resized")
  def copy(self): return sealeddict(self)
  def update(self, *other, **kwarg):
    if other:
      if len(other) > 1: raise TypeError(f"update expected at most 1 argument, got {len(other)}")
      other, = other
      if hasattr(other, "keys"):
        for k in other.keys(): self[k] = other[k]
      else:
        for k, v in other: self[k] = v
    if kwarg:
      for k, v in kwarg.items(): self[k] = v
  def setdefault(self, key, default=None):
    try: return self[key]
    except KeyError: pass
    raise ValueError("sealeddict cannot be resized")
