# addjoin.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def addjoin():
  def addjoin(iterable, *default):
    if len(default) > 1: raise TypeError(f"addjoin() takes 2 positional arguments but {len(default) + 1} were given")
    it = iter(iterable)
    for _ in it:
      o = _
      break
    else:
      if default: return default[0]
      raise ValueError("iterable should contain at least one value")
    for _ in it: o = o + _
    return o
  def addjoin_withsep(iterable, sep, *default):
    if len(default) > 1: raise TypeError(f"addjoin() takes 3 positional arguments but {len(default) + 2} were given")
    it = iter(iterable)
    for _ in it:
      o = _
      break
    else:
      if default: return default[0]
      raise ValueError("iterable should contain at least one value")
    for _ in it: o = o + sep + _
    return o
  addjoin.withsep = addjoin_withsep
  return addjoin
addjoin = addjoin()
