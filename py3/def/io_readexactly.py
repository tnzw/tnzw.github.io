# io_readexactly.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def io_readexactly(reader, n):
  """\
Read exactly n bytes.

Raise an io_IncompleteReadError if EOF is reached before n can be read. Use the
IncompleteReadError.partial attribute to get the partially read data.
"""
  # https://docs.python.org/3/library/asyncio-stream.html#asyncio.StreamReader.readexactly
  data = reader.read(n)
  if not data: raise io_IncompleteReadError(data, n)
  data_length = len(data)
  while data_length < n:
    d = reader.read(n - data_length)
    if not d: raise io_IncompleteReadError(data, n)
    data += d
    data_length = len(data)
  if data_length != n: raise io_IncompleteReadError(data, n)  # same if data > n ?
  return data
io_readexactly._required_globals = ["io_IncompleteReadError"]
