# rangeinf.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class rangeinf(tuple):
  """\
rangeinf(start[, step])

Same as range() without stop.
"""
  __slots__ = ()
  @property
  def start(self): return tuple.__getitem__(self, 0)
  @property
  def step(self): return tuple.__getitem__(self, 1)

  def __new__(cls, *a):
    def _int(v):
      if isinstance(v, int): return v
      raise TypeError(type(v) + " object cannot be interpreted as an integer")
    la = len(a)
    if la == 0: raise TypeError("rangef expected at least 1 argument, got 0")
    if la == 1: return tuple.__new__(cls, (_int(a[0]), 1))
    if la == 2:
      if a[1] == 0: raise ValueError("rangeinf() arg 2 must not be zero")
      return tuple.__new__(cls, (_int(a[0]), _int(a[1])))
    raise TypeError("rangeinf expected at most 2 arguments, got " + str(la))

  def index(self, x):
    v = x
    try:
      v -= self.start
      index, m = divmod(v, self.step)
      if m or self.step > 0 and self.start > x or self.step < 0 and self.start < x:
        raise ValueError(f"{x!r} is not in range")
      return index
    except TypeError: pass
    raise ValueError(f"sequence.index(x): x not in sequence")

  def count(self, x):
    try: self.index(x)
    except ValueError: return 0
    return 1

  def __contains__(self, x): return True if self.count(x) else False

  def __bool__(self): return True

  def __iter__(self):
    start, step = self.start, self.step
    e, i = 0, start
    if step < 0:
      while True:
        yield i
        e += 1
        i = start + e * step
    else:
      while True:
        yield i
        e += 1
        i = start + e * step

  def __reversed__(self): return self[::-1].__iter__()  # raises to make reverse(rangeinf()) to fail

  def __getitem__(self, key):
    sstart, sstep = self.start, self.step
    if isinstance(key, slice):
      kstart, kstop, kstep = 0 if key.start is None else int(key.start), key.stop, 1 if key.step is None else int(key.step)
      if kstop is None:
        if kstep == 0: raise ValueError("slice step cannot be zero")
        if kstart < 0 or kstep < 0: raise ValueError("cannot start from inf or -inf")
        return rangeinf(sstart + kstart * sstep, sstep)
      return range(sstart, sstart + (abs(kstart) + abs(kstop)) * sstep, sstep)[key]
    else:
      return range(sstart, sstart + (abs(key) + 1) * sstep, sstep)[key]
