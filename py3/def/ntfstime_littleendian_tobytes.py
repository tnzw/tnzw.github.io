# ntfstime_littleendian_tobytes.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def ntfstime_littleendian_tobytes(ntfstime):
  if ntfstime < 0: raise ValueError('invalid ntfs time')
  if ntfstime > 0xFFFFFFFFFFFFFFFF: raise ValueError('ntfs time must be < year ~60095')
  return uint64_littleendian_tobytes(ntfstime)
ntfstime_littleendian_tobytes._required_globals = ['uint64_littleendian_tobytes']
