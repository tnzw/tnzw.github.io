# sequence_lt.py Version 1.0.1
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def sequence_lt(self, other):
  # "ab" < "abc"
  # "abc" < "bc"
  r = iter(other)
  l = iter(self)
  for lv in l:
    try:
      rv = next(r)
      if lv < rv: return True
      if lv > rv: return False
    except StopIteration: return False
  for _ in r: return True
  return False
