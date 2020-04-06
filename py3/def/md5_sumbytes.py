# md5_sumbytes.py Version 1.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def md5_sumbytes(bytes_data):
  return b"".join(uint32_littleendian_tobytes(_) for _ in md5_as4uint32_sumbytes(bytes_data))
md5_sumbytes._required_globals = [
  "md5_as4uint32_sumbytes",
  "uint32_littleendian_tobytes",
]
