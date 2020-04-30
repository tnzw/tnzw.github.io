# fs_move.py Version 1.0.5
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def fs_move(src, dst,
            preserve_timestamps=True, preserve_mode=True, preserve_ownership=True,
            auto_remove=True, clobber=True, force=False,
            buffer_size=None):
  """\
Moves src file tree to dst. If dst already exists, it attemps to overwrite only if clobber is set.
If src and dst are two directories, it merges the content of src to dst.

fs_move(src, dst, **opt) -> Error
  opt
    preserve_timestamps => True
    preserve_mode => True
    preserve_ownership => True
    auto_remove => True         : Do not remove source files if they are moved (copied) in another device.
    clobber => True             : Overwrite existing files.
    force => False              : Remove node before copying.
    buffer_size => None         : Used for copying files. Could be either an int or None.
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

  srcl = len(src)
  sep = os.sep
  if isinstance(src, bytes): sep = sep.encode("ascii")
  sepl = len(sep)

  def act(cur, curstat, new, newstat):
    if stat.S_ISLNK(curstat.st_mode):
      if newstat and not clobber: return None
      err, lnk = catch2(lambda: os.readlink(cur), syscall="readlink")
      if err: return err
      if not newstat or stat.S_ISREG(newstat.st_mode) or stat.S_ISLNK(newstat.st_mode):
        err = catch(lambda: os.rename(cur, new), syscall="rename")
        if not err: return None
        if err != errno.EXDEV: return err
        err = catch(lambda: os.unlink(new), syscall="unlink")
        if err: return err
        err = catch(lambda: os.symlink(lnk, new), syscall="symlink")
        if err: return err
      elif stat.S_ISDIR(newstat.st_mode):
        return mkerr(IsADirectoryError, errno.EISDIR, "cannot overwrite directory " + repr(new) + " with non-directory", filename=new)
      else:
        return NotImplementedError("unhandled node " + repr(new))
      if auto_remove: err = catch(lambda: os.unlink(cur), syscall="unlink")
      if err: return err
    elif stat.S_ISDIR(curstat.st_mode):
      if newstat and not clobber: return fs_iterdirsdiff(rec, [cur])
      if not newstat:
        err = catch(lambda: os.rename(cur, new), syscall="rename")
        if not err: return fs_iterdirsdiff(rec, [cur])
        if err != errno.EXDEV: return err
        err = catch(lambda: os.mkdir(new), syscall="mkdir")
        if err: return err
      elif not stat.S_ISDIR(newstat.st_mode):
        return mkerr(IsADirectoryError, errno.EISDIR, "cannot overwrite directory " + repr(new) + " with non-directory", filename=new)

      err = fs_iterdirsdiff(rec, [cur])
      if err: return err

      if not newstat:
        if preserve_timestamps:
          err = catch(lambda: os.utime(new, (curstat.st_atime, curstat.st_mtime)), syscall="utime")
          if err: return err
        if preserve_mode:
          err = catch(lambda: os.chmod(new, curstat.st_mode & 0o777), syscall="chmod")
          if err: return err
        if preserve_ownership:
          err = catch(lambda: getattr(os, "chown", lambda *a,**k: None)(new, curstat.st_uid, curstat.st_gid), syscall="chown")
          if err: return err
      if auto_remove: err = catch(lambda: os.rmdir(cur), syscall="rmdir")
      if err: return err
    elif stat.S_ISREG(curstat.st_mode):
      if newstat and not clobber: return None
      if not newstat or stat.S_ISLNK(newstat.st_mode) or stat.S_ISREG(newstat.st_mode):
        err = catch(lambda: os.rename(cur, new), syscall="rename")
        if not err: return None
        if err != errno.EXDEV: return err
        if stat.S_ISREG(newstat.st_mode) and force:
          # or should we use os.chmod(path, stat.S_IWRITE) ? -> remove file readonly flag
          err = catch(lambda: os.unlink(cur), syscall="unlink")
          if err: return err
        err = fs_copyfile(cur, new, preserve_timestamps=preserve_timestamps, preserve_mode=preserve_mode, preserve_ownership=preserve_ownership, buffer_size=buffer_size)
        if err: return err
      elif stat.S_ISDIR(newstat.st_mode):
        return mkerr(NotADirectoryError, errno.ENOTDIR, "cannot overwrite non-directory " + repr(new) + " with directory " + repr(cur), filename=new)
      else:
        return NotImplementedError("unhandled node " + repr(new))
      if auto_remove: err = catch(lambda: os.unlink(cur), syscall="unlink")
      if err: return err
    else:
      return NotImplementedError("unhandled node " + repr(cur))
    return None

  def rec(err, name, roots):
    if err: return err
    curdir, = roots
    com = (curdir+sep+name)[srcl+sepl:]
    cur, new = src+sep+com, dst+sep+com
    err, curstat = catch2(lambda: os.lstat(cur), syscall="lstat")
    if err: return err
    err, newstat = catch2(lambda: os.lstat(new), syscall="lstat")
    if err and err.errno == errno.ENOENT: err = None
    if err: return err
    return act(cur, curstat, new, newstat)

  err, srcstat = catch2(lambda: os.lstat(src), syscall="lstat")
  if err: return err
  err, dststat = catch2(lambda: os.lstat(dst), syscall="lstat")
  if err and err.errno == errno.ENOENT: err = None
  if err: return err
  return act(src, srcstat, dst, dststat)
fs_move._required_globals = ["errno", "os", "stat", "fs_iterdirsdiff"]
