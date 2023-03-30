# int32_fromint.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def int32_fromint(i):
  # has the same behavior as in javascript `i|0`
  if   i < -0xFFFFFFFF: i = (-i) & 0xFFFFFFFF
  elif i >  0xFFFFFFFF: i =   i  & 0xFFFFFFFF
  if i >  0x7FFFFFFF: return -(i ^ 0xFFFFFFFF) - 1
  if i < -0x80000000: return -(i ^ 0xFFFFFFFF) - 1
  return i
