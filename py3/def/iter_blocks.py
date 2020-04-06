# iter_blocks.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def iter_blocks(iterable, block_size):
  """\
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
    block[:] = block[:i]
    yield block
