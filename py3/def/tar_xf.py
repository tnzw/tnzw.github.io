# tar_xf.py Version 0.1.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

# Inspired by https://github.com/calccrypto/tar/blob/master/tar.c

def tar_xf(file, directory=b".", same_owner=False, verbose=None, print_kw=None, buffer_size=None):
  """\
tar_xf(ARCHIVE, **OPTIONS)
  directory=DIR  change to directory DIR
  same_owner     try extracting file with the same ownership as
                 exists in the archive
  verbose        verbosely list files processed
  print_kw=DICT  given to each line print if verbose
  buffer_size=N  the max size of each read data chunk
"""
  TYPE_REGULAR    =    0
  TYPE_NORMAL     = 0x30
  TYPE_HARDLINK   = 0x31
  TYPE_SYMLINK    = 0x32
  TYPE_CHAR       = 0x33
  TYPE_BLOCK      = 0x34
  TYPE_DIRECTORY  = 0x35
  TYPE_FIFO       = 0x36
  TYPE_CONTIGUOUS = 0x37
  TYPE_LONGLINK   = 0x4c
  def count(iterable, value, count=0):
    for _ in iterable:
      if _ == value: count += 1
    return count
  def apply_attr(block, path):
    os.utime(path, (block.mtime, block.mtime))
    os.chmod(path, block.mode & 0o777)
    if same_owner and hasattr(os, "chown"):
      os.chown(path, block.uid, block.gid)
  deferred = []
  if isinstance(file, (str, bytes)):
    file = open(file, "rb")
  elif hasattr(file, "buffer"):
    file = file.buffer
  sep = os.fsencode(os.sep)
  directory = os.fsencode(directory)
  if not print_kw: print_kw = {}
  with file:
    long_link = None
    for type, value in tar_reader_itertokens(file, buffer_size=buffer_size):
      if type == "metadata_block":
        block = value
        name = block.name if long_link is None else long_link[:-1]
        path = os.path.normpath(b"/" + name).lstrip(sep)
        long_link = None
        sep_count = count(path, sep[0])
        path = os.path.join(directory, path)
        if tar_calculate_checksum(block) != block.checksum:
          raise ValueError("invalid checksum: %s" % (block.name,))
        if block.type == TYPE_LONGLINK:
          long_link = b""
        else:
          if verbose:
            print(os.fsdecode(name), **print_kw)
          if sep_count:
            err = fs_mkdir(os.path.dirname(path), parents=-sep_count + 1, exist_ok=True)
            if err: raise err
          if block.type == TYPE_DIRECTORY:
            err = fs_mkdir(path, exist_ok=True)
            if err: raise err
            deferred.append((apply_attr, block, path))
          elif block.type == TYPE_NORMAL:
            pass
          elif block.type == TYPE_HARDLINK:  # XXX what about long_link poiting to a long_link ?!?
            print(hex(block.type))
            XXX
          elif block.type == TYPE_SYMLINK:  # XXX what about long_link poiting to a long_link ?!?
            print(hex(block.type))
            XXX
          else:
            print(hex(block.type))
            XXX
      elif type == "data_chunk":
        if long_link is None:
          out.write(value)
        else:
          long_link += value
      elif type == "data_chunk_start":
        if long_link is None:
          out = open(path, "wb")
      elif type == "data_chunk_end":
        if long_link is None:
          out.close()
          apply_attr(block, path)
      elif type == "end_of_record":
        break
  for _ in deferred: _[0](*_[1:])
tar_tvf._required_globals = [
  "os",
  "tar_reader_itertokens",
  "fs_mkdir",
  "tar_calculate_checksum",
]
