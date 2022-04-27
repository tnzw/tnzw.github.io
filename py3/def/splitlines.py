# splitlines.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def splitlines(array, sep=None):
  # acts like io.readlines() but with an array (str, bytes, ...)
  if sep is None: sep = "\n" if isinstance(array, str) else b"\n"
  larray = len(array); lsep = len(sep); j = 0; split = []
  for i in range(lsep, larray):
    if array[i - lsep:i] == sep:
      split.append(array[j:i])
      j = i
  if j < larray: split.append(array[j:])
  return split
