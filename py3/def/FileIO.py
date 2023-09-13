# FileIO.py Version 2.1.3
# Copyright (c) 2020-2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class FileIO(object):
  """\
fileobj = FileIO('my_file', 'rb')
fileobj = FileIO(os.open('my_file', os.O_RDONLY))
"""
  # https://docs.python.org/3/library/io.html#io.FileIO
  # dir(io.FileIO()) → ['__IOBase_closed', '__class__',
  #  '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__ne__', '__new__', '__next__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
  #  '_blksize', '_checkClosed', '_checkReadable', '_checkSeekable', '_checkWritable', '_dealloc_warn', '_finalizing',
  #  'close', 'closed', 'closefd', 'fileno', 'flush', 'isatty', 'mode', 'name', 'read', 'readable', 'readall', 'readinto', 'readline', 'readlines', 'seek', 'seekable', 'tell', 'truncate', 'writable', 'write', 'writelines']

  # mix with RawIOBase
  for _ in ("__del__", "_checkClosed", "_checkReadable", "_checkSeekable", "_checkWritable",
            # IOBase mixins methods
            "close", "__enter__", "__exit__", "flush", "isatty", "__iter__", "__next__", "readable", "readline", "readlines", "seekable", "tell", "writable", "writelines",
            # IOBase stub methods
            "fileno", "seek", "truncate",
            # RawIOBase mixins methods
            "read", "readall",
            # RawIOBase mixins methods
            "readinto", "write"):
    exec(f"def {_}(*a, **k): return RawIOBase.{_}(*a, **k)", globals(), locals())
  del _

  def __repr__(self): return f'<{self.__class__.__qualname__} name={self.name!r} mode={self.mode!r} closefd={self._closefd!r}>'

  @property
  def closed(self): return self._closed
  @property
  def closefd(self): return self._closefd
  def fileno(self): return self._fileno

  mode = 'r'
  name = ''
  def __init__(self, name, mode='r', closefd=True, opener=None, *, blksize=None, os_module=None):
    self._closed = False
    self._fileno = None
    if os_module is None: os_module = os
    self._os_module = os_module
    self.name = name
    self._closefd = bool(closefd)  # Should only be used on __del__ method.
    if blksize is None: blksize = -1
    elif not isinstance(blksize, int): raise TypeError("blksize is not of type 'int'")
    if isinstance(name, int):
      self._fileno = name
    else:
      if not self._closefd: raise ValueError("Cannot use closefd=False with file name")
      p,a,b,r,t,w,x = io_parsemode(mode)
      if t: raise ValueError(f"invalid mode: {mode!r}")
      flags = 0
      if p: flags |= os_module.O_RDWR
      elif r: flags |= os_module.O_RDONLY
      else: flags |= os_module.O_WRONLY
      if w: flags |= os_module.O_CREAT | os_module.O_TRUNC
      elif x: flags |= os_module.O_CREAT | os_module.O_EXCL
      elif a: flags |= os_module.O_CREAT | os_module.O_APPEND
      # windows : + O_BINARY + O_NOINHERIT
      flags |= getattr(os_module, "O_BINARY", 0) | getattr(os_module, "O_NOINHERIT", 0)
      # linux : + O_CLOEXEC
      flags |= getattr(os_module, "O_CLOEXEC", 0)
      self.mode = a+r+w+x+"b"+p
      self._readable = bool(r+p)
      self._writable = bool(a+w+x+p)
      self._seekable = True  # Yes, it is even "seekable" if O_APPEND.
      if opener is None: opener = self._os_module.open
      self._fileno = opener(name, flags)
    # https://docs.python.org/3/library/io.html#io.DEFAULT_BUFFER_SIZE
    if blksize < 0:
      if hasattr(os_module, "fstat"):
        try: self._blksize = os_module.fstat(self._fileno).st_blksize
        except (OSError, AttributeError): pass
    elif blksize == 0: pass
    else:
      self._blksize = blksize

  _blksize = 4096
  # _dealloc_warn
  # _finalizing
  
  def __del__(self):
    if self._closefd: self.close()
  def close(self):
    if self._closed: return
    self.flush()
    self._os_module.close(self._fileno)
    self._closed = True
  def flush(self):
    # seems that sometimes an fd cannot be synced…
    try: self._os_module.fsync(self._fileno)
    except OSError as err:
      if err.errno != errno.EBADF: raise

  def readable(self): return self._readable
  def readall(self):
    self._checkReadable()
    self._checkClosed()
    read = []
    while True:
      r = self._os_module.read(self._fileno, self._blksize)
      if r: read.append(r)
      else: break
    return b"".join(read)
  def read(self, size=-1):
    self._checkReadable()
    self._checkClosed()
    if size is None or size < 0: return self.readall()
    read, l = [], 0
    while l < size:
      r = self._os_module.read(self._fileno, size - l)
      l += len(r)
      if r: read.append(r)
      else: break
    return b"".join(read)

  def read1(self, size=-1):
    self._checkReadable()
    self._checkClosed()
    if size is None or size < 0: size = self._blksize
    return self._os_module.read(self._fileno, size)

  def readinto(self, b):
    d = self.read(len(b))
    ld = len(d)
    b[:ld] = d
    return ld
  def readinto1(self, b):
    d = self.read1(len(b))
    ld = len(d)
    b[:ld] = d
    return ld

  def seek(self, offset, whence=0):
    self._checkSeekable()
    self._checkClosed()
    o = self._os_module
    return o.lseek(self._fileno, offset, (o.SEEK_SET, o.SEEK_CUR, o.SEEK_END)[whence])
  def seekable(self): return self._seekable

  def truncate(self, size=None):
    self._checkWritable()
    self._checkClosed()
    if size is None: size = self.tell()
    #if size < 0: raise OSError(errno.EINVAL, "Invalid argument")  # just propagate
    self._os_module.ftruncate(self._fileno, size)
  def writable(self): return self._writable
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

FileIO._required_globals = ["errno", "os", "RawIOBase", "io_parsemode"]
