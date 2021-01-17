# os_read.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_read(fd, n, *, force_seek=False, _seek_position=None, exact=False, os_module=None):
  """\
os_read(fd, n, **opt)
  opt
    force_seek      If true, then it uses `os.lseek` and `os.SEEK_CUR` to move if seek position hasn't changed automatically.
    _seek_position  Current `fd` lseek position. If None, then `os.lseek(fd, 0, os.SEEK_CUR)` is used to set it.
    exact           If true, then it uses `os.read` until precisely `n` size is reached.
                    If read data length is lower than n, then EOF is reached. If greater, then it raises an OSError.
    os_module       Uses another `os` module.
"""
  # is option ok ?    atmost          If false, then it uses `os.read` until `n` size is reached.
  if os_module is None: os_module = os
  if force_seek:
    if _seek_position is None: _seek_position = os_module.lseek(fd, 0, os_module.SEEK_CUR)
    def read(fd, n, p):
      data = os_module.read(fd, n)
      if p == os_module.lseek(fd, 0, os_module.SEEK_CUR): p = os_module.lseek(fd, len(data), os_module.SEEK_CUR)
      return data, p
  else:
    def read(fd, n, p): return os_module.read(fd, n), None
  data, _seek_position = read(fd, n, _seek_position)
  if exact:
    len_data = len(data)
    while len_data < n:
      d, _seek_position = read(fd, n - len_data, _seek_position)
      if not d: break
      data += d
      len_data += len(d)
    if len_data > n: raise OSError(0, "too much data")
  return data

os_read._required_globals = ["os"]
