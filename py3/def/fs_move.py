# fs_move.py Version 2.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def fs_move(src, dst,
            preserve_timestamps=True, preserve_mode=True, preserve_ownership=True,
            auto_remove=True, clobber=True, force=False,
            src_os_module=None, dst_os_module=None, buffer_size=None):
  """\
Moves src file tree to dst. If dst already exists, it attemps to overwrite only if clobber is set.
If src and dst are two directories, it merges the content of src to dst.

fs_move(src, dst, **opt)
  opt
    preserve_timestamps => True
    preserve_mode => True
    preserve_ownership => True
    auto_remove => True         : Do not remove source files if they are moved (copied) in another device.
    clobber => True             : Overwrite existing files.
    force => False              : Remove node before copying.
    src_os_module => None       : the module to use to act on src (defaults to os module)
                                  requires os.sep, os.fsencode, os.readlink, os.rename, os.unlink, os.rmdir, os.lstat + fs_copyfile requirements
    dst_os_module => None       : the module to use to act on dst (defaults to os module)
                                  requires os.unlink, os.symlink, os.mkdir, os.utime, os.chmod, os.chown, os.lstat + fs_copyfile requirements
    buffer_size => None         : Used for copying files. Could be either an int or None.
"""
  if src_os_module is None: src_os_module = os
  if dst_os_module is None: dst_os_module = os

  srcl = len(src)
  srcsep = src_os_module.sep
  dstsep = dst_os_module.sep
  if isinstance(src, bytes): srcsep = src_os_module.fsencode(srcsep)
  if isinstance(dst, bytes): dstsep = src_os_module.fsencode(dstsep)
  srcsepl = len(srcsep)

  def rec(curdir):
    for name in src_os_module.listdir(curdir):
      com = (curdir+srcsep+name)[srcl+srcsepl:]
      cur, new = src+srcsep+com, dst+dstsep+com
      curstat = src_os_module.lstat(cur)
      newstat = None
      try: newstat = dst_os_module.lstat(new)
      except FileNotFoundError: pass
      except OSError: raise
      act(cur, curstat, new, newstat)

  def act(cur, curstat, new, newstat):
    if stat.S_ISLNK(curstat.st_mode):
      if newstat and not clobber: return
      lnk = src_os_module.readlink(cur)
      if not newstat or stat.S_ISREG(newstat.st_mode) or stat.S_ISLNK(newstat.st_mode):
        try: src_os_module.rename(cur, new)
        except OSError as err:
          if err.errno != errno.EXDEV: raise
        else: return
        dst_os_module.unlink(new)
        dst_os_module.symlink(lnk, new)
      elif stat.S_ISDIR(newstat.st_mode):
        raise IsADirectoryError(errno.EISDIR, "cannot overwrite directory " + repr(new) + " with non-directory", new)
      else:
        raise NotImplementedError("unhandled node " + repr(new))
      if auto_remove: src_os_module.unlink(cur)
    elif stat.S_ISDIR(curstat.st_mode):
      if newstat and not clobber: return rec(cur)
      if not newstat:
        try: src_os_module.rename(cur, new)
        except OSError as err:
          if err.errno != errno.EXDEV: raise
        else: return rec(cur)
        dst_os_module.mkdir(new)
      elif not stat.S_ISDIR(newstat.st_mode):
        raise IsADirectoryError(errno.EISDIR, "cannot overwrite directory " + repr(new) + " with non-directory", new)

      rec(cur)

      if not newstat:
        if preserve_timestamps: dst_os_module.utime(new, (curstat.st_atime, curstat.st_mtime))
        if preserve_mode: dst_os_module.chmod(new, curstat.st_mode & 0o777)
        if preserve_ownership: dst_os_module.chown(new, curstat.st_uid, curstat.st_gid)
      if auto_remove: src_os_module.rmdir(cur)
    elif stat.S_ISREG(curstat.st_mode):
      if newstat and not clobber: return
      if not newstat or stat.S_ISLNK(newstat.st_mode) or stat.S_ISREG(newstat.st_mode):
        try: src_os_module.rename(cur, new)
        except OSError as err:
          if err.errno != errno.EXDEV: raise
        else: return
        if stat.S_ISREG(newstat.st_mode) and force:
          # or should we use os.chmod(path, stat.S_IWRITE) ? -> remove file readonly flag
          src_os_module.unlink(cur)
        fs_copyfile(cur, new, preserve_timestamps=preserve_timestamps, preserve_mode=preserve_mode, preserve_ownership=preserve_ownership, buffer_size=buffer_size, src_os_module=src_os_module, dst_os_module=dst_os_module)
      elif stat.S_ISDIR(newstat.st_mode):
        raise NotADirectoryError(errno.ENOTDIR, "cannot overwrite non-directory " + repr(new) + " with directory " + repr(cur), new)
      else:
        raise NotImplementedError("unhandled node " + repr(new))
      if auto_remove: src_os_module.unlink(cur)
    else:
      raise NotImplementedError("unhandled node " + repr(cur))

  srcstat = src_os_module.lstat(src)
  dststat = None
  try: dststat = dst_os_module.lstat(dst)
  except OSError as err:
    if err.errno != errno.ENOENT: raise
  act(src, srcstat, dst, dststat)
fs_move._required_globals = ["errno", "os", "stat", "fs_copyfile"]
