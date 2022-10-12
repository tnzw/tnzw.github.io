# paddingarray.py Version 1.0.0
# Copyright (c) 2022 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class paddingarray:
  def __init__(self, value, length):
    self.value = value
    if type(length) != int: raise TypeError('length must be an int')
    self.length = length
  def __len__(self): return self.length
  def __iter__(self):
    for i in range(len(self)): yield self.value
  def __contains__(self, item): return item == self.value
  def __repr__(self): return f'{self.__class__.__name__}({self.value!r}, {self.length!r})'
  def __getitem__(self, key):
    if type(key) == slice:
      length = len(range(len(self))[key])
      return paddingarray(self.value, length)
    range(len(self))[key]
    return self.value
  def __setitem__(self, key, item):
    raise TypeError('cannot modify read-only paddingarray')
  def __eq__(self, other): return sequence_eq(self, other)
  def __ne__(self, other): return sequence_ne(self, other)
  def __ge__(self, other): return sequence_ge(self, other)
  def __gt__(self, other): return sequence_gt(self, other)
  def __le__(self, other): return sequence_le(self, other)
  def __lt__(self, other): return sequence_lt(self, other)
  def count(self, x): return sequence_count(self, x)
  def index(self, *a, **k): return sequence_index(self, *a, **k)
  #def __add__(self, other): raise TypeError(f'unsupported operand type(s) for +: {self.__class__.__name__} and {type(other)}')
  #def __mul__(self, other): raise TypeError(f'unsupported operand type(s) for *: {self.__class__.__name__} and {type(other)}')
  #def __rmul__(self, other): raise TypeError(f'unsupported operand type(s) for *: {type(other)} and {self.__class__.__name__}')

paddingarray._require_globals = ['sequence_eq', 'sequence_ne', 'sequence_ge', 'sequence_gt', 'sequence_le', 'sequence_lt', 'sequence_count', 'sequence_index']
