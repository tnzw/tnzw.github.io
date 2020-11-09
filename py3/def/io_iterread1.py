# io_iterread1.py Version 1.1.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def io_iterread1(reader, length=None, size=None, fallback=True):
  """\
io_iterread1(reader, length=4096, size=1024, fallback=True)
  reader => an object that is readable
  length => None or < 0 : read/write as most data as possible
                      0 : read/write no data
                    > 0 : maximum read/write amount of data
  size => None or < 0 : use the default maximum chunk size to read
                  > 0 : maximum chunk size to read
  fallback => True : fallback to reader.read if reader.read1 is not available
"""
  def getsize(v):
    if isinstance(v, int) and v > 0: return v
    raise TypeError("invalid buffer size")
  if fallback:
    read = getattr(reader, "read1", None)
    if read is None:
      read = reader.read
      if size is None or size < 0:
        size = 32 * 1024
        try: size = getsize(io_iterread1.DEFAULT_BUFFER_SIZE)
        except (AttributeError, TypeError):
          try: size = getsize(DEFAULT_BUFFER_SIZE)
          except (NameError, TypeError):
            try: size = getsize(io.DEFAULT_BUFFER_SIZE)
            except (NameError, AttributeError, TypeError): pass
  else:
    read = reader.read1
  if length is None or length < 0:
    size = [] if size is None else [size]
    while 1:
      data = read(*size)
      if data: yield data
      else: break
  elif size is None or size < 0:
    while length > 0:
      data = read(length)
      if data: yield data
      else: break
      length -= len(data)
  else:
    while length > 0:
      data = read(length if length < size else size)
      if data: yield data
      else: break
      length -= len(data)
