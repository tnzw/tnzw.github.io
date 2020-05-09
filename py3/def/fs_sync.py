# fs_sync.py Version 1.2.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def fs_sync():
  def fs_sync(src, dst, source_directory=None, target_directory=None, verbose=None, onverbose=None, content=None, head=None, archive=None, recursive=None, backup=None, backup_dir=None, suffix=None, update=None, dirs=None, links=None, perms=None, executability=None, chmod=None, owner=None, group=None, times=None, omit_dir_times=None, omit_link_times=None, dry_run=None, existing=None, ignore_existing=None, remove_source_files=None, remove_source_dirs=None, delete=None, force=None, chown=None, size_only=None, modify_window=None, exclude=None, include=None, ignore_errors=None, ignore_backup_delete_errors=None, ignore_listdir_errors=None, onerror=None, buffer_size=None, as_func=None):
    """\
fs_sync(src, dst, **opt)

  Synchronizes src as dst to make src and dst similar.
  Unlike rsync, dst is NOT a target directory by default.
  There is no protection preventing sync in cross file trees!
  This fonction is inspired by `man rsync`.

  opt  (all options are None by default)
    source_directory     synchronize src inner content to dst, implies target_directory (equiv: rsync src/ dst/)
    target_directory     synchronize src inside dst directory (equiv: rsync src dst)

    verbose              verbosity level
    onverbose            calls onverbose(action_name, common_path) before starting action
                         action_name could be "create", "update" or "delete"
                         the arguments varies according to verbose level

    content              skip based on content, not mod-time & size
    head=INT             compare files content first bytes
    archive              archive mode; equals recursive = links = perms = times = group = owner = True
    recursive            recurse into directories
    backup               make backups (see suffix & backup_dir)
                         backup files are overwritten
    backup_dir=PATH      make backups into hierarchy based in backup_dir
                         behavior is different from original rsync --backup-dir (where --backup-dir=bak points to dst+"/bak")
                         here, backup_dir points to an external dir
    suffix=SUFFIX        backup suffix (default ~ w/o backup_dir)
    update               skip files that are newer on the receiver
    dirs                 transfer directories without recursing
    links                copy symlinks as symlinks XXX SHOULD ALWAYS BE TRUE FOR THE MOMENT
    perms                preserve permissions
    executability        preserve executability
    chmod=MODE           affect file and/or directory permissions
    owner                preserve owner (no effect on windows)
    group                preserve group (no effect on windows)
    times                preserve modification times
    omit_dir_times       omit directories from times
    omit_link_times      omit symlinks from times XXX always set to true for now
    dry_run              perform a trial run with no changes made
    existing             skip creating new files on receiver
    ignore_existing      skip updating files that exist on receiver
    remove_source_files  sender removes synchronized files (non-dir)
    remove_source_dirs   sender removes synchronized dirs
    delete               delete extraneous files from dest dirs
    force                force deletion of dirs even if not empty (useless for the moment)
    chown=(UID,GID)      affect file and directory username and groupname (no effect on windows)
    size_only            skip files that match in size
    modify_window=NUM    compare mod-times with reduced accuracy
    exclude=FUNC         exclude files if FUNC(common_path) returns True
    include=FUNC         don't exclude files if FUNC(common_path) returns True
    buffer_size          used for copying file. Could be either an int or None.

    ignore_errors                ignores failures during a node synchronisation, allowing to continue to next node
    ignore_backup_delete_errors  ignores failures during a backup of node that should be removed by the delete option
    ignore_listdir_errors        ignores failures during the walk in the file tree
    onerror                      calls onerror(func, arg, exc_info) on error if not ignore_errors
                                 you can retry the process by calling func(arg)
                                 or you can propagate the active exception by using raise

fs_sync.merge(src, dst, **kw)
  equiv fs_sync with archive=True

fs_sync.mirror(src, dst, **kw)
  equiv fs_sync with archive=True, delete=True

fs_sync.clean(src, dst, **kw)
  equiv fs_sync with recursive=True, delete=True, existing=True, ignore_existing=True

fs_sync.remove(dst)
  equiv fs_sync with remove_source_files=True, remove_source_dirs=True
"""
    if source_directory:
      if target_directory is None: target_directory = True
      elif not target_directory: raise ValueError("target_directory=False conflicts with source_directory=True")
    if archive:
      if recursive is None: recursive = True
      if links     is None: links     = True
      if perms     is None: perms     = True
      if times     is None: times     = True
      if group     is None: group     = True
      if owner     is None: owner     = True
    if backup_dir:
      if backup is None: backup = True
      if suffix is None: suffix = ""
    else:
      if suffix is None: suffix = "~"
      elif not suffix: raise ValueError("suffix must not be empty")
    #if omit_link_times: XXX ignore this option for the moment
    omit_link_times = True
    if chown is not None:
      chown_uid, chown_gid = chown
    if exclude is None:
      exclude = lambda _: False
    if include is None:
      include = lambda _: False
    if not isinstance(verbose, int):
      verbose = 1 if verbose else 0
    if verbose and onverbose is None:
      def onverbose(*a): print(": ".join(os.fsdecode(_) for _ in a))
    if ignore_backup_delete_errors is None:
      ignore_backup_delete_errors = True

    user_check = True if size_only or update or content else False

    def mkerr(E,*a,**k):
      e = E(*a)
      for p,v in k.items(): setattr(e,p,v)
      return e
    def iter_sum(iterable):
      i, p = False, None
      for _ in iterable:
        if i: p += _
        else: p, i = _, True
        yield p

    def lstat(a):     return os.lstat(a)
    def readlink(a):  return os.readlink(a)
    def openrb(a):    return open(a, "rb")
    def symlink(*a):  return None if dry_run else os.symlink(*a)
    def utime(*a):    return None if dry_run else os.utime(*a)
    def _chmod(*a):   return None if dry_run else os.chmod(*a)
    if hasattr(os, "chown"):
      def _chown(*a): return None if dry_run else os.chown(*a)
    else:
      def _chown(*a): return None
    def mkdir(a):     return None if dry_run else os.mkdir(a)
    def rename(*a):   return None if dry_run else os.rename(*a)
    def unlink(a):    return None if dry_run else os.unlink(a)
    def rmdir(a):     return None if dry_run else os.rmdir(a)
    def _sync(*a):    return None if dry_run else fs_sync(*a, archive=True, buffer_size=buffer_size)
    def rm(a,s):      return rmdir(a) if stat.S_ISDIR(s.st_mode) else unlink(a)
    def mv(*a):
      err = fs_move(*a, buffer_size=buffer_size)  # XXX fs_move needs to be reforged ?
      if err: raise err
    def copyfile(*a,**k):
      err = fs_copyfile(*a, buffer_size=buffer_size)  # XXX fs_copyfile needs to be reforged ?
      if err: raise err

    def copystat(dst, src_stats, dst_stats=None):
      # rsync copies the stats in any cases, without doing backup
      # does not update times of update is True and dst >= src
      if chmod:
        if (not dst_stats or (chmod & 0o777) != (dst_stats.st_mode & 0o777)):
          _chmod(dst, chmod & 0o777)
      elif perms:
        if (not dst_stats or (src_stats.st_mode & 0o777) != (dst_stats.st_mode & 0o777)):
          _chmod(dst, src_stats.st_mode & 0o777)
      elif executability:
        if (not dst_stats or (src_stats.st_mode & 0o444) != (dst_stats.st_mode & 0o444)):
          _chmod(dst, (src_stats.st_mode & 0o444) | (dst_stats.st_mode & 0o333))
      if hasattr(os, "chown"):
        if chown:
          if not dst_stats or (chown_uid >= 0 and chown_uid != dst_stats.st_uid) or (chown_gid >= 0 and chown_gid != dst_stats.st_gid):
            _chown(dst, chown_uid, chown_gid)
        elif (owner and (not dst_stats or src_stats.st_uid != dst_stats.st_uid)) or \
             (group and (not dst_stats or src_stats.st_gid != dst_stats.st_gid)):
          _chown(dst, src_stats.st_uid if owner else -1, src_stats.st_gid if group else -1)
      if times:
        if omit_dir_times and stat.S_ISDIR(src_stats.st_mode): pass
        else:
          diff = supmodifywindow if update else diffmodifywindow
          if (not dst_stats or diff(src_stats.st_mtime, dst_stats.st_mtime)):
            utime(dst, (src_stats.st_atime, src_stats.st_mtime))

    def dobackup(dst, backup_dir, bakname, copy=False):
      # XXX what if backing up (rename) an hardlinked file ?
      if backup_dir:
        for _ in iter_sum(sep+_ for _ in os_path_splitall(bakname)[:-1]):  # create parent dirs
          try: mkdir(backup_dir + _)
          except FileExistsError: pass
        bak = backup_dir + sep + bakname
        if copy: return _sync(dst, bak)
        return mv(dst, bak)
      else:
        # rsync behavior rmdir(dst+suffix) before rename (even with --force), if fails, print warning and ignore
        if copy: return _sync(dst, dst + suffix)
        return rename(dst, dst + suffix)
      return None

    def diffmodifywindow(i, j):
      if modify_window is None: return i != j  # use int() ?
      return i + modify_window < j - modify_window or i - modify_window > j + modify_window

    def supmodifywindow(i, j):
      if modify_window is None: return i > j
      return i - modify_window > j + modify_window

    def file_diff(src, dst, length=None):
      with openrb(src) as src_f:
        with openrb(dst) as dst_f:
          equal = io_diff(src_f, dst_f, length=length)
          if equal: return 0
      return 1

    def difflink(src_link, dst):
      return src_link != readlink(dst)

    def diffdir(src_stats, dst_stats):
      if update:
        if supmodifywindow(src_stats.st_mtime, dst_stats.st_mtime): return 1
        return 0
      if diffmodifywindow(src_stats.st_mtime, dst_stats.st_mtime): return 1
      return 0

    def difffilecontent(src, dst, src_stats, dst_stats):
      # user checks
      if user_check:
        if update:
          if supmodifywindow(src_stats.st_mtime, dst_stats.st_mtime): return 1
        if size_only:
          if src_stats.st_size != dst_stats.st_size: return 1
        if content:
          diff = file_diff(src, dst, length=None if head is None or head < 0 else head)
          if diff: return 1
        return 0

      # rsync "quick check" is check mod-time & size
      if src_stats.st_size != dst_stats.st_size: return 1
      if diffmodifywindow(src_stats.st_mtime, dst_stats.st_mtime): return 1

      # additional checks
      if head is not None:
        diff = file_diff(src, dst, length=None if head < 0 else head)
        if diff: return 1

      # XXX add options for additional checks ? mode ? owner ? group ?
      #if src_stats.st_mode != dst_stats.st_mode: return None, 1
      #if src_stats.st_uid != dst_stats.st_uid: return None, 1
      #if src_stats.st_gid != dst_stats.st_gid: return None, 1
      return 0

    def rec(err, name, roots):
      if err:
        if ignore_listdir_errors: return
        raise
      srcdir, dstdir = roots
      comdir = srcdir[srcl:] if srcdir else dstdir[dstl:]
      com = comdir + sep + name if comdir else name
      arg = ((srcroot, com), (dstroot, com), (backup_dir, com))
      try: return sync(arg)
      except OSError:
        if ignore_errors: return
        if onerror is not None:
          onerror(sync, arg, sys.exc_info())
          return
        raise

    def sync(pathsplits):
      """sync((("src/root", "common/path"), ("dst/root", "common/path"), ("backup/root", "common/path"))"""
      ((srcroot, srcname), (dstroot, dstname), (backup_dir, bakname)) = pathsplits
      src = sep.join(_ for _ in (srcroot, srcname) if _) or None
      dst = sep.join(_ for _ in (dstroot, dstname) if _) or None

      def rec(err, name, roots):
        if err:
          if ignore_listdir_errors: return
          raise
        arg = ((srcroot, srcname + sep + name), (dstroot, dstname + sep + name), (backup_dir, bakname + sep + name))
        try: return sync(arg)
        except OSError:
          if ignore_errors: return
          if onerror is not None:
            onerror(sync, arg, sys.exc_info())
            return
          raise

      if exclude(srcname):
        if not include(srcname):
          return None

      try: src_stats = lstat(src)
      except FileNotFoundError: src_stats = None

      if src_stats:
        try: dst_stats = lstat(dst)
        except FileNotFoundError: dst_stats = None
        _existing = existing
        _progressed = 0
        if dst_stats:  # backup/delete file for update
          if not ignore_existing:
            if (src_stats.st_mode & 0xF000) != (dst_stats.st_mode & 0xF000):
              if verbose > 0: _progressed, _ = 1, onverbose("update", dstname)
              # src and dst exist but are different type
              if delete and stat.S_ISDIR(dst_stats.st_mode): fs_iterdirsdiff(rec, [None, dst])
              if backup: dobackup(dst, backup_dir, bakname)
              else:
                try: rm(dst, dst_stats)
                except OSError as err:
                  if err.errno != errno.ENOTEMPTY: raise
                  if not force: raise
                  remove(dst, recursive=True)  # no event handling (progress/error)…?
              dst_stats = None
              _existing = False
        if not dst_stats:  # creating new file
          if _existing: return
          if verbose > 0:
            if not _progressed: onverbose("create", dstname)
          if stat.S_ISLNK(src_stats.st_mode):
            if not links: XXX  # link dereference not implemented !
            link = readlink(src)
            # XXX if dereference link then becareful of unsafe links !
            symlink(link, dst)
            # copy_stat does not work on many OSes
            if remove_source_files: unlink(src)
          elif stat.S_ISREG(src_stats.st_mode):
            copyfile(src, dst)
            copystat(dst, src_stats)
            if remove_source_files: unlink(src)
          elif stat.S_ISDIR(src_stats.st_mode):
            if recursive or dirs:
              mkdir(dst)
              if recursive: fs_iterdirsdiff(rec, [src, None])
              copystat(dst, src_stats)
            else:
              pass  # skip directories
            if remove_source_dirs: rmdir(src)
          else:
            XXX  # unhandled node type
        else:  # updating file
          # dst is always same type as src here
          if stat.S_ISLNK(src_stats.st_mode):
            if not ignore_existing:
              if not links: XXX  # link dereference not implemented !
              link = readlink(src)
              if difflink(link, dst):
                if verbose > 0:
                  onverbose("update", dstname)
                if backup: dobackup(dst, backup_dir, bakname)
                else: unlink(dst)
                # XXX if dereference link then becareful of unsafe links !
                symlink(link, dst)
                # copy_stat does not work on many OSes
              if remove_source_files: unlink(src)
          elif stat.S_ISREG(src_stats.st_mode):
            if not ignore_existing:
              if difffilecontent(src, dst, src_stats, dst_stats):
                if verbose > 0:
                  onverbose("update", dstname)
                if backup: dobackup(dst, backup_dir, bakname)
                copyfile(src, dst)
              copystat(dst, src_stats, dst_stats)
              if remove_source_files: unlink(src)
          elif stat.S_ISDIR(src_stats.st_mode):
            if recursive or dirs:
              if diffdir(src_stats, dst_stats):
                if not ignore_existing:
                  if verbose > 0:
                    onverbose("update", dstname)
              if recursive:
                fs_iterdirsdiff(rec, [src, dst])
                if not ignore_existing:
                  if backup: dst_stats = lstat(dst)  # a backup may change the directory stats
              if not ignore_existing:
                copystat(dst, src_stats, dst_stats)
            else:
              pass  # skip directories
            if not ignore_existing:
              if remove_source_dirs: rmdir(src)
          else:
            if not ignore_existing:
              XXX  # unhandled node type
      else:  # deleting file
        dst_stats = lstat(dst)  # dst should always exists here
        # ignore_existing has no effect here
        if delete:  # XXX man rsync says: If the sending side detects any I/O errors, then the deletion of any files at the destination  will  be automatically  disabled
          if stat.S_ISDIR(dst_stats.st_mode): fs_iterdirsdiff(rec, [None, dst])
          if verbose > 0:
            onverbose("delete", dstname)  # XXX before/after fs_iterdirsdiff ?
          if backup_dir or not dst.endswith(suffix):
            if backup:
              try: dobackup(dst, backup_dir, bakname)
              except OSError:
                if ignore_backup_delete_errors: return
                raise
            else: rm(dst, dst_stats)

    if as_func:
      return sync

    sep = os.sep
    if isinstance(src, bytes):
      sep = bytes(sep, "ascii")
      if not isinstance(suffix, bytes): suffix = bytes(suffix, "ascii")
      #dot = b"."
    #else: dot = "."

    if source_directory:  # implies target_directory
      srcroot, dstroot = src, dst
      srcl, dstl = len(srcroot), len(dstroot)
      if srcl: srcl += len(sep)
      if dstl: dstl += len(sep)
      if not os.path.isdir(src):
        if ignore_listdir_errors: return
        raise mkerr(NotADirectoryError, errno.ENOTDIR, "not a directory", filename=src)
      return fs_iterdirsdiff(rec, [src, dst])

    if target_directory:
      srcroot, srcname = os.path.split(src)
      return sync(((srcroot, srcname), (dst, srcname), (backup_dir, srcname)))

    srcroot, srcname = os.path.split(src)
    dstroot, dstname = os.path.split(dst)
    return sync(((srcroot, srcname), (dstroot, dstname), (backup_dir, dstname)))

  def merge(src, dst, **k):
    kw = {"archive": True}
    kw.update(k)
    return fs_sync(src, dst, **kw)

  def mirror(src, dst, **k):
    kw = {"archive": True, "delete": True}
    kw.update(k)
    return fs_sync(src, dst, **kw)

  def clean(src, dst, **k):
    kw = {"recursive": True, "delete": True, "existing": True, "ignore_existing": True}
    kw.update(k)
    return fs_sync(src, dst, **kw)

  def remove(dst, **k):
    kw = {"remove_source_files": True, "remove_source_dirs": True}
    kw.update(k)
    return fs_sync(dst, dst, **kw)

  #def move(src, dst, **k):  # needs to implement a mechanism to use os.rename instead of copying everything

  fs_sync.merge = merge
  fs_sync.mirror = mirror
  fs_sync.clean = clean
  fs_sync.remove = remove
  return fs_sync

fs_sync = fs_sync()
fs_sync._required_globals = ["os", "stat", "sys", "errno", "fs_iterdirsdiff", "fs_copyfile", "fs_move", "os_path_splitall", "io_diff"]
