# io_parsemode.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def io_parsemode(mode):
  p,a,b,r,t,w,x = "","","","","","",""
  for _ in mode:
    if   _ == "+": p += "+"
    elif _ == "a": a += "a"
    elif _ == "b": b += "b"
    elif _ == "r": r += "r"
    elif _ == "t": t += "t"
    #elif _ == "U": U = r = 1
    elif _ == "w": w += "w"
    elif _ == "x": x += "x"
    else: ValueError(f"invalid mode: {mode!r}")
  if any(len(_) > 1 for _ in (p,a,b,r,t,w,x)): raise ValueError(f"invalid mode: {mode!r}")
  #if U:
  #  if x or w or a or u: raise ValueError("mode U cannot be combined with 'x', 'w', 'a', or '+'")
  #  raise DeprecationWarning("'U' mode is deprecated")
  if t and b: raise ValueError("can't have text and binary mode at once")
  _ = len(x+r+w+a)
  if _ < 1: raise ValueError("must have exactly one of create/read/write/append mode and at most one plus")
  if _ > 1: raise ValueError("must have exactly one of create/read/write/append mode")
  return p,a,b,r,t,w,x
