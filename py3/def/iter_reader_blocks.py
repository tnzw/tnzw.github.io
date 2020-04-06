# iter_reader_blocks.py Version 1.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def iter_reader_blocks(reader, block_size):
  """\
for data_block in iter_reader_blocks(open(filename, "rb"), 4096):
  handle(data_block)
"""
  data = reader.read(block_size)
  while data:
    yield data
    data = reader.read(block_size)
