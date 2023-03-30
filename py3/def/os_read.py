# os_read.py Version 2.0.0
# Copyright (c) 2021, 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_read(fd, n, *, atleast=False, force_seek=False, _seek_position=None, os_module=None):
  """\
os_read(fd, n, **opt)
  opt
    atleast         If true, then it uses os.read() until at least n size is reached.
                    If read data length is lower than n, then EOF is reached.
    force_seek      If true, then it uses os.lseek() and os.SEEK_CUR to move if seek position hasn't changed automatically.
                    Useful on some cases where reading directly on harddrive (on windows) does change file cursor.
    _seek_position  Current fd lseek position.  If None, then `os.lseek(fd, 0, os.SEEK_CUR)` is used to set it.
    os_module       Uses another os module object.
"""
  if os_module is None: os_module = os
  read = os_module.read
  if force_seek:
    lseek = os_module.lseek; SEEK_CUR = os_module.SEEK_CUR
    if _seek_position is None: _seek_position = lseek(fd, 0, SEEK_CUR)
    def read2(fd, n, p):
      data = read(fd, n)
      if p == lseek(fd, 0, SEEK_CUR): p = lseek(fd, len(data), SEEK_CUR)
      return data, p
  else:
    def read2(fd, n, p): return read(fd, n), None
  data, _seek_position = read2(fd, n, _seek_position)
  if atleast:
    len_data = len(data)
    while len_data < n:
      d, _seek_position = read2(fd, n - len_data, _seek_position)
      if not d: break
      data += d
      len_data += len(d)
    #if exact and len_data > n: raise OSError(0, "too much data")
  return data
os_read._required_globals = ['os']
