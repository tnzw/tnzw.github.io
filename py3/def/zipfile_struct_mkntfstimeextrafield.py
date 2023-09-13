# zipfile_struct_mkntfstimeextrafield.py Version 1.0.1
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def zipfile_struct_mkntfstimeextrafield(mntfstime, antfstime=None, cntfstime=None):
  """zipfile_struct_mkntfstimeextrafield(ntfstime_fromtimestamp(os.stat(...).st_mtime, True), 0, 0) -> bytes"""
  # NB: here, an ntfstime == 0 means undefined time
  # NB: cntfstime is creation time
  # https://github.com/mcmilk/7-Zip/blob/c2a1bdb0235368e80cf6d434baf448c94469e04d/CPP/7zip/Archive/Zip/ZipItem.cpp#L123
  if   cntfstime is not None: ntfstimesf = 'QQQ'; l = 24; ntfstimes = (mntfstime, antfstime, cntfstime)
  elif antfstime is not None: ntfstimesf = 'QQ';  l = 16; ntfstimes = (mntfstime, antfstime)
  else:                       ntfstimesf = 'Q';   l =  8; ntfstimes = (mntfstime,)
  return struct.pack('<HHLHH' + ntfstimesf,
    0xA,         # b'\x0a\x00': NTFS time extra field signature
    l + 8,       #          <H: This extra field content length
    0,           #          <L: reserved...
    1,           #          <H: TagTime key
    l,           #          <H: Attributes size
    *ntfstimes)  #        <QQQ: mtime & atime & ctime
zipfile_struct_mkntfstimeextrafield._required_globals = ['struct']
