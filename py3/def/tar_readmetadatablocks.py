# tar_readmetadatablocks.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

# Inspired by https://github.com/calccrypto/tar/blob/master/tar.c

def tar_readmetadatablocks(reader, blocking_factor=20):
  """\
for meta in tar_readmetadatablocks(open(filename, "rb")):
  print(meta.name)
"""
  RECORD_SIZE = 512 * blocking_factor
  entries = []
  tar_position = 0
  update = 1
  while 1:
    if update: block = tar_MetadataBlock(reader.read(512))
    update = 1
    if not any(block):
      block = tar_MetadataBlock(reader.read(512))
      if not any(block):
        reader.seek(RECORD_SIZE - (tar_position % RECORD_SIZE), 1)
        break
      update = 0
    block._file_position = tar_position
    tar_data_size = block.size
    if tar_data_size % 512: tar_data_size += 512 - (tar_data_size % 512)
    tar_position += 512 + tar_data_size
    reader.seek(tar_data_size, 1)
    entries.append(block)
  return entries
tar_readmetadatablocks._required_globals = ["tar_MetadataBlock"]
