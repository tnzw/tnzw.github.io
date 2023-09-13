# tar_reader_itertokens.py Version 1.0.1
# Copyright (c) 2020, 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

# Inspired by https://github.com/calccrypto/tar/blob/master/tar.c

def tar_reader_itertokens(reader, buffer_size=None, blocking_factor=20):
  """\
with open(tarfile, "rb") as f:
  for token, data in tar_reader_itertokens(f):
    print(token, len(data))
"""
  RECORD_SIZE = 512 * blocking_factor
  tar_position = 0
  update = 1
  while 1:
    if update: block = tar_MetadataBlock(reader.read(512))
    update = 1
    if not any(block):
      next_block = tar_MetadataBlock(reader.read(512))
      if not any(next_block):
        yield "end_of_record", b""
        for _ in io_iterread1(reader, buffer_size, RECORD_SIZE - (tar_position % RECORD_SIZE)):
          yield "end_of_record_chunk", _
        break
      yield "zero_block", block
      block, next_block = next_block, None
      update = 0
    block._file_position = tar_position
    yield "metadata_block", block
    data_size = block.size
    if data_size:
      yield "data_chunk_start", b""
      for _ in io_iterread1(reader, buffer_size, data_size):
        yield "data_chunk", _
      yield "data_chunk_end", b""
      padding_size = data_size % 512
      if padding_size: padding_size = 512 - padding_size
      for _ in io_iterread1(reader, buffer_size, padding_size):
        yield "padding_chunk", _
tar_reader_itertokens._required_globals = ['tar_MetadataBlock', 'io_iterread1']
