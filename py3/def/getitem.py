# getitem.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def getitem(obj, key, *default):
  if len(default) > 1: raise TypeError(f"getitem expected at most 3 arguments, got {len(default)}")
  m = type(obj).__getitem__
  if default:
    try: return m(obj, key)
    except KeyError: return default[0]
  return m(obj, key)
