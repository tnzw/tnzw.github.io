# HexDumpEncoder.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

# could be easily python codec compatible
# see https://docs.python.org/3/library/codecs.html#incremental-encoding-and-decoding
class HexDumpEncoder(object):
  """\
HexDumpEncoder(**opt)

Transcode bytes input data to canonical hex+ascii bytes like :

    >>> HexDumpEncoder().encode(b'abcdefghijklmnopqrstuvwxyz')
    b'00000000  61 62 63 64 65 66 67 68  69 6A 6B 6C 6D 6E 6F 70  |abcdefghijklmnop|\n'
    b'00000010  71 72 73 74 75 76 77 78  79 7A                    |qrstuvwxyz|'

opt:
  state : internal use only.

Interfaces:
- copyable (ie. `copy()`)
- transcoder (ie. `transcode(iterable=None, *, stream=False)`)
"""
  def copy(self): return self.__class__(**{k: v for k, v in self.__dict__.items()})
  def __init__(self, *, errors="strict", state=None):
    self.state = (0, 0, 0, b'') if state is None else state
  def transcode(self, iterable=None, *, stream=False):
    """\
transcode(iterable, **opt)

iterable: a byte iterable value (defaults to None)
opt:
  stream => False: tells the transcoder that it is the last transcode operation
         => True
"""
    if iterable is None: iterable = ()

    index, ioffset, offset, side = self.state
    chunk = b''

    i = index % 16
    if i != offset % 16:
      # here, offset is 16
      chunk += f'\n{index:08X}'.encode() + b' ' * (i * 3 + (2 if i > 8 else 1))
      ioffset = offset = i

    for b in iterable:
      # here, offset is like i (but 1 <= offset <= 16)
      if offset == 0: chunk += f'{index:08X}'.encode()
      elif offset >= 16: chunk += f'\n{index:08X}'.encode(); ioffset = offset = 0
      side += bytes((b,)) if 0x20 <= b < 0x7f else b'.'
      if offset in (0, 8): chunk += f'  {b:02X}'.encode()
      else: chunk += f' {b:02X}'.encode()
      if offset == 15: chunk += b' ' * ioffset + b'  |' + side + b'|'; side = b''
      index += 1
      offset += 1

    if stream:
      self.state = (index, ioffset, offset, side)
      return chunk

    i = 16 - index % 16
    if i > 8: chunk += b' ' * (i * 3 + 1)
    else: chunk += b' ' * (i * 3)
    chunk += b' ' * ioffset + b'  |' + side + b'|'
    self.state = (index, 0, 16, b'')
    return chunk
  encode = transcode
