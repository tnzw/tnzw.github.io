# KeyValueListAsDict.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class KeyValueListAsDict(object):
  def __init__(self, list=None): self.list = [] if list is None else list
  # https://docs.python.org/3/library/stdtypes.html#dict
  # https://docs.python.org/3/reference/datamodel.html
  def __contains__(self, key): return key in (k for k, v in self.list)
  def __delitem__(self, key):
    """\
Delete all items matching the given key.
Raises a KeyError if no item found.
"""
    indices = []
    for i, (k, v) in enumerate(self.list):
      if k == key: indices.insert(0, i)
    if indices:
      for i in indices: self.list[:] = self.list[:i] + self.list[i+1:]
    else: raise KeyError(key)
  def __getitem__(self, key):
    """\
Get the first item value matching the given key.
Raises a KeyError if no item found.
"""
    for k, v in self.list:
      if k == key: return v
    raise KeyError(key)
    # XXX do not use another method ?
    #marker = []
    #v = self.get(key, marker)
    #if v is marker: raise KeyError(key)
    #return v
    # XXX could return several values as list ?
    # values = []
    # for k, v in self.list:
    #   if k == key: values.append(v)
    # if values: return values[0] if len(values) == 1 else values
    # raise KeyError(key)
  def __ior__(self, other):
    self.update(other)
    return self
  def __iter__(self): return (k for k, v in self.list)
  def __len__(self): return self.list.__len__()
  def __or__(self, other):
    copy = self.copy()
    copy.update(other)
    return copy
  def __repr__(self): return f"{self.__class__.__name__}({self.list})"
  def __setitem__(self, key, value):
    """\
Add a new item or replace the first item value matching the given key.
Deletes the other item matching the given key.
"""
    indices = []
    for i, (k, v) in enumerate(self.list):
      if k == key: indices.insert(0, i)
    for i in indices[:-1]: self.list[:] = self.list[:i] + self.list[i+1:]
    if indices: self.list[indices[-1]] = (key, value)
    else: self.list.append((key, value))
    return value
  def append(self, key, value): self.list.append((key, value))
  def clear(self): self.list[:] = []
  def copy(self): return self.__class__(self.list.copy())
  @classmethod
  def fromdict(cls, dict): return cls([(k, v) for k, v in dict.items()])
  @classmethod
  def fromkeys(cls, iterable, value=None): return cls([(_, value) for _ in iterable])
  def get(self, key, default=None):
    """\
Return the first item value matching the given key.
Returns default if no item found.
"""
    for k, v in self.list:
      if k == key: return v
    return default
  def getall(self, key, default=None):
    """\
Return a list of item values matching the given key.
Returns default if no item found.
"""
    return [v for k, v in self.list if k == key] or default
  get_all = getall  # to match email.message.Message get_all method name
  def items(self): return iter(self.list)
  def keys(self): return (k for k, v in self.list)
  def pop(self, key):
    for i, (k, v) in enumerate(self.list):
      if k == key:
        self.list[:] = self.list[:i] + self.list[i+1:]
        return v
    raise KeyError(key)
  def popall(self, key):
    indices = []
    values = []
    for i, (k, v) in enumerate(self.list):
      if k == key:
        indices.insert(0, i)
        values.append(v)
    for i in indices: self.list[:] = self.list[:i] + self.list[i+1:]
    return values
  def popitem(self):
    i = None
    for i, (k, v) in enumerate(self.list): pass
    if i is None: raise KeyError('popitem(): list is empty')
    self.list[:] = self.list[:i]
    return k, v
  def popallitems(self):
    kv = [(k, v) for k, v in self.list]
    self.list[:] = ()
    return kv
  def replace(self, key, value):
    """\
Replace the first item value matching the given key.
Raises a KeyError if no item found.
"""
    for i, (k, v) in enumerate(self.list):
      if k == key:
        self.list[i] = (key, value)
        return value
    raise KeyError(key)
  def replaceall(self, key, values, appends=True):
    """\
Replace several item values matching the given key.
Raises a IndexError if no value is remaining for an item. XXX KeyError ?

if appends is True:
  d <- [("id", 1), ("id", 2)]
  d.replaceall("he", ("ho",)) -> [("id", 3), ("id", 2), ("he", "ho")]
  d.replaceall("id", (3,)) -> [("id", 3), ("id", 2), ("he", "ho")]
  d.replaceall("id", (4, 5, 6)) -> [("id", 4), ("id", 5), ("he", "ho"), ("id", 6)]

if appends is False:
  d <- [("id", 1), ("id", 2)]
  d.replaceall("he", ("ho",)) -> IndexError
  d.replaceall("id", (3,)) -> [("id", 3), ("id", 2)]
  d.replaceall("id", (4, 5)) -> [("id", 4), ("id", 5)]
"""
    vi = iter(values)
    try:
      for i, (k, v) in enumerate(self.list):
        if k == key: self.list[i] = (k, next(vi))
    except StopIteration: return
    if appends:
      for v in vi: self.list.append((key, v))
    else:
      for v in vi: raise IndexError()
  def set(self, key, value):
    """Act like __setitem__"""
    self[key] = value
    return value
  def setall(self, key, values):
    """\
Replace several item values matching the given key as long as there is values.
Deletes other items matching the given key if no value is remaining.

d.setall("id", (1, 2)) -> [("id", 1), ("id", 2)]
d.setall("he", ("ho",)) -> [("id", 1), ("id", 2), ("he", "ho")]
d.setall("id", (3,)) -> [("id", 3), ("he", "ho")]
d.setall("id", (4, 5)) -> [("id", 4), ("he", "ho"), ("id", 5)]
"""
    vi = iter(values)
    li = enumerate(self.list)
    try:
      for i, (k, v) in li:
        if k == key: self.list[i] = (k, next(vi))
    except StopIteration:
      indices = [i]
      for i, (k, v) in li:
        if k == key: indices.insert(0, i)
      for i in indices: self.list[:] = self.list[:i] + self.list[i+1:]
      return
    for v in vi: self.list.append((key, v))
  def setdefault(self, key, value):
    """\
Search for an item matching key and return its value.
Add a new item if none is found.
"""
    for i, (k, v) in enumerate(self.list):
      if k == key: return v
    self.list.append((key, value))
    return value
  def sort(self, *a, **kw): return self.list.sort(*a, **kw)
  def update(self, other, **kw):
    """\
Act like setall from each other item keys and values.
**kw defines one value for each key.
"""
    kv = {}
    for k, v in other.items():
      if k in kv: kv[k].append(v)
      else: kv[k] = [v]
    for k, v in kw.items():
      if k in kv: kv[k].append(v)
      else: kv[k] = [v]
    for k, vv in kv.items(): self.setall(k, vv)
  def values(self): return (v for k, v in self.list)
