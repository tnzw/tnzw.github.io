# find2.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def find2(string, sub, *start_end):
  """\
find2(S, sub[, start[, end]]) -> int

Return the lowest index in S where subsection sub is found,
such that sub is contained within S[start:end].  Optional
arguments start and end are interpreted as in slice notation.

Return -1 on failure.

sub could be a tuple of subsection to search for.
"""
  is_string = type(string) in (str, bytes, bytearray)
  if type(sub) is tuple:
    if not sub: raise ValueError('empty sub collection')
  else:
    if is_string: return string.find(sub, *start_end)  # using native find()
    sub = (sub,)
  stringlen = len(string)
  match start_end:
    case start, end: pass
    case start,: end = stringlen
    case (): start = 0; end = stringlen
    case _: raise TypeError(f'find2() takes at most 4 arguments ({len(start_end) + 2} given)')
  if start < -stringlen: start = 0
  elif start < 0: start = stringlen + start
  elif start > stringlen: return -1
  if end < -stringlen: return -1
  elif end < 0: end = stringlen + end
  elif end > stringlen: end = stringlen
  if is_string:
    index = -1
    for s in sub:
      i = string.find(s, start, end)  # using native find()
      if i != -1:
        if index == -1 or i < index: index = i
    return index
  else:
    stringlen = len(string)
    def find1(string, sub, start, end):
      l = len(sub)
      for i in range(start, end):
        if string[i:i + l] == sub: return i
      return -1
    index = -1
    for s in sub:
      i = find1(string, s, start, end)
      if i != -1:
        if index == -1 or i < index: index = i
    return index
