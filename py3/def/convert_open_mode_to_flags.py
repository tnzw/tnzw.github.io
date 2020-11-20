# convert_open_mode_to_flags.py Version 1.0.2
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def convert_open_mode_to_flags(mode, o_binary=False, flags_as_str_list=False, os_module=None):
  # https://github.com/python/cpython/blob/47a23fc63fa5df2da8dbc542e78e521d4a7f10c9/Modules/_io/_iomodule.c
  x,r,w,a,u,t,b,U = 0,0,0,0,0,0,0,0
  for _ in mode[:7]:
    if   _ == "x": x = 1
    elif _ == "r": r = 1
    elif _ == "w": w = 1
    elif _ == "a": a = 1
    elif _ == "+": u = 1
    elif _ == "t": t = 1
    elif _ == "b": b = 1
    #elif _ == "U": U = r = 1
    else: raise ValueError(f"invalid mode: '{mode}'")
  if len(mode) != x+r+w+a+u+t+b+U: raise ValueError(f"invalid mode: '{mode}'")
  #if U:
  #  if x or w or a or u: raise ValueError("mode U cannot be combined with 'x', 'w', 'a', or '+'")
  #  raise DeprecationWarning("'U' mode is deprecated")
  if t and b: raise ValueError("can't have text and binary mode at once")
  if not b: raise ValueError("cannot convert text mode to flags")
  if x+r+w+a > 1: raise ValueError("must have exactly one of create/read/write/append mode")
  flags = []
  if u:
    if r: flags = flags + ["O_RDWR"]
    elif w: flags = flags + ["O_RDWR", "O_CREAT", "O_TRUNC"]
    elif x: flags = flags + ["O_RDWR", "O_CREAT", "O_EXCL"]
    elif a: flags = flags + ["O_RDWR", "O_CREAT", "O_APPEND"]
  elif r: flags = flags + ["O_RDONLY"]
  elif w: flags = flags + ["O_WRONLY", "O_CREAT", "O_TRUNC"]
  elif x: flags = flags + ["O_WRONLY", "O_CREAT", "O_EXCL"]
  elif a: flags = flags + ["O_WRONLY", "O_CREAT", "O_APPEND"]
  if o_binary: flags = flags + ["O_BINARY"]
  if flags_as_str_list: return flags
  if os_module is None: os_module = os
  x = 0
  for r in flags: x |= getattr(os_module, r)
  return x
convert_open_mode_to_flags._required_globals = ["os"]
