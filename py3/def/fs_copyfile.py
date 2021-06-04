# fs_copyfile.py Version 2.0.2
# Copyright (c) 2019-2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def fs_copyfile():
  def fs_copyfile(*a, **k):
    """\
fs_copyfile(src, dst, flags, **opt) -> read, written
  src => as str or byte : path of the file to open, read and close
         as int         : file descriptor to read from
  dst => as str or byte : path of the file to open, write and close
         as int         : file descriptor to write into
  flags => 0b001 or EXCL          : do not overwrite dst file
           0b010 or FICLONE       : (NIY)
           0b100 or FICLONE_FORCE : (NIY)
  opt
    preserve_timestamps => 0 : if 1, copy src atime and mtime to dst
    preserve_mode => 0       : if 1: copy src mode to dst
    preserve_ownership => 0  : if 1: copy src uid and gid to dst
    src_os_module => None    : the module to use to act on src (defaults to os module)
                               requires os.open, os.O_RDONLY, os.O_BINARY, os.fstat, os.read, os.close
    dst_os_module => None    : the module to use to act on dst (defaults to os module)
                               requires os.open, os.O_WRONLY, os.O_CREATE, os.O_BINARY, os.EXCL, os.chmod, os.chown, os.write
    buffer_size => None      : Defaults to src stat.st_blksize (or 32Ki).
"""
    for read, written in fs_copyfile.iter(*a, **k): pass
    return read, written
  def iter(src, dst, flags=0, *,
           preserve_timestamps=False, preserve_mode=False, preserve_ownership=False,
           src_os_module=None, dst_os_module=None, buffer_size=None):
    """for read, written in fs_copyfile.iter(src, dst, flags, **opt): notify_progress(read, written)"""
    def checkbufsize(v):
      if isinstance(v, int) and v > 0: return v
      raise TypeError("invalid buffer size type")
    def noop(*a,**k): pass

    if src_os_module is None: src_os_module = os
    if dst_os_module is None: dst_os_module = os
    excl = dst_os_module.O_EXCL if flags & 1 else 0
    read, written = 0, 0

    close_src, in_fd = (False, src) if isinstance(src, int) else (True, src_os_module.open(src, src_os_module.O_RDONLY | getattr(src_os_module, "O_BINARY", 0)))  # acts like "rb"
    try:
      close_dst, out_fd = (False, dst) if isinstance(dst, int) else (True, dst_os_module.open(dst, dst_os_module.O_WRONLY | dst_os_module.O_CREAT | (excl or dst_os_module.O_TRUNC) | getattr(dst_os_module, "O_BINARY", 0)))  # acts like "wb" or "xb"
      try:
        stats = src_os_module.fstat(in_fd)

        if buffer_size is None or buffer_size < 0:
          buffer_size = 32768
          try: buffer_size = checkbufsize(stats.st_blksize)
          except (AttributeError, TypeError): pass

        if preserve_mode: dst_os_module.chmod(dst, stats.st_mode)  # XXX use fchmod ?
        if preserve_ownership: getattr(dst_os_module, "chown", noop)(dst, stats.st_uid, stats.st_gid)  # XXX use fchown ?

        data = src_os_module.read(in_fd, buffer_size)
        read += len(data)
        yield read, written
        while data:
          l = dst_os_module.write(out_fd, data)
          if l == 0:
            raise OSError(0, "Cannot write", dst)
          written += l
          yield read, written
          if l != len(data):
            data = data[l:]
          else:
            data = src_os_module.read(in_fd, buffer_size)
            read += len(data)
            yield read, written

      finally:
        if close_dst: dst_os_module.close(out_fd)
    finally:
      if close_src: src_os_module.close(in_fd)

    if preserve_timestamps: dst_os_module.utime(dst, (stats.st_atime, stats.st_mtime))

  fs_copyfile.iter = iter
  fs_copyfile.EXCL = 1
  fs_copyfile.FICLONE = 2
  fs_copyfile.FICLONE_FORCE = 4
  return fs_copyfile
fs_copyfile = fs_copyfile()
fs_copyfile._required_globals = ["os"]
