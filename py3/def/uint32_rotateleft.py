# uint32_rotateleft.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def uint32_rotateleft(uint32, n):
  n %= 32
  if n < 0: n += 32
  return (((uint32 << n) & 0xFFFFFFFF) | (uint32 >> (32 - n)))
