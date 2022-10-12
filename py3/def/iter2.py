# iter2.py Version 1.0.1
# Copyright (c) 2021-2022 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def iter2(iterable):
  """\
It is actualy an re-implementation of iter() builtin.
"""
  # class Iterable():
  #   def __iter__(self): yield value
  try: it = iterable.__iter__
  except AttributeError: pass
  else:
    it = it()
    def __iter__():
      while True:
        try: v = it.__next__()
        except StopIteration: break
        yield v
    return __iter__()
  try: it = iterable.__getitem__
  except AttributeError: pass
  else:
    # class Iterable():
    #   def __getitem__(self, index): return value or raise IndexError
    def __iter__():
      i = 0
      while True:
        try: v = it(i)
        except IndexError: break
        yield v
        i += 1
    return __iter__()
  raise TypeError(f"{iterable.__class__.__qualname__!r} object is not iterable")
