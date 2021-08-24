# DirEntry.py Version 1.2.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class DirEntry(object):
  # /!\ It does not follow os.chdir calls. Use `dir_fd` for more security.
  #     It does not guess `path`, it has to be set manually.
  #     It does not use `os.fspath` to clean up `path` or `name`.
  #     It does not check the type of any value.
  __slots__ = ("name", "path", "dir_fd", "os", "_lstat", "_stat")
  def __init__(self, path=None, *, name=None, dir_fd=None, os_module=None, _lstat=None, _stat=None):
    self.os = os if os_module is None else os_module
    self.path = path
    self.dir_fd = dir_fd
    self.name = self.os.path.basename(path) if name is None else name
    self._lstat = _lstat
    self._stat = _stat
  def __repr__(self): return f"<{self.__class__.__name__} {self.name!r}>"
  def inode(self): return self.stat(follow_symlinks=False).st_ino
  def is_dir(self, *, follow_symlinks=True): return stat.S_ISDIR(self.stat(follow_symlinks=follow_symlinks).st_mode)
  def is_file(self, *, follow_symlinks=True): return stat.S_ISREG(self.stat(follow_symlinks=follow_symlinks).st_mode)
  def is_symlink(self): return stat.S_ISLNK(self.stat(follow_symlinks=False).st_mode)
  def stat(self, *, follow_symlinks=True):
    if follow_symlinks:
      if self._stat: return self._stat
      self._stat = self.os.stat(self.path, dir_fd=self.dir_fd, follow_symlinks=True)
      return self._stat
    if self._lstat: return self._lstat
    self._lstat = self.os.stat(self.path, dir_fd=self.dir_fd, follow_symlinks=False)
    return self._lstat
