# tar_MetadataBlock.py Version 1.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

# Inspired by https://github.com/calccrypto/tar/blob/master/tar.c

class tar_MetadataBlock(bytearray):
  """\
block = tar_MetadataBlock(file.read(512))
"""
  def __init__(self, *v):
    if len(v) == 0:
      self[:] = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x000000000\x000000000\x000000000\x0000000000000\x0000000000000\x00007077\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00ustar\x0000\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x000000000\x000000000\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    else:
      self[:] = bytearray(*v)
      if len(self) != 512:
        raise ValueError("invalid length (!= 512)")
  # Pre-POSIX.1-1988 format
  @property
  def name(self): return self._cstr_tobytes(self[0:100])
  @name.setter
  def name(self, value): self[0:100] = self._cstr_pad(value, 100)
  @property
  def mode(self): return int(self[100:107], 8)
  @mode.setter
  def mode(self, value): self[100:108] = self._cstr_pad(b"%07o" % (value,), 7) + b"\x00"
  @property
  def uid(self): return int(self[108:115], 8)
  @uid.setter
  def uid(self, value): self[108:116] = self._cstr_pad(b"%07o" % (value,), 7) + b"\x00"
  @property
  def gid(self): return int(self[116:123], 8)
  @gid.setter
  def gid(self, value): self[116:124] = self._cstr_pad(b"%07o" % (value,), 7) + b"\x00"
  @property
  def size(self): return int(self[124:135], 8)
  @size.setter
  def size(self, value): self[124:136] = self._cstr_pad(b"%011o" % (value,), 11) + b"\x00"
  @property
  def mtime(self): return int(self[136:147], 8)
  @mtime.setter
  def mtime(self, value): self[136:148] = self._cstr_pad(b"%011o" % (value,), 11) + b"\x00"
  @property
  def checksum(self): return int(self[148:154], 8)
  @checksum.setter
  def checksum(self, value): self[148:156] = self._cstr_pad(b"%06o" % (value,), 6) + b"\x00 "
  # both format
  @property
  def link(self): return self[156]
  @link.setter
  def link(self, value): self[156] = value
  @property
  def type(self): return self.link
  @type.setter
  def type(self, value): self.link = value
  @property
  def link_name(self): return self._cstr_tobytes(self[157:257])
  @link_name.setter
  def link_name(self, value): self[157:257] = self._cstr_pad(value, 100)
  # UStar format (POSIX IEEE P1003.1)
  @property
  def ustar(self): return bytes(self[257:265])
  @ustar.setter
  def ustar(self, value): self[257:265] = (value + b"\x00"*8)[:8]
  @property
  def owner(self): return self._cstr_tobytes(self[265:297])
  @owner.setter
  def owner(self, value): self[265:297] = self._cstr_pad(value, 32)
  @property
  def group(self): return self._cstr_tobytes(self[297:329])
  @group.setter
  def group(self, value): self[297:329] = self._cstr_pad(value, 32)
  @property
  def major(self): return int(self[329:336], 8)
  @major.setter
  def major(self, value): self[329:337] = self._cstr_pad(b"%07o" % (value,), 7) + b"\x00"
  @property
  def minor(self): return int(self[337:344], 8)
  @minor.setter
  def minor(self, value): self[337:345] = self._cstr_pad(b"%07o" % (value,), 7) + b"\x00"
  @property
  def prefix(self): return self._cstr_tobytes(self[345:500])
  @prefix.setter
  def prefix(self, value): self[345:500] = self._cstr_pad(value, 155)
  @property
  def extra(self): return bytes(self[500:512])
  @extra.setter
  def extra(self, value): self[500:512] = (value + b"\x00"*12)[:12]
  def tobytes(self): return bytes(self)
  @staticmethod
  def frombytes(bytes): return tar_MetadataBlock(bytes)
  def copy(self): return tar_MetadataBlock(self)
  def _cstr_tobytes(self, cstr):
    cstr = bytes(cstr)
    i = cstr.find(b"\x00")
    if i == -1:
      return cstr
    return cstr[:i]
  def _cstr_pad(self, cstr, length):
    cstr = self.cstr_to_bytes(cstr)
    if len(cstr) > length:  # `tar` behavior. `7z` behavior would be with a >=
      raise ValueError("too long")
    return (cstr + b"\x00" * length)[:length]
