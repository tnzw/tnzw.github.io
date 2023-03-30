# iter_mapping.py Version 1.0.3
# Copyright (c) 2021-2022 <tnzw@github.triton.ovh>
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
  t = type(mapping)
  if t is dict: return iter(t.items(mapping))
  # class Mapping():
  #   def keys(self): yield key
  #   def __getitem__(self, key): return value
  if hasattr(t, 'keys'): return ((k, mapping[k]) for k in iter(t.keys(mapping)))
  # class Iterable():
  #   def __iter__(self): yield (key, value)
  # class Iterable():
  #   def __getitem__(self, index): return (key, value) or raise IndexError
  return ((k, v) for k, v in iter(mapping))
