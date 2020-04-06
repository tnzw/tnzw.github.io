# int64_bigendian_frombytes.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def int64_bigendian_frombytes(bb):
  i = bb[7]
  i |= bb[6] << 8
  i |= bb[5] << 16
  i |= bb[4] << 24
  i |= bb[3] << 32
  i |= bb[2] << 40
  i |= bb[1] << 48
  b = bb[0]
  i |= (b & 0x7F) << 56
  if b & 0x80:
    return -0x8000000000000000 + i
  return i
