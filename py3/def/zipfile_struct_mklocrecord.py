# zipfile_struct_mklocrecord.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def zipfile_struct_mklocrecord(version_needed, bitflags, compression_method, dos_mtime, crc32, compressed_size, uncompressed_size, filename, extrafields=b''):
  # Make Local File Header Record
  # NB: Having filename & comment in UTF-8 is the only way to get the same result in all platforms and all versions.
  # see https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT
  return struct.pack('<LHHHLLLLHH',  # struct.pack() raises struct.error on invalid types/values
    0x04034B50,          # b'PK\x03\x04': Local file header signature
    version_needed,      #            <H: Version needed to extract (minimum) (I often see 0x2d for ZIP64 archive, otherwise 0xa)
    bitflags,            #            <H: General purpose bit flag
    compression_method,  #            <H: Compression method; e.g. none = 0, DEFLATE = 8 (or "\x08\x00")
    dos_mtime,           #           <HH: File last modification time + File last modification date
    crc32,               #            <L: CRC-32 of uncompressed data (or 0 for stream)
    compressed_size,     #            <L: Compressed size (or 0xffffffff for ZIP64 or 0 for stream)
    uncompressed_size,   #            <L: Uncompressed size (or 0xffffffff for ZIP64 or 0 for stream)
    len(filename),       #            <H: File name length
    len(extrafields)     #            <H: Extra field length
    ) + filename + extrafields
zipfile_struct_mklocrecord._required_globals = ['struct']
