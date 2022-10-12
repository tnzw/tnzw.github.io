# winreg_KeyEntry.py Version 1.0.0
# Copyright (c) 2022 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class winreg_KeyEntry(tuple):
  __slots__ = ()
  def __new__(cls, type, name, data=None, data_type=None): return tuple.__new__(cls, (type, name, data, data_type))
  def __repr__(self): return f'{self.__class__.__name__}({self.type!r}, {self.name!r})'
  @property
  def type(self): return tuple.__getitem__(self, 0)
  @property
  def name(self): return tuple.__getitem__(self, 1)
  @property
  def data(self): return tuple.__getitem__(self, 2)
  @property
  def data_type(self): return tuple.__getitem__(self, 3)
