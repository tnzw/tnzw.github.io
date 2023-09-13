# io_iterread.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def io_iterread(reader, buffer_size, length=None):
  """\
io_iterread(reader, 1024, 4096)

Calls `reader.read()` until length (or EOF) is reached.

  reader => an object that is readable
  buffer_size => None or < 0 : try to read all at once
                         > 0 : maximum chunk size to read
  length => None or < 0 : read as most data as possible
                      0 : read no data
                    > 0 : maximum read amount of data
"""
  read = reader.read
  if length is None or length < 0:
    while 1:
      data = read(buffer_size)
      if data: yield data
      else: break
  elif buffer_size is None or buffer_size < 0:
    while length > 0:
      data = read(length)
      if data: yield data
      else: break
      length -= len(data)
  else:
    while length > 0:
      data = read(length if length < buffer_size else buffer_size)
      if data: yield data
      else: break
      length -= len(data)
