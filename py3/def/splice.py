# splice.py Version 2.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def splice(*array_key_replacement):
  """\
splice(array[, start[, count[, replacement]]])
splice(array[, slice_key[, replacement]])

Changes the contents of an array by removing or replacing existing elements
and/or adding new elements in place.

/!\\ javascript Array.prototype.splice has different API

    js: array.splice (start, count,  item1, item2, ... )
    py: splice(array, start, count, (item1, item2, ...))
"""
  replacement = ()
  l = len(array_key_replacement)
  if l > 4:
    raise TypeError(f"splice() expected at most 4 arguments, got {l}")
  elif l == 4:
    array, start, count, replacement = array_key_replacement
    if start < 0:
      start = len(array) + start
      if start < 0: start = 0
    key = slice(start, start + count)
  elif l == 3:
    array, start, count = array_key_replacement
    if isinstance(start, slice): key, replacement = start, count
    else:
      if start < 0:
        start = len(array) + start
        if start < 0: start = 0
      key = slice(start, start + count)
  elif l == 2:
    array, start = array_key_replacement
    if isinstance(start, slice): key = start
    else: key = slice(start, None)
  elif l == 1:
    array, = array_key_replacement
    key = slice(None)
  else:
    raise TypeError(f"splice() expected at least 1 argument, got {l}")
  chunk, array[key] = array[key], replacement
  return chunk
