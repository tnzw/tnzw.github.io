# xor.py Version 1.1.0
# Copyright (c) 2020-2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def xor(a, *b, default=None):
  """\
xor() acts like a logical "xor" for any kind of values, like do `and` and `or`
in python.

    >>> (False and 0, False or 0, xor(False, 0))
    (False, 0, False)
    >>> (1 and 2, 1 or 2, xor(1, 2), xor(1, 2, False), xor(1, 2, default=False))
    (2, 1, None, False, False)
    >>> (0 and 2, 0 or 2, xor(0, 2))
    (0, 2, 2)
    >>> (0 and 1 and 2, 0 or 1 or 2, xor(0, 1, 2))
    (0, 1, 0)
"""
  if a:
    if default: raise ValueError("'default' is equivalent to True")
  else: default = a
  for c in b:
    if a:
      if c: a = default
      else: default = c
    else: a = c
  return a
