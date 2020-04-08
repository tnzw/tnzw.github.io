# io_pipe.py Version 1.1.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def io_pipe(fsrc, fdst, buffer_size=None):
  """\
io_pipe(fsrc, fdst, **opt) -> Error, read_count, written_count
  buffer_size => None : read/write chunks with default max buffer_size then loop
                 > 0  : read/write chunks with max buffer_size then loop
                 < 0  : read full data and write
"""
  err, read, written = None, 0, 0
  try:
    if isinstance(buffer_size, int) and buffer_size < 0:
      data = fsrc.read()
      read = len(data)
      fdst.write(data)
      written = read
    else:
      for data in io_iterread1(fsrc, size=buffer_size):
        read += len(data)
        fdst.write(data)
        written = read
  except Exception as e:
    err = e
  return err, read, written
