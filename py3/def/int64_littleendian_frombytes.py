# int64_littleendian_frombytes.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def int64_littleendian_frombytes(bb):
  i = bb[0]
  i |= bb[1] << 8
  i |= bb[2] << 16
  i |= bb[3] << 24
  i |= bb[4] << 32
  i |= bb[5] << 40
  i |= bb[6] << 48
  b = bb[7]
  i |= (b & 0x7F) << 56
  if b & 0x80:
    return -0x8000000000000000 + i
  return i
