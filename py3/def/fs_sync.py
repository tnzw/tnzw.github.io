# fs_sync.py Version 2.1.1-2
# Copyright (c) 2020-2022 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

# TODO think about modify_accuracy option.
#   see XXX in the code next to diffmodifywindow
# TODO add possibility to run it partialy using fs_sync.iter(…)
#   when to yield? after copied data chunk? after handled node?
#   also, think about these options
#     progress    show progress during transfer
#     info=FLAGS  fine-grained informational verbosity
#     info=("progress2",)
#     info=("stats2", "misc1", "flist0")
# TODO add these options
#   copy_dest=PATH       ... and include copies of unchanged files
#   link_dest=PATH       hardlink to files in PATH when unchanged
# TODO add this option if possible
#   copy_unsafe_links    only "unsafe" symlinks are transformed
#   safe_links           ignore symlinks that point outside the source tree
#   munge_links          munge symlinks to make them safer (but unusable)
#   hard_links           preserve hard links
# TODO add option to make rec() to listdir() on src and dst (as usual) plus adding ability to make name matching
#   eg   src/a matches dst/b so sync("src/a" with "dst/b")
def fs_sync():
  def fs_sync(src, dst, *, follow_symlinks=False, source_directory=None, target_directory=None, src_noent_ok=None, content=None, head=None, archive=None, recursive=None, backup=None, backup_dir=None, suffix=None, inplace=None, temp_dir=None, update=None, dirs=None, links=None, copy_links=None, copy_dirlinks=None, keep_dirlinks=None, perms=None, executability=None, chmod=None, owner=None, group=None, devices=None, specials=None, times=None, omit_dir_times=None, omit_link_times=None, dry_run=None, existing=None, ignore_non_existing=None, ignore_existing=None, remove_source_files=None, remove_source_dirs=None, delete=None, force=None, chown=None, ignore_times=None, size_only=None, times_only=None, modify_window=None, src_time_offset=None, exclude=None, include=None, file_matcher=None, copy_function=None, verbose=None, onverbose=None, ignore_errors=None, ignore_listdir_errors=None, ignore_exdev_errors=None, onerror=None, buffer_size=None, as_func=None, os_module=None):
    """\
fs_sync(src, dst, **opt)

  Synchronizes src as dst to make src and dst similar.
  Unlike rsync, dst is NOT a target directory by default.
  There is no protection preventing sync in cross file trees!
  This fonction is inspired by `man rsync`.

  opt  (all options are None by default)
    follow_symlinks      follow src target if src is a symlink (not used in recursion)
    source_directory     synchronize src inner content to dst, implies target_directory (equiv: rsync src/ dst/)
    target_directory     synchronize src inside dst directory (equiv: rsync src dst)
    src_noent_ok         sync even if src does not exist

    content              skip based on content, not mod-time & size
    head=INT             compare files content first bytes
    archive              archive mode; equals recursive = links = devices = specials = perms = times = group = owner = True (on windows: group = owner = False)
    recursive            recurse into directories
    backup               make backups (see suffix & backup_dir)
                         backup files are overwritten
    backup_dir=PATH      make backups into hierarchy based in backup_dir
                         /!\\ behavior is different from original rsync --backup-dir (where --backup-dir=bak points to dst+"/bak")
                         here, backup_dir points to an external dir
    suffix=SUFFIX        backup suffix (default ~ w/o backup_dir)
    inplace              update destination files in-place
    temp_dir=PATH        create temporary files in directory PATH (must be in the same device as dst)
    update               skip files that are newer on the receiver
    dirs                 transfer directories without recursing
    links                copy symlinks as symlinks
    copy_links           transform symlink into referent file/dir
    copy_dirlinks        transform symlink to a dir into referent dir
    keep_dirlinks        treat symlinked dir on receiver as dir
    perms                preserve permissions
    executability        preserve executability
    chmod=MODE           affect file and/or directory permissions
    owner                preserve owner
    group                preserve group
    devices              preserve device files (may require super-user)
    specials             preserve special files
    times                preserve modification times
    omit_dir_times       omit directories from times
    omit_link_times      omit symlinks from times
    dry_run              perform a trial run with no changes made
    ignore_non_existing,
    existing             skip creating new files on receiver
    ignore_existing      skip updating files that exist on receiver
    remove_source_files  sender removes synchronized files (non-dir)
    remove_source_dirs   sender removes synchronized dirs
    delete               delete extraneous files from dest dirs
    force                force deletion of dirs even if not empty (useless for the moment)
    chown=(UID,GID)      affect file and directory username and groupname
    ignore_times         don't skip files that match in size and mod-time
    size_only            skip files that match in size
    times_only           skip files that match in mtime
    modify_window=NUM    compare mod-times with reduced accuracy
    src_time_offset=NUM  use src times with additional seconds
    exclude=FUNC         exclude files if FUNC(common_path) returns True
    include=FUNC         don't exclude files if FUNC(common_path) returns True
    file_matcher=FUNC    don't skip files if not FUNC(src, dst, src_stats, dst_stats)
    copy_function=FUNC   use FUNC(src_reader, dst_writer) to copy files data
    buffer_size          used for copying file. Could be either an int or None

    verbose              verbosity level
    onverbose=FUNC       verbose=1 :
                         calls onverbose(action_name, common_path) before starting action
                         action_name could be "create", "update" or "delete"
                         the arguments varies according to verbose level
                         verbose=2 : (info)
                         calls onverbose(state_name, common_path) on each skipped action
                         state_name could be "uptodate", "exists", "absent", "skip"
                         verbose>=3 : (debug)
                         calls onverbose(function_name, *arguments) before each operation on files

    ignore_errors                ignores failures during a node synchronisation, allowing to continue to next node
    ignore_listdir_errors        ignores failures during the walk in the file tree
    ignore_exdev_errors          fallback to tree copy on replace failures (default True)
    onerror=FUNC                 calls onerror(func, arg, exc_info) on error if not ignore_errors
                                 you can retry the process by calling func(arg)
                                 or you can propagate the active exception by using raise

    os_module                    the module to use to act on src and dst (defaults to os module)

fs_sync.merge(src, dst, **kw)
  equiv fs_sync with archive=True

fs_sync.mirror(src, dst, **kw)
  equiv fs_sync with archive=True, delete=True

fs_sync.clean(src, dst, **kw)
  equiv fs_sync with recursive=True, delete=True, ignore_non_existing=True, ignore_existing=True, links=True, devices=True, specials=True

fs_sync.move(src, dst, **kw)
  equiv fs_sync with recursive=True, remove_source_files=True, remove_source_dirs=True, links=True, devices=True, specials=True

fs_sync.remove(dst, **kw)
  equiv fs_sync with remove_source_files=True, remove_source_dirs=True, links=True, devices=True, specials=True (with dst passed as src and dst)
"""
    def _raise(error): raise error
    def pathextend(path, *paths, sep=None, altsep=None):
      paths = [_ for _ in (path,) + paths if _]
      if paths: *paths, last = paths
      else: return path
      paths = [_[:-1] if _[-1:] in (sep, altsep) else _ for _ in paths] + [last]  # XXX len(sep) and len(altsep) are hardcoded
      return sep.join(paths)
    def dbl(a): return a, a
    def countendswith(s, suffix):
      l = len(suffix)
      i = 0
      while s.endswith(suffix): i, s = i + 1, s[:-l]
      return i

    if os_module is None: _os, _open, _open_kw = os, open, {}
    else: _os, _open, _open_kw = os_module, open2, {"os_module": os_module}
    if not isinstance(src, (str, bytes)): src = _os.fspath(src)
    if not isinstance(dst, (str, bytes)): dst = _os.fspath(dst)
    if source_directory:
      if target_directory is None: target_directory = True
      elif not target_directory: raise ValueError("target_directory=False conflicts with source_directory=True")
    if archive:
      if recursive is None: recursive = True
      if links     is None: links     = True
      if devices   is None: devices   = True
      if specials  is None: specials  = True
      if perms     is None: perms     = True
      if times     is None: times     = True
      if group     is None: group     = True if hasattr(_os, "chown") else False
      if owner     is None: owner     = True if hasattr(_os, "chown") else False
    if backup_dir:
      if backup is None: backup = True
      if suffix is None: suffix = dst[:0]
    else:
      if suffix is None: suffix = "~" if isinstance(dst, str) else b"~"
      elif suffix: dst + suffix
      else: raise ValueError("suffix must not be empty")
    if delete and not (recursive or dirs):
      raise ValueError("'delete' does not work without 'recursive' or 'dirs'")  # XXX it's rsync behavior, but what's the problem?
    if delete: force = True  # 'force' option is only relevant if 'delete' is not active
    if dirs is None and recursive: dirs = True  # this is internal magic
    _top_verbose = True
    chown_uid, chown_gid = -1, -1
    if chown is not None:
      chown_uid, chown_gid = chown
      chown = True
    if src_time_offset is None: src_time_offset = 0
    _omit_link_copystat = True if omit_link_times is None or omit_link_times else False  # XXX Avoids NotImplementedError: chmod: follow_symlinks unavailable on this platform
    if exclude is None: exclude = lambda _: False
    if include is None: include = lambda _: False
    if not isinstance(verbose, int): verbose = 1 if verbose else 0
    if verbose and onverbose is None:
      def onverbose(*a): print(": ".join(getattr(_, "decode", lambda a,b: str(_))("UTF-8", "replace") for _ in a))
    if ignore_non_existing is None: ignore_non_existing = existing
    #elif existing is not None and bool(ignore_non_existing) != bool(existing): raise TypeError()
    if ignore_exdev_errors is None: ignore_exdev_errors = True

    src + dst
    if backup_dir and not isinstance(backup_dir, (str, bytes)): backup_dir = _os.fspath(backup_dir); dst + backup_dir
    if temp_dir and not isinstance(temp_dir, (str, bytes)): temp_dir = _os.fspath(temp_dir); dst + temp_dir

    sep = _os.sep
    altsep = getattr(_os, "altsep", sep) or sep
    if isinstance(src, bytes): sep, altsep = _os.fsencode(sep), _os.fsencode(altsep)

    custom_check = True if size_only or times_only or update or content or head is not None or file_matcher else False

    def   _sync(    srcname, dstname, src_dir,         dst_dir,         src_lstats=None,       dst_lstats=None,       src_stats=None,      dst_stats=None,      _in_delete=False,      _in_backup=False,      follow_symlinks=False,           custom_check=custom_check, listdir_src=None,        source_directory=False,            target_directory=False,            src_noent_ok=True,         content=content, head=head, recursive=recursive, backup=backup, backup_dir=backup_dir, suffix=suffix, inplace=inplace, temp_dir=temp_dir, update=update, dirs=dirs,  links=links, copy_links=copy_links, copy_dirlinks=copy_dirlinks, keep_dirlinks=keep_dirlinks, perms=perms, executability=executability, chmod=chmod, owner=owner, group=group, devices=devices, specials=specials, times=times, omit_dir_times=omit_dir_times, omit_link_times=omit_link_times, _omit_link_copystat=_omit_link_copystat, dry_run=dry_run, ignore_non_existing=ignore_non_existing, ignore_existing=ignore_existing, remove_source_files=remove_source_files, remove_source_dirs=remove_source_dirs, delete=delete, force=force, chown=chown, chown_uid=chown_uid, chown_gid=chown_gid, ignore_times=ignore_times, size_only=size_only, times_only=times_only, modify_window=modify_window, src_time_offset=src_time_offset, exclude=exclude,         include=include,         file_matcher=file_matcher, copy_function=copy_function, _top_verbose=True,         verbose=verbose, onverbose=onverbose, ignore_errors=ignore_errors, ignore_listdir_errors=ignore_listdir_errors, ignore_exdev_errors=ignore_exdev_errors, onerror=onerror, buffer_size=buffer_size, _open=_open, _open_kw=_open_kw, os_module=os_module, _os=_os,  sep=sep,  altsep=altsep):
      return   sync(  # [..] propagating some parameters to `sync()` (parent parameters are kept)
                    # line below produces a very long stacktrace line, prefer to explain with the line just above.
                    srcname, dstname, src_dir=src_dir, dst_dir=dst_dir, src_lstats=src_lstats, dst_lstats=dst_lstats, src_stats=src_stats, dst_stats=dst_stats, _in_delete=_in_delete, _in_backup=_in_backup, follow_symlinks=follow_symlinks, custom_check=custom_check, listdir_src=listdir_src, source_directory=source_directory, target_directory=target_directory, src_noent_ok=src_noent_ok, content=content, head=head, recursive=recursive, backup=backup, backup_dir=backup_dir, suffix=suffix, inplace=inplace, temp_dir=temp_dir, update=update, dirs=dirs,  links=links, copy_links=copy_links, copy_dirlinks=copy_dirlinks, keep_dirlinks=keep_dirlinks, perms=perms, executability=executability, chmod=chmod, owner=owner, group=group, devices=devices, specials=specials, times=times, omit_dir_times=omit_dir_times, omit_link_times=omit_link_times, _omit_link_copystat=_omit_link_copystat, dry_run=dry_run, ignore_non_existing=ignore_non_existing, ignore_existing=ignore_existing, remove_source_files=remove_source_files, remove_source_dirs=remove_source_dirs, delete=delete, force=force, chown=chown, chown_uid=chown_uid, chown_gid=chown_gid, ignore_times=ignore_times, size_only=size_only, times_only=times_only, modify_window=modify_window, src_time_offset=src_time_offset, exclude=exclude,         include=include,         file_matcher=file_matcher, copy_function=copy_function, _top_verbose=_top_verbose, verbose=verbose, onverbose=onverbose, ignore_errors=ignore_errors, ignore_listdir_errors=ignore_listdir_errors, ignore_exdev_errors=ignore_exdev_errors, onerror=onerror, buffer_size=buffer_size, _open=_open, _open_kw=_open_kw, os_module=os_module, _os=_os,  sep=sep,  altsep=altsep)
    def sync(       srcname, dstname, src_dir,         dst_dir,         src_lstats=None,       dst_lstats=None,       src_stats=None,      dst_stats=None,      _in_delete=False,      _in_backup=False,      follow_symlinks=False,           custom_check=False,        listdir_src=None,        source_directory=False,            target_directory=False,            src_noent_ok=True,         content=False,   head=None, recursive=False,     backup=False,  backup_dir=False,      suffix=None,   inplace=False,   temp_dir=None,     update=False,  dirs=False, links=False, copy_links=False,      copy_dirlinks=False,         keep_dirlinks=False,         perms=False, executability=False,         chmod=None,  owner=False, group=False, devices=False,   specials=False,    times=False, omit_dir_times=False,          omit_link_times=False,           _omit_link_copystat=True,                dry_run=False,   ignore_non_existing=False,               ignore_existing=False,           remove_source_files=False,               remove_source_dirs=False,              delete=False,  force=False, chown=False, chown_uid=-1,        chown_gid=-1,        ignore_times=False,        size_only=False,     times_only=False,      modify_window=None,          src_time_offset=None,            exclude=lambda _: False, include=lambda _: False, file_matcher=None,         copy_function=None,          _top_verbose=True,         verbose=0,       onverbose=None,      ignore_errors=False,         ignore_listdir_errors=False,                 ignore_exdev_errors=True,                onerror=None,    buffer_size=None,        _open=open,  _open_kw={},       os_module=None,      _os=None, sep=None, altsep=None):
      def _sync(    srcname, dstname, src_dir,         dst_dir,         src_lstats=None,       dst_lstats=None,       src_stats=None,      dst_stats=None,      _in_delete=_in_delete, _in_backup=_in_backup, follow_symlinks=False,           custom_check=custom_check, listdir_src=None,        source_directory=False,            target_directory=False,            src_noent_ok=True,         content=content, head=head, recursive=recursive, backup=backup, backup_dir=backup_dir, suffix=suffix, inplace=inplace, temp_dir=temp_dir, update=update, dirs=dirs,  links=links, copy_links=copy_links, copy_dirlinks=copy_dirlinks, keep_dirlinks=keep_dirlinks, perms=perms, executability=executability, chmod=chmod, owner=owner, group=group, devices=devices, specials=specials, times=times, omit_dir_times=omit_dir_times, omit_link_times=omit_link_times, _omit_link_copystat=_omit_link_copystat, dry_run=dry_run, ignore_non_existing=ignore_non_existing, ignore_existing=ignore_existing, remove_source_files=remove_source_files, remove_source_dirs=remove_source_dirs, delete=delete, force=force, chown=chown, chown_uid=chown_uid, chown_gid=chown_gid, ignore_times=ignore_times, size_only=size_only, times_only=times_only, modify_window=modify_window, src_time_offset=src_time_offset, exclude=exclude,         include=include,         file_matcher=file_matcher, copy_function=copy_function, _top_verbose=True,         verbose=verbose, onverbose=onverbose, ignore_errors=ignore_errors, ignore_listdir_errors=ignore_listdir_errors, ignore_exdev_errors=ignore_exdev_errors, onerror=onerror, buffer_size=buffer_size, _open=_open, _open_kw=_open_kw, os_module=os_module, _os=_os,  sep=sep,  altsep=altsep):
        return sync(  # [..] propagating some parameters to `sync()` (parent parameters are forgotten)
                    # line below produces a very long stacktrace line, prefer to explain with the line just above.
                    srcname, dstname, src_dir=src_dir, dst_dir=dst_dir, src_lstats=src_lstats, dst_lstats=dst_lstats, src_stats=src_stats, dst_stats=dst_stats, _in_delete=_in_delete, _in_backup=_in_backup, follow_symlinks=follow_symlinks, custom_check=custom_check, listdir_src=listdir_src, source_directory=source_directory, target_directory=target_directory, src_noent_ok=src_noent_ok, content=content, head=head, recursive=recursive, backup=backup, backup_dir=backup_dir, suffix=suffix, inplace=inplace, temp_dir=temp_dir, update=update, dirs=dirs,  links=links, copy_links=copy_links, copy_dirlinks=copy_dirlinks, keep_dirlinks=keep_dirlinks, perms=perms, executability=executability, chmod=chmod, owner=owner, group=group, devices=devices, specials=specials, times=times, omit_dir_times=omit_dir_times, omit_link_times=omit_link_times, _omit_link_copystat=_omit_link_copystat, dry_run=dry_run, ignore_non_existing=ignore_non_existing, ignore_existing=ignore_existing, remove_source_files=remove_source_files, remove_source_dirs=remove_source_dirs, delete=delete, force=force, chown=chown, chown_uid=chown_uid, chown_gid=chown_gid, ignore_times=ignore_times, size_only=size_only, times_only=times_only, modify_window=modify_window, src_time_offset=src_time_offset, exclude=exclude,         include=include,         file_matcher=file_matcher, copy_function=copy_function, _top_verbose=_top_verbose, verbose=verbose, onverbose=onverbose, ignore_errors=ignore_errors, ignore_listdir_errors=ignore_listdir_errors, ignore_exdev_errors=ignore_exdev_errors, onerror=onerror, buffer_size=buffer_size, _open=_open, _open_kw=_open_kw, os_module=os_module, _os=_os,  sep=sep,  altsep=altsep)

      src = pathextend(src_dir, srcname, sep=sep, altsep=altsep)
      dst = pathextend(dst_dir, dstname, sep=sep, altsep=altsep)

      def verbose3(fn, name=None):
        if isinstance(fn, str): return lambda _: verbose3(_, fn)
        if verbose > 2:
          if name is None: name = fn.__name__
          def _verbose3(*a,**k):
            if k: onverbose(name, *a, k)
            else: onverbose(name, *a)
            return fn(*a,**k)
          return _verbose3
        return fn

      def _verb(level, *a):
        if _top_verbose and verbose >= level: onverbose(*a)

      @verbose3
      def listdir(a):      return _os.listdir(a)
      @verbose3("stat")
      def _stat(a):        return _os.stat(a)
      @verbose3
      def lstat(a):        return _os.lstat(a)
      @verbose3
      def readlink(a):     return _os.readlink(a)
      @verbose3("diff")
      def same(*a,**k):    return not fs_diff(*a, os_modules=(os_module,) * len(a), **k)
      @verbose3
      def symlink(*a):     return None if dry_run else _os.symlink(*a)
      @verbose3
      def utime(*a, **k):  return None if dry_run else _os.utime(*a, **k)
      @verbose3("chmod")
      def _chmod(*a, **k): return None if dry_run else _os.chmod(*a, **k)
      @verbose3("chown")
      def _chown(*a, **k): return None if dry_run else _os.chown(*a, **k)
      @verbose3
      def mkdir(a):        return None if dry_run else _os.mkdir(a)
      @verbose3
      def replace(*a):     return None if dry_run else _os.replace(*a)
      @verbose3
      def unlink(a):       return None if dry_run else _os.unlink(a)
      @verbose3
      def rmdir(a):        return None if dry_run else _os.rmdir(a)
      def rm(a,s):         return rmdir(a) if stat.S_ISDIR(s.st_mode) else unlink(a)
      def softrmdir(a,s=None):  # softrmdir() uses unlink (rm()) for symlinks that point to dirs
        try: rmdir(a) if s is None else rm(a,s)
        except OSError as err:
          if err.errno == errno.ENOTEMPTY: return
          raise
      def softreplace(src, dst):
        try: replace(src, dst)
        except OSError as err:
          if ignore_exdev_errors and err.errno == errno.EXDEV: return False
          raise
        return True

      def makedirsfor(path, parent, sep, altsep):
        if altsep: path.replace(altsep, sep)
        split = path.split(sep)
        it = iter(split)
        for _ in it: p = _; break
        for _ in it:
          try: mkdir(pathextend(parent, p, sep=sep, altsep=altsep))
          except FileExistsError: pass
          p += sep + _

      # note: Having an option `copyfile_function(src_path, dst_path)` is not relevant 'cause
      # 1) copy_function do the job
      # 2) fs_sync doesn't use file_matcher to find destination tree corresponding file,
      #    so copyfile_function must not write to a different dst_path.
      if copy_function:
        @verbose3("copy")
        def copyfileinplace(src, dst):
          # copyfileinplace(path_or_filelike, path_or_filelike)
          if dry_run: return
          if isinstance(src, (str, bytes)):
            with _open(src, "rb", **_open_kw) as f: return copyfileinplace(f, dst)
          if isinstance(dst, (str, bytes)):
            with _open(dst, "wb", **_open_kw) as f: return copyfileinplace(src, f)
          return copy_function(src, dst)
      else:
        @verbose3("copy")
        def copyfileinplace(src, dst):
          # copyfileinplace(path, path_or_filelike)
          if dry_run: return
          try: dst = dst if isinstance(dst, int) else dst.fileno()
          except AttributeError: pass
          return fs_copyfile(src, dst, buffer_size=buffer_size, os_module=os_module)


      def diffstat():  # copy/paste from _copystat()
        if chmod:
          if (not dst_stats or (chmod & 0o777) != (dst_stats.st_mode & 0o777)): return 1
        elif perms:
          if (not dst_stats or (src_stats.st_mode & 0o777) != (dst_stats.st_mode & 0o777)): return 1
        elif executability:
          if (not dst_stats or (src_stats.st_mode & 0o444) != (dst_stats.st_mode & 0o444)): return 1
        if chown:
          if not dst_stats or (chown_uid >= 0 and chown_uid != dst_stats.st_uid) or (chown_gid >= 0 and chown_gid != dst_stats.st_gid): return 1
        elif (owner and (not dst_stats or src_stats.st_uid != dst_stats.st_uid)) or \
             (group and (not dst_stats or src_stats.st_gid != dst_stats.st_gid)): return
        if times:
          if omit_dir_times and stat.S_ISDIR(src_stats.st_mode): pass  # better check dst instead?
          elif omit_link_times and stat.S_ISLNK(src_stats.st_mode): pass  # better check dst instead?
          else:
            diff = supmodifywindow if update else diffmodifywindow
            if (not dst_stats or diff(src_stats.st_mtime + src_time_offset, dst_stats.st_mtime)): return 1
        return 0
      def _copystat(dst, src_stats, dst_stats=None, dst_islnk=False):
        # rsync copies the stats in any cases, without doing backup
        # does not update times if update is True and dst >= src
        if dst_islnk and _omit_link_copystat: return  # XXX the goal is remove this statement
        opt = {"follow_symlinks": False} if dst_islnk else {}
        if chmod:
          if (not dst_stats or (chmod & 0o777) != (dst_stats.st_mode & 0o777)):
            _chmod(dst, chmod & 0o777, **opt)
        elif perms:
          if (not dst_stats or (src_stats.st_mode & 0o777) != (dst_stats.st_mode & 0o777)):
            _chmod(dst, src_stats.st_mode & 0o777, **opt)
        elif executability:
          if (not dst_stats or (src_stats.st_mode & 0o444) != (dst_stats.st_mode & 0o444)):
            _chmod(dst, (src_stats.st_mode & 0o444) | (dst_stats.st_mode & 0o333), **opt)
        if chown:
          if not dst_stats or (chown_uid >= 0 and chown_uid != dst_stats.st_uid) or (chown_gid >= 0 and chown_gid != dst_stats.st_gid):
            _chown(dst, chown_uid, chown_gid, follow_symlinks=False)
        elif (owner and (not dst_stats or src_stats.st_uid != dst_stats.st_uid)) or \
             (group and (not dst_stats or src_stats.st_gid != dst_stats.st_gid)):
          _chown(dst, src_stats.st_uid if owner else -1, src_stats.st_gid if group else -1, follow_symlinks=False)
        if times:
          if omit_dir_times and stat.S_ISDIR(src_stats.st_mode): pass  # better check dst instead?
          elif omit_link_times and dst_islnk: pass  # better check src instead?
          else:
            diff = supmodifywindow if update else diffmodifywindow
            if (not dst_stats or diff(src_stats.st_mtime + src_time_offset, dst_stats.st_mtime)):
              utime(dst, (src_stats.st_atime + src_time_offset, src_stats.st_mtime + src_time_offset), **opt)
      def copystat(dst_stats=None, dst_islnk=False): return _copystat(dst, src_stats, dst_stats, dst_islnk=dst_islnk)
      def copystattmp(dst_islnk=False): return _copystat(tmp, src_stats, dst_islnk=dst_islnk)

      # XXX for file mtime comparison
      #     for modify_window=2, fs_sync takes mtime +/- 1 second,
      #     rsync acts a bit different, please think about it.
      #     see https://unix.stackexchange.com/questions/461283/why-modify-window-1-when-using-rsync-command
      #     and https://rsync.samba.org/doxygen/head/util_8c.html#a35
      # XXX but in FAT or exFAT case, mtimes are a multiple of 2, (NTFS accuracy is 0.0000001 = 100ns)
      #     if stat returns 1234.028, in reality, written mtime is 1236 (eg `ceil(mtime)`). (tested with python 3.10.4)
      #     so a copy between two devices may be lossy!
      #     fs_sync should handle it somehow, think about it. Add option `modify_accuracy=2`?
      #         if isinstance(modify_accuracy, float): raise XXX  # force modify_accuracy to be an integer, else undefined system behavior may occur due to float precision
      #         actual_mtime = mtime + mtime % modify_accuracy  # not really precise if modify_accuracy is a float : 123.4 + 123.4 % 0.2 => 123.60000000000001 => system could write 123.8 (how to check ?)
      #     does it solve if fs_sync acts like rsync? I think not, this a different issue.
      def diffmodifywindow(i, j):
        if modify_window is None: return int(i) != int(j)  # using int() because sometimes it compares 1589402770.3552 with 1589402770.3575144. Should we use int() before this line ? like i,j=int(i),int(j)
        return i + modify_window < j - modify_window or i - modify_window > j + modify_window

      def supmodifywindow(i, j):
        if modify_window is None: return int(i) > int(j)  # using int() because sometimes it compares 1589402770.3552 with 1589402770.3575144. Should we use int() before this line ? like i,j=int(i),int(j)
        return i - modify_window > j + modify_window

      _readlink = None
      def difflink():
        nonlocal _readlink
        _readlink = readlink(src)
        return _readlink != readlink(dst)

      def diffdir():
        if times and not omit_dir_times:
          if update:
            if supmodifywindow(src_stats.st_mtime + src_time_offset, dst_stats.st_mtime): return 1
            return 0
          if diffmodifywindow(src_stats.st_mtime + src_time_offset, dst_stats.st_mtime): return 1
          return 0
        return 0

      def difffile():
        if custom_check:
          if update:
            if supmodifywindow(src_stats.st_mtime + src_time_offset, dst_stats.st_mtime): return 1
          if size_only:
            if src_stats.st_size != dst_stats.st_size: return 1
          if times_only:
            if diffmodifywindow(src_stats.st_mtime + src_time_offset, dst_stats.st_mtime): return 1
          # XXX add options for additional custom checks ? mode ? owner ? group ?
          #if src_stats.st_mode != dst_stats.st_mode: return None, 1
          #if src_stats.st_uid != dst_stats.st_uid: return None, 1
          #if src_stats.st_gid != dst_stats.st_gid: return None, 1
          if file_matcher:
            if not file_matcher(src, dst, src_stats, dst_stats): return 1
          if content:
            equals = same(src, dst, compare_size=False, max_length=None if head is None or head < 0 else head, stats=(src_stats, dst_stats))
            if not equals: return 1
          elif head is not None:
            equals = same(src, dst, max_length=None if head < 0 else head, stats=(src_stats, dst_stats))
            if not equals: return 1
          return 0

        if ignore_times: return 1
        # rsync "quick check" is check mod-time & size
        if src_stats.st_size != dst_stats.st_size: return 1
        if diffmodifywindow(src_stats.st_mtime + src_time_offset, dst_stats.st_mtime): return 1
        return 0

      if source_directory or target_directory:
        try: g = set((listdir(src) if listdir_src is None else listdir_src) if source_directory else []) | set(listdir(dst) if target_directory else [])
        except OSError:
          if ignore_listdir_errors: return
          # XXX onerror ?
          raise
        g = sorted(g)  # XXX it's not mandatory to sort. Add an fs_sync parameter for this ?
        #if suffix: g = sorted(g, key=lambda k: countendswith(k, suffix))  # backup files MUST be after update files.
        for name in g:
          args = (pathextend(srcname, name, sep=sep, altsep=altsep), pathextend(dstname, name, sep=sep, altsep=altsep), src_dir, dst_dir)
          try: _sync(*args)
          except OSError:
            if ignore_errors: pass
            elif onerror is not None: onerror(_sync, args, sys.exc_info())
            else: raise
        return

      # Start sync'ing src node to dst node

      if exclude(srcname):
        if not include(srcname):
          return None

      if src_lstats is None:
        try: src_lstats = lstat(src)
        except (FileNotFoundError, NotADirectoryError):
          if src_noent_ok: pass
          else: raise
      if src_stats is None:
        src_stats = src_lstats
        if src_lstats and stat.S_ISLNK(src_lstats.st_mode):
          if copy_links or follow_symlinks:
            try: src_stats = _stat(src)
            except (FileNotFoundError, NotADirectoryError): src_stats = None
          elif copy_dirlinks:
            try: tmp = _stat(src)
            except (FileNotFoundError, NotADirectoryError): pass
            else:
              if stat.S_ISDIR(tmp.st_mode): src_stats = tmp
          #elif copy_unsafe_links XXX

      if dst_lstats is None:
        try: dst_lstats = lstat(dst)
        except (FileNotFoundError, NotADirectoryError): pass
      if dst_stats is None:
        dst_stats = dst_lstats
        if keep_dirlinks and dst_lstats and stat.S_ISLNK(dst_lstats.st_mode):
          try: tmp = _stat(dst)
          except (FileNotFoundError, NotADirectoryError): pass
          else:
            if stat.S_ISDIR(tmp.st_mode): dst_stats = tmp

      def verbosecreate(): _verb(2, "backup to", dstname) if _in_backup else _verb(1, "create", dstname)
      def verboseupdate(): _verb(2, "backup to", dstname) if _in_backup else _verb(1, "update", dstname)
      def verbosedelete(): _verb(1, "delete", dstname)
      def verboseskip(): _verb(1, "delete", srcname) if _in_delete else _verb(2, "skip", dstname)
      def verboseuptodate(): _verb(1, "delete", srcname) if _in_delete else _verb(2, "uptodate", dstname)
      def verboseabsent(): _verb(2, "absent", dstname)
      def verboseexists(): _verb(2, "exists", dstname)
      def _rmtree(name, dir, lstats): return sync(name, name, src_dir=dir, dst_dir=dir, src_lstats=lstats, dst_lstats=lstats, src_stats=lstats, dst_stats=lstats, _top_verbose=False, _in_delete=True, remove_source_files=True, remove_source_dirs=True, recursive=True, links=True, devices=True, specials=True, custom_check=True, size_only=True, inplace=True, verbose=verbose, onverbose=onverbose, ignore_errors=ignore_errors, ignore_listdir_errors=ignore_listdir_errors, onerror=onerror, dry_run=dry_run, buffer_size=buffer_size, _open=_open, _open_kw=_open_kw, os_module=os_module, _os=_os, sep=sep, altsep=altsep)
      def _dobackup(s, d, sd, dd, ls): return sync(s, d, src_dir=sd, dst_dir=dd, src_lstats=ls, src_stats=ls, _top_verbose=True, _in_backup=True, remove_source_files=True, remove_source_dirs=True, force=True, recursive=True, links=True, devices=True, specials=True, perms=perms, times=times, group=group, owner=owner, ignore_times=True, inplace=inplace, verbose=verbose, onverbose=onverbose, ignore_exdev_errors=ignore_exdev_errors, ignore_errors=ignore_errors, ignore_listdir_errors=ignore_listdir_errors, onerror=onerror, dry_run=dry_run, buffer_size=buffer_size, _open=_open, _open_kw=_open_kw, os_module=os_module, _os=_os, sep=sep, altsep=altsep)
      def dobackup():
        if backup_dir:
          makedirsfor(dstname, backup_dir, sep, altsep)
          return _dobackup(dstname, dstname, dst_dir, backup_dir, dst_lstats)
        #if suffix:
        return _dobackup(dstname, dstname + suffix, dst_dir, dst_dir, dst_lstats)
      def rmtree(): return _rmtree(dstname, dst_dir, dst_lstats)

      def rec(): return _sync(srcname, dstname, src_dir, dst_dir, source_directory=True, target_directory=True)
      def recsrc(): return _sync(srcname, dstname, src_dir, dst_dir, source_directory=True)
      #def recdst(): return _sync(srcname, dstname, src_dir, dst_dir, target_directory=True)

      tmpf = None
      tmp = None
      def opentmp():
        if dry_run: return
        nonlocal tmpf
        nonlocal tmp
        dstdir, dstbase = _os.path.split(dst)
        _ = _os.path.join(temp_dir, dstbase) if temp_dir else dst
        # rsync uses   ".{basename(dst)}.{random_6_letters()}"
        # here it uses ".{basename(dst)}.{random_4_or_more_b64_symbols()}"
        tmpf = opennewfile.temp(_, "xb", base_format=".{base}.{rand}", os_module=os_module)
        tmp = tmpf.name
      def closetmp():
        if dry_run: return
        tmpf.close()
      def mktmp():
        if dry_run: return
        nonlocal tmp
        i = 0
        encode = (lambda e: e) if isinstance(dst, str) else (lambda e: e.encode())
        dot = encode(".")
        dstdir, dstbase = _os.path.split(dst)
        _ = _os.path.join(temp_dir, dot + dstbase) if temp_dir else _os.path.join(dstdir, dot + dstbase)
        while 1:
          # rsync uses   ".{basename(dst)}.{random_6_letters()}"
          # here it uses ".{basename(dst)}.{random_4_or_more_b64_symbols()}"
          path = _ + encode("." + "".join(f"{b:02x}" for b in os.urandom(2 + i)))
          try: lstat(path)
          except FileNotFoundError: tmp = path; return
          i += 1
      def replacetmp():
        if dry_run: return
        nonlocal tmpf
        nonlocal tmp
        _tmpf = tmpf
        _tmp = tmp
        tmpf = tmp = None  # prevent auto closing+removing tmp file from now
        # normally closed by caller : _.close()  # closing sets mtime
        replace(_tmp, dst)  # do not ignore exdev errors here! If this error is raised, then it might be because temp_dir is outside dst filesystem.

      try:

        #           dst_noent ignore_non_existing                    : verboseabsent()  # remove_source_* has no effect here
        # src_noent dst_noent                                        : verboseuptodate
        # src_noent           ignore_existing                        : verboseexists
        # src_noent dst_isdir recursive|dirs delete suffix dst_isbak : verboseskip
        # src_noent dst_isdir recursive|dirs delete backup           : verbosedelete dobackup
        # src_noent dst_isdir recursive|dirs delete                  : verbosedelete rmtree
        ## src_noent dst_isdir recursive                              : verboseskip recdst  # seems useless
        # src_noent dst_isdir                                        : verboseskip
        # src_noent                     delete suffix dst_isbak      : verboseskip
        # src_noent                     delete backup                : verbosedelete dobackup
        # src_noent                     delete                       : verbosedelete unlink
        # src_noent                                                  : verboseskip
        if   dst_stats is None and ignore_non_existing: verboseabsent();                     return
        if src_stats is None:
          if dst_stats is None:                         verboseuptodate();                   return
          if   ignore_existing:                         verboseexists();                     return
          if stat.S_ISDIR(dst_stats.st_mode):
            if dirs:
              if delete:
                if suffix and dstname.endswith(suffix): verboseskip();                       return
                if backup:                              verbosedelete(); dobackup();         return
                1;                                      verbosedelete(); rmtree();           return
              1;                                        verboseskip();                       return
            1;                                          verboseskip();                       return
          if     delete:
                if suffix and dstname.endswith(suffix): verboseskip();                       return
                if backup:                              verbosedelete(); dobackup();         return
                1;                                      verbosedelete(); unlink(dst);        return
          1;                                            verboseskip();                       return

        # src_isdir dst_noent remove_source_dirs recursive         : verbosecreate softreplace or (mkdir() rec() copystat() softrmdir(src,lstats))  # copystat() with remove_source_{dirs|files}+recursive might have unexpected behavior.
        # src_isdir dst_noent remove_source_dirs dirs              : verbosecreate                 mkdir()       copystat() softrmdir(src,lstats)
        # src_isdir dst_noent remove_source_dirs                   : verboseskip                                            softrmdir(src,lstats)
        # src_isdir dst_noent                    recursive         : verbosecreate mkdir() rec() copystat()
        # src_isdir dst_noent                    dirs              : verbosecreate mkdir()       copystat()
        # src_isdir dst_noent                                      : verboseskip
        # src_isdir dst_isdir ignore_existing    recursive         : verboseexists   rec copystat()  # copystat() on ignore_existing? yes, rsync behavior.
        # src_isdir dst_isdir ignore_existing    dirs              : verboseexists
        # src_isdir dst_isdir ignore_existing                      : verboseskip
        # src_isdir dst_isdir remove_source_dirs recursive diffdir : verboseupdate   rec copystat() softrmdir(src,lstats)
        # src_isdir dst_isdir remove_source_dirs recursive         : verboseuptodate rec copystat() softrmdir(src,lstats)
        # src_isdir dst_isdir remove_source_dirs dirs      diffdir : verboseupdate       copystat() softrmdir(src,lstats)
        # src_isdir dst_isdir remove_source_dirs dirs              : verboseuptodate     copystat() softrmdir(src,lstats)
        # src_isdir dst_isdir remove_source_dirs                   : verboseskip                    softrmdir(src,lstats)
        # src_isdir dst_isdir                    recursive diffdir : verboseupdate   rec copystat()
        # src_isdir dst_isdir                    recursive         : verboseuptodate rec copystat()
        # src_isdir dst_isdir                    dirs      diffdir : verboseupdate       copystat()
        # src_isdir dst_isdir                    dirs              : verboseuptodate     copystat()
        # src_isdir dst_isdir                                      : verboseskip
        # src_isdir           ignore_existing                      : verboseexists  # with recursive and when src_isdir, rsync goes down src dir... but why?
        # src_isdir           remove_source_dirs recursive backup  : verboseupdate dobackup()  softreplace() or (mkdir() rec() copystat() softrmdir(src,lstats))
        # src_isdir           remove_source_dirs recursive         : verboseupdate unlink(dst) softreplace() or (mkdir() rec() copystat() softrmdir(src,lstats))  # copytree before replace? inplace does not matter for src_isdir?
        # src_isdir           remove_source_dirs dirs      backup  : verboseupdate dobackup()                    mkdir()       copystat() softrmdir(src,lstats)  # XXX softreplace if src dir is empty?
        # src_isdir           remove_source_dirs dirs              : verboseupdate unlink(dst)                   mkdir()       copystat() softrmdir(src,lstats)  # XXX softreplace if src dir is empty?
        # src_isdir           remove_source_dirs                   : verboseskip                                                          softrmdir(src,lstats)
        # src_isdir                              recursive backup  : verboseupdate dobackup()                    mkdir() rec() copystat()
        # src_isdir                              recursive         : verboseupdate unlink(dst)                   mkdir() rec() copystat()
        # src_isdir                              dirs      backup  : verboseupdate dobackup()                    mkdir()       copystat()
        # src_isdir                              dirs              : verboseupdate unlink(dst)                   mkdir()       copystat()
        # src_isdir                                                : verboseskip
        if stat.S_ISDIR(src_stats.st_mode):
          if dst_stats is None:
            if remove_source_dirs:
              if recursive:     verbosecreate();              softreplace(src, dst) or (mkdir(dst), recsrc(), copystat(), softrmdir(src, src_lstats)); return
              if dirs:          verbosecreate();                                        mkdir(dst); recsrc(); copystat(); softrmdir(src, src_lstats);  return
              1;                verboseskip();                                                                            softrmdir(src, src_lstats);  return
            if   recursive:     verbosecreate();                                        mkdir(dst); recsrc(); copystat();                              return
            if   dirs:          verbosecreate();                                        mkdir(dst);           copystat();                              return
            1;                  verboseskip();                                                                                                         return
          if stat.S_ISDIR(dst_stats.st_mode):
            if ignore_existing:
              if recursive:     verboseexists();                                                    rec();    copystat();                              return
              if dirs:          verboseexists();                                                                                                       return
              1;                verboseskip();                                                                                                         return
            if remove_source_dirs:
              if recursive:
                if diffdir():   verboseupdate();                                                    rec();    copystat(); softrmdir(src, src_lstats);  return
                1;              verboseuptodate();                                                  rec();    copystat(); softrmdir(src, src_lstats);  return
              if dirs:
                if diffdir():   verboseupdate();                                                              copystat(); softrmdir(src, src_lstats);  return
                1;              verboseuptodate();                                                            copystat(); softrmdir(src, src_lstats);  return
              1;                verboseskip();                                                                            softrmdir(src, src_lstats);  return
            if   recursive:
                if diffdir():   verboseupdate();                                                    rec();    copystat();                              return
                1;              verboseuptodate();                                                  rec();    copystat();                              return
            if   dirs:
                if diffdir():   verboseupdate();                                                              copystat();                              return
                1;              verboseuptodate();                                                            copystat();                              return
            1;                  verboseskip();                                                                                                         return
          if   ignore_existing: verboseexists();                                                                                                       return
          if   remove_source_dirs:
            if recursive:
              if backup:        verboseupdate(); dobackup();  softreplace(src, dst) or (mkdir(dst), recsrc(), copystat(), softrmdir(src, src_lstats)); return
              1;                verboseupdate(); unlink(dst); softreplace(src, dst) or (mkdir(dst), recsrc(), copystat(), softrmdir(src, src_lstats)); return
            if dirs:
              if backup:        verboseupdate(); dobackup();                            mkdir(dst);           copystat(); softrmdir(src, src_lstats);  return
              1;                verboseupdate(); unlink(dst);                           mkdir(dst);           copystat(); softrmdir(src, src_lstats);  return
            1;                  verboseskip();                                                                            softrmdir(src, src_lstats);  return
          if   recursive:
              if backup:        verboseupdate(); dobackup();                            mkdir(dst); recsrc(); copystat();                              return
              1;                verboseupdate(); unlink(dst);                           mkdir(dst); recsrc(); copystat();                              return
          if   dirs:
              if backup:        verboseupdate(); dobackup();                            mkdir(dst);           copystat();                              return
              1;                verboseupdate(); unlink(dst);                           mkdir(dst);           copystat();                              return
          1;                    verboseskip();                                                                                                         return

        # src_isreg dst_noent remove_source_files inplace                 : verbosecreate softreplace() or (        copyfile          copystat            unlink(src))
        # src_isreg dst_noent remove_source_files                         : verbosecreate softreplace() or (opentmp copyfile closetmp copystat replacetmp unlink(src))
        # src_isreg dst_noent                     inplace                 : verbosecreate                           copyfile          copystat
        # src_isreg dst_noent                                             : verbosecreate                   opentmp copyfile closetmp copystat replacetmp
        # src_isreg           ignore_existing                             : verboseexists
        # src_isreg dst_isdir remove_source_files backup       inplace    : verboseupdate dobackup softreplace or (        copyfile          copystat            unlink(src))
        # src_isreg dst_isdir remove_source_files backup                  : verboseupdate dobackup softreplace or (opentmp copyfile closetmp copystat replacetmp unlink(src))  # do backup/rmtree before copy because if softreplace works and backup fails, src doesn't exist anymore.
        # src_isreg dst_isdir remove_source_files force|delete inplace    : verboseupdate rmtree   softreplace or (        copyfile          copystat            unlink(src))
        # src_isreg dst_isdir remove_source_files force|delete            : verboseupdate rmtree   softreplace or (opentmp copyfile closetmp copystat replacetmp unlink(src))
        # src_isreg dst_isdir remove_source_files              inplace    : verboseupdate rm       softreplace or (        copyfile          copystat            unlink(src)) # cannot delete non-empty directory: {dst!r} & could not make way for new regular file: {src!r}
        # src_isreg dst_isdir remove_source_files                         : verboseupdate rm       softreplace or (opentmp copyfile closetmp copystat replacetmp unlink(src)) # cannot delete non-empty directory: {dst!r} & could not make way for new regular file: {src!r}
        # src_isreg dst_isdir                     backup       inplace    : verboseupdate dobackup                         copyfile          copystat
        # src_isreg dst_isdir                     backup                  : verboseupdate dobackup                 opentmp copyfile closetmp copystat replacetmp           # do backup/rmtree before copy? safer than copy before backup/rmtree?
        ## src_isreg dst_isdir                     backup                  : verboseupdate                          opentmp copyfile closetmp copystat dobackup replacetmp  # do copy before backup/rmtree? takes more space on device. and if backup fails, we have copied file for nothing.
        # src_isreg dst_isdir                     force|delete inplace    : verboseupdate rmtree                           copyfile          copystat
        # src_isreg dst_isdir                     force|delete            : verboseupdate rmtree                   opentmp copyfile closetmp copystat replacetmp
        # src_isreg dst_isdir                                  inplace    : verboseupdate rm                               copyfile          copystat                         # cannot delete non-empty directory: {dst!r} & could not make way for new regular file: {src!r}
        # src_isreg dst_isdir                                             : verboseupdate rm                       opentmp copyfile closetmp copystat replacetmp              # cannot delete non-empty directory: {dst!r} & could not make way for new regular file: {src!r}
        # src_isreg dst_isreg remove_source_files difffile backup inplace : verboseupdate dobackup softreplace or (        copyfile          copystat            unlink(src))
        # src_isreg dst_isreg remove_source_files difffile backup         : verboseupdate dobackup softreplace or (opentmp copyfile closetmp copystat replacetmp unlink(src))
        # src_isreg dst_isreg remove_source_files difffile        inplace : verboseupdate          softreplace or (        copyfile          copystat            unlink(src))
        # src_isreg dst_isreg remove_source_files difffile                : verboseupdate          softreplace or (opentmp copyfile closetmp copystat replacetmp unlink(src))
        # src_isreg dst_isreg remove_source_files diffstat                : verboseupdate                                                    copystat            unlink(src)
        # src_isreg dst_isreg remove_source_files                         : verboseuptodate                                                                      unlink(src)
        # src_isreg dst_isreg                     difffile backup inplace : verboseupdate dobackup                         copyfile          copystat
        # src_isreg dst_isreg                     difffile backup         : verboseupdate dobackup                 opentmp copyfile closetmp copystat replacetmp
        # src_isreg dst_isreg                     difffile        inplace : verboseupdate                                  copyfile          copystat
        # src_isreg dst_isreg                     difffile                : verboseupdate                          opentmp copyfile closetmp copystat replacetmp
        # src_isreg dst_isreg                     diffstat                : verboseupdate                                                    copystat
        # src_isreg dst_isreg                                             : verboseuptodate
        # src_isreg           remove_source_files          backup inplace : verboseupdate dobackup softreplace or (        copyfile          copystat            unlink(src))
        # src_isreg           remove_source_files          backup         : verboseupdate dobackup softreplace or (opentmp copyfile closetmp copystat replacetmp unlink(src))
        # src_isreg           remove_source_files                 inplace : verboseupdate          softreplace or (        copyfile          copystat            unlink(src))
        # src_isreg           remove_source_files                         : verboseupdate          softreplace or (opentmp copyfile closetmp copystat replacetmp unlink(src))
        # src_isreg                                        backup inplace : verboseupdate dobackup                         copyfile          copystat
        # src_isreg                                        backup         : verboseupdate dobackup                 opentmp copyfile closetmp copystat replacetmp
        # src_isreg                                               inplace : verboseupdate                                  copyfile          copystat
        # src_isreg                                                       : verboseupdate                          opentmp copyfile closetmp copystat replacetmp
        if stat.S_ISREG(src_stats.st_mode):
          if dst_stats is None:
            if remove_source_files:
              if inplace:       verbosecreate();                      softreplace(src, dst) or (           copyfileinplace(src, dst),                copystat(),                  unlink(src)); return
              1;                verbosecreate();                      softreplace(src, dst) or (opentmp(), copyfileinplace(src, tmpf), closetmp(),   copystattmp(), replacetmp(), unlink(src)); return
            if   inplace:       verbosecreate();                                                           copyfileinplace(src, dst);                copystat();                                return
            1;                  verbosecreate();                                                opentmp(); copyfileinplace(src, tmpf); closetmp();   copystattmp(); replacetmp();               return
          if   ignore_existing: verboseexists();                                                                                                                                                return
          if stat.S_ISDIR(dst_stats.st_mode):
            if remove_source_files:
              if backup:
                if inplace:     verboseupdate(); dobackup();          softreplace(src, dst) or (           copyfileinplace(src, dst),                copystat(),                  unlink(src)); return
                1;              verboseupdate(); dobackup();          softreplace(src, dst) or (opentmp(), copyfileinplace(src, tmpf), closetmp(),   copystattmp(), replacetmp(), unlink(src)); return
              if force:
                if inplace:     verboseupdate(); rmtree();            softreplace(src, dst) or (           copyfileinplace(src, dst),                copystat(),                  unlink(src)); return
                1;              verboseupdate(); rmtree();            softreplace(src, dst) or (opentmp(), copyfileinplace(src, tmpf), closetmp(),   copystattmp(), replacetmp(), unlink(src)); return
              if   inplace:     verboseupdate(); rm(dst, dst_lstats); softreplace(src, dst) or (           copyfileinplace(src, dst),                copystat(),                  unlink(src)); return
              1;                verboseupdate(); rm(dst, dst_lstats); softreplace(src, dst) or (opentmp(), copyfileinplace(src, tmpf), closetmp(),   copystattmp(), replacetmp(), unlink(src)); return
            if   backup:
                if inplace:     verboseupdate(); dobackup();                                               copyfileinplace(src, dst);                copystat();                                return
                1;              verboseupdate(); dobackup();                                    opentmp(); copyfileinplace(src, tmpf); closetmp();   copystattmp(); replacetmp();               return
                #1;              verboseupdate();                                                opentmp(); copyfileinplace(src, tmpf); closetmp();   copystattmp(); dobackup(); replacetmp();   return
            if   force:
                if inplace:     verboseupdate(); rmtree();                                                 copyfileinplace(src, dst);                copystat();                                return
                1;              verboseupdate(); rmtree();                                      opentmp(); copyfileinplace(src, tmpf); closetmp();   copystattmp(); replacetmp();               return
                #1;              verboseupdate();                                                opentmp(); copyfileinplace(src, tmpf); closetmp();   copystattmp(); rmtree();   replacetmp();   return
            if     inplace:     verboseupdate(); rm(dst, dst_lstats);                                      copyfileinplace(src, dst);                copystat();                                return
            1;                  verboseupdate(); rm(dst, dst_lstats);                           opentmp(); copyfileinplace(src, tmpf); closetmp();   copystattmp(); replacetmp();               return
          if stat.S_ISREG(dst_stats.st_mode):
            if remove_source_files:
              if difffile():
                if backup:
                  if inplace: verboseupdate(); dobackup(); softreplace(src, dst) or (           copyfileinplace(src, dst),                copystat(),                  unlink(src)); return
                  1;          verboseupdate(); dobackup(); softreplace(src, dst) or (opentmp(), copyfileinplace(src, tmpf), closetmp(),   copystattmp(), replacetmp(), unlink(src)); return
                if   inplace: verboseupdate();             softreplace(src, dst) or (           copyfileinplace(src, dst),                copystat(),                  unlink(src)); return
                1;            verboseupdate();             softreplace(src, dst) or (opentmp(), copyfileinplace(src, tmpf), closetmp(),   copystattmp(), replacetmp(), unlink(src)); return
              if diffstat():  verboseupdate();                                                                                            copystat();                  unlink(src);  return
              1;              verboseuptodate();                                                                                                                       unlink(src);  return
            if   difffile():
                if backup:
                  if inplace: verboseupdate(); dobackup();                                      copyfileinplace(src, dst);                copystat();                                return
                  1;          verboseupdate(); dobackup();                           opentmp(); copyfileinplace(src, tmpf); closetmp();   copystattmp(); replacetmp();               return
                if   inplace: verboseupdate();                                                  copyfileinplace(src, dst);                copystat();                                return
                1;            verboseupdate();                                       opentmp(); copyfileinplace(src, tmpf); closetmp();   copystattmp(); replacetmp();               return
            if   diffstat():  verboseupdate();                                                                                            copystat();                                return
            1;                verboseuptodate();                                                                                                                                     return
          if   remove_source_files:
                if backup:
                  if inplace: verboseupdate(); dobackup(); softreplace(src, dst) or (           copyfileinplace(src, dst),                copystat(),                  unlink(src)); return
                  1;          verboseupdate(); dobackup(); softreplace(src, dst) or (opentmp(), copyfileinplace(src, tmpf), closetmp(),   copystattmp(), replacetmp(), unlink(src)); return
                if   inplace: verboseupdate();             softreplace(src, dst) or (           copyfileinplace(src, dst),                copystat(),                  unlink(src)); return
                1;            verboseupdate();             softreplace(src, dst) or (opentmp(), copyfileinplace(src, tmpf), closetmp(),   copystattmp(), replacetmp(), unlink(src)); return
          if       backup:
                  if inplace: verboseupdate(); dobackup();                                      copyfileinplace(src, dst);                copystat();                                return
                  1;          verboseupdate(); dobackup();                           opentmp(); copyfileinplace(src, tmpf); closetmp();   copystattmp(); replacetmp();               return
          if         inplace: verboseupdate();                                                  copyfileinplace(src, dst);                copystat();                                return
          1;                  verboseupdate();                                       opentmp(); copyfileinplace(src, tmpf); closetmp();   copystattmp(); replacetmp();               return


        # src_islnk links dst_noent remove_source_files                         : verbosecreate softreplace or (symlink copystat unlink(src))
        # src_islnk links dst_noent                                             : verbosecreate                 symlink copystat
        # src_islnk links           ignore_existing                             : verboseexists
        # src_islnk links dst_isdir remove_source_files backup       inplace    : verboseupdate dobackup softreplace or (      symlink copystat            unlink(src))
        # src_islnk links dst_isdir remove_source_files backup                  : verboseupdate dobackup softreplace or (mktmp symlink copystat replacetmp unlink(src))  # do backup/rmtree before copy because if softreplace works and backup fails, src doesn't exist anymore.
        # src_islnk links dst_isdir remove_source_files force|delete inplace    : verboseupdate rmtree   softreplace or (      symlink copystat            unlink(src))
        # src_islnk links dst_isdir remove_source_files force|delete            : verboseupdate rmtree   softreplace or (mktmp symlink copystat replacetmp unlink(src))
        # src_islnk links dst_isdir remove_source_files              inplace    : verboseupdate rm       softreplace or (      symlink copystat            unlink(src)) # cannot delete non-empty directory: {dst!r}
        # src_islnk links dst_isdir remove_source_files                         : verboseupdate rm       softreplace or (mktmp symlink copystat replacetmp unlink(src)) # cannot delete non-empty directory: {dst!r}
        # src_islnk links dst_isdir                     backup       inplace    : verboseupdate dobackup symlink copystat
        # src_islnk links dst_isdir                     backup                  : verboseupdate dobackup symlink copystat replacetmp
        # src_islnk links dst_isdir                     force|delete inplace    : verboseupdate rmtree   symlink copystat
        # src_islnk links dst_isdir                     force|delete            : verboseupdate rmtree   symlink copystat replacetmp
        # src_islnk links dst_isdir                                  inplace    : verboseupdate rm                             symlink copystat            unlink(src)  # cannot delete non-empty directory: {dst!r}
        # src_islnk links dst_isdir                                             : verboseupdate rm                       mktmp symlink copystat replacetmp unlink(src)  # cannot delete non-empty directory: {dst!r}
        # src_islnk links dst_islnk remove_source_files difflink backup inplace : verboseupdate dobackup softreplace or (      symlink copystat            unlink(src))
        # src_islnk links dst_islnk remove_source_files difflink backup         : verboseupdate dobackup softreplace or (mktmp symlink copystat replacetmp unlink(src))
        # src_islnk links dst_islnk remove_source_files difflink        inplace : verboseupdate          softreplace or (      symlink copystat            unlink(src))
        # src_islnk links dst_islnk remove_source_files difflink                : verboseupdate          softreplace or (mktmp symlink copystat replacetmp unlink(src))
        # src_islnk links dst_islnk remove_source_files                         : verboseuptodate                                                          unlink(src)
        # src_islnk links dst_islnk                     difflink backup inplace : verboseupdate dobackup                       symlink copystat
        # src_islnk links dst_islnk                     difflink backup         : verboseupdate dobackup                 mktmp symlink copystat replacetmp
        # src_islnk links dst_islnk                     difflink        inplace : verboseupdate                                symlink copystat
        # src_islnk links dst_islnk                     difflink                : verboseupdate                          mktmp symlink copystat replacetmp
        # src_islnk links dst_islnk                                             : verboseuptodate
        # src_islnk links           remove_source_files backup inplace          : verboseupdate dobackup softreplace or (      symlink copystat            unlink(src))
        # src_islnk links           remove_source_files backup                  : verboseupdate dobackup softreplace or (mktmp symlink copystat replacetmp unlink(src))
        # src_islnk links           remove_source_files        inplace          : verboseupdate          softreplace or (      symlink copystat            unlink(src))
        # src_islnk links           remove_source_files                         : verboseupdate          softreplace or (mktmp symlink copystat replacetmp unlink(src))
        # src_islnk links                               backup inplace          : verboseupdate dobackup                       symlink copystat
        # src_islnk links                               backup                  : verboseupdate dobackup                 mktmp symlink copystat replacetmp
        # src_islnk links                                      inplace          : verboseupdate                                symlink copystat
        # src_islnk links                                                       : verboseupdate                          mktmp symlink copystat replacetmp
        # src_islnk                                                             : verboseskip
        if stat.S_ISLNK(src_stats.st_mode):
          if links:
            if dst_stats is None:
              if remove_source_files: verbosecreate();                      softreplace(src, dst) or (         symlink(readlink(src), dst), copystat(dst_islnk=True),                  unlink(src)); return
              1;                      verbosecreate();                                                         symlink(readlink(src), dst); copystat(dst_islnk=True);                                return
            if   ignore_existing:     verboseexists();                                                                                                                                               return
            if stat.S_ISDIR(dst_stats.st_mode):
              if remove_source_files:
                if backup:
                  if inplace:         verboseupdate(); dobackup();          softreplace(src, dst) or (         symlink(readlink(src), dst), copystat(dst_islnk=True),                  unlink(src)); return
                  1;                  verboseupdate(); dobackup();          softreplace(src, dst) or (mktmp(), symlink(readlink(src), tmp), copystattmp(dst_islnk=True), replacetmp(), unlink(src)); return
                if force:
                  if inplace:         verboseupdate(); rmtree();            softreplace(src, dst) or (         symlink(readlink(src), dst), copystat(dst_islnk=True),                  unlink(src)); return
                  1;                  verboseupdate(); rmtree();            softreplace(src, dst) or (mktmp(), symlink(readlink(src), tmp), copystattmp(dst_islnk=True), replacetmp(), unlink(src)); return
                if   inplace:         verboseupdate(); rm(dst, dst_lstats); softreplace(src, dst) or (         symlink(readlink(src), dst), copystat(dst_islnk=True),                  unlink(src)); return
                1;                    verboseupdate(); rm(dst, dst_lstats); softreplace(src, dst) or (mktmp(), symlink(readlink(src), tmp), copystattmp(dst_islnk=True), replacetmp(), unlink(src)); return
              if   backup:
                  if inplace:         verboseupdate(); dobackup();                                             symlink(readlink(src), dst); copystat(dst_islnk=True);                                return
                  1;                  verboseupdate(); dobackup();                                    mktmp(); symlink(readlink(src), tmp); copystattmp(dst_islnk=True); replacetmp();               return
                  #1;                  verboseupdate();                                                mktmp(); symlink(readlink(src), tmp); copystattmp(dst_islnk=True); dobackup(); replacetmp();   return
              if   force:
                  if inplace:         verboseupdate(); rmtree();                                               symlink(readlink(src), dst); copystat(dst_islnk=True);                                return
                  1;                  verboseupdate(); rmtree();                                      mktmp(); symlink(readlink(src), tmp); copystattmp(dst_islnk=True); replacetmp();               return
                  #1;                  verboseupdate();                                                mktmp(); symlink(readlink(src), tmp); copystattmp(dst_islnk=True); rmtree();   replacetmp();   return
              if     inplace:         verboseupdate(); rm(dst, dst_lstats);                                    symlink(readlink(src), dst); copystat(dst_islnk=True);                                return
              1;                      verboseupdate(); rm(dst, dst_lstats);                           mktmp(); symlink(readlink(src), tmp); copystattmp(dst_islnk=True); replacetmp();               return
            if stat.S_ISLNK(dst_stats.st_mode):
              if remove_source_files:
                if difflink():
                  if backup:
                    if inplace:       verboseupdate(); dobackup(); softreplace(src, dst) or (         symlink(_readlink, dst),     copystat(dst_islnk=True),                  unlink(src)); return
                    1;                verboseupdate(); dobackup(); softreplace(src, dst) or (mktmp(), symlink(_readlink, tmp),     copystattmp(dst_islnk=True), replacetmp(), unlink(src)); return
                  if   inplace:       verboseupdate();             softreplace(src, dst) or (         symlink(_readlink, dst),     copystat(dst_islnk=True),                  unlink(src)); return
                  1;                  verboseupdate();             softreplace(src, dst) or (mktmp(), symlink(_readlink, tmp),     copystattmp(dst_islnk=True), replacetmp(), unlink(src)); return
                1;                    verboseuptodate();                                                                                                                      unlink(src);  return
              if   difflink():
                  if backup:
                    if inplace:       verboseupdate(); dobackup();                                    symlink(_readlink, dst);     copystat(dst_islnk=True);                                return
                    1;                verboseupdate(); dobackup();                           mktmp(); symlink(_readlink, tmp);     copystattmp(dst_islnk=True); replacetmp();               return
                  if   inplace:       verboseupdate();                                                symlink(_readlink, dst);     copystat(dst_islnk=True);                                return
                  1;                  verboseupdate();                                       mktmp(); symlink(_readlink, tmp);     copystattmp(dst_islnk=True); replacetmp();               return
              1;                      verboseuptodate();                                                                                                                                    return
            if   remove_source_files:
                  if backup:
                    if inplace:       verboseupdate(); dobackup(); softreplace(src, dst) or (         symlink(readlink(src), dst), copystat(dst_islnk=True),                  unlink(src)); return
                    1;                verboseupdate(); dobackup(); softreplace(src, dst) or (mktmp(), symlink(readlink(src), tmp), copystattmp(dst_islnk=True), replacetmp(), unlink(src)); return
                  if   inplace:       verboseupdate();             softreplace(src, dst) or (         symlink(readlink(src), dst), copystat(dst_islnk=True),                  unlink(src)); return
                  1;                  verboseupdate();             softreplace(src, dst) or (mktmp(), symlink(readlink(src), tmp), copystattmp(dst_islnk=True), replacetmp(), unlink(src)); return
            if       backup:
                    if inplace:       verboseupdate(); dobackup();                                    symlink(readlink(src), dst); copystat(dst_islnk=True);                                return
                    1;                verboseupdate(); dobackup();                           mktmp(); symlink(readlink(src), tmp); copystattmp(dst_islnk=True); replacetmp();               return
            if         inplace:       verboseupdate();                                                symlink(readlink(src), dst); copystat(dst_islnk=True);                                return
            1;                        verboseupdate();                                       mktmp(); symlink(readlink(src), tmp); copystattmp(dst_islnk=True); replacetmp();               return
          1;                          verboseskip();                                                                                                                                        return

        # src_isblk devices dst_noent                                  : verbosecreate raise NotImplementedError(f"don't know how to copy device: {src!r}")
        # src_isblk devices           ignore_existing                  : verboseexists
        # src_isblk devices dst_isdir remove_source_files backup       : verboseupdate dobackup softreplace or NIE
        # src_isblk devices dst_isdir remove_source_files force|delete : verboseupdate rmtree   softreplace or NIE
        # src_isblk devices dst_isdir remove_source_files              : verboseupdate rm       softreplace or NIE
        # src_isblk devices dst_isdir                                  : verboseupdate NIE
        # src_isblk devices           remove_source_files backup       : verboseupdate dobackup softreplace or NIE
        # src_isblk devices           remove_source_files              : verboseupdate          softreplace or NIE
        # src_isblk devices                                            : verboseupdate NIE
        # src_isblk                                                    : verboseskip
        # src_ischr devices SAME
        # src_ispip specials SAME
        # src_issoc specials SAME
        t = ""
        if stat.S_ISSOCK(src_stats.st_mode) or stat.S_ISFIFO(src_stats.st_mode):
          if not specials:      verboseskip(); return
          t = "special"
        elif stat.S_ISBLK(src_stats.st_mode) or stat.S_ISCHR(src_stats.st_mode):
          if not devices:       verboseskip(); return
          t = "device"
        if t:
          if dst_stats is None: verbosecreate(); raise NotImplementedError(f"don't know how to copy {t}: {src!r}")
          if   ignore_existing: verboseexists(); return
          if stat.S_ISDIR(dst_stats.st_mode):
            if remove_source_files:
              if backup:        verboseupdate(); dobackup();          softreplace(src, dst) or _raise(NotImplementedError(f"don't know how to copy {t}: {src!r}")); return
              if force:         verboseupdate(); rmtree();            softreplace(src, dst) or _raise(NotImplementedError(f"don't know how to copy {t}: {src!r}")); return
              1;                verboseupdate(); rm(dst, dst_lstats); softreplace(src, dst) or _raise(NotImplementedError(f"don't know how to copy {t}: {src!r}")); return
            1;                  verboseupdate(); raise NotImplementedError(f"don't know how to copy {t}: {src!r}")
          if   remove_source_files:
            if     backup:      verboseupdate(); dobackup(); softreplace(src, dst) or _raise(NotImplementedError(f"don't know how to copy {t}: {src!r}")); return
            1;                  verboseupdate();             softreplace(src, dst) or _raise(NotImplementedError(f"don't know how to copy {t}: {src!r}")); return
          1;                    verboseupdate(); raise NotImplementedError(f"don't know how to copy {t}: {src!r}")

        raise NotImplementedError(f"unhandled node for copy: {src!r}")

      finally:
        if tmpf is not None:
          tmpf.close()
          try: unlink(tmpf.name)
          except OSError: pass
        elif tmp is not None:
          try: unlink(tmp)
          except OSError: pass

    if as_func: return _sync

    if source_directory:  # implies target_directory
      return _sync(src[:0], dst[:0], src, dst, source_directory=True, target_directory=True, follow_symlinks=follow_symlinks, src_noent_ok=src_noent_ok)

    if target_directory:
      src_dir, srcname = _os.path.split(src)
      return _sync(src[:0], dst[:0], src_dir, dst, listdir_src=(srcname,), source_directory=True, target_directory=True, follow_symlinks=follow_symlinks, src_noent_ok=src_noent_ok)

    src_dir, srcname = _os.path.split(src)
    dst_dir, dstname = _os.path.split(dst)
    return _sync(srcname, dstname, src_dir, dst_dir, follow_symlinks=follow_symlinks, src_noent_ok=src_noent_ok)

  def merge(src, dst, **k):
    kw = {"archive": True}
    kw.update(k)
    return fs_sync(src, dst, **kw)

  def mirror(src, dst, **k):
    kw = {"archive": True, "delete": True}
    kw.update(k)
    return fs_sync(src, dst, **kw)

  def clean(src, dst, **k):
    kw = {"recursive": True, "delete": True, "ignore_non_existing": True, "ignore_existing": True, "link": True, "devices": True, "specials": True}
    kw.update(k)
    return fs_sync(src, dst, **kw)

  def move(src, dst, **k):
    kw = {"recursive": True, "remove_source_files": True, "remove_source_dirs": True, "links": True, "devices": True, "specials": True}
    kw.update(k)
    return fs_sync(src, dst, **kw)

  def remove(dst, **k):
    kw = {"remove_source_files": True, "remove_source_dirs": True, "links": True, "devices": True, "specials": True}
    kw.update(k)
    return fs_sync(dst, dst, **kw)

  fs_sync.merge = merge
  fs_sync.mirror = mirror
  fs_sync.clean = clean
  fs_sync.move = move
  fs_sync.remove = remove
  return fs_sync

fs_sync = fs_sync()
fs_sync._required_globals = ["errno", "os", "stat", "sys", "fs_copyfile", "fs_diff", "open2", "opennewfile"]
