# uint16_reversebits.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def uint16_reversebits(uint16):
  uint16 = (uint16 & 0xFF00) >> 8 | (uint16 & 0x00FF) << 8
  uint16 = (uint16 & 0xF0F0) >> 4 | (uint16 & 0x0F0F) << 4
  uint16 = (uint16 & 0xCCCC) >> 2 | (uint16 & 0x3333) << 2
  return   (uint16 & 0xAAAA) >> 1 | (uint16 & 0x5555) << 1
