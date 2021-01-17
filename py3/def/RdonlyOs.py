# RdonlyOs.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class RdonlyOs(object):
  """\
Same as os module but disallow writing the file system
"""
  # https://docs.python.org/3/library/os.html
  def __init__(self, os_module=None):
    self.os = os if os_module is None else os_module
    for _ in "error name path SEEK_SET SEEK_CUR SEEK_END O_RDONLY O_WRONLY O_RDWR O_APPEND O_CREAT O_EXCL O_TRUNC O_BINARY O_NOINHERIT curdir pardir sep altsep exstep pathsep linesep".split():
      if hasattr(self.os, _): setattr(self, _, getattr(self.os, _))
    def mkmeth(_):
      def fn(*a,**k): return getattr(self.os, _)(*a,**k)
      fn.__name__ = _
      return fn
    for _ in "fsencode fsdecode fspath umask close dup dup2 fstat isatty lseek pread preadv read readv chdir chroot getcwd getcwdb listdir lstat readlink scandir stat walk fwalk".split():
      setattr(self, _, mkmeth(_))
      #exec(f"""@property\ndef {_}(self):\n return self.os.{_}\nself.{_} = {_}\n""", globals(), locals())
    def mknop(_):
      def fn(*a,**k): raise OSError(errno.EROFS, "Read-only file system")
      fn.__name__ = _
      return fn
    for _ in "copy_file_range fchmod fchown fdatasync fsync ftruncate pwrite pwritev write writev chmod chown lchmod lchown link mkdir makedirs remove removedirs rename replace rmdir symlink sync truncate unlink utime".split():
      setattr(self, _, mknop(_))
    # for _ in "supports_dir_fd supports_effective_ids supports_fd supports_follow_symlinks".split(): XXX
  def open(self, path, flags, mode=0o777, *, dir_fd=None):
    if flags & sum(getattr(self, _, 0) for _ in "O_WRONLY O_RDWR O_APPEND O_CREAT O_TRUNC".split()): raise OSError(errno.EROFS, "Read-only file system")
    return self.os.open(path, flags, mode=mode, dir_fd=dir_fd)
  def fdopen(self, fd, mode="r", *a, **k):
    if "r" not in mode or "+" in mode: raise OSError(errno.EROFS, "Read-only file system")
    return self.os.fdopen(fd, mode=mode, *a, **k)

RdonlyOs._required_globals = ["os", "errno"]
