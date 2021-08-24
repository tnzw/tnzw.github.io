# ziptree.py Version 1.1.1
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def ziptree():
  def ziptree(src, dst, *, prefix=None, source_directory=None, src_os_module=None, dst_os_module=None, os_module=None):
    """\
Create a zip file or fill a file-like object.

Defaults:
  Follows symlinks.
  Only dirs and files are archived, other types are ignored.
  `compression=zipfile.ZIP_DEFLATED` is used.
  Empty directories are stored.
  Opens dst using mode="wb"

`src` is the path to file/folder to compress so that compressing `/hello` would
produce an archive with at least one entry -> `hello` (not `/hello`).
If `src` basename is empty or "." or "..", then source_directory is implied.

`dst` could be a path-like object or a file-like object that would contain the
produced zip file.

`prefix` is the common prefix of all files and directories in the archive.
E.g. prefix="hey" -> os.path.join(prefix, "hello") -> "hey/hello"

`source_directory` allow to compress `src` files without adding `src` folder
itself.
"""
    if src_os_module is None: src_os_module = os_module
    if dst_os_module is None: dst_os_module = os_module
    dstc = None
    try:
      try: dst = (os if dst_os_module is None else dst_os_module).fspath(dst)
      except TypeError: pass
      else:
        dstc = open2(dst, "wb", os_module=dst_os_module)
        dst = dstc
      for chunk in ziptree_iter(src, prefix=prefix, source_directory=source_directory, os_module=src_os_module):
        dst.write(chunk)
    finally:
      if dstc is not None: dstc.close()

  def ziptree_iter(path, *, prefix=None, source_directory=None, os_module=None):
    def is_folder_empty(path):
      it = None
      try:
        it = os_module.scandir(path)
        try: next(it)
        except StopIteration: return True
        return False
      finally:
        if it is not None: it.close()
    def ZipFile_write(self, filename, arcname=None, compress_type=None, compresslevel=None, allow_directory=None):#, os_module=None):  # XXX is not "iterable" -> ZipFile_write.iter()
      #if os_module is None: os_module = os
      #sep = os_module.sep
      #if isinstance(os_module.fspath(filename), bytes): sep = os_module.fsencode(sep)
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
        with open2(filename, "rb", os_module=os_module) as f:
          # XXX arg f.read() consumes a lot of memory ><'
          return self.writestr(zi, f.read(), compress_type=compress_type, compresslevel=compresslevel)
    if os_module is None: os_module = os
    path = os_module.fspath(path)
    sep = os_module.sep  # for ZipFile_write()
    curdir = os_module.curdir
    pardir = os_module.pardir
    if isinstance(path, bytes):
      sep = os_module.fsencode(sep)
      curdir = os_module.fsencode(curdir)
      pardir = os_module.fsencode(pardir)
    written = []
    def write(chunk):
      written.append(chunk)
      return len(chunk)
    def tmp(): pass
    tmp.write = write
    tmp.flush = lambda: None
    def __iter__():
      with zipfile.ZipFile(tmp, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=-1) as z:
        if source_directory:
          offset = len(path) + len(sep)
        else:
          base = os_module.path.basename(path)
          if base in (pardir, curdir): offset = len(path) + len(sep)
          elif not base: offset = len(path)
          else:
            offset = len(path) - len(base)
            ZipFile_write(z, base)
            if written: yield b"".join(written); written[:] = []
        for root, dirs, files in os_module.walk(path):
          nroot = root[offset:]
          for entry in dirs:
            filename = os_module.path.join(root, entry)
            if is_folder_empty(filename):
              arcname = (entry,)
              if nroot: arcname = (nroot,) + arcname
              if prefix: arcname = (prefix,) + arcname
              arcname = os_module.path.join(*arcname)
              # XXX convert os_module paths to ZipFile paths … ?
              ZipFile_write(z, filename, arcname=arcname, allow_directory=True)#, os_module=os_module)
              if written: yield b"".join(written); written[:] = []
          for entry in files:
            arcname = (entry,)
            if nroot: arcname = (nroot,) + arcname
            if prefix: arcname = (prefix,) + arcname
            arcname = os_module.path.join(*arcname)
            # XXX convert os_module paths to ZipFile paths … ?
            ZipFile_write(z, os_module.path.join(root, entry), arcname=arcname)#, os_module=os_module)
            if written: yield b"".join(written); written[:] = []
      if written: yield b"".join(written); written[:] = []
    return __iter__()

  ziptree.iter = ziptree_iter
  return ziptree
ziptree = ziptree()
ziptree._required_globals = ["os", "stat", "time", "zipfile", "open2"]
