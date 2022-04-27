# list_sorted_insert.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def list_sorted_insert(self, x, *, key=None, reverse=False):
  """\
>>> l = [1, 3]; list_sorted_insert(l, 4); l
[1, 3, 4]
>>> l = [1, 3, 5]; list_sorted_insert(l, 4); l
[1, 3, 4, 5]
>>> l = [3, 1]; list_sorted_insert(l, 4, reverse=True); l
[4, 3, 1]
>>> l = [5, 3, 1]; list_sorted_insert(l, 4, reverse=True); l
[5, 4, 3, 1]
"""
  if reverse:
    l = len(self)
    if key is not None:
      kx = key(x)
      for i, y in enumerate(reversed(self)):
        y = key(y)
        if kx <= y:
          self.insert(l - i, x)
          break
      else:
        self.insert(0, x)
    else:
      for i, y in enumerate(reversed(self)):
        if x <= y:
          self.insert(l - i, x)
          break
      else:
        self.insert(0, x)
  else:
    if key is not None:
      kx = key(x)
      for i, y in enumerate(self):
        y = key(y)
        if kx <= y:
          self.insert(i, x)
          break
      else:
        self.append(x)
    else:
      for i, y in enumerate(self):
        if x <= y:
          self.insert(i, x)
          break
      else:
        self.append(x)
