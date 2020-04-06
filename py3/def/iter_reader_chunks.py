# iter_reader_chunks.py Version 1.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def iter_reader_chunks(reader, block_size=None, buffer_size=None):
  """\
for data_chunk in iter_reader_chunks(open(filename, "rb")):
  handle(data_chunk)
"""
  if getattr(reader, "encoding", None) is None:
    fileno = getattr(reader, "fileno", lambda: None)()
  else:
    fileno = None

  if buffer_size is None:
    if block_size is not None:
      buffer_size = block_size
    else:
      buffer_size = 32 * 1024
      try:
        if isinstance(BUFFER_SIZE, int) and BUFFER_SIZE > 0: buffer_size = BUFFER_SIZE
      except NameError: pass
  if block_size is None:
    block_size = buffer_size

  if isinstance(fileno, int):
    data = os.read(fileno, buffer_size)
    while data:
      yield data
      data = os.read(fileno, buffer_size)
  else:
    fileno = None  # avoid keeping useless links in memory
    data = reader.read(block_size)
    while data:
      yield data
      data = reader.read(block_size)
iter_reader_chunks._required_globals = ["os"]
