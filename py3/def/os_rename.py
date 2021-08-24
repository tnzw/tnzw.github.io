# os_rename.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_rename(src, dst, *, src_dir_fd=None, dst_dir_fd=None, os_module=None):
  """\
Ensure `os.rename()` to fail if dst exists,
using os.stat(…, follow_symlinks=False) and os.rename().
Does not ensure atomicity (yet), but operation is still atomic on windows.
"""
  if os_module is None: os_module = os
  try: os_module.stat(dst, dir_fd=dst_dir_fd, follow_symlinks=False)
  except FileNotFoundError: pass
  else: raise FileExistsError(errno.EEXIST, "Cannot create a file when that file already exists", src, 183, dst)
  return os_module.rename(src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)
os_rename._required_globals = ["errno", "os"]
