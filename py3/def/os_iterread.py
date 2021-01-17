# os_iterread.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_iterread(fd, length=None, size=None, *, os_module=None):
  """\
ex: os_iterread(fd, length=4096, size=1024)
  fd => a readable file descriptor
  length => None or < 0 : read as most data as possible
                      0 : read no data
                    > 0 : maximum read amount of data
  size => None or < 0 : use the default maximum chunk size to read
                    0 : read no data
                  > 0 : maximum chunk size to read
  os_module => None : the module to use to act on fd (defaults to os module)
                      required os.read
"""
  if os_module is None: os_module = os
  def getsize(v):
    if isinstance(v, int) and v > 0: return v
    raise TypeError("invalid buffer size")
  if size is None or size < 0:
    size = 32 * 1024
    try: size = getsize(os_iterread.DEFAULT_BUFFER_SIZE)
    except (AttributeError, TypeError):
      try: size = getsize(DEFAULT_BUFFER_SIZE)
      except (NameError, TypeError):
        try: size = getsize(io.DEFAULT_BUFFER_SIZE)
        except (NameError, AttributeError, TypeError): pass

  if length is None or length < 0:
    while 1:
      data = os_module.read(fd, size)
      if data: yield data
      else: break
  else:
    while length > 0:
      data = os_module.read(fd, length if length < size else size)
      if data: yield data
      else: break
      length -= len(data)
os_iterread._required_globals = ["os"]
