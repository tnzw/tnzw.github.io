# zipfile_struct_mkddrecord.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def zipfile_struct_mkddrecord(crc32, compressed_size, uncompressed_size):
  # Make Data Descriptor Record
  return struct.pack('<LLLL',
    0x08074B50,         # b'PK\x07\x08': Data descriptor signature
    crc32,              #            <L: CRC-32 of uncompressed data
    compressed_size,    #            <L: Compressed size
    uncompressed_size)  #            <L: Uncompressed size
zipfile_struct_mkddrecord._required_globals = ['struct']
