# RawIOBase.py Version 1.0.1
# Copyright (c) 2020-2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class RawIOBase(object):
  # https://docs.python.org/3/library/io.html#io.IOBase
  # https://docs.python.org/3/library/io.html#io.RawIOBase

  def __del__(self): self.close()
  def _checkClosed(self):
    if self.closed: raise ValueError("I/O operation on closed file.")
  def _checkReadable(self):
    if not self.readable(): raise io.UnsupportedOperation("not readable")
  def _checkSeekable(self):
    if not self.seekable(): raise io.UnsupportedOperation("not seekable")
  def _checkWritable(self):
    if not self.writable(): raise io.UnsupportedOperation("not writable")

  # IOBase mixins methods and properties
  def close(self):
    if self.closed: return
    self.flush()
    # ...
  @property
  def closed(self): return False
  def __enter__(self): pass
  def __exit__(self, type, value, traceback): self.close()
  def flush(self): self._checkClosed()
  def isatty(self): return False
  def __iter__(self): return self
  def __next__(self):
    line = self.readline()
    if line: return line
    raise StopIteration
  def readable(self): return False
  def readline(self, size=-1):
    if size is None: size = -1
    if size == 0: return b""
    line, l = b"", 0
    d = self.read(1)
    while d:
      line, l = line + d, l + len(d)
      if d == b"\n" or (size > 0 and l >= size): return line
      d = self.read(1)
    return line
  def readlines(self, hint=-1):
    if hint is None: hint = -1
    l, lines = 0, []
    for line in self:
      lines.append(line)
      l += len(line)
      if hint >= 0 and l >= hint: return lines
    return lines
  def seekable(self): return False
  def tell(self): return self.seek(0, 1)  # io.SEEK_CUR
  def writable(self): return False
  def writelines(self, lines):
    for line in lines: self.write(line)

  # IOBase stub methods
  def fileno(self): raise io.UnsupportedOperation("fileno")
  def seek(self, offset, whence=0): raise io.UnsupportedOperation("seek")
  def truncate(self, size=None): raise io.UnsupportedOperation("truncate")

  # RawIOBase mixins methods
  def read(self, size=-1):
    if size is None or size < 0: return self.readall()
    if size == 0: return b""
    read = []
    buffer = bytearray(size)
    while buffer:
      r = self.readinto(buffer)
      if r is None: raise io.UnsupportedOperation("unhandled non-blocking mode")
      if r <= 0: break
      read.append(buffer[:r])
      buffer = buffer[r:]
    return b"".join(read)
  def readall(self):
    def checkbufsize(v):
      if isinstance(v, int) and v > 0: return v
      raise TypeError("invalid blksize")
    blksize = 8192
    try: blksize = checkbufsize(DEFAULT_BUFFER_SIZE)
    except (NameError, TypeError):
      try: blksize = checkbufsize(io.DEFAULT_BUFFER_SIZE)
      except (NameError, AttributeError, TypeError): pass
    read = []
    while True:
      buffer = bytearray(blksize)
      r = self.readinto(buffer)
      if r is None: raise io.UnsupportedOperation("unhandled non-blocking mode")
      if r <= 0: break
      read.append(buffer[:r])
    return b"".join(read)

  # RawIOBase stub methods
  def readinto(self, b): raise NotImplementedError
  def write(self, b): raise NotImplementedError

  ## custom methods, to be overriden
  #def readinto(self, b):
  #  self._checkReadable()
  #  self._checkClosed()
  #  ...
  #def write(self, b):
  #  self._checkWritable()
  #  self._checkClosed()
  #  ...
  #def seek(self, offset, whence=SEEK_SET):
  #  self._checkSeekable()
  #  self._checkClosed()
  #  ...
  #def truncate(self, size=None):
  #  self._checkWritable()
  #  self._checkClosed()
  #  ...

RawIOBase._required_globals = ["io"]
