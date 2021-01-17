# devnull_bytearray.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class devnull_bytearray(bytearray):
  # https://docs.python.org/3/reference/datamodel.html
  # https://docs.python.org/3/library/operator.html
  # https://docs.python.org/3/library/stdtypes.html#bytearray
  def __new__(cls): return bytearray.__new__(cls)
  def __setitem__(self, key, value): pass
  def append(self, int): pass
  def extend(self, iterable_int): pass
  def insert(self, index, int): pass
