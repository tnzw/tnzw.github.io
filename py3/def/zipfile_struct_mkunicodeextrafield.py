# zipfile_struct_mkunicodeextrafield.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def zipfile_struct_mkunicodeextrafield(extrafield_signature, version, crc32, text):
  # see https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT
  return (struct.pack('<HHBL',
    extrafield_signature,  # b'\x75\x70': Info-ZIP Unicode Path Extra Field, b'\x75\x63': Info-ZIP Unicode Comment Extra Field
    len(text) + 5,         #          <H: Field length after this point
    version,               #           B: Version of this extra field (always 1 for the moment)
    crc32) +               #          <L: CRC-32 of non UTF-8 encoded text
    text)                  #              UTF-8 encoded text
zipfile_struct_mkunicodeextrafield._required_globals = ['struct']
