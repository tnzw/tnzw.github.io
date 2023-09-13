# zipfile_struct_mkzip64extrafield.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def zipfile_struct_mkzip64extrafield(uncompressed_size, compressed_size=None, offset=None, start_disk_number=None):
  if   start_disk_number is not None: f = 'QQQL'; l = 28; s = (uncompressed_size, compressed_size, offset, start_disk_number)
  elif offset is not None:            f = 'QQQ';  l = 24; s = (uncompressed_size, compressed_size, offset)
  elif compressed_size is not None:   f = 'QQ';   l = 16; s = (uncompressed_size, compressed_size)
  else:                               f = 'Q';    l =  8; s = (uncompressed_size,)
  return struct.pack('<HH' + f,
    1,   # b'\x01\x00': Header ID
    l,   #          <H: Size of the extra field chunk (8, 16, 24 or 28)
    *s)  #          <Q: Uncompressed size
         #          <Q: Compressed size
         #          <Q: Offset of start of central directory, relative to start of archive
         #          <L: Number of the disk on which this file starts
zipfile_struct_mkzip64extrafield._required_globals = ['struct']
