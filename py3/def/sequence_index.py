# sequence_index.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def sequence_index(self, x, i=0, *j):
  def count(f):
    while True:
      yield f
      f += 1
  if j:
    j, = j
    r = range(i, j)
  else:
    r = count(i)
  it = iter(self)
  for _ in zip(range(i), it): pass
  for f, _ in zip(r, it):
    if x == _: return f
  c = self.__class__.__name__
  raise ValueError(f"{x!r} is not in {c}")
