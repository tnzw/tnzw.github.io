# io_readuntil.py Version 1.2.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def io_readuntil():
  # io_readuntil[.iter]
  # io_readuntil.separators[.iter]
  # io_readuntil.condition[.iter]

  def splitsuffixpart(bb, seps):
    seps = list((sep, len(sep)) for sep in seps)
    for sep, sepl in seps:
      if bb[-sepl:] == sep: return bb[:-sepl], bb[-sepl:]
    i = 1
    while seps:
      for sep, sepl in seps:
        sepli = sepl - i
        if sepli <= 0: seps.remove((sep, sepl))
        elif bb[-sepli:] == sep[:sepli]: return bb[:-sepli], bb[-sepli:]
      i += 1
    return bb, bb[:0]

  def io_readuntil(reader, separator=b"\n", *, errors="strict"):
    """\
Read data from the stream until separator is found.

On success, the data and separator will be removed from the internal buffer
(consumed). Returned data will include the separator at the end.

If EOF is reached before the complete separator is found, an IncompleteReadError
exception is raised, and the internal buffer is reset. The
IncompleteReadError.partial attribute may contain a portion of the separator.
"""
    # https://docs.python.org/3/library/asyncio-stream.html#asyncio.StreamReader.readuntil
    len_sep = len(separator)
    if len_sep <= 0: raise ValueError("empty separator")
    def condition(data):
      d, s = splitsuffixpart(data, (separator,))
      if s == separator: return 0
      return len_sep - len(s)
    return io_readuntil_condition(reader, condition, len_sep, errors=errors)

  def io_readuntil_iter(reader, separator=b"\n", *, errors="strict"):
    len_sep = len(separator)
    if len_sep <= 0: raise ValueError("empty separator")
    def condition(data):
      d, s = splitsuffixpart(data, (separator,))
      if s == separator: return 0, d, s
      return len_sep - len(s), d, s
    return io_readuntil_condition_iter(reader, condition, len_sep, errors=errors)

  def io_readuntil_separators(reader, separator, *separators, errors="strict"):
    """\
Same but with multiple separators. Firsts separators have higher priority.
"""
    separators = (separator,) + separators
    min_len_sep = min(len(s) for s in separators)
    #separators = tuple(sorted((separator,) + separators, key=lambda s: len(s)))
    #lens = list(len(_) for _ in separators)
    if min_len_sep <= 0: raise ValueError("empty separator")
    def condition(data):
      d, s = splitsuffixpart(data, separators)
      if s in separators: return 0
      ms = min_len_sep - len(s)
      if ms > 0: return ms
      return 1
    return io_readuntil_condition(reader, condition, min_len_sep, errors=errors)

  def io_readuntil_separators_iter(reader, separator, *separators, errors="strict"):
    separators = (separator,) + separators
    min_len_sep = min(len(s) for s in separators)
    if min_len_sep <= 0: raise ValueError("empty separator")
    def condition(data):
      d, s = splitsuffixpart(data, separators)
      if s in separators: return 0, d, s
      ms = min_len_sep - len(s)
      if ms > 0: return ms, d, s
      return 1, d, s
    return io_readuntil_condition_iter(reader, condition, min_len_sep, errors=errors)

  def io_readuntil_condition(reader, condition, initial_read_size, *, errors="strict"):
    """\
Read data from the reader until condition() returns 0.

`condition` should return a positive integer that will be used to read the next
chunk. It is called with one positional argument : a consolidation of read
chunks using the `+=` operator.
"""
    data = reader.read(initial_read_size)
    if not data:
      if errors == "strict": raise io_IncompleteReadError(data, initial_read_size)
      elif errors == "ignore": return
      else: raise LookupError(f"unknown error handler name {errors!r}")
    n = condition(data)
    if n <= 0: return data
    while True:
      d = reader.read(n)
      if not d:
        if errors == "strict": raise io_IncompleteReadError(data, len(data) + n)
        elif errors == "ignore": return
        else: raise LookupError(f"unknown error handler name {errors!r}")
      data += d
      n = condition(data)
      if n <= 0: return data

  def io_readuntil_condition_iter(reader, condition, initial_read_size, *, errors="strict"):
    d = reader.read(initial_read_size)
    if not d:
      if errors == "strict": raise io_IncompleteReadError(d, initial_read_size)
      elif errors == "yieldempty": yield d; return
      elif errors == "ignore": return
      else: raise LookupError(f"unknown error handler name {errors!r}")
    n, d, s = condition(d)
    if d: yield d
    if n <= 0:
      if s: yield s
      return
    while True:
      d = reader.read(n)
      if not d:
        if errors == "strict": raise io_IncompleteReadError(d, n)
        if s: yield s
        if errors == "yieldempty": yield d; return
        elif errors == "ignore": return
        else: raise LookupError(f"unknown error handler name {errors!r}")
      n, d, s = condition(s + d)
      if d: yield d
      if n <= 0:
        if s: yield s
        return

  io_readuntil.iter = io_readuntil_iter
  io_readuntil.separators = io_readuntil_separators
  io_readuntil.separators.iter = io_readuntil_separators_iter
  io_readuntil.condition = io_readuntil_condition
  io_readuntil.condition.iter = io_readuntil_condition_iter
  return io_readuntil

io_readuntil = io_readuntil()
io_readuntil._required_globals = ["io_IncompleteReadError"]
