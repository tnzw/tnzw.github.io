# ArrayOnFile.py Version 1.1.1
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class ArrayOnFile(tuple):
  # (slice, fileno, os_module)
  # extending tuple is just a way to make ArrayOnFile an immutable object
  __slots__ = ()
  # usage:
  #   with ArrayOnFile.open("path") as fa:
  #     # ...

  # inspired by bytearray (without the operations that change its length)

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

  # >>> dir(())
  # ['__add__', '__class__', '__class_getitem__', '__contains__', '__delattr__',
  #  '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
  #  '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init__',
  #  '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__',
  #  '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmul__',
  #  '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'count',
  #  'index']

  @staticmethod
  def open(path, mode="rw", os_module=None):
    # mode could be "ro", "wo" or "rw" + some of `open(..., mode)` syntax
    def _or(iterable):
      r = 0
      for _ in iterable: r |= _
      return r
    if os_module is None: os_module = os
    mode = "".join(sorted(mode))
    # force opening with o_binary to avoid side effects.
    if   mode in ("rw",):           flags = ("O_RDWR", "O_BINARY") #, "O_CREAT")  # we want an existing file as an array, so don't o_creat.
    elif mode in ("r", "or", "br"): flags = ("O_RDONLY", "O_BINARY")
    #elif mode in ("w", "ow", "bw"): flags = ("O_WRONLY", "O_BINARY") #, "O_CREAT", "O_TRUNC")  # we want an existing file as an array, so don't o_creat or o_trunc.
    elif mode in ("+r", "+br"):     flags = ("O_RDWR", "O_BINARY")
    #elif mode in ("+w", "+bw"):     flags = ("O_RDWR", "O_BINARY") #, "O_CREAT", "O_TRUNC")  # same
    else: raise ValueError(f"unhandled mode {mode!r}")
    return ArrayOnFile(os_module.open(path, _or(getattr(os_module, _, 0) for _ in flags)), os_module=os_module)

  @staticmethod
  def range_slice(range):
    start, stop, step = range.start, range.stop, range.step
    return slice(start, None if stop < 0 else stop, step)

  @property
  def _slice(self): return tuple.__getitem__(self, 0)
  def fileno(self): return tuple.__getitem__(self, 1)
  @property
  def    _os(self): return tuple.__getitem__(self, 2)
  #@property
  #def   opts(self): return tuple.__getitem__(self, 3)

  def getindices(self): return self._slice.indices(self._os.lseek(self.fileno(), 0, self._os.SEEK_END))
  def getrange(self): return range(*self.getindices())

  def __new__(cls, fileno, slice_key=None, *, relative_slice=False, os_module=None):
    if os_module is None: os_module = os
    if slice_key is None: return tuple.__new__(cls, (slice(0, None, 1), fileno, os_module))
    if relative_slice: return tuple.__new__(cls, (slice(slice_key.start, slice_key.stop, slice_key.step), fileno, os_module))
    #if slice_key is None: slice_key = slice(0, None, 1)
    size = os_module.lseek(fileno, 0, os_module.SEEK_END)
    start, stop, step = slice_key.indices(size)
    return tuple.__new__(cls, (slice(start, None if stop < 0 else stop, step), fileno, os_module))

  def is_slice(self):
    s = self._slice
    if s.start == 0 and s.stop is None and s.step == 1: return False
    return True

  #def __del__(self): close? NO! 'cause __getitem__ creates new instances so previous ones are deleted!
  #                   it would work if `fileno` could have a __del__.
  def __enter__(self): return self
  def __exit__(self, *a): self._os.close(self.fileno())

  def __len__(self): return len(self.getrange())

  def iter(self, buffer_size=4096): return self.__iter__(buffer_size=buffer_size)
  def __iter__(self, buffer_size=4096):  # XXX buffer_size is a bit hardcoded
    # without O_BINARY flag on windows, you may have different amount of data than "size" told you...
    start, stop, step = self.getindices()
    length = len(range(start, stop, step))
    if length <= 0: return
    os, fd = self._os, self.fileno()
    SEEK_SET, SEEK_CUR = os.SEEK_SET, os.SEEK_CUR
    if step < 0:
      start += 1
      stride, chunk, extra_step = 1, b"", 0
      if step < 1: length = (length - 1) * -step + 1
      while stride:
        if step < 1:
          for c in chunk[::-1]:
            if extra_step == 0:
              yield c  # ouch, big inconsistency here without O_BINARY flag!
              extra_step = -step - 1
            else:
              extra_step -= 1
        else:
          for c in chunk[::-1]:
            yield c
        stride, desired_stride = 0, min(buffer_size, length)
        while stride != desired_stride:
          s = os.lseek(fd, start - desired_stride + stride, SEEK_SET)
          chunk += os.read(fd, desired_stride - stride)
          stride += os.lseek(fd, 0, SEEK_CUR) - s  # `stride += len(chunk)` isn't correct on windows without O_BINARY flag.
        length -= stride
        start -= stride
    else:
      stride, chunk, extra_step = 1, b"", 0
      if step > 1: length = (length - 1) * step + 1
      while stride:
        if step > 1:
          for c in chunk:
            if extra_step == 0:
              yield c  # ouch, big inconsistency here without O_BINARY flag!
              extra_step = step - 1
            else:
              extra_step -= 1
        else:
          for c in chunk:
            yield c
        s = os.lseek(fd, start, SEEK_SET)
        chunk = os.read(fd, min(buffer_size, length))
        stride = os.lseek(fd, 0, SEEK_CUR) - s  # `stride += len(chunk)` isn't correct on windows without O_BINARY flag.
        length -= stride
        start += stride

  def __contains__(self, item):
    for _ in self:
      if _ == item: return True
    return False

  def __eq__(self, other): return sequence_eq(self, other)
  def __ne__(self, other): return sequence_ne(self, other)
  def __gt__(self, other): return sequence_gt(self, other)
  def __ge__(self, other): return sequence_ge(self, other)
  def __lt__(self, other): return sequence_lt(self, other)
  def __le__(self, other): return sequence_le(self, other)
  def count(self, x): return sequence_count(self, x)
  def index(self, *a, **k): return sequence_index(self, *a, **k)

  def __array__(self): return bytes(self)

  def __repr__(self): return f"{self.__class__.__name__}({self.fileno()!r}, {self._slice!r})"  # XXX _slice could be relative
  #def __repr__(self): return self.__class__.__name__ + " [" + ",".join(repr(_) for _ in self) + "]"

  def __str__(self):
    M, S = 60, "..."
    SL = len(S)
    s = repr(bytes(self[:M + 1]))
    if len(s) > M: s = s[:M - SL] + S
    return self.__class__.__name__ + " " + s

  def __getitem__(self, key):
    if isinstance(key, slice):
      key = ArrayOnFile.range_slice(self.getrange()[key])
      return self.__class__(self.fileno(), key)
    key = self.getrange()[key]
    os, fd = self._os, self.fileno()
    os.lseek(fd, key, os.SEEK_SET)
    return os.read(fd, 1)[0]

  def __iadd__(self, other):
    if self.is_slice(): raise ValueError("cannot append on a slice")
    if not isinstance(other, (bytes, bytearray)): other = bytes(other)
    itemlen = len(other)
    os, fd = self._os, self.fileno()
    os.lseek(fd, 0, os.SEEK_END)
    written = 0
    while written < itemlen:
      w = os.write(fd, other[written:])
      if w == 0: break
      written += w
    return self

  def __imul__(self, other):
    if self.is_slice(): raise ValueError("cannot append on a slice")
    if not isinstance(other, int): raise TypeError("can't multiply sequence by non-int")
    os, fd = self._os, self.fileno()
    if other < 1:
      os.ftruncate(fd, 0)
      return self
    SEEK_END = os.SEEK_END
    l = os.lseek(fd, 0, SEEK_END)
    copy_file_range = getattr(os, "copy_file_range", os_copy_file_range)
    try: copy_file_range(fd, fd, 0, 0, 0)  # testing the method
    except OSError as e:
      if e.errno != errno.ENOSYS: raise  # hm… I wish I had no try…except.
      copy_file_range = os_copy_file_range
    for i in range(1, other, 1):
      copy_file_range(fd, fd, l, 0, l * i)
    return self

  def __setitem__(self, key, item):
    os, fd = self._os, self.fileno()
    if isinstance(key, slice):
      key = ArrayOnFile.range_slice(self.getrange()[key])
      if not isinstance(item, (bytes, bytearray)): item = bytes(item)
      itemlen = len(item)
      #start, stop, step = key.indices(os.lseek(fd, 0, os.SEEK_END))
      start, stop, step = key.start, key.stop, key.step
      if stop is None: stop = -1
      deslen = len(range(start, stop, step))
      resize = 0
      if step == 1 and not self.is_slice() and stop == len(self):
        # allow to write more or less (with truncate if necessary)
        resize = itemlen - deslen
      else:
        if itemlen < deslen: raise ValueError(f"not enough values to unpack (expected {deslen})")
        if itemlen > deslen: raise ValueError(f"too many values to unpack (expected {deslen})")
      if step == 1:
        os.lseek(fd, start, os.SEEK_SET)
        written = 0
        while written < itemlen:
          w = os.write(fd, item[written:])
          if w == 0: break
          written += w
      elif step == -1:
        item = item[::-1]
        os.lseek(fd, stop + 1, os.SEEK_SET)
        written = 0
        while written < itemlen:
          w = os.write(fd, item[written:])
          if w == 0: break
          written += w
      else:
        for i, v in zip(range(start, stop, step), item):
          os.lseek(fd, i, os.SEEK_SET)
          os.write(fd, bytes((v,))[:1])
      if resize < 0: os.truncate(fd, os.lseek(fd, 0, os.SEEK_CUR))
      return
    key = self.getrange()[key]
    os.lseek(fd, key, os.SEEK_SET)
    os.write(fd, bytes((item,))[:1])

ArrayOnFile._required_globals = [
  "errno",
  "os_copy_file_range",
  "sequence_count",
  "sequence_eq",
  "sequence_ge",
  "sequence_gt",
  "sequence_index",
  "sequence_le",
  "sequence_lt",
  "sequence_ne",
]
