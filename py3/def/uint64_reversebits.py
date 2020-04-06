# uint64_reversebits.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def uint64_reversebits(uint64):
  uint64 = (uint64 & 0xFFFFFFFF00000000) >> 32 | (uint64 & 0x00000000FFFFFFFF) << 32
  uint64 = (uint64 & 0xFFFF0000FFFF0000) >> 16 | (uint64 & 0x0000FFFF0000FFFF) << 16
  uint64 = (uint64 & 0xFF00FF00FF00FF00) >>  8 | (uint64 & 0x00FF00FF00FF00FF) <<  8
  uint64 = (uint64 & 0xF0F0F0F0F0F0F0F0) >>  4 | (uint64 & 0x0F0F0F0F0F0F0F0F) <<  4
  uint64 = (uint64 & 0xCCCCCCCCCCCCCCCC) >>  2 | (uint64 & 0x3333333333333333) <<  2
  return   (uint64 & 0xAAAAAAAAAAAAAAAA) >>  1 | (uint64 & 0x5555555555555555) <<  1
