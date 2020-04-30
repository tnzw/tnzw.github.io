# io_diff.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def io_diff(src, dst, *dsts, length=None, buffer_size=None):
  """\
io_diff(reader1, reader2, reader3..., length=1024, buffer_size=None) -> True if contents are equal, else False
  readers => file like objects
  length  => the total amount of data to compare
"""
  dsts = (dst,) + dsts
  l = 0
  for data in io_iterread1(src, length=length, size=buffer_size):
    data_len = len(data)
    l += data_len
    for dst in dsts:
      cmp_data = dst.read(data_len)
      if data != cmp_data: return False
  if l != length:
    for dst in dsts:
      if dst.read(1): return False
  return True

io_diff._required_globals = ["io_iterread1"]
