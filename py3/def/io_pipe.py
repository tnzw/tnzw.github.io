# io_pipe.py Version 1.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def io_pipe(fsrc, fdst, buffer_size=16*1024):
  """\
io_pipe(fsrc, fdst, **opt) -> Error, read_count, written_count
  buffer_size => 16*1024 : > 0 : read and write chunks then loop
                           < 0 : read full data and write
"""
  if buffer_size < 0: buffer_size = None
  err, read, written = None, 0, 0
  try:
    data = fsrc.read(buffer_size)
    while data:
      read += len(data)
      fdst.write(data)
      written = read
  except Exception as e:
    err = e
  return err, read, written
