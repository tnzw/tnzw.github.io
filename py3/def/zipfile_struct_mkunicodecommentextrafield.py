# zipfile_struct_mkunicodecommentextrafield.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def zipfile_struct_mkunicodecommentextrafield(crc32, comment):
  return zipfile_struct_mkunicodeextrafield(0x6375, 1, crc32, comment)
zipfile_struct_mkunicodecommentextrafield._required_globals = ['zipfile_struct_mkunicodeextrafield']
