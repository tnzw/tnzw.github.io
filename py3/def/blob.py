# blob.py Version 1.4.0
# Copyright (c) 2021-2022 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def blob():

  # Why blob and arrayview ?
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

  class blob(tuple):
    # extending tuple is just a way to make blob an immutable object
    __slots__ = ()

    @property
    def _chunks(self): return tuple.__getitem__(self, 0)
    @property
    def type(self): return tuple.__getitem__(self, 1)
    @property
    def readonly(self): return tuple.__getitem__(self, 2)

    def __new__(cls, chunks, *, type="", readonly=None):
      if not isinstance(type, str): raise TypeError("type is not of type str")
      chunks = (*(
        c
        for chunk in chunks
        for c in (chunk._chunks if isinstance(chunk, blob) else (arrayview(chunk),))
      ),)
      if readonly is None:
        for av in chunks:
          if av.readonly:
            readonly = True
            break
      return tuple.__new__(cls, (chunks, type, bool(readonly)))

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

    def slice(self, start, stop=None, step=None, *, type="", readonly=None):
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
      new_blob = blob(new_chunks, type=type, readonly=self.readonly if readonly is None else readonly)
      if step != 1:  # this is very unoptimized, 'blob' is not made for step != 1...
        if not new_blob: return new_blob
        if step < 0: r = range(len(new_blob) - 1, -1, step)
        else: r = range(0, len(new_blob), step)
        new_blob = blob(tuple(new_blob[i:i+1] for i in r), type=type, readonly=self.readonly if readonly is None else readonly)
      return new_blob

    def __getitem__(self, key):
      if isinstance(key, slice):
        return self.slice(key.start, key.stop, key.step)  # cannot predict 'type' for a slice
      for c in self.slice(key, key + 1, 1): return c
      raise IndexError("index out of range")

    def __setitem__(self, key, value):
      if self.readonly: raise TypeError('cannot modify read-only blob')
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
    def copy(self): return blob((list(self),), type=self.type)

    def __add__(self, other): return blob((self, other))
    def __eq__(self, other): return sequence_eq(self, other)
    def __ge__(self, other): return sequence_ge(self, other)
    def __gt__(self, other): return sequence_gt(self, other)
    def __le__(self, other): return sequence_le(self, other)
    def __lt__(self, other): return sequence_lt(self, other)
    def __mul__(self, other): return blob((self,) * other)
    def __ne__(self, other): return sequence_ne(self, other)
    def __rmul__(self, other): return self.__mul__(other)
    def count(self, x): return sequence_count(self, x)
    def index(self, *a, **k): return sequence_index(self, *a, **k)

  return blob

blob = blob()
blob._require_globals = ['arrayview', 'sequence_eq', 'sequence_ne', 'sequence_ge', 'sequence_gt', 'sequence_le', 'sequence_lt', 'sequence_count', 'sequence_index']
