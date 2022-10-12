# arrayview.py Version 1.1.0
# Copyright (c) 2021-2022 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class arrayview(tuple):
  '''\
A memoryview-like that allows different types than bytes.
May or may not have fixed size.

    arrayview([a,b,c,d,e,f,g], slice(3, 6)) => [a,b,c,<d,e,f>,g] => <d,e,f>
'''
  # extending tuple is just a way to make arrayview an immutable object
  __slots__ = ()
  @property
  def obj(self): return tuple.__getitem__(self, 0)
  @property
  def _slice(self): return tuple.__getitem__(self, 1)
  @property
  def readonly(self): return tuple.__getitem__(self, 2)
  @property
  def _range(self): return range(*self._slice.indices(len(self.obj)))
  @property
  def shape(self): return (len(self._range),)
  @property
  def strides(self): return (self._range.step,)
  def __new__(cls, array, slice_key=None, *, readonly=None):
    if slice_key is None: slice_key = slice(0, None, 1)
    elif type(slice_key) != slice: raise TypeError('invalid slice key')
    t = type(array)
    if readonly is None:
      if t in (memoryview, arrayview): readonly = array.readonly
      elif t in (str, bytes, tuple): readonly = True
    if t == arrayview:  # avoid arrayview to contain another arrayview
      r = array._range[slice_key]
      return tuple.__new__(cls, (array.obj, slice(r.start, None if r.stop < 0 else r.stop, r.step), bool(readonly)))
    return tuple.__new__(cls, (array, slice_key, bool(readonly)))
  def __len__(self): return len(self._range)
  def __iter__(self):
    for _ in self.obj[self._slice]: yield _
  def __contains__(self, item):
    for _ in self:
      if _ == item: return True
    return False
  def __repr__(self): return f'{self.__class__.__name__}({self.obj!r}, {self._slice!r})'
  def __str__(self): return f'<{self.__class__.__name__} {self.obj[self._slice]!r}>'
  def __getitem__(self, key):
    if type(key) == slice:
      r = self._range[key]
      return arrayview(self.obj, slice(r.start, None if r.stop < 0 else r.stop, r.step), readonly=self.readonly)
    return self.obj[self._range[key]]
  def __setitem__(self, key, item):
    if self.readonly: raise TypeError('cannot modify read-only arrayview')
    if type(key) == slice:
      key_range = self._range[key]
      key = slice(key_range.start, None if key_range.stop < 0 else key_range.stop, key_range.step)
      klen = len(key_range)
      titem = type(item)
      if titem not in (str, bytes, tuple, memoryview):  # bytearray|list|arrayview may change size during assignment if item._slice.stop is None
        raise TypeError(f'a fixed length primitive is required (str, bytes, tuple, …), not {titem.__name__!r}')
        #if titem in bytearray: item = bytes(item)
        #else: item = [v for i, v in zip(range(klen + 1), item)]
      ilen = len(item)
      if klen != ilen: raise ValueError(f'{self.__class__.__name__} assignment: lvalue and rvalue have different structures')
      self.obj[key] = item
    else:
      self.obj[self._range[key]] = item
  def toreadonly(self): return arrayview(self.obj, self._slice, readonly=True)
  def __eq__(self, other): return sequence_eq(self, other)
  def __ne__(self, other): return sequence_ne(self, other)
  def __ge__(self, other): return sequence_ge(self, other)
  def __gt__(self, other): return sequence_gt(self, other)
  def __le__(self, other): return sequence_le(self, other)
  def __lt__(self, other): return sequence_lt(self, other)
  def count(self, x): return sequence_count(self, x)
  def index(self, *a, **k): return sequence_index(self, *a, **k)
  def __add__(self, other): raise TypeError(f'unsupported operand type(s) for +: {self.__class__.__name__} and {type(other)}')
  def __mul__(self, other): raise TypeError(f'unsupported operand type(s) for *: {self.__class__.__name__} and {type(other)}')
  def __rmul__(self, other): raise TypeError(f'unsupported operand type(s) for *: {type(other)} and {self.__class__.__name__}')

arrayview._require_globals = ['sequence_eq', 'sequence_ne', 'sequence_ge', 'sequence_gt', 'sequence_le', 'sequence_lt', 'sequence_count', 'sequence_index']
