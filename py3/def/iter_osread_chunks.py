# iter_osread_chunks.py Version 1.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def iter_osread_chunks(fileno, buffer_size=None):
  """\
with open(filename, "rb") as f:
  for data_chunk in iter_osread_chunks(f.fileno()):
    handle(data_chunk)
"""
  if buffer_size is None:
    buffer_size = 32 * 1024
    try:
      if isinstance(BUFFER_SIZE, int) and BUFFER_SIZE > 0: buffer_size = BUFFER_SIZE
    except NameError: pass

  data = os.read(fileno, buffer_size)
  while data:
    yield data
    data = os.read(fileno, buffer_size)
iter_osread_chunks._required_globals = ["os"]
