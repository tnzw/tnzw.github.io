# TranscodedPathOs.py Version 1.1.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class TranscodedPathOs(object):
  # https://docs.python.org/3/library/os.html

  def __init__(self, encoder, decoder, *, os_module=None):
    self.os = os if os_module is None else os_module
    self._path_encoder = encoder
    self._path_decoder = decoder

    for _ in ("open", "chdir", "chmod", "chown", "chroot", "lchmod", "lchown", "lstat", "mkdir", "makedirs", "readlink", "remove", "removedirs", "rmdir", "stat", "truncate", "unlink", "utime", "walk"):
      if hasattr(self.os, _):
        exec(f"def {_}(path, *a, **k): return self.os.{_}(path if isinstance(path, int) else self._path_encoder(path), *a, **k)\nself.{_} = {_}", {"self": self}, {})
    for _ in ("link", "rename", "replace", "symlink"):
      if hasattr(self.os, _):
        exec(f"def {_}(src, dst, *a, **k): return self.os.{_}(src if isinstance(src, int) else self._path_encoder(src), dst if isinstance(dst, int) else self._path_encoder(dst), *a, **k)\nself.{_} = {_}", {"self": self}, {})
    if hasattr(self.os, "getcwdb"):
      def getcwdb(): return self._path_decoder(self.os.getcwdb())
      self.getcwdb = getcwdb
      def getcwd(): return self.fsdecode(self.getcwdb())
      self.getcwd = getcwd
    else:
      def getcwd(): return self._path_decoder(self.os.getcwd())
      self.getcwd = getcwd

  def listdir(self, path="."):
    path = self._path_encoder(path)
    return [self._path_decoder(_) for _ in self.os.listdir(path)]

  def __getattr__(self, name): return getattr(self.os, name)

  class DirEntry(object):
    def __init__(self, actual_entry, os_module):
      self._actual_entry = actual_entry
      self.name = os_module._path_decoder(self._actual_entry.name)
      #if not isinstance(path, str): getcwd = getattr(os_module, "getcwdb", lambda: os_module.fsencode(os_module.getcwd()))()
      #else: getcwd = os_module.getcwd()
      # ARG getcwd cannot be correct as we should getcwd of CALLER os…
      #self.path = os_module.path.join(getcwd, path, self.name)
    @property
    def path(self): raise NotImplementedError()
    def __getattr__(self, name): return getattr(self._actual_entry, name)

  def scandir(self, path="."):
    path = self._path_encoder(path)
    return (self.DirEntry(_, self) for _ in self.os.scandir(path))

  #def fwalk(self, top=".", topdown=True, onerror=True, *, follow_symlinks=False, dir_fd=None): XXX

TranscodedPathOs._required_globals = ["os"]
