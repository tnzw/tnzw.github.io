# split2.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def split2(string, sep=None, maxsplit=-1):
  """\
split2('a/b', '/')
split2('a/b\\\\c', ('/', '\\\\'))

Return a list of the sections in the string, using sep as the delimiter.
Also works with all array like values (bytes, list, ...).

  sep
    The delimiter according which to split the string.
    None (the default value) means split on ASCII whitespace characters
    (space, tab, return, newline, formfeed, vertical tab).
    tuple of strings means splits on first found delimiter on every splits.
  maxsplit
    Maximum number of splits to do.
    -1 (the default value) means no limit.
"""
  is_string = type(string) in (str, bytes, bytearray)
  if type(sep) is tuple:
    if not sep: raise ValueError('empty separator')
  else:
    if is_string: return string.split(sep, maxsplit)  # using native split()
    if sep is None: raise TypeError('sep cannot be None when string is not str, bytes or bytearray')
    sep = (sep,)
  if is_string:
    def find2(string, sep, start=0):
      index = -1; l = 0
      for s in sep:
        i = string.find(s, start)  # using native find()
        if i != -1:
          if index == -1 or i < index: index = i; l = len(s)
      return index, l
  else:
    for s in sep:
      if len(s) <= 0: raise ValueError('empty separator')
    stringlen = len(string)
    def find1(string, sep, start=0):
      l = len(sep)
      for i in range(start, stringlen):
        if string[i:i + l] == sep: return i
      return -1
    def find2(string, sep, start=0):
      index = -1; l = 0
      for s in sep:
        i = find1(string, s, start)
        if i != -1:
          if index == -1 or i < index: index = i; l = len(s)
      return index, l
  split = []; s = 0
  while maxsplit != 0:
    i, l = find2(string, sep, s)
    if i == -1: break
    split.append(string[s:i])
    s = i + l
    maxsplit -= 1
  split.append(string[s:])
  return split
