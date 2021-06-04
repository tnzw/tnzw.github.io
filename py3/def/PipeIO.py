# PipeIO.py Version 1.2.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class PipeIO(object):
  # io.IOBase
  #   mixins ["close", "closed", "__enter__", "__exit__", "flush", "isatty",
  #           "__iter__", "__next__", "readable", "readline", "readlines",
  #           "seekable", "tell", "writable", "writelines"]
  #   stubs  ["fileno", "seek", "truncate"]

  for _ in ("__enter__", "__exit__", "flush", "isatty",
            "__iter__", "__next__", "readline", "readlines", "writelines",
            "fileno", "_checkClosed"):
    exec(f"def {_}(self, *a, **k): return RawIOBase.{_}(self, *a, **k)", globals(), locals())
  del _

  # io.RawIOBase
  #   mixins IOBase + ["read", "readall"]
  #   stubs  ["readinto", "write"]

  # io.BufferedIOBase
  #   mixins IOBase + ["readinto", "readinto1"]
  #   stubs  ["detach", "read", "read1", "write"]

  @property
  def closed(self): return self.buffer is None
  def close(self): self.buffer = None

  _cast = None
  buffer = None
  def __init__(self, buffer=None, cast=None):
    self.buffer = bytearray() if buffer is None else buffer
    if cast is None and isinstance(self.buffer, bytearray): self._cast = bytes
    else: self._cast = cast

  def peek(self, size=-1):
    self._checkClosed()
    if size is None or size < 0: return self.buffer[:]
    d = self.buffer[:size]
    return self._cast(d) if self._cast else d

  def readable(self): return True

  def readinto1(self, b):
    self._checkClosed()
    l = min(len(self.buffer), len(b))
    b[:l], self.buffer[:] = self.buffer[:l], self.buffer[l:]
    return l

  def read1(self, size=-1):
    self._checkClosed()
    if size is None or size < 0:
      d, self.buffer[:] = self.buffer[:], ()
    else:
      d, self.buffer[:] = self.buffer[:size], self.buffer[size:]
    return self._cast(d) if self._cast else d

  def readall(self):
    self._checkClosed()
    d, self.buffer[:] = self.buffer[:], ()
    return self._cast(d) if self._cast else d

  def readinto(self, b): return self.readinto1(b)
  def read(self, size=-1): return self.read1(size)

  def seekable(self): return False

  def lwrite(self, b):
    self._checkClosed()
    lb = len(b)
    self.buffer[:0] = b
    return lb

  def write(self, b):
    self._checkClosed()
    lr, lb = len(self.buffer), len(b)
    self.buffer[lr:] = b
    return lb

  def writable(self): return True
