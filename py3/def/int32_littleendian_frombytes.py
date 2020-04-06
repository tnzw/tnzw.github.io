# int32_littleendian_frombytes.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def int32_littleendian_frombytes(bb):
  i = bb[0]
  i |= bb[1] << 8
  i |= bb[2] << 16
  b = bb[3]
  i |= (b & 0x7F) << 24
  if b & 0x80:
    return -0x80000000 + i
  return i
