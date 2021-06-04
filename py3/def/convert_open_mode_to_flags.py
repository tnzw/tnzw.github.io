# convert_open_mode_to_flags.py Version 1.0.3
# Copyright (c) 2020-2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def convert_open_mode_to_flags(mode, o_binary=False, flags_as_str_list=False, os_module=None):
  # https://github.com/python/cpython/blob/47a23fc63fa5df2da8dbc542e78e521d4a7f10c9/Modules/_io/_iomodule.c
  p,a,b,r,t,w,x = io_parsemode(mode)
  if not b: raise ValueError("cannot convert text mode to flags")
  flags = []
  if p:
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
convert_open_mode_to_flags._required_globals = ["os", "io_parsemode"]
