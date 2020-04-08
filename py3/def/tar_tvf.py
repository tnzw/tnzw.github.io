# tar_tvf.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

# Inspired by https://github.com/calccrypto/tar/blob/master/tar.c

def tar_tvf(file, **k):
  TYPE_REGULAR    =    0
  TYPE_NORMAL     = 0x30
  TYPE_HARDLINK   = 0x31
  TYPE_SYMLINK    = 0x32
  TYPE_CHAR       = 0x33
  TYPE_BLOCK      = 0x34
  TYPE_DIRECTORY  = 0x35
  TYPE_FIFO       = 0x36
  TYPE_CONTIGUOUS = 0x37
  sep = k.get("sep", " ")
  def format_for_print(name):
    try:
      return name.decode("UTF-8")
    except UnicodeDecodeError:
      return str(name)
  if isinstance(file, (str, bytes)):
    file = open(file, "rb")
  with file:
    for entry in tar_readmetadatablocks(file):
      s = ""
      if tar_calculate_checksum(entry) != entry.checksum:
        s += "/!\ invalid checksum" + sep
      mode_bytes = (
        ("-hlcbdp-"[entry.type - 0x30 if entry.type else 0:])[:1] +
        ("r" if entry.mode & 0o400 else "-") +
        ("w" if entry.mode & 0o200 else "-") +
        ("x" if entry.mode & 0o100 else "-") +
        ("r" if entry.mode & 0o040 else "-") +
        ("w" if entry.mode & 0o020 else "-") +
        ("x" if entry.mode & 0o010 else "-") +
        ("r" if entry.mode & 0o004 else "-") +
        ("w" if entry.mode & 0o002 else "-") +
        ("x" if entry.mode & 0o001 else "-")
      )
      s += "%s%s%s/%s%s" % (mode_bytes, sep, format_for_print(entry.owner) or entry.uid, format_for_print(entry.group) or entry.gid, sep)
      if entry.type in (TYPE_REGULAR, TYPE_NORMAL, TYPE_CONTIGUOUS,
                        TYPE_HARDLINK, TYPE_SYMLINK, TYPE_DIRECTORY, TYPE_FIFO):
        s += "%u" % (entry.size,)
      elif entry.type in (TYPE_CHAR, TYPE_BLOCK):
        s += "%d/%d" % (entry.major, entry.minor)
      else:
        s += "?"
      mtime = time.localtime(entry.mtime)
      s += "%s%d-%02d-%02d %02d:%02d%s" % (sep, mtime.tm_year, mtime.tm_mon, mtime.tm_mday, mtime.tm_hour, mtime.tm_min, sep)
      #s += "%s%d%s" % (sep, entry.mtime, sep)
      s += format_for_print(entry.name)
      if entry.type in (TYPE_HARDLINK,):
        s += sep + "link to " + format_for_print(entry.link_name)
      elif entry.type in (TYPE_SYMLINK,):
        s += sep + "-> " + format_for_print(entry.link_name)
      print(s, **k)
tar_tvf._required_globals = ["time", "tar_readmetadatablocks", "tar_calculate_checksum"]
