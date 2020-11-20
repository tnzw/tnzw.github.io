# FileIO.py Version 1.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class FileIO(io.IOBase):  # XXX test it !!!
  # https://docs.python.org/3/library/io.html#io.FileIO
  # dir(io.FileIO()) → ['__IOBase_closed', '__class__',
  #  '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__ne__', '__new__', '__next__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
  #  '_blksize', '_checkClosed', '_checkReadable', '_checkSeekable', '_checkWritable', '_dealloc_warn', '_finalizing',
  #  'close', 'closed', 'closefd', 'fileno', 'flush', 'isatty', 'mode', 'name', 'read', 'readable', 'readall', 'readinto', 'readline', 'readlines', 'seek', 'seekable', 'tell', 'truncate', 'writable', 'write', 'writelines']
  # RawIOBase like mixins methods
  #def read(self, size=None): raise io.UnsupportedOperation("read")
  def readall(self):
    f, d = self.read(), self.read()
    while d: f, d = f + d, self.read()
    return f

  # RawIOBase like stub methods
  def readinto(self, b):  # actualy not sure it uses self.read
    d = self.read(len(b))
    ld = len(d)
    b[:ld] = d
    return ld
    #i, d = -1, self.read(len(b))
    #for i,c in enumerate(d): b[i] = c
    #return i + 1

  # FileIO methods
  DEFAULT_BUFFER_SIZE = io.DEFAULT_BUFFER_SIZE
  _closed = False
  def __init__(self, name, mode="r", closefd=True, opener=None, os_module=None):
    if os_module is None: os_module = os
    self._os_module = os_module
    if opener is None: opener = self._os_module.open
    self.name = name
    self._closefd = True if closefd else False
    flags = convert_open_mode_to_flags(mode, os_module=self._os_module) | getattr(self._os_module, "O_NOINHERIT", 0) | getattr(self._os_module, "O_BINARY", 0)
    self.mode = convert_open_flags_to_mode(flags, os_module=self._os_module)
    self._fileno = opener(name, flags)
    w,rw = flags & self._os_module.O_WRONLY, flags & self._os_module.O_RDWR
    r = 1 if w + rw == 0 else 0
    self._readable = True if r or rw else False
    self._writable = True if w or rw else False
    self._seekable = True
  # __del__ is implemented by IOBase
  # __enter__ is implemented by IOBase
  # __exit__ is implemented by IOBase

  # _blksize
  def _checkClosed(self):
    if self.closed: raise ValueError("I/O operation on closed file.")
  def _checkReadable(self):
    if not self.readable(): raise io.UnsupportedOperation("not readable")
  def _checkSeekable(self):
    if not self.seekable(): raise io.UnsupportedOperation("not seekable")
  def _checkWritable(self):
    if not self.writable(): raise io.UnsupportedOperation("not writable")
  # _dealloc_warn
  # _finalizing

  def close(self):  # overrides IOBase method
    if self.closed: return
    self.flush()
    if self._closefd: self._os_module.close(self._fileno)
    self._closed = True
  @property
  def closed(self): return self._closed  # overrides IOBase method
  def fileno(self): return self._fileno  # overrides IOBase method
  def flush(self):  # overrides IOBase method
    self._os_module.fsync(self._fileno)
  # isatty is implemented by IOBase
  mode = "r"
  name = ""
  def read(self, size=None):
    self._checkReadable()
    self._checkClosed()
    if size is None: size = -1
    if size < 0:
      f, d = self._os_module.read(self._fileno, self.DEFAULT_BUFFER_SIZE), self._os_module.read(self._fileno, self.DEFAULT_BUFFER_SIZE)
      while d: f, d = f + d, self._os_module.read(self._fileno, self.DEFAULT_BUFFER_SIZE)
      return f
    f = self._os_module.read(self._fileno, self.DEFAULT_BUFFER_SIZE if self.DEFAULT_BUFFER_SIZE < size else size)
    size -= len(f)
    d = self._os_module.read(self._fileno, self.DEFAULT_BUFFER_SIZE if self.DEFAULT_BUFFER_SIZE < size else size)
    size -= len(d)
    while d and size > 0:
      f, d = self._os_module.read(self._fileno, self.DEFAULT_BUFFER_SIZE if self.DEFAULT_BUFFER_SIZE < size else size)
      size -= len(d)
    return f
  def read1(self, size=-1): return self._os_module.read(size)
  def readable(self): return self._readable  # overrides IOBase method
  # readline is implemented by IOBase
  # readlines is implemented by IOBase
  def seek(self, offset, whence=0):  # overrides IOBase method
    self._checkSeekable()
    self._checkClosed()
    return self._os_module.lseek(self._fileno, offset, whence)
  def seekable(self): return self._seekable  # overrides IOBase method
  # tell is implemented by IOBase
  def truncate(self, size=None):
    self._checkWritable()
    self._checkClosed()
    if size is None: size = self.tell()
    if size < 0: XXX
    self._os_module.ftruncate(self._fileno, size)
  def writable(self): return self._writable  # overrides IOBase method
  def write(self, b):
    self._checkWritable()
    self._checkClosed()
    lb = len(b)
    i = self._os_module.write(self._fileno, b)
    w = i
    while i > 0 and w < lb:
      i = self._os_module.write(self._fileno, b[w:])
      w += i
    return w
  # writelines is implemented by IOBase

FileIO._required_globals = ["os", "io"]
