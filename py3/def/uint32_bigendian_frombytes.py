# uint32_bigendian_frombytes.py Version 1.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def uint32_bigendian_frombytes(bb):
  return bb[3] | (bb[2] << 8) | (bb[1] << 16) | (bb[0] << 24)
