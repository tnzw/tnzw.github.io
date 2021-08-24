# tupledict.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class tupledict(tuple):
  """\
A tupledict is an ordered mapping that cannot be modified at all.
"""
# XXX It does not use hash to get items, this is an optimization that could be
#     implemented.
  __slots__ = ()

  for _ in (_
    for _ in dir(tuple()) if _ not in (
      # keep these ones
      "__class__", "__class_getitem__",
      "__delattr__", "__dir__", "__doc__",
      "__getattribute__", "__init__", "__init_subclass__",
      "__module__", "__new__", "__setattr__", "__sizeof__", "__str__",
      "__subclasshook__",
      "__getitem__",
    )
  ):
    exec(f"@property\ndef {_}(self): raise AttributeError(f'{{self.__class__.__name__!r}} object has no attribute ' + repr({_!r}))", {}, locals())
  del _
  def __dir__(self): return [_ for _ in tuple.__dir__(self) if hasattr(self, _)]
  def __repr__(self): return f"{self.__class__.__qualname__}({dict(self)})"
  def __len__(self): return super().__len__()
  def __iter__(self): return self.keys()
  def __contains__(self, x): return any(k == x for k in self.keys())
  def __or__(self, other):
    self = dict(self)
    if hasattr(other, "keys"):
      for k in other.keys(): self[k] = other[k]
    else:
      for k, v in other: self[k] = v
    return tupledict(self)
  def __getitem__(self, key):
    for k, v in self.items():
      if k == key: return v
    raise KeyError(key)

  @classmethod
  def fromkeys(cls, keys, value=None):
    return cls({k: value for k in keys})

  def __new__(cls, *iterable, **kw):
    if iterable:
      if iterable[1:2]: raise TypeError("tupledict expected at most 1 argument, got " + str(len(iterable)))
      iterable = iterable[0]
      if hasattr(iterable, "keys"):
        for k in iterable.keys(): kw.setdefault(k, iterable[k])
      else:
        for k, v in iterable: kw.setdefault(k, v)
    return tuple.__new__(cls, tuple(kw.items()))

  def keys(self):
    for i in range(len(self)):
      k, _ = super().__getitem__(i)
      yield k
  def values(self):
    for i in range(len(self)):
      _, v = super().__getitem__(i)
      yield v
  def items(self):
    for i in range(len(self)):
      yield super().__getitem__(i)
