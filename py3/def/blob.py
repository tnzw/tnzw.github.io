# blob.py Version 1.2.2
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def blob():

  # Why blob and blob.arrayview ?
  # because we cannot extend a bytearray with a "reference" to another one,
  # ie. a.extend(b) extends 'a' by "copying" 'b' instead of "sharing" 'b' data
  # with/in 'a' extension.
  #   blob((bytearray(b"lol"), another_blob), type="text/plain")

  # inspired by list (without the operations that change its length)

  # >>> dir([])
  # ['__add__', '__class__', '__class_getitem__', '__contains__', '__delattr__',
  #  '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
  #  '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__',
  #  '__imul__', '__init__', '__init_subclass__', '__iter__', '__le__',
  #  '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__',
  #  '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__',
  #  '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'append',
  #  'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove',
  #  'reverse', 'sort']

  # >>> dir(())
  # ['__add__', '__class__', '__class_getitem__', '__contains__', '__delattr__',
  #  '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
  #  '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init__',
  #  '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__',
  #  '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmul__',
  #  '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'count',
  #  'index']

  def sequence__eq__(self, other):  # generic sequence_eq
    if hasattr(other, "__len__"): # and hasattr(self, "__len__")
      if len(self) != len(other): return False
    r = iter(other)
    l = iter(self)
    for lv in l:
      try:
        rv = next(r)
        if lv != rv: return False
      except StopIteration: return False
    for _ in r: return False
    return True
  def sequence__ge__(self, other):  # generic sequence_ge
    r = iter(other)
    l = iter(self)
    for lv in l:
      try:
        rv = next(r)
        if lv > rv: return True
        if lv < rv: return False
      except StopIteration: return True
    for _ in r: return False
    return True
  def sequence__gt__(self, other):  # generic sequence_gt
    r = iter(other)
    l = iter(self)
    for lv in l:
      try:
        rv = next(r)
        if lv > rv: return True
        if lv < rv: return False
      except StopIteration: return True
    return False
  def sequence__le__(self, other):  # generic sequence_le
    r = iter(other)
    l = iter(self)
    for lv in l:
      try:
        rv = next(r)
        if lv < rv: return True
        if lv > rv: return False
      except StopIteration: return False
    for _ in r: return True
    return True
  def sequence__lt__(self, other):  # generic sequence_lt
    r = iter(other)
    l = iter(self)
    for lv in l:
      try:
        rv = next(r)
        if lv < rv: return True
        if lv > rv: return False
      except StopIteration: return False
    for _ in r: return True
    return False
  def sequence__ne__(self, other): return not sequence__eq__(self, other)
  def sequence_count(self, x): return sum(x == _ for _ in self)  # generic sequence_count
  def sequence_index(self, x, i=0, *j):  # generic sequence_index
    def count(f):
      while True:
        yield f
        f += 1
    if j:
      j, = j
      r = range(i, j)
    else:
      r = count(i)
    it = iter(self)
    for _ in zip(range(i), it): pass
    for f, _ in zip(r, it):
      if x == _: return f
    c = self.__class__.__name__
    raise ValueError(f"{x!r} is not in {c}")

  class arrayview(tuple):
    # extending tuple is just a way to make arrayview an immutable object
    __slots__ = ()

    @staticmethod
    def range_slice(range):
      start, stop, step = range.start, range.stop, range.step
      return slice(start, None if stop < 0 else stop, step)

    @property
    def buffer(self): return tuple.__getitem__(self, 0)
    @property
    def range(self): return tuple.__getitem__(self, 1)

    def __new__(cls, array, slice_key=None):
      if slice_key is None: slice_key = slice(0, None, 1)
      return tuple.__new__(cls, (array, range(*slice_key.indices(len(array)))))

    def __len__(self): return len(self.range)

    def __iter__(self):
      for _ in self.buffer[self.range_slice(self.range)]: yield _

    def __contains__(self, item):
      for _ in self:
        if _ == item: return True
      return False

    def __array__(self): return self.buffer[self.range_slice(self.range)]

    def __repr__(self): return self.__class__.__name__ + "(" + repr(self.buffer) + ", " + repr(self.range_slice(self.range)) + ")"
    #def __repr__(self): return self.__class__.__name__ + " [" + ",".join(repr(_) for _ in self) + "]"

    def __str__(self):
      M, S, J = 60, "...", ", "
      SL, JL = len(S), len(J)
      l, s = -JL, []
      for _ in self:
        r = repr(_)
        l += len(r) + JL
        s.append(r)
        if l > M:
          s = J.join(s)[:M - SL] + S
          break
      else:
        s = J.join(s)
      return self.__class__.__name__ + " [ " + s + " ]"

    def __getitem__(self, key):
      if isinstance(key, slice):
        return self.__class__(self.buffer, self.range_slice(self.range[key]))
      return self.buffer[self.range[key]]

    def __setitem__(self, key, item):
      # no need to protect this method from unpack errors when arrayview is only used by blob
      if isinstance(key, slice):
        key_range = self.range[key]
        key = self.range_slice(key_range)
        klen = len(key_range)
        #klen = len(range(*key.indices(len(self.buffer))))
        if not hasattr(item, "__len__"):
          item = list(v for i, v in zip(range(klen + 1), item))
        ilen = len(item)
        if klen != ilen: raise ValueError(f"{self.__class__.__name__} assignment: lvalue and rvalue have different structures")
        self.buffer[key] = item
      else:
        # only this line is necessary when arrayview is only used by blob
        self.buffer[self.range[key]] = item

    def __add__(self, other): raise NotImplementedError
    def __eq__(self, other): return sequence__eq__(self, other)
    def __ge__(self, other): return sequence__ge__(self, other)
    def __gt__(self, other): return sequence__gt__(self, other)
    def __le__(self, other): return sequence__le__(self, other)
    def __lt__(self, other): return sequence__lt__(self, other)
    def __mul__(self, other): raise NotImplementedError
    def __ne__(self, other): return sequence__ne__(self, other)
    def __rmul__(self, other): return self.__mul__(other)
    def count(self, x): return sequence_count(self, x)
    def index(self, *a, **k): return sequence_index(self, *a, **k)

  class blob(tuple):
    # extending tuple is just a way to make arrayview an immutable object
    __slots__ = ()

    @property
    def _chunks(self): return tuple.__getitem__(self, 0)
    @property
    def type(self): return tuple.__getitem__(self, 1)

    def __new__(cls, chunks, *, type=""):
      if not isinstance(type, str): raise TypeError("type is not of type str")
      chunks = tuple(
        c
        for chunk in chunks
        for c in (chunk._chunks if isinstance(chunk, blob) else ((chunk if isinstance(chunk, arrayview) else arrayview(chunk)),))
      )
      return tuple.__new__(cls, (chunks, type))

    def __len__(self): return sum(len(c) for c in self._chunks)

    # "blob.size" is more suitable for "memory size" like __sizeof__. Please use len() instead
    #@property
    #def size(self): return len(self)

    def __iter__(self):
      for chunk in self._chunks:
        for c in chunk:
          yield c

    def __iter_setitem__(self):
      for chunk in self._chunks:
        for i, c in enumerate(chunk):
          yield c, i, chunk

    def __bool__(self):
      for _ in self: return True
      return False

    def __repr__(self):
      type = self.type
      return (
        self.__class__.__name__ +
        "([" + ", ".join(repr(_) for _ in self._chunks) + "]" +
        (", type=" + repr(type) if type else "") +
        ")")

    def __str__(self):
      return self.__class__.__name__ + " { len = " + repr(len(self)) + ", type = " + repr(self.type) + " }"
    #def __str__(self):
    #  M, S, J = 60, "...", ", "
    #  SL, JL = len(S), len(J)
    #  l, s = -JL, []
    #  for _ in self:
    #    r = repr(_)
    #    l += len(r) + JL
    #    s.append(r)
    #    if l > M:
    #      s = J.join(s)[:M - SL] + S
    #      break
    #  else:
    #    s = J.join(s)
    #  return self.__class__.__name__ + " [ " + s + " ]"

    def slice(self, start, stop=None, step=None, *, type=""):
      start, stop, step = slice(start, stop, step).indices(len(self))
      chunks = self._chunks
      new_chunks = []
      length = 0
      # seek for first eligible view, append view part, if last return
      vvi = 0
      for v in chunks:
        vl = len(v)
        if length + vl > start:
          delta = start - length
          if length + vl >= stop:
            new_chunks.append(v[delta:stop - length])
            chunks = ()  # exit all loops
            break
          new_chunks.append(v[delta:])
          length += vl
          vvi += 1
          break
        length += vl
        vvi += 1
      # append full views and last view part
      for v in chunks[vvi:]:
        vl = len(v)
        if length + vl >= stop:
          new_chunks.append(v[:stop-length])
          break
        new_chunks.append(v)
        length += vl
      new_blob = self.__class__(new_chunks, type=type)
      if step != 1:  # this is very unoptimized, 'blob' is not made for step != 1...
        if not new_blob: return new_blob
        if step < 0: r = range(len(new_blob) - 1, -1, step)
        else: r = range(0, len(new_blob), step)
        new_blob = self.__class__(tuple(new_blob[i:i+1] for i in r), type=type)
      return new_blob

    def __getitem__(self, key):
      if isinstance(key, slice):
        return self.slice(key.start, key.stop, key.step)  # cannot predict 'type' for a slice
      for c in self.slice(key, key + 1, 1): return c
      raise IndexError("index out of range")

    def __setitem__(self, key, value):
      if not isinstance(key, slice):
        key = slice(key, key + 1, 1)
        value = (value,)
      klen = len(range(*key.indices(len(self))))
      if not hasattr(value, "__len__") or not hasattr(value, "__getitem__"):
        value = list(v for i, v in zip(range(klen + 1), value))
      vlen = len(value)
      if klen != vlen: raise ValueError(f"{self.__class__.__name__} assignment: lvalue and rvalue have different structures")
      self = self[key]
      l = 0
      for chunk in self._chunks:
        clen = len(chunk)
        #if klen - l < clen:  # should never happen
        #  chunk[:klen - l] = value[l:klen]
        #  break
        chunk[:] = value[l:l+clen]
        l += clen

    # is "detach" a good name ? is "flatten" better (as in v8 cons-string / flat-string, but losing "detach" idea) ? "copy" is pretty good.
    def copy(self): return self.__class__((list(self),), type=self.type)

    def __add__(self, other): return self.__class__((self, other))
    def __eq__(self, other): return sequence__eq__(self, other)
    def __ge__(self, other): return sequence__ge__(self, other)
    def __gt__(self, other): return sequence__gt__(self, other)
    def __le__(self, other): return sequence__le__(self, other)
    def __lt__(self, other): return sequence__lt__(self, other)
    def __mul__(self, other): return self.__class__((self,) * other)
    def __ne__(self, other): return sequence__ne__(self, other)
    def __rmul__(self, other): return self.__mul__(other)
    def count(self, x): return sequence_count(self, x)
    def index(self, *a, **k): return sequence_index(self, *a, **k)

  blob.arrayview = arrayview

  class readonly_blob(blob):
    # same as blob without write operations
    def __setitem__(self):
      raise ValueError("blob is read only")

  blob.readonly = readonly_blob

  return blob

blob = blob()
