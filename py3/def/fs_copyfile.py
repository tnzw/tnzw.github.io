# fs_copyfile.py Version 1.3.5
# Copyright (c) 2019-2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def fs_copyfile(src, dst, flags=0,
                preserve_timestamps=False, preserve_mode=False, preserve_ownership=False,
                buffer_size=None):
  """\
fs_copyfile(src, dst, [flags, [**opt...]]) -> Error
  flags 0b001 => EXCL
        0b010 => FICLONE (NIY)
        0b100 => FICLONE_FORCE (NIY)
  opt
    preserve_timestamps => 0
    preserve_mode => 0
    preserve_ownership => 0
    check_platform => 1
    buffer_size => None      : Defaults to src stat.st_blksize or
                               fs_copyfile.DEFAULT_BUFFER_SIZE or
                               DEFAULT_BUFFER_SIZE or
                               io.DEFAULT_BUFFER_SIZE or
                               32Ki.
"""
  def catch(fn, **k):
    try: fn()
    except OSError as e:
      for p,v in k.items(): setattr(e,p,v)
      return e
  def catch2(fn, *d, **k):
    try: return None, fn()
    except OSError as e:
      for p,v in k.items(): setattr(e,p,v)
      return e, d[0] if d else None
  def mkerr(E, *a, **k):
    e = E(*a)
    for p,v in k.items(): setattr(e,p,v)
    return e
  def getbufsize(v):
    if isinstance(v, int) and v > 0: return v
    raise TypeError("invalid buffer size")

  excl = "x" if flags & 1 else ""

  err, in_f = catch2(lambda: open(src, "rb"), syscall="open")
  if err: return err
  in_fd = in_f.fileno()

  try:
    err, out_f = catch2(lambda: open(dst, "wb" + excl), syscall="open")
    if err: return err
    out_fd = out_f.fileno()
    try:
      err, stats = catch2(lambda: os.fstat(in_fd), syscall="fstat")
      if err: return err

      if buffer_size is None:
        buffer_size = 32 * 1024
        try: buffer_size = getbufsize(stats.st_blksize)
        except (AttributeError, TypeError):
          try: buffer_size = getbufsize(fs_copyfile.DEFAULT_BUFFER_SIZE)
          except (AttributeError, TypeError):
            try: buffer_size = getbufsize(DEFAULT_BUFFER_SIZE)
            except (NameError, TypeError):
              try: buffer_size = getbufsize(io.DEFAULT_BUFFER_SIZE)
              except (NameError, AttributeError, TypeError): pass

      if preserve_mode:
        err = catch(lambda: os.chmod(dst, stats.st_mode), syscall="chmod")
        if err: return err
      if preserve_ownership:
        err = catch(lambda: getattr(os, "chown", lambda *a,**k: None)(dst, stats.st_uid, stats.st_gid), syscall="chown")
        if err: return err

      data = os.read(in_fd, buffer_size)
      while data:
        l = os.write(out_fd, data)
        if l == 0:
          return mkerr(OSError, 0, "Cannot write", filename=dst)
        if l != len(data):
          data = data[l:]
        else:
          data = os.read(in_fd, buffer_size)
    finally:
      catch(lambda: out_f.close(), syscall="close")  # XXX warn!
  finally:
    catch(lambda: in_f.close(), syscall="close")  # XXX warn!

  if data: return mkerr(OSError, 0, "Cannot write", filename=dst)

  if preserve_ownership:
    err = catch(lambda: os.utime(dst, (stats.st_atime, stats.st_mtime)), syscall="utime")
    if err: return err
  return None

fs_copyfile.EXCL = 1
fs_copyfile.FICLONE = 2
fs_copyfile.FICLONE_FORCE = 4
fs_copyfile._required_globals = ["os"]
