# open2.py Version 2.1.2
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def open2(file, mode="r", buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None, blksize=None, os_module=None):
  """\
Similar to `io.open` or `open` except:
- You can choose default os module to use (`os_module = os` by default);
- Does not check for valid file descriptor returned by opener.
- `encoding` is "UTF-8" by default and `errors` is "strict"
- Uses os_module.linesep or fallback to "" if newline is None
"""
  if os_module is None: os_module = os
  if encoding is None: encoding = "UTF-8"
  if errors is None: errors = "strict"
  if newline is None: newline = getattr(os_module, "linesep", "")
  if opener is None: opener = os_module.open
  mode = "".join(sorted(mode))
  io_opt = {}
  if buffering >= 0: io_opt["buffer_size"] = buffering
  p,a,b,r,t,w,x = io_parsemode(mode)
  io_mode = a+r+w+x+"b"+p
  file_io = FileIO(file, io_mode, closefd=closefd, opener=opener, blksize=blksize, os_module=os_module)
  if buffering == 0:
    if b: return file_io
    raise ValueError("can't have unbuffered text I/O")
  # "io" is not required when open2(..., mode="rb", buffering=0, ...)
  if p: io_buf = io.BufferedRandom(file_io, **io_opt)
  elif r: io_buf = io.BufferedReader(file_io, **io_opt)
  else: io_buf = io.BufferedWriter(file_io, **io_opt)
  if b: return io_buf
  return io.TextIOWrapper(io_buf, encoding=encoding, errors=errors, newline=newline)
open2._required_globals = ["os", "io", "FileIO", "io_parsemode"]
