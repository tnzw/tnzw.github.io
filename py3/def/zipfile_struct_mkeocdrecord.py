# zipfile_struct_mkeocdrecord.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def zipfile_struct_mkeocdrecord(disk_number, start_disk_number, this_disk_count, count, central_size, local_size, comment=b''):
  # Make End Of Central Directory Record
  return struct.pack('<LHHHHLLH',
    0x06054B50,         # b'PK\x05\x06': End of central directory signature
    disk_number,        #            <H: Number of this disk (or 0xffff for ZIP64)
    start_disk_number,  #            <H: Disk where central directory starts (or 0xffff for ZIP64)
    this_disk_count,    #            <H: Number of central directory records on this disk (or 0xffff for ZIP64)
    count,              #            <H: Total number of central directory records (or 0xffff for ZIP64)
    central_size,       #            <L: Size of central directory (bytes) (or 0xffffffff for ZIP64)
    local_size,         #            <L: Offset of start of central directory, relative to start of archive (or 0xffffffff for ZIP64)
    len(comment)        #            <H: Comment length
    ) + comment
zipfile_struct_mkeocdrecord._required_globals = ['struct']
