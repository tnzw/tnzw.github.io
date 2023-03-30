# os_find_in_file.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_find_in_file(fileno, sub, start=0, end=None, *, buffer_size=32768, os_module=None):
  """\
os_find_in_file(fileno, sub[, start[, end]]) -> int

Return the lowest index in S where subsection sub is found,
such that sub is contained within S[start:end].  Optional
arguments start and end are interpreted as in slice notation.

Return -1 on failure.
"""
  def count(f):
    while 1: yield f; f += 1
  if os_module is None: os_module = os
  lseek = os_module.lseek; SEEK_SET = os_module.SEEK_SET; read = os_module.read
  if start is None: start = 0
  if start < 0 or end is not None and end < 0: start, end, _ = slice(start, end).indices(lseek(fileno, 0, os_module.SEEK_END))
  if end is None: r = count(start)
  else: r = iter(range(start, end))
  sub_type = type(sub)
  if sub_type == int:
    lseek(fileno, start, SEEK_SET)
    while 1:
      l = buffer_size if end is None else min(buffer_size, end - start)
      if l <= 0: return -1
      d = read(fileno, l)
      if not d: return -1
      for b, c in zip(d, r):
        if b == sub: return c
      start += len(d)
  sub = memoryview(sub)  # raise TypeError(f'a bytes-like object is required, not {sub_type.__name__!r}')
  #if sub_type not in (bytes, bytearray): sub = bytes(sub)
  lsub = sub.nbytes
  if lsub <= 0:
    lseek(fileno, start, SEEK_SET)
    if read(fileno, 1): return start
    return -1
  d = b''
  lseek(fileno, start, SEEK_SET)
  while 1:
    l = buffer_size if end is None else min(buffer_size, end - start)
    if l <= 0: return -1
    c = read(fileno, l); lc = len(c)
    if lc <= 0: return -1
    d = d[len(d) - lsub + 1:] + c
    for b, c, a in zip(d[:len(d) - lsub + 1], r, count(0)):
      if d[a:a + lsub] == sub: return c
    start += lc
os_find_in_file._required_globals = ['os']
