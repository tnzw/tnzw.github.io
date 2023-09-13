# hashlib_crc32.py Version 1.1.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class hashlib_crc32:
  # same algorithm as zlib.crc32()
  name = 'crc32'
  digest_size = 4
  block_size = 1
  crc32table = None
  def __init__(self, iv=0):
    if iv < 0 or 0xFFFFFFFF < iv: raise ValueError('iv argument must be between 0 and 0xFFFFFFFF')
    self._sum = iv ^ 0xFFFFFFFF
    if self.crc32table is None:
      # make crc table
      crc32table = [0] * 256
      for n in range(256):
        c = n
        for k in range(8): c = 0xEDB88320 ^ (c >> 1) if c & 1 else c >> 1
        crc32table[n] = c
      hashlib_crc32.crc32table = tuple(crc32table)
  def update(self, data):
    crc = self._sum
    crc32table = self.crc32table
    for b in data:
      crc = (crc >> 8) ^ crc32table[(crc ^ b) & 0xFF]
    self._sum = crc & 0xFFFFFFFF
  def uint32digest(self):
    return self._sum ^ 0xFFFFFFFF
  def digest(self):
    uint32 = self.uint32digest()
    return bytes((uint32 & 0xFF, (uint32 >> 8) & 0xFF, (uint32 >> 16) & 0xFF, (uint32 >> 24) & 0xFF))  # little endian
  def hexdigest(self):
    return ''.join(f'{_:02x}' for _ in self.digest())
  def copy(self):
    o = hashlib_crc32()
    o._sum = self._sum
    return o
