# io_iterread1.py Version 1.0.2
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def io_iterread1(reader, length=None, size=None, fallback=True):
  """\
io_iterread1(reader, length=4096, size=1024, fallback=True)
  reader   => an object that is readable
  length   => the total amount of data to read
  size     => the maximum chunk size to read
  fallback => fallback to reader.read if reader.read1 is not available
"""
  def getsize(v):
    if isinstance(v, int) and v > 0: return v
    raise TypeError("invalid buffer size")
  if fallback:
    read = getattr(reader, "read1", None)
    if read is None:
      read = reader.read
      if size is None:
        size = 32 * 1024
        try: size = getsize(io_iterread1.DEFAULT_BUFFER_SIZE)
        except (AttributeError, TypeError):
          try: size = getsize(DEFAULT_BUFFER_SIZE)
          except (NameError, TypeError):
            try: size = getsize(io.DEFAULT_BUFFER_SIZE)
            except (NameError, AttributeError, TypeError): pass
  else:
    read = reader.read1
  if length is None:
    size = [] if size is None else [size]
    while 1:
      data = read(*size)
      if data: yield data
      else: break
  elif size is None:
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
