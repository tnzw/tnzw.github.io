# iaddjoin.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def iaddjoin():
  def iaddjoin(iterable, *default):
    if len(default) > 1: raise TypeError(f"iaddjoin() takes 2 positional arguments but {len(default) + 1} were given")
    it = iter(iterable)
    for _ in it:
      o = _
      break
    else:
      if default: return default[0]
      raise ValueError("iterable should contain at least one value")
    for _ in it: o += _
    return o
  def iaddjoin_withsep(iterable, sep, *default):
    if len(default) > 1: raise TypeError(f"iaddjoin() takes 3 positional arguments but {len(default) + 2} were given")
    it = iter(iterable)
    for _ in it:
      o = _
      break
    else:
      if default: return default[0]
      raise ValueError("iterable should contain at least one value")
    for _ in it:
      o += sep
      o += _
    return o
  iaddjoin.withsep = iaddjoin_withsep
  return iaddjoin
iaddjoin = iaddjoin()
