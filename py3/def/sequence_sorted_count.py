# sequence_sorted_count.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def sequence_sorted_count(self, x, reverse=False):
  """\
>>> sequence_sorted_count([1, 3], 3)
1
>>> sequence_sorted_count([1, 3, 3], 3)
2
>>> sequence_sorted_count([1, 3, 4, 3, 3], 3)  # list is not correctly sorted
1
>>> sequence_sorted_count([1, 3, 4, 3, 3], 3, reverse=True)  # list is not correctly sorted
2
"""
  c = 0
  if reverse: it = reversed(self)
  else: it = iter(self)
  for v in it:
    if x == v:
      c += 1
      break
  for v in it:
    if x == v: c += 1
    else: break
  return c
