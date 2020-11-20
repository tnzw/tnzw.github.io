# BytearrayIO.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

#if __name__ != "__main__": import io

class BytearrayIO(io.IOBase):  # XXX test it !!!
  """\
ba = bytearray()
io = BytearrayIO(ba)
io.write(b"blue")
ba  # bytearray(b"blue")
"""
  # https://docs.python.org/3/library/io.html#io.IOBase
  # RawIOBase like mixins methods
  #def read(self, size=None): raise io.UnsupportedOperation("read")
  def readall(self):
    f, d = self.read(), self.read()
    while d: f, d = f + d, self.read()
    return f

  # RawIOBase like stub methods
  def readinto(self, b):  # actualy not sure it uses self.read
    i, d = -1, self.read(len(b))
    for i,c in enumerate(d): b[i] = c
    return i + 1

  # BytearrayIO methods
  _index = 0
  def __init__(self, buffer=None, *, readable=None, writable=None, seekable=None, append=None, truncate=None):
    if buffer is None: buffer = bytearray()
    if not isinstance(buffer, bytearray): raise TypeError("buffer is not bytearray")
    self._buffer = buffer
    self._readable = True if readable is None or readable else False
    self._writable = True if writable is None or writable else False
    self._seekable = True if seekable is None or seekable else False
    self._append = True if append is not None and append else False
    self._truncate = True if truncate is not None and truncate else False
  def readable(self): return self._readable  # override method
  def read(self, size=None):
    if not self.readable(): raise io.UnsupportedOperation("not readable")
    if self.closed: raise ValueError("I/O operation on closed file.")
    if size is None or size < 0: d = bytes(self._buffer[self._index:])
    else: d = bytes(self._buffer[self._index:self._index + size])
    self._index = self._index + len(d)
    return d
  #def read1(self, size=-1): return self.read(size)
  def writable(self): return self._writable  # override method
  def write(self, b):
    if not self.writable(): raise io.UnsupportedOperation("not writable")
    if self.closed: raise ValueError("I/O operation on closed file.")
    l = len(b)
    if self._append: self._buffer.extend(b)
    else:
      i, lb = self._index, len(self._buffer)
      delta = i - lb
      if delta > 0: self._buffer[lb:] = b"\x00" * delta  # normaly sparse file ?
      self._buffer[i:i + l] = b
    self._index += l
    return l
  #readline is already implemented by IOBase
  #readlines is already implemented by IOBase
  def seekable(self): return self._seekable  # override method
  def seek(self, offset, whence=0):  # text io cannot have offset != 0
    if not self.seekable(): raise io.UnsupportedOperation("not seekable")
    if self.closed: raise ValueError("I/O operation on closed file.")
    if whence == 0: i = offset
    elif whence == 1: i = self._index + offset
    elif whence == 2: i = len(self._buffer) + offset
    else: raise ValueError(f"invalid whence ({whence}, should be 0, 1 or 2)")
    if i < 0: raise OSError(errno.EINVAL, "Invalid argument")
    self._index = i
    return i
  #tell is already implemented by IOBase, it uses seek.
  def truncate(self, size=None):
    if not self.writable(): raise io.UnsupportedOperation("not writable")
    if self.closed: raise ValueError("I/O operation on closed file.")
    if size is None: size = self._index
    lb = len(self._buffer)
    delta = size - lb
    if delta == 0: return size
    if delta > 0:
      self._buffer[lb:] = b"\x00" * delta
      return lb + delta
    self._buffer[:] = self._buffer[:size]
    return size

BytearrayIO._required_globals = ["io"]
