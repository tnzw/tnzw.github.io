# zipfile_struct_mkeocd64locatorrecord.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def zipfile_struct_mkeocd64locatorrecord(start_disk_number, offset, disk_count):
  return struct.pack('<LLQL',
    0x07064B50,         # b'PK\x06\x07': ZIP64 End of central directory locator signature
    start_disk_number,  #            <L: Disk where central directory starts
    offset,             #            <Q: Offset of start of ZIP64 EOCD, relative to start of archive
    disk_count)         #            <L: Number of disks
zipfile_struct_mkeocd64locatorrecord._required_globals = ['struct']
