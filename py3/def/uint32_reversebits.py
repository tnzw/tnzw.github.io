# uint32_reversebits.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def uint32_reversebits(uint32):
  uint32 = (uint32 & 0xFFFF0000) >> 16 | (uint32 & 0x0000FFFF) << 16
  uint32 = (uint32 & 0xFF00FF00) >>  8 | (uint32 & 0x00FF00FF) <<  8
  uint32 = (uint32 & 0xF0F0F0F0) >>  4 | (uint32 & 0x0F0F0F0F) <<  4
  uint32 = (uint32 & 0xCCCCCCCC) >>  2 | (uint32 & 0x33333333) <<  2
  return   (uint32 & 0xAAAAAAAA) >>  1 | (uint32 & 0x55555555) <<  1
