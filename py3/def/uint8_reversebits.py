# uint8_reversebits.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def uint8_reversebits(uint8):
  uint8 = (uint8 & 0xF0) >> 4 | (uint8 & 0x0F) << 4
  uint8 = (uint8 & 0xCC) >> 2 | (uint8 & 0x33) << 2
  return  (uint8 & 0xAA) >> 1 | (uint8 & 0x55) << 1
