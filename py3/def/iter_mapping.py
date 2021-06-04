# iter_mapping.py Version 1.0.2
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def iter_mapping(mapping):
  """\
iter_mapping(mapping)
iter_mapping(iterable)

Iterate on mapping key-value pairs.
Inspired by native dict.update() behavior.
"""
  # class Mapping():
  #   def keys(self): yield key
  #   def __getitem__(self, key): return value
  if hasattr(mapping, "keys"):
    it = mapping.keys()
    def __iter__():
      for k in it: yield k, mapping[k]
    return __iter__()
  # class Iterable():
  #   def __iter__(self): yield (key, value)
  # class Iterable():
  #   def __getitem__(self, index): return (key, value) or raise IndexError
  it = iter(mapping)
  def __iter__():
    for k, v in it: yield k, v
  return __iter__()
