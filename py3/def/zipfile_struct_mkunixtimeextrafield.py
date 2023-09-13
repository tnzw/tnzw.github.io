# zipfile_struct_mkunixtimeextrafield.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def zipfile_struct_mkunixtimeextrafield(munixtime=None, aunixtime=None, cunixtime=None):
  """zipfile_struct_mkunixtimeextrafield(int(os.stat(...).st_mtime)) -> bytes"""
  # https://github.com/mcmilk/7-Zip/blob/c2a1bdb0235368e80cf6d434baf448c94469e04d/CPP/7zip/Archive/Zip/ZipItem.cpp#L154
  flags = 0; unixtimesf = ''; unixtimes = []
  if munixtime is not None: flags |= 1; unixtimesf += 'L'; unixtimes.append(munixtime)
  if aunixtime is not None: flags |= 2; unixtimesf += 'L'; unixtimes.append(aunixtime)
  if cunixtime is not None: flags |= 4; unixtimesf += 'L'; unixtimes.append(cunixtime)
  return struct.pack('<HHB' + unixtimesf,
    0x5455,                   # b'UT': UNIX time extra field signature
    len(unixtimesf) * 4 + 1,  #    <H: sizeof(flags + attributes)
    flags,                    #     B: flags 0x1 mtime, 0x2 atime, 0x4 ctime
    *unixtimes)               #  <LLL: mtime & atime & ctime
zipfile_struct_mkunixtimeextrafield._required_globals = ['struct']
