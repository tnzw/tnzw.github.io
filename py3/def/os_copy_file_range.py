# os_copy_file_range.py Version 1.0.1
# Copyright (c) 2020-2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_copy_file_range(src, dst, count, offset_src=None, offset_dst=None, *, os_module=None):
  """\
A polyfill of `os.copy_file_range()`.

Copy *count* bytes from file descriptor *src*, starting from offset
*offset_src*, to file descriptor *dst*, starting from offset *offset_dst*.
If *offset_src* is None, then *src* is read from the current position;
respectively for *offset_dst*.

In the original feature, the files pointed by *src* and *dst* must reside in the
same filesystem, otherwise an `OSError` is raised with `errno` set to
`errno.EXDEV`. However, in this polyfill, the copy is done by using
`os.lseek(src or dst, …)`, `os.read(src, …)` and `os.write(dst, …)`.

In the original feature, the copy is done as if both files are opened as binary.
However, in this polyfill, the file descriptors are taken as they were opened,
it may lead to inconsistencies.

The return value is the amount of bytes copied. This could be less than the
amount requested.

Original documentation:
https://docs.python.org/3/library/os.html#os.copy_file_range

More info:
https://lwn.net/Articles/659523/
"""
  # we should not use src/dst_os_module
  buffer_size = 32768  # XXX hardcoded
  if os_module is None: os_module = os
  if offset_src is None: offset_src = os_module.lseek(src, 0, os_module.SEEK_CUR)
  if offset_dst is None: offset_dst = os_module.lseek(dst, 0, os_module.SEEK_CUR)
  SEEK_SET = os_module.SEEK_SET
  copied = 0
  while count > 0:
    os_module.lseek(src, offset_src, SEEK_SET)
    d = os_module.read(src, min(buffer_size, count))
    dlen = len(d)
    if dlen == 0:
      if src == dst: os_module.lseek(dst, offset_dst, SEEK_SET)  # XXX is it necessary ?
      break
    count -= dlen
    offset_src += dlen
    written = 0
    while written < dlen:
      os_module.lseek(dst, offset_dst, SEEK_SET)
      w = os_module.write(dst, d[written:])
      if w == 0: XXX  # XXX what should we do here ?
      copied += w
      written += w
      offset_dst += w
  return copied
os_copy_file_range._required_globals = ["os"]
