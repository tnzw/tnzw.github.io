# uniq.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def uniq(iterable, *iterables, key=None):
  def defaultkey(r): return r
  iterables = (iterable,) + iterables
  if key is None: key = defaultkey
  keys = set()
  for iterable in iterables:
    for value in iterable:
      valuekey = key(value)
      if valuekey not in keys:
        yield value
        keys.add(valuekey)
