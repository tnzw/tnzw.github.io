# io_copy.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def io_copy():
  def io_copy(*a, **k):
    """\
io_copy(fsrc, fdst, **opt) -> read, written
  length => None or < 0 : read/write as most data as possible
                      0 : read/write no data
                    > 0 : maximum read/write amount of data
  buffer_size => None : read/write chunks with default max buffer_size then loop
                 > 0  : read/write chunks with max buffer_size then loop
                 < 0  : read full data and write
"""
    for read, written in iter(*a, **k): pass
    return read, written
  def iter(fsrc, fdst, length=None, buffer_size=None):
    """for read, written in io_copy.iter(fsrc, fdst, **opt): notify_progress(read, written)"""
    read, written = None, 0, 0
    if length is not None and length > 0:
      if buffer_size is not None and buffer_size < 0:
        length = [] if length is None else [length]
        data = fsrc.read(*length)
        read = len(data)
        yield read, written
        fdst.write(data)
        written = read
        yield read, written
      else:
        for data in io_iterread1(fsrc, length=length, size=buffer_size):
          read += len(data)
          yield read, written
          fdst.write(data)
          written = read
          yield read, written
    if read == 0: yield read, written
  io_copy.iter = iter
  return io_copy
io_copy = io_copy()
