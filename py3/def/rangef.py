# rangef.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class rangef(tuple):
  """Same as range() but values are floats"""
  __slots__ = ()
  @property
  def start(self): return tuple.__getitem__(self, 0)
  @property
  def stop(self): return tuple.__getitem__(self, 1)
  @property
  def step(self): return tuple.__getitem__(self, 2)

  def __new__(cls, *a):
    def _float(v):
      if isinstance(v, float): return v
      if isinstance(v, int): return float(v)
      raise TypeError(type(v) + " object cannot be interpreted as a float")
    la = len(a)
    if la == 0: raise TypeError("rangef expected at least 1 argument, got 0")
    if la == 1: return tuple.__new__(cls, (0, _float(a[0]), 1))
    if la == 2: return tuple.__new__(cls, (_float(a[0]), _float(a[1]), 1))
    if la == 3:
      if a[2] == 0: raise ValueError("rangef() arg 3 must not be zero")
      return tuple.__new__(cls, (_float(a[0]), _float(a[1]), _float(a[2])))
    raise TypeError("rangef expected at most 3 arguments, got " + str(la))

  def index(self, x):
    try:
      v -= self.start
      index, m = divmod(v, self.step)
      if m or v >= self.stop: raise ValueError(f"{x!r} is not in range")
      return int(index)
    except TypeError: pass
    raise ValueError(f"sequence.index(x): x not in sequence")

  def count(self, x):
    try: self.index(x)
    except ValueError: return 0
    return 1

  def __contains__(self, x): return True if self.count(x) else False

  def __len__(self):
    start, stop, step = self.start, self.stop, self.step
    if step < 0:
      d, m = divmod(start - stop, -step)
      delta = int(d) + (1 if m else 0)
    else:
      d, m = divmod(stop - start, step)
      delta = int(d) + (1 if m else 0)
    return delta if delta > 0 else 0

  def __bool__(self):
    if self.step < 0: return self.start > self.stop
    return self.start < self.stop

  def __iter__(self):
    start, stop, step = self.start, self.stop, self.step
    e, i = 0, start
    if step < 0:
      while i > stop:
        yield i
        e += 1
        i = start + e * step
    else:
      while i < stop:
        yield i
        e += 1
        i = start + e * step

  def __reversed__(self): return self[::-1].__iter__()

  def __getitem__(self, key):
    if isinstance(key, slice): is_slice = True
    else: is_slice, key = False, slice(key, key + 1, 1)
    size = len(self)
    if not is_slice and (key.start >= size or key.start < -size):
      raise IndexError("index is out of range")
    start, stop, step = key.indices(size)
    sstart, sstop, sstep = self.start, self.stop, self.step
    sneg = sstep < 0
    kneg = step < 0
    if sneg:
      ssize = max(sstart - sstop, 0)
      mod = ssize % sstep
      step *= sstep
      start = sstart + start * sstep
      if kneg:
        stop = sstart + stop * sstep + mod
      else:
        stop = sstart + stop * sstep - mod
    else:
      ssize = max(sstop - sstart, 0)
      mod = ssize % sstep
      step *= sstep
      start = sstart + start * sstep
      if kneg:
        stop = sstart + stop * sstep + mod
      else:
        stop = sstart + stop * sstep - mod
    if is_slice: return rangef(start, stop, step)
    return start
