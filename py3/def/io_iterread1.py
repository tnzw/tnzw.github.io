# io_iterread1.py Version 2.0.0
# Copyright (c) 2020, 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def io_iterread1(reader, buffer_size=None, length=None, fallback=True):
  """\
io_iterread1(reader, -1, 4096, fallback=True)

Calls `reader.read1()` until length (or EOF) is reached.

  reader => an object that is readable
  buffer_size => None or < 0 : use the default maximum chunk size to read
                         > 0 : maximum chunk size to read
  length => None or < 0 : read as most data as possible
                      0 : read no data
                    > 0 : maximum read amount of data
  fallback => True : fallback to reader.read if reader.read1 is not available
"""
  def getsize(v):
    if isinstance(v, int) and v > 0: return v
    raise TypeError("invalid buffer size")
  if fallback:
    read = getattr(reader, "read1", None)
    if read is None:
      read = reader.read
      if buffer_size is None or buffer_size < 0:
        buffer_size = 32 * 1024
        try: buffer_size = getsize(io_iterread1.DEFAULT_BUFFER_SIZE)
        except (AttributeError, TypeError):
          try: buffer_size = getsize(DEFAULT_BUFFER_SIZE)
          except (NameError, TypeError):
            try: buffer_size = getsize(io.DEFAULT_BUFFER_SIZE)
            except (NameError, AttributeError, TypeError): pass
  else:
    read = reader.read1
  if length is None or length < 0:
    buffer_size = [] if buffer_size is None else [buffer_size]
    while 1:
      data = read(*buffer_size)
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
