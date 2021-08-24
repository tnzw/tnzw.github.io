# TranscodedContentOs.py Version 1.0.3
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class TranscodedContentOs(object):
  # https://docs.python.org/3/library/os.html

  _proc_fds = None

  def __init__(self, mkencoder, mkdecoder, *, os_module=None):
    self.os = os if os_module is None else os_module
    self._mkencoder = mkencoder
    self._mkdecoder = mkdecoder
    self._proc_fds = {}

    for _ in ("ftruncate", "truncate",):
      if hasattr(self.os, _):
        exec(f"def {_}(path, *a, **k):\n if isinstance(path, int): raise OSError(errno.EBADF, 'Bad file descriptor')\n return self.os.{_}(path, *a, **k)\nself.{_} = {_}", {"self": self}, {})

  def __getattr__(self, name): return getattr(self.os, name)

  def fdopen(self, *a, **k): return open2(*a, os_module=self, **k)

  def open(self, path, flags, mode=0o777, *, dir_fd=None):
    fd = None
    try:
      fd = self.os.open(path, flags | getattr(self, "O_BINARY", 0), mode, dir_fd=dir_fd)
      fds = {"path": self.os.fspath(path), "flags": flags, "EOF": False, "encoder": None, "decoder": None}
      if (flags & self.os.O_RDWR) == self.os.O_RDWR: fds["encoder"], fds["decoder"] = self._mkencoder(path, flags), self._mkdecoder(path, flags)
      elif (flags & self.os.O_WRONLY) == self.os.O_WRONLY: fds["encoder"] = self._mkencoder(path, flags)
      elif (flags & self.os.O_RDONLY) == self.os.O_RDONLY: fds["decoder"] = self._mkdecoder(path, flags)
      else: raise OSError(errno.EINVAL, "unhandled flags")
      self._proc_fds[fd] = fds
    except:
      if fd is not None: self.close(fd)
      raise
    return fd

  def lseek(self, fd, pos, how):
    if pos != 0 or how != self.os.SEEK_END:
      raise OSError(errno.EINVAL, f"{self.__class__.__name__}: unhandled lseek (fd, pos={pos!r}, how={how!r})")
    return self.os.lseek(fd, pos, how)

  def read(self, fd, n):
    fds = self._proc_fds[fd]
    if fds["EOF"]: return b""
    o_binary = getattr(self.os, "O_BINARY", 0)
    binary = (fds["flags"] & o_binary) == o_binary
    linesepb = getattr(self.os, "linesep", "\n").encode("ascii")
    def rep(d):
      if binary or linesepb == b"\n": return d
      if linesepb == b"\r\n": return d.replace(b"\r", b"")
      if len(linesepb) == 1: return d.replace(linesepb, b"\n")
      raise NotImplementedError()
    d = fds["decoder"]
    data = b""
    while data == b"":
      str = self.os.read(fd, n)
      if not str:
        fds["EOF"] = True
        return rep(d.decode())
      data = rep(d.decode(str, stream=True))
    return data

  def write(self, fd, str):
    fds = self._proc_fds[fd]
    O_BINARY = getattr(self.os, "O_BINARY", 0)
    LINESEP = getattr(self.os, "linesep", "\n")
    e = fds["encoder"]
    if (fds["flags"] & O_BINARY) == O_BINARY or LINESEP == "\n": astr = str
    else: astr = str.replace(b"\n", LINESEP.encode("ascii"))
    data = e.encode(astr, stream=True)
    written, expected = 0, len(data)
    while written < expected:
      w = self.os.write(fd, data[written:])
      if w == 0: raise OSError(XXX)
      written += w
    return len(str)  # on windows, `os.write(no_binary_fd, b"a\nb")` returns 3, but file size is 4.

  def close(self, fd):
    fds = self._proc_fds.get(fd, None)
    if fds is not None and fds["encoder"] is not None:
      data = fds["encoder"].encode()
      written, expected = 0, len(data)
      while written < expected:
        w = self.os.write(fd, data[written:])
        if w == 0: raise OSError(XXX)
        written += w
    try: self.os.close(fd)
    except OSError as err:
      if err.errno != errno.EBADF: raise
    if fd in self._proc_fds: del self._proc_fds[fd]

TranscodedContentOs._required_globals = ["errno", "os", "open2"]
