# iter_blocks.py Version 1.1.0
# Copyright (c) 2020-2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def iter_blocks(iterable, block_size, errors=None, *, padding=None):
  """\
iter_blocks(iterable, block_size, **options)

iterable  : the iterable to split in blocks.
block_size: the amount of element per block.
options:
  padding: the value to use on padding (defaults to None) (see errors => "pad")
  errors :
    => "strict"  : raise a ValueError on unterminated block.
    => "truncate": truncate the final block.
    => "pad"     : pad each remaining block cell by `padding`.
    => "ignore"  : ignore the unterminated block.
    => None      : (default) same as "truncate".

Usage:
  for block in iter_blocks([0, 1, 2, 3, 4], 2): print(block)
  → [0, 1]
  → [2, 3]
  → [4]
"""
  block = [None]*block_size
  i = 0
  for _ in iterable:
    block[i] = _
    i += 1
    if i == block_size:
      yield block
      i = 0
  if i:
    if errors == "strict":
      raise ValueError("unterminated block")
    elif errors in ("truncate", None):
      block[:] = block[:i]
      yield block
    elif errors == "pad":
      for _ in range(i, block_size, 1): block[_] = padding
      yield block
    elif errors == "ignore": pass
    else: raise LookupError(f"unknown error handler name {errors!r}")
