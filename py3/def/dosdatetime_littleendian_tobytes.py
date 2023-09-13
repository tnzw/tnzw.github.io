# dosdatetime_littleendian_tobytes.py Version 1.0.1
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def dosdatetime_littleendian_tobytes(ddt):
  if ddt < 0: raise ValueError('invalid dos date time')
  if ddt > 0xFFFFFFFF: raise ValueError('year must be < 2108')
  return uint32_littleendian_tobytes(ddt)
dosdatetime_littleendian_tobytes._required_globals = ['uint32_littleendian_tobytes']
