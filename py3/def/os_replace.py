# os_replace.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_replace(src, dst, *, src_dir_fd=None, dst_dir_fd=None, dst_st_mode=None, os_module=None):
  """\
Ensure `os.replace()` to respect documentation behavior.

Official documentation says:

    Rename the file or directory src to dst. If dst is a directory,
    OSError will be raised. If dst exists and is a file, it will be
    replaced silently if the user has permission. [..]

    >>> os.mkdir("haha")
    >>> os.mkdir("hihi")
    >>> os.replace("haha", "hihi")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    FileExistsError: [WinError 183] Cannot create a file when that file already exists: 'haha' -> 'hihi'

Actual behavior of native os.replace() on linux is:

    If src and dst are both directories, OSError will be
    raised only if dst is not empty.

    >>> os.mkdir("one")
    >>> os.mkdir("two")
    >>> os.replace("one", "two")  # no error
"""
  if os_module is None: os_module = os
  if dst_st_mode is None:
    if dst_dir_fd: dst_st_mode = os_module.fstat(dst_dir_fd).st_mode
    else: dst_st_mode = os_module.lstat(dst).st_mode
  if stat.S_ISDIR(dst_st_mode):
    raise FileExistsError(errno.EEXIST, "Cannot create a file when that file already exists", src, 183, dst)
  return os_module.replace(src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)
os_replace._required_globals = ["errno", "os", "stat"]
