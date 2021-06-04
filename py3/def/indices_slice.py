# indices_slice.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def indices_slice(indices, key):
  if isinstance(key, slice): is_slice = True
  else: is_slice, key = False, slice(key, key + 1, 1)
  size = indices_len(indices)
  if not is_slice and (key.start >= size or key.start < -size):
    raise IndexError("index is out of range")
  start, stop, step = key.indices(size)
  sstart, sstop, sstep = indices
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
      if stop < 0: stop = None
  else:
    ssize = max(sstop - sstart, 0)
    mod = ssize % sstep
    step *= sstep
    start = sstart + start * sstep
    if kneg:
      stop = sstart + stop * sstep + mod
      if stop < 0: stop = None
    else:
      stop = sstart + stop * sstep - mod
  if is_slice: return slice(start, stop, step)
  return start
indices_slice._required_globals = ["indices_len"]
