# tar_calculate_checksum.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

# Inspired by https://github.com/calccrypto/tar/blob/master/tar.c

def tar_calculate_checksum(block):
  check = 0
  for _ in block[:148]: check += _
  for _ in      b" "*8: check += _
  for _ in block[156:]: check += _
  return check
