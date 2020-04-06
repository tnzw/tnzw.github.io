# uint64_bigendian_frombytes.py Version 1.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def uint64_bigendian_frombytes(bb):
  return bb[7] | (bb[6] << 8) | (bb[5] << 16) | (bb[4] << 24) | (bb[3] << 32) | (bb[2] << 40) | (bb[1] << 48) | (bb[0] << 56)
