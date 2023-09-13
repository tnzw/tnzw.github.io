# zipfile_struct_mkeocd64record.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def zipfile_struct_mkeocd64record(version_madeby, version_needed, disk_number, start_disk_number, this_disk_count, count, central_size, local_size, comment=b''):
  # Make End Of Central Directory (ZIP64) Record
  # You don't have to use EOCD64 even if there is central ZIP64 extra field
  return struct.pack('<LQHHLLQQQQ',
    0x06064B50,         # b'PK\x06\x06': ZIP64 End of central directory signature
    len(comment) + 44,  #            <Q: Size of this record after this point
    version_madeby,     #            <H: Version made by
    version_needed,     #            <H: Version needed to extract (minimum)
    disk_number,        #            <L: Number of this disk
    start_disk_number,  #            <L: Disk where central directory starts
    this_disk_count,    #            <Q: Number of central directory records on this disk
    count,              #            <Q: Total number of central directory records
    central_size,       #            <Q: Size of central directory
    local_size          #            <Q: Offset of start of central directory, relative to start of archive
    ) + comment         #                ZIP comment
zipfile_struct_mkeocd64record._required_globals = ['struct']
