# zipfile_struct_mkcenrecord.py Version 1.0.0-2
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def zipfile_struct_mkcenrecord(version_madeby, version_needed, bitflags, compression_method, dos_mtime, crc32, compressed_size, uncompressed_size, start_disk_number, internal_file_attributes, external_file_attributes, offset, filename, extrafields=b'', comment=b''):
  # Make Central Directory Entry Record
  # see https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT
  # see https://en.wikipedia.org/wiki/File_attribute
  # see https://stackoverflow.com/questions/434641/how-do-i-set-permissions-attributes-on-a-file-in-a-zip-file-using-pythons-zip
  # see http://unix.stackexchange.com/questions/14705/the-zip-formats-external-file-attribute
  # External file attributes
  #     TTTTsstrwxrwxrwx?EIOCLsTNdADVSHR 32 bits (high to low)
  #     ^^^^____________________________ file type, see zipinfo.c (UNX_*)
  #         ^^^_________________________ setuid, setgid, sticky
  #            ^^^^^^^^^________________ permissions
  #                     ^_______________ have GMT mod/acc times (only used in beta ZIP, please DON'T USE it anymore!)
  #                      ^______________ have UNIX UID/GID info (no longer used?)
  #                      ^^^^^^^^^______ Windows/NTFS attribute bits?: Encrypted, not content-Indexed, Offline, Compressed, reparse point (~symLink), s?, Temporary, Normal (and indexed), d?
  #                               ^^^^^^ DOS attribute bits: Archive, Directory, Volume label, System file, Hidden, Read-only
  return struct.pack('<LHHHHLLLLHHHHHLL',
    0x02014B50,                # b'PK\x01\x02': Central directory file header signature
    version_madeby,            #            <H: Version made by (jszip uses 0x31e for UNIX version 3.0 and 0x14 for DOS version 2.0, 7zip uses 0x3F I think)
    version_needed,            #            <H: Version needed to extract (minimum) (I often see 0x2d for ZIP64 archive, otherwise 0xa)
    bitflags,                  #            <H: General purpose bit flag
    compression_method,        #            <H: Compression method; e.g. none = 0, DEFLATE = 8 (or b'\x08\x00')
    dos_mtime,                 #           <HH: File last modification time + File last modification date
    crc32,                     #            <L: CRC-32 of uncompressed data
    compressed_size,           #            <L: Compressed size (or 0xffffffff for ZIP64)
    uncompressed_size,         #            <L: Uncompressed size (or 0xffffffff for ZIP64)
    len(filename),             #            <H: File name length
    len(extrafields),          #            <H: Extra field length
    len(comment),              #            <H: File comment length
    start_disk_number,         #            <H: Disk number where file starts (or 0xffff for ZIP64)
    internal_file_attributes,  #            <H: Internal file attributes (set to 0 everytime?)
    external_file_attributes,  #            <L: External file attributes (see version madeby doc)
    offset                     #            <L: Relative offset of local file header (or 0xffffffff for ZIP64).
                               #                This is the number of bytes between the start of the first disk on which the file occurs, and the start of the local file header.
                               #                This allows software reading the central directory to locate the position of the file inside the ZIP file.
    ) + filename + extrafields + comment
zipfile_struct_mkcenrecord._required_globals = ['struct']
