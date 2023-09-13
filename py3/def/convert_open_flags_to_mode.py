# convert_open_flags_to_mode.py Version 1.0.3
# Copyright (c) 2020, 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def convert_open_flags_to_mode(flags, text=None, use_t=False, os_module=None):
  if os_module is None: os_module = os
  # assuming all flags uses only ONE bit
  fields = ('O_RDONLY', 'O_WRONLY', 'O_RDWR', 'O_APPEND', 'O_CREAT', 'O_TRUNC', 'O_EXCL')
  #def flags_contains(flags, flag): return flag and (flags & flag) == flag
  #r,w,rw,a,c,t,x = [flags_contains(flags, getattr(os_module, _)) for _ in fields]
  r,w,rw,a,c,t,x = [flags & getattr(os_module, _) for _ in fields]
  if os_module.O_RDONLY == 0 and not w and not rw: r = 1
  u = '+' if rw else ''
  b = 'b' if not text else ('t' if use_t else '')
  if not r and (w or rw) and     c and     t and not a and not x: return 'w' + u + b
  if not r and (w or rw) and     c and not t and     a and not x: return 'a' + u + b
  if not r and (w or rw) and     c           and not a and     x: return 'x' + u + b
  if (r or rw) and not w and not c and not t and not a and not x: return 'r' + u + b
  raise ValueError("invalid flag combination")
convert_open_flags_to_mode._required_globals = ['os']
