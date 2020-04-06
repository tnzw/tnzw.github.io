# uint64_bigendian_tobytes.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def uint64_bigendian_tobytes(uint64):
  return bytes((
    (uint64 >> 56) & 0xFF,
    (uint64 >> 48) & 0xFF,
    (uint64 >> 40) & 0xFF,
    (uint64 >> 32) & 0xFF,
    (uint64 >> 24) & 0xFF,
    (uint64 >> 16) & 0xFF,
    (uint64 >>  8) & 0xFF,
     uint64        & 0xFF,
  ))
