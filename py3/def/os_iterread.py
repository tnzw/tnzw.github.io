# os_iterread.py Version 1.0.1
# Copyright (c) 2020-2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_iterread(fd, length=None, size=None, *, os_module=None):
  """\
os_iterread(fd, [length, [size]], **opt)

ex: os_iterread(fd, 4096, size=st_blksize)

fd: a readable file descriptor
length => None or < 0: read as most data as possible (default)
                    0: read no data
                  > 0: maximum read amount of data
size => None or < 0: maximum chunk size to read is 4096 (default)
                  0: read no data
                > 0: maximum chunk size to read
                     (use the file blksize for optimal performances)
opt:
  os_module: the module to use to act on fd (defaults to os module)
             (uses os.read)
"""
  if os_module is None: os_module = os
  if size is None or size < 0: size = 4096
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
