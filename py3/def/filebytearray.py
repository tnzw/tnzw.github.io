# filebytearray.py Version 1.0.0
# Copyright (c) 2022-2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class filebytearray:
  # usage:
  #   with filebytearray('path') as fba:
  #     # ...

  # >>> dir(bytearray(0))
  # ['__add__', '__alloc__', '__class__', '__contains__', '__delattr__',
  #  '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
  #  '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__',
  #  '__imul__', '__init__', '__init_subclass__', '__iter__', '__le__',
  #  '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__',
  #  '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__',
  # '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__',
  # 'append', 'capitalize', 'center', 'clear', 'copy', 'count', 'decode',
  # 'endswith', 'expandtabs', 'extend', 'find', 'fromhex', 'hex', 'index',
  # 'insert', 'isalnum', 'isalpha', 'isascii', 'isdigit', 'islower', 'isspace',
  # 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans',
  # 'partition', 'pop', 'remove', 'removeprefix', 'removesuffix', 'replace',
  # 'reverse', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip',
  # 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title',
  # 'translate', 'upper', 'zfill']

  @property
  def closed(self): return self._closed
  @property
  def closefd(self): return self._closefd
  def fileno(self): return self._fileno
  @property
  def readonly(self): return self._readonly

  mode = 'r'
  name = ''
  _blksize = 4096
  def __init__(self, name, mode='r', closefd=True, opener=None, *, blksize=None, os_module=None):
    self._closed = False
    self._fileno = None
    if os_module is None: os_module = os
    self._os_module = os_module
    self.name = name
    self._closefd = bool(closefd)
    if blksize is None: blksize = -1
    elif not isinstance(blksize, int): raise TypeError("blksize is not of type 'int'")
    if isinstance(name, int):
      self._fileno = name
    else:
      if not self._closefd: raise ValueError("Cannot use closefd=False with file name")
      p,a,b,r,t,w,x = io_parsemode(mode)
      if t or a: raise ValueError(f"invalid mode: {mode!r}")
      flags = 0
      if p: flags |= os_module.O_RDWR
      elif r: flags |= os_module.O_RDONLY
      else: flags |= os_module.O_WRONLY
      if w: flags |= os_module.O_CREAT | os_module.O_TRUNC
      elif x: flags |= os_module.O_CREAT | os_module.O_EXCL
      #elif a: flags |= os_module.O_CREAT | os_module.O_APPEND
      # windows : + O_BINARY + O_NOINHERIT
      flags |= getattr(os_module, "O_BINARY", 0) | getattr(os_module, "O_NOINHERIT", 0)
      # linux : + O_CLOEXEC
      flags |= getattr(os_module, "O_CLOEXEC", 0)
      self.mode = r+w+x+"b"+p
      self._readonly = not (w+x+p)
      if opener is None: opener = os_module.open
      self._fileno = opener(name, flags)
    # https://docs.python.org/3/library/io.html#io.DEFAULT_BUFFER_SIZE
    if blksize < 0:
      if hasattr(os_module, 'fstat'):
        try: self._blksize = os_module.fstat(self._fileno).st_blksize
        except (OSError, AttributeError): pass
    elif blksize == 0: pass
    else:
      self._blksize = blksize
  def __repr__(self): return f'<{self.__class__.__qualname__} name={self.name!r} mode={self.mode!r} closefd={self._closefd!r}>'
  def __del__(self):
    if self._closefd: self.close()
  def __enter__(self): return self
  def __exit__(self, *a): self.close()
  def __len__(self): _os = self._os_module; return _os.lseek(self._fileno, 0, _os.SEEK_END)
  def close(self):
    if self.closed: return
    self.flush()
    if self._closefd: self._os_module.close(self._fileno)
    self._closed = True
  def flush(self):
    # seems that sometimes an fd cannot be synced...
    try: self._os_module.fsync(self._fileno)
    except OSError as err:
      if err.errno != errno.EBADF: raise

  def __getitem__(self, key):
    key_type = type(key)
    if key_type is slice:
      _, _, step = key.indices(0)  # checking slice value types
      start, stop = key.start, key.stop
      _os = self._os_module; fileno = self._fileno; lseek = _os.lseek; SEEK_SET = _os.SEEK_SET; SEEK_END = _os.SEEK_END; read = _os.read
      data = bytearray()
      if step > 0:
        if start is None: start = 0
        if start < 0 or stop is not None and stop < 0: start, stop, step = key.indices(lseek(fileno, 0, SEEK_END))
        if step == 1:
          blksize = self._blksize
          lseek(fileno, start, SEEK_SET)
          l = blksize if stop is None else stop - start
          while l > 0:
            d = read(fileno, l); ld = len(d)
            if not ld: return data
            data.extend(d)
            start += ld
            l = blksize if stop is None else stop - start
          return data
        else:
          while stop is None or start < stop:
            lseek(fileno, start, SEEK_SET)
            d = read(fileno, 1)
            if not d: return data
            data.append(d[0])
            start += step
          return data
      else:
        start, stop, step = key.indices(lseek(fileno, 0, SEEK_END))
        for i in range(start, stop, step):
          lseek(fileno, i, SEEK_SET)
          d = read(fileno, 1)
          if not d: return data
          data.append(d[0])
        return data
    elif key_type is int:
      _os = self._os_module; fileno = self._fileno; lseek = _os.lseek; SEEK_SET = _os.SEEK_SET; read = _os.read
      if key < 0:
        key = lseek(fileno, 0, _os.SEEK_END) + key
        if key < 0: raise IndexError('filebytearray index out of range')
      lseek(fileno, key, SEEK_SET)
      d = read(fileno, 1)
      if d: return d[0]
      raise IndexError('filebytearray index out of range')
    raise TypeError(f'filebytearray indices must be integers or slices, not {key_type.__name__!r}')

  def __setitem__(self, key, item):
    if self._readonly: raise TypeError('cannot modify read-only filebytearray')
    key_type = type(key)
    item_type = type(item)
    if key_type is slice:
      _, _, step = key.indices(0)  # checking slice value types
      start, stop = key.start, key.stop
      #item = memoryview(item).tobytes()  # ensure that item is a bytes-like object
      #if item_type not in (str, bytes, tuple):  # bytearray|list|arrayview may change size during assignment if item._slice.stop is None
      #  raise TypeError(f'a fixed length primitive is required (str, bytes, tuple, ...), not {item_type.__name__!r}')
      if item_type is not bytes: item = bytes(item)  # make byte-iterables to work
      item_len = len(item)
      _os = self._os_module; fileno = self._fileno; lseek = _os.lseek; SEEK_SET = _os.SEEK_SET; SEEK_END = _os.SEEK_END; write = _os.write; ftruncate = _os.ftruncate
      if step == 1:
        if stop is None:
          if start is None: start = 0
          elif start < 0: start = max(0, lseek(fileno, 0, SEEK_END) + start)
          lseek(fileno, start, SEEK_SET)
          write(fileno, item)  # XXX check amount of data written?
          ftruncate(fileno, start + item_len)
        elif stop < 0:
          size = lseek(fileno, 0, SEEK_END)
          if start is None: start = 0
          elif start < 0: start = max(0, size + start)
          stop = max(0, size + stop)
          if stop - start != item_len: raise ValueError(f"attempt to assign bytes of size {item_len} to slice of size {stop - start}")
          lseek(fileno, start, SEEK_SET)
          write(fileno, item)  # XXX check amount of data written?
        else:
          if start is None: start = 0
          elif start < 0: start = max(0, lseek(fileno, 0, SEEK_END) + start)
          if stop - start != item_len: raise ValueError(f"attempt to assign bytes of size {item_len} to slice of size {stop - start}")
          lseek(fileno, start, SEEK_SET)
          write(fileno, item)  # XXX check amount of data written?
      else:
        start, stop, step = key.indices(lseek(fileno, 0, SEEK_END))
        key_range = range(start, stop, step)
        key_len = len(key_range)
        if step == -1:
          if key_len != item_len: raise ValueError(f"attempt to assign bytes of size {item_len} to slice of size {key_len}")
          lseek(fileno, stop + 1, SEEK_SET)
          write(fileno, item[::-1])  # XXX check amount of data written?
        else:
          if key_len != item_len: raise ValueError(f"attempt to assign bytes of size {item_len} to extended slice of size {key_len}")
          for i, b in zip(key_range, item):
            lseek(fileno, i, SEEK_SET)
            write(fileno, bytes((b,)))
    elif key_type is int:
      #if item_type not in (int, bool): raise TypeError(f"{item_type.__name__!r} object cannot be interpreted as an integer")
      item = bytes((item,))
      _os = self._os_module; fileno = self._fileno; lseek = _os.lseek; SEEK_SET = _os.SEEK_SET; SEEK_END = _os.SEEK_END; write = _os.write
      size = lseek(fileno, 0, SEEK_END)
      if key < -size or key >= size: raise IndexError('filebytearray index out of range')
      if key < 0: key = size + key
      lseek(fileno, key, SEEK_SET)
      write(fileno, item)  # XXX check amount of data written?
    else:
      raise TypeError(f'filebytearray indices must be integers or slices, not {key_type.__name__!r}')

  # XXX add missing bytearray methods
  # '__hash__', '__rmod__', '__rmul__',
  # 'istitle', 'rfind', 'rindex',

  def __add__(self, other): return self.copy() + other

  def __contains__(self, item, **k): return self.find(item, **k) != -1

  def __eq__(self, other):
    def iter_blocks(it, size):
      b = it[:size]
      i = size
      while b:
        yield b
        b = it[i:i + size]
        i += size
    if other is self: return True
    if type(other) is filebytearray:
      if len(self) != len(other): return False
    else:
      # ensure that other is a bytes-like object
      try: other = memoryview(other)
      except TypeError: return False
      if len(self) != other.nbytes: return False
    blksize = self._blksize
    for a, b in zip(iter_blocks(self, blksize), iter_blocks(other, blksize)):
      if a != b: return False
    return True

  @staticmethod
  def _gle(self, other, op, gt, lt, eq):
    def iter_blocks(it, size):
      b = it[:size]
      i = size
      while b:
        yield b
        b = it[i:i + size]
        i += size
      while 1: yield b
    if other is self: return eq
    if type(other) is not filebytearray:
      # ensure that other is a bytes-like object
      try: other = memoryview(other)
      except TypeError: raise TypeError(f"{op!r} not supported between instances of 'filebytearray' and {type(other).__name__!r}") from None
    blksize = self._blksize
    for a, b in zip(iter_blocks(self, blksize), iter_blocks(other, blksize)):
      if a > b: return gt
      if a < b: return lt
      if not a: break
    return eq

  def __ge__(self, other): return filebytearray._gle(self, other, '>=', True, False, True)
  def __gt__(self, other): return filebytearray._gle(self, other, '>', True, False, False)

  def __iadd__(self, other): self.extend(other); return self

  def __imul__(self, other):
    bytearray() * other  # checking types
    if other <= 0:
      self.clear()
      return
    _os = self._os_module; fileno = self._fileno; blksize = self._blksize; lseek = _os.lseek; SEEK_SET = _os.SEEK_SET; SEEK_END = _os.SEEK_END; read = _os.read; write = _os.write
    size = lseek(fileno, 0, SEEK_END)
    for i in range(1, other):
      start = 0
      while 1:
        l = min(blksize, size - start)
        if l <= 0: break
        lseek(fileno, start, SEEK_SET)
        d = read(fileno, l); ld = len(d)
        if ld <= 0: break
        lseek(fileno, 0, SEEK_END)
        write(fileno, d)
        start += ld
    return self

  def __iter__(self, *, buffer_size=1):
    _os = self._os_module; fileno = self._fileno; lseek = _os.lseek; SEEK_SET = _os.SEEK_SET; read = _os.read
    i = 0
    lseek(fileno, i, SEEK_SET)
    d = read(fileno, buffer_size)
    while d:
      i += len(d)
      yield from d
      lseek(fileno, i, SEEK_SET)
      d = read(fileno, buffer_size)

  def __le__(self, other): return filebytearray._gle(self, other, '<=', False, True, True)
  def __lt__(self, other): return filebytearray._gle(self, other, '<', False, True, False)

  def __mod__(self, other): return self.copy() % other
  def __mul__(self, other): return self.copy() * other

  def append(self, item):
    item = bytes((item,))
    _os = self._os_module; fileno = self._fileno; lseek = _os.lseek; SEEK_END = _os.SEEK_END; write = _os.write
    lseek(fileno, 0, SEEK_END)
    write(fileno, item)

  def clear(self): self._os_module.ftruncate(self._fileno, 0)

  def copy(self): return self[:]

  def count(self, sub, start=0, end=None, *, buffer_size=None):
    c = 0
    sub = bytes(sub)
    l = len(sub)
    start = self.find(sub, start, end, buffer_size=buffer_size)
    while start != -1:
      c += 1
      start = self.find(sub, start + l, end, buffer_size=buffer_size)
    return c

  def endswith(self, suffix, start=0, end=None):
    def readatleast(fd, n):
      data = d = read(fd, n)
      if not d: return data
      ld = len(d)
      while ld < n:
        d = read(fd, n - ld)
        if not d: return data
        data += d
        ld += len(d)
      return data
    if type(suffix) is tuple: suffix = (*(memoryview(_) for _ in suffix),)
    else: suffix = (memoryview(suffix),)
    _os = self._os_module; fileno = self._fileno; blksize = self._blksize; lseek = _os.lseek; SEEK_SET = _os.SEEK_SET; SEEK_END = _os.SEEK_END; read = _os.read
    size = lseek(fileno, 0, SEEK_END)
    if start is None: start = 0
    elif start < 0: start = max(0, size + start)
    elif start > size: start = size
    if end is None: end = size
    elif end < 0: end = max(0, size + end)
    elif end > size: end = size
    l = max(0, end - start)
    suffix = (*(_ for _ in suffix if _.nbytes <= l),)
    if not suffix: return False
    l = max(_.nbytes for _ in suffix)
    lseek(fileno, end - l, SEEK_SET)
    d = readatleast(fileno, l)
    return d.endswith(suffix)  # using native method

  def extend(self, item):
    item = bytes(item)  # make byte-iterables to work
    _os = self._os_module; fileno = self._fileno; lseek = _os.lseek; SEEK_END = _os.SEEK_END; write = _os.write
    lseek(fileno, 0, SEEK_END)
    write(fileno, item)  # XXX check amount of data written?

  def find(self, sub, start=0, end=None, *, buffer_size=None):
    if buffer_size is None: buffer_size = self._blksize
    return os_find_in_file(self._fileno, sub, start, end, buffer_size=buffer_size, os_module=self._os_module)

  def hex(self):
    return ''.join(f'{_:02x}' for _ in self.__iter__(buffer_size=self._blksize))

  def index(self, sub, *a, **k):
    i = self.find(sub, *a, **k)
    if i == -1: raise ValueError(f"{sub!r} is not in fileview")
    return i

  def insert(self, index, byte):
    d = bytes((byte,))
    _os = self._os_module; fileno = self._fileno; lseek = _os.lseek; SEEK_END = _os.SEEK_END; write = _os.write
    size = lseek(fileno, 0, SEEK_END)
    if index > size: index = size
    elif index < 0:
      if index < -size: index = 0
      else: index = size + index
    if index < size: raise ValueError("cannot insert this element without rewriting the file")
    write(fileno, d)

  def isalnum(self):
    it = self.__iter__(buffer_size=self._blksize)
    found = False
    for b in it:
      if 0x30 <= b <= 0x39 or 0x41 <= b <= 0x5a or 0x61 <= b <= 0x7a: found = True; break
      else: return False
    for b in it:
      if not (0x30 <= b <= 0x39 or 0x41 <= b <= 0x5a or 0x61 <= b <= 0x7a): return False
    return found
  def isalpha(self):
    it = self.__iter__(buffer_size=self._blksize)
    found = False
    for b in it:
      if 0x41 <= b <= 0x5a or 0x61 <= b <= 0x7a: found = True; break
      else: return False
    for b in it:
      if not (0x41 <= b <= 0x5a or 0x61 <= b <= 0x7a): return False
    return found
  def isascii(self):
    it = self.__iter__(buffer_size=self._blksize)
    for b in it:
      if b > 0x7f: return False
    return True
  def isdigit(self):
    it = self.__iter__(buffer_size=self._blksize)
    found = False
    for b in it:
      if 0x30 <= b <= 0x39: found = True; break
      else: return False
    for b in it:
      if not (0x30 <= b <= 0x39): return False
    return found
  def islower(self):
    it = self.__iter__(buffer_size=self._blksize)
    found = False
    for b in it:
      if 0x61 <= b <= 0x7a: found = True; break
      elif 0x41 <= b <= 0x5a: return False
    for b in it:
      if 0x41 <= b <= 0x5a: return False
    return found
  def isspace(self):
    it = self.__iter__(buffer_size=self._blksize)
    found = False
    for b in it:
      if 0x9 <= b <= 0xd or b == 0x20: found = True; break
      else: return False
    for b in it:
      if not (0x9 <= b <= 0xd or b == 0x20): return False
    return found
  #XXX def istitle(self):
  def isupper(self):
    it = self.__iter__(buffer_size=self._blksize)
    found = False
    for b in it:
      if 0x41 <= b <= 0x5a: found = True; break
      elif 0x61 <= b <= 0x7a: return False
    for b in it:
      if 0x61 <= b <= 0x7a: return False
    return found

  def pop(self, *index):
    if index:
      try: index, = index
      except ValueError: raise TypeError(f"pop expected at most 1 argument, got {len(index)}") from None
      _os = self._os_module; fileno = self._fileno; lseek = _os.lseek; SEEK_SET = _os.SEEK_SET; SEEK_END = _os.SEEK_END; read = _os.read; ftruncate = _os.ftruncate
      size = lseek(fileno, 0, SEEK_END)
      if index >= size or index < -size: raise IndexError('pop index out of range')
      if index < 0: index = size + index
      if index < size - 1: raise ValueError("cannot pop this element without rewriting the file")
      if size <= 0: raise IndexError('pop from an empty filebytearray')
    else:
      _os = self._os_module; fileno = self._fileno; lseek = _os.lseek; SEEK_SET = _os.SEEK_SET; SEEK_END = _os.SEEK_END; read = _os.read; ftruncate = _os.ftruncate
      size = lseek(fileno, 0, SEEK_END)
      if size <= 0: raise IndexError('pop from an empty filebytearray')
    lseek(fileno, size - 1, SEEK_SET)
    b = read(fileno, 1)[0]  # also checks for data validity
    ftruncate(fileno, size - 1)
    return b

  #XXX def rfind(self, sub, start=0, end=None): do os_rfind_in_file.py
  #XXX def rindex(self, sub, start=0, end=None): use rfind once implemented

  def remove(self, item):
    raise ValueError("feature disabled, rewriting the whole file is forbidden")  # XXX implement it anyway?

  def reverse(self):
    def readatleast(fd, n):
      data = d = read(fd, n)
      if not d: return data
      ld = len(d)
      while ld < n:
        d = read(fd, n - ld)
        if not d: return data
        data += d
        ld += len(d)
      return data
    _os = self._os_module; fileno = self._fileno; blksize = self._blksize; lseek = _os.lseek; SEEK_SET = _os.SEEK_SET; SEEK_END = _os.SEEK_END; read = _os.read; write = _os.write
    size = lseek(fileno, 0, SEEK_END)
    start = 0; stop = size // 2
    while start < stop:
      l = min(blksize, stop - start)
      lseek(fileno, start, SEEK_SET); bd = readatleast(fileno, l)
      if l != len(bd): raise ValueError('file size changed during reverse()')
      lseek(fileno, size - start - l, SEEK_SET); ed = readatleast(fileno, l)
      if l != len(ed): raise ValueError('file size changed during reverse()')
      lseek(fileno, size - start - l, SEEK_SET); write(fileno, bd[::-1])  # XXX check amount of data written?
      lseek(fileno, start, SEEK_SET); write(fileno, ed[::-1])  # XXX check amount of data written?
      start += l

  def startswith(self, prefix, start=0, end=None):
    def readatleast(fd, n):
      data = d = read(fd, n)
      if not d: return data
      ld = len(d)
      while ld < n:
        d = read(fd, n - ld)
        if not d: return data
        data += d
        ld += len(d)
      return data
    if type(prefix) is tuple: prefix = (*(memoryview(_) for _ in prefix),)
    else: prefix = (memoryview(prefix),)
    _os = self._os_module; fileno = self._fileno; blksize = self._blksize; lseek = _os.lseek; SEEK_SET = _os.SEEK_SET; SEEK_END = _os.SEEK_END; read = _os.read
    size = None
    if start is None: start = 0
    elif start < 0:
      if size is None: size = lseek(fileno, 0, SEEK_END)
      start = max(0, size + start)
    if end is None: pass
    elif end < 0:
      if size is None: size = lseek(fileno, 0, SEEK_END)
      end = max(0, size + end)
    if end is not None:
      l = max(0, end - start)
      prefix = (*(_ for _ in prefix if _.nbytes <= l),)
      if not prefix: return False
    l = max(_.nbytes for _ in prefix)
    lseek(fileno, start, SEEK_SET)
    d = readatleast(fileno, l)
    return d.startswith(prefix)  # using native method

  @staticmethod
  def maketrans(*a, **k):
    return bytearray.maketrans(*a, **k)  # XXX not reimplemented (lol)
  def capitalize(self, *a, **k):  # acts on a copy
    return self.copy().capitalize(*a, **k)  # could be optimized... but *sigh*...
  def center(self, *a, **k):  # acts on a copy
    return self.copy().center(*a, **k)  # could be optimized... but *sigh*...
  def decode(self, *a, **k):  # acts on a copy
    return self.copy().decode(*a, **k)  # could be optimized... but *sigh*...
  def expandtabs(self, *a, **k):  # acts on a copy
    return self.copy().expandtabs(*a, **k)  # could be optimized... but *sigh*...
  def join(self, *a, **k):  # acts on a copy
    return self.copy().join(*a, **k)  # could be optimized... but *sigh*...
  def ljust(self, *a, **k):  # acts on a copy
    return self.copy().ljust(*a, **k)  # could be optimized... but *sigh*...
  def lower(self, *a, **k):  # acts on a copy
    return self.copy().lower(*a, **k)  # could be optimized... but *sigh*...
  def lstrip(self, *a, **k):  # acts on a copy
    return self.copy().lstrip(*a, **k)  # could be optimized... but *sigh*...
  def partition(self, *a, **k):  # acts on a copy
    return self.copy().partition(*a, **k)  # could be optimized... but *sigh*...
  def removeprefix(self, *a, **k):  # acts on a copy
    return self.copy().removeprefix(*a, **k)  # could be optimized... but *sigh*...
  def removesuffix(self, *a, **k):  # acts on a copy
    return self.copy().removesuffix(*a, **k)  # could be optimized... but *sigh*...
  def replace(self, *a, **k):  # acts on a copy
    return self.copy().replace(*a, **k)  # could be optimized... but *sigh*...
  def rjust(self, *a, **k):  # acts on a copy
    return self.copy().rjust(*a, **k)  # could be optimized... but *sigh*...
  def rpartition(self, *a, **k):  # acts on a copy
    return self.copy().rpartition(*a, **k)  # could be optimized... but *sigh*...
  def rsplit(self, *a, **k):  # acts on a copy
    return self.copy().rsplit(*a, **k)  # could be optimized... but *sigh*...
  def rstrip(self, *a, **k):  # acts on a copy
    return self.copy().rstrip(*a, **k)  # could be optimized... but *sigh*...
  def split(self, *a, **k):  # acts on a copy
    return self.copy().split(*a, **k)  # could be optimized... but *sigh*...
  def splitlines(self, *a, **k):  # acts on a copy
    return self.copy().splitlines(*a, **k)  # could be optimized... but *sigh*...
  def strip(self, *a, **k):  # acts on a copy
    return self.copy().strip(*a, **k)  # could be optimized... but *sigh*...
  def swapcase(self, *a, **k):  # acts on a copy
    return self.copy().swapcase(*a, **k)  # could be optimized... but *sigh*...
  def title(self, *a, **k):  # acts on a copy
    return self.copy().title(*a, **k)  # could be optimized... but *sigh*...
  def translate(self, *a, **k):  # acts on a copy
    return self.copy().translate(*a, **k)  # could be optimized... but *sigh*...
  def upper(self, *a, **k):  # acts on a copy
    return self.copy().upper(*a, **k)  # could be optimized... but *sigh*...
  def zfill(self, *a, **k):  # acts on a copy
    return self.copy().zfill(*a, **k)  # could be optimized... but *sigh*...

filebytearray._required_globals = ['os', 'io_parsemode', 'os_find_in_file']
