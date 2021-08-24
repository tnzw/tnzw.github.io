# ZipFile_write.py Version 1.0.1
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def ZipFile_write(self, filename, arcname=None, compress_type=None, compresslevel=None, allow_directory=None, os_module=None):
  # is like zipfile.ZipFile.write() method, but allow to set a different os module.
  # + allow_directory : if True allow to write a directory entry, else ignore dirs
  # XXX is not "iterable" -> do a ZipFile_write.iter() ?
  if os_module is None: os_module = os
  sep = os_module.sep
  filename = os_module.fspath(filename)
  if isinstance(filename, bytes): sep = os_module.fsencode(sep)
  if arcname is None:
    # by default, this will be the same as filename, but without a drive letter and with leading path separators removed
    d, p = os_module.path.splitdrive(filename)
    len_sep = len(sep)
    if len_sep:
      while p.endswith(sep): p = p[:-len_sep]
      if not p: p = sep
    arcname = p
  stats = os_module.stat(filename)
  if stat.S_ISDIR(stats.st_mode):
    if allow_directory:
      # XXX convert os_module paths to ZipInfo paths … ?
      zi = zipfile.ZipInfo(filename=os_module.fsdecode(arcname + sep), date_time=time.localtime(stats.st_mtime)[:6])
      return self.writestr(zi, "")
    else: return
  if stat.S_ISREG(stats.st_mode):
    # XXX convert os_module paths to ZipInfo paths … ?
    zi = zipfile.ZipInfo(filename=os_module.fsdecode(arcname), date_time=time.localtime(stats.st_mtime)[:6])
    zi.compress_type = self.compression if compress_type is None else compress_type
    with open2(filename, "rb", os_module=os_module) as f:
      # XXX arg f.read() consumes a lot of memory ><'
      return self.writestr(zi, f.read(), compress_type=compress_type, compresslevel=compresslevel)
  # ignore other formats
ZipFile_write._required_globals = ["os", "stat", "time", "zipfile", "open2"]
