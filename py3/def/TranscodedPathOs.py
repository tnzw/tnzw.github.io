# TranscodedPathOs.py Version 2.1.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class TranscodedPathOs(object):
  # https://docs.python.org/3/library/os.html
  # encode_method example :
  #   def encode_method(transpathos, path, dir_path=None, dir_fd=None):
  #     # `path` is relative to `dir_path` which is relative to transpathos.getcwd().
  #     # `dir_path` is set on `listdir(dir_path)` or `scandir(dir_path)` calls.
  #     # ... do encode
  #     return encoded_path

  def __init__(self, encode_method, decode_method, *, path_module=None, os_module=None):
    self.os = os if os_module is None else os_module
    if path_module is not None: self.path = path_module
    self._encode_path_method = encode_method
    self._decode_path_method = decode_method

    for _ in ("open", "chdir", "chmod", "chown", "chroot", "lchmod", "lchown", "lstat", "mkdir", "makedirs", "readlink", "remove", "removedirs", "rmdir", "stat", "truncate", "unlink", "utime", "walk"):
      if hasattr(self.os, _):
        exec(f"def {_}(path, *a, **k): return self.os.{_}(path if isinstance(path, int) else self._encode_path_method(self, path), *a, **k)\nself.{_} = {_}", {"self": self}, {})
    for _ in ("link", "rename", "replace", "symlink"):
      if hasattr(self.os, _):
        exec(f"def {_}(src, dst, *a, **k): return self.os.{_}(src if isinstance(src, int) else self._encode_path_method(self, src), dst if isinstance(dst, int) else self._encode_path_method(self, dst), *a, **k)\nself.{_} = {_}", {"self": self}, {})
    if hasattr(self.os, "getcwdb"):
      def getcwdb(): return self._decode_path_method(self, self.os.getcwdb())
      self.getcwdb = getcwdb
      def getcwd(): return self.fsdecode(self.getcwdb())
      self.getcwd = getcwd
    else:
      def getcwd(): return self._decode_path_method(self, self.os.getcwd())
      self.getcwd = getcwd

  def listdir(self, path="."):
    if isinstance(path, int):
      return [self._decode_path_method(self, _, dir_fd=path) for _ in self.os.listdir(path)]
    epath = self._encode_path_method(self, path)
    return [self._decode_path_method(self, _, dir_path=epath) for _ in self.os.listdir(epath)]

  def __getattr__(self, name): return getattr(self.os, name)

  def scandir(self, path="."):
    if isinstance(path, int):
      scan = self.os.scandir(path)
      return ScandirIterator(scan, (DirEntry(name=self._decode_path_method(self, _.name, dir_fd=path), dir_fd=path, os_module=self) for _ in scan))
    epath = self._encode_path_method(self, path)
    scan = self.os.scandir(epath)
    def __iter__():
      for _ in scan:
        name = self._decode_path_method(self, _.name, dir_path=epath)
        full = self.path.join(path, name)
        yield DirEntry(path=full, name=name, os_module=self)
    return ScandirIterator(scan, __iter__())

  #def fwalk(self, top=".", topdown=True, onerror=True, *, follow_symlinks=False, dir_fd=None): XXX

TranscodedPathOs._required_globals = ["os", "DirEntry", "ScandirIterator"]
