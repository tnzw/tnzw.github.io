# fs_sync.py Version 3.0.5
# Copyright (c) 2020-2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

# Idea: make temporary file named like f'{tmp_prefix}{basename}.{random}{tmp_suffix}' where option tmp_prefix could be '.fs_sync.' and option tmp_suffix '.syncing'
# TODO think about these options (other prints or yields?)
#   progress    show progress during transfer → f'{bytes:d} {percent:03d}% {rate: 7.2f}{rate_unit}B/s {hours: 4d}:{minutes:02d}:{seconds:02d}'
#   info=FLAGS  fine-grained informational verbosity
#   info=('progress2',)
#   info=('stats2', 'misc1', 'flist0')
#   info=('flist2', 'name', 'progress')
#   debug=('none',)
#   debug=('del2', 'acl')
# TODO think about time_accuracy option.
#   see XXX in the code next to diffmodifywindow
# TODO add these options
#   copy_dest=PATH       ... and include copies of unchanged files
#   link_dest=PATH       hardlink to files in PATH when unchanged
# TODO add these options if possible
#   copy_unsafe_links    only "unsafe" symlinks are transformed
#   safe_links           ignore symlinks that point outside the source tree
#   munge_links          munge symlinks to make them safer (but unusable)
#   hard_links           preserve hard links
# TODO add option to make rec() to listdir() on src and dst (as usual) plus adding ability to make name matching
#   eg   src/a matches dst/b so sync("src/a" with "dst/b")
def fs_sync():

  def fs_sync(src, dst, *, follow_symlinks=False, source_directory=None, target_directory=None, src_noent_ok=None, content=None, head=None, archive=None, recursive=None, backup=None, backup_dir=None, suffix=None, inplace=None, temp_dir=None, update=None, dirs=None, links=None, copy_links=None, copy_dirlinks=None, keep_dirlinks=None, perms=None, executability=None, chmod=None, owner=None, group=None, devices=None, specials=None, times=None, omit_dir_times=None, omit_link_times=None, dry_run=None, existing=None, ignore_non_existing=None, ignore_existing=None, remove_source_files=None, remove_source_dirs=None, delete=None, force=None, chown=None, ignore_times=None, size_only=None, times_only=None, modify_window=None, src_time_offset=None, exclude=None, include=None, file_matcher=None, yields=None, yield_all=None, yield_info=None, yield_debug=None, yield_nodes=None, yield_sync=None, yield_skip=None, yield_os_calls=None, yield_all_errors=None, yield_sync_errors=None, yield_listdir_errors=None, verbose=None, onverbose=None, ignore_errors=None, ignore_sync_errors=None, ignore_listdir_errors=None, ignore_exdev_errors=None, onerror=None, buffer_size=None, as_func=None, os_module=None):
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
    force                force deletion of dirs even if not empty
    chown=(UID,GID)      affect file and directory username and groupname
    ignore_times         don't skip files that match in size and mod-time
    size_only            skip files that match in size
    times_only           skip files that match in mtime
    modify_window=NUM    compare mod-times with reduced accuracy
    src_time_offset=NUM  use src times with additional seconds
    exclude=FUNC         exclude files if FUNC(common_path) returns True
    include=FUNC         don't exclude files if FUNC(common_path) returns True
    file_matcher=FUNC    don't skip files if not FUNC(src, dst, src_stats, dst_stats)
    buffer_size          used for copying file. Could be either an int or None

    yields               make this function to return a generator object
                         each yield_* options allow to yield info during the
                         process, also allowing some interactions with it.
                         any yield_* options implies yields=True.
                         yield_*_errors options allow some interactions with the
                         process by using send() method right after the yield
                         -> send('ignore'): ignore the error and continue the process
                                            (also works with 'pass' and 'resume')
                         -> send('raise'): raise the error
                         -> send(None): default behavior, no interaction
                         /!\\ ignore_*_errors options prevent these yields
    yield_all            enable all non error yield_* options
    yield_info           enable yield_sync and yield_skip options
    yield_debug          enable yield_nodes and yield_os_calls options
    yield_nodes          yields at every not excluded nodes to be sync'ed  XXX find a better option name?
    yield_sync           yields at every node to node sync start
    yield_skip           yields at every node to node noop operation
    yield_os_calls       yields before every os call, even with dry_run=True
    yield_all_errors     enable all yields_*_errors options
    yield_sync_errors    yields errors on sync error
    yield_listdir_errors  yields errors on listdir calls for recursive sync

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

    ignore_errors        delete even if there are I/O errors
    ignore_sync_errors   ignores failures during a node synchronisation, allowing to continue to next node
    ignore_listdir_errors  ignores failures during the walk in the file tree
    ignore_exdev_errors  fallback to tree copy on replace failures (default True)
    onerror=FUNC         calls onerror(func, args, exc_info) on sync error if ignore_sync_errors is disabled
                         you can retry the node sync by calling func(*args)
                         or you can propagate the active exception by using `raise`

    os_module            the module to use to act on src and dst (defaults to os module)

  Here is a list of os methods and properties used by this tool:

  - os.sep is used for path concatenation (os.altsep could also be used if exists);
  - os.stat(), os.lstat(), os.readlink() are used to compare nodes;
  - os.symlink(), os.utime(), os.chmod(), os.chown(), os.mkdir(), os.unlink(), os.rmdir(), os.replace() are used to create/update/delete nodes;
  - os.open(), os.read(), os.write(), os.close(), os.O_RDONLY, os.O_WRONLY, os.O_CREAT, os.O_TRUNC, os.O_EXCL  (and optionaly os.O_BINARY, os.O_NOINHERIT, os.O_CLOEXEC) are used to copy/compare files content
  - os.listdir() is used when *_directory=True or recursive=True;
  - os.fspath() could be used if paths are not str or bytes;
  - os.fsencode() could be used to get os.sep as bytes if paths are bytes;
  - os.path.split(), os.path.join() is used to generate backup paths, temporary paths, etc.

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
    ########################
    # DEFINE GENERIC TOOLS #
    ########################

    def _raise(error):
      if 0: yield  # enable generator
      raise error  # used to raise in a oneline code
    def _yerr(cmd):  # only called in except blocks
      if cmd in ('ignore', 'resume', 'pass'): return True
      if cmd in ('raise',): raise
      if cmd is None: return False
      raise LookupError(f'invalid yield error command {cmd!r}')
    def pathextend(path, *paths, sep=None, altsep=None):
      paths = [_ for _ in (path,) + paths if _]
      if paths: *paths, last = paths
      else: return path
      lsep = len(sep)  # assuming sep is never empty
      if altsep:
        laltsep = len(altsep)
        paths = [_[:-lsep] if _[-lsep:] == sep else (_[:-laltsep] if _[-laltsep:] == altsep else _) for _ in paths] + [last]
      else:
        paths = [_[:-lsep] if _[-lsep:] == sep else _ for _ in paths] + [last]
      return sep.join(paths)
    #def countendswith(s, suffix):
    #  l = len(suffix)
    #  i = 0
    #  while s.endswith(suffix): i, s = i + 1, s[:-l]
    #  return i

    ######################################
    # CHECK PARAMETERS AND SET SYNC VARS #
    ######################################

    _os = os if os_module is None else os_module
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
      if suffix is None: suffix = b'~' if isinstance(dst, bytes) else '~'
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
    # any yield_*=True implies yields=True
    if yield_all:
      if yield_info is None: yield_info = True
      if yield_debug is None: yield_debug = True
      if yield_nodes is None: yield_nodes = True
      if yield_sync is None: yield_sync = True
      if yield_skip is None: yield_skip = True
      if yield_os_calls is None: yield_os_calls = True
    if yield_info:
      if yield_sync is None: yield_sync = True
      if yield_skip is None: yield_skip = True
    if yield_debug:
      if yield_nodes is None: yield_nodes = True
      if yield_os_calls is None: yield_os_calls = True
    if yield_all_errors:
      if yield_sync_errors is None: yield_sync_errors = True
      if yield_listdir_errors is None: yield_listdir_errors = True
    if (yields or
        yield_all or yield_info or yield_debug or
        yield_nodes or yield_sync or yield_skip or yield_os_calls or
        yield_all_errors or
        yield_sync_errors or yield_listdir_errors):
      if yields is None: yields = True
      elif not yields: raise ValueError('yields=False conflicts with any yield_*=True')
      cast_sync = None
    else:
      def cast_sync(*a, **k):
        for _ in _sync(*a, **k): raise RuntimeError(f'_sync() should not yield anything! → {_!r}')
        #for _ in _sync(*a, **k): pass  # for debug
        #for _ in _sync(*a, **k): print('WARNING CAST', _)  # for debug
    if not isinstance(verbose, int): verbose = 1 if verbose else 0
    if verbose and onverbose is None:
      def onverbose(*a): print(': '.join(getattr(_, 'decode', lambda a,b: str(_))('UTF-8', 'replace') for _ in a))
    if ignore_non_existing is None: ignore_non_existing = existing
    #elif existing is not None and bool(ignore_non_existing) != bool(existing): raise TypeError()
    if ignore_exdev_errors is None: ignore_exdev_errors = True

    src + dst
    if backup_dir and not isinstance(backup_dir, (str, bytes)): backup_dir = _os.fspath(backup_dir); dst + backup_dir
    if temp_dir and not isinstance(temp_dir, (str, bytes)): temp_dir = _os.fspath(temp_dir); dst + temp_dir

    sep = _os.sep
    altsep = getattr(_os, 'altsep', sep) or sep
    if isinstance(src, bytes): fsencode = _os.fsencode; sep = fsencode(sep); altsep = fsencode(altsep); del fsencode

    custom_check = True if size_only or times_only or update or content or head is not None or file_matcher else False

    def   _sync(    srcname, dstname, src_dir,         dst_dir,         src_lstats=None,       dst_lstats=None,       src_stats=None,      dst_stats=None,      _in_delete=False,      _in_backup=False,      follow_symlinks=False,           custom_check=custom_check, _src_dirlist=None,         _dst_dirlist=None,         source_directory=False,            target_directory=False,            src_noent_ok=True,         content=content, head=head, recursive=recursive, backup=backup, backup_dir=backup_dir, suffix=suffix, inplace=inplace, temp_dir=temp_dir, update=update, dirs=dirs,  links=links, copy_links=copy_links, copy_dirlinks=copy_dirlinks, keep_dirlinks=keep_dirlinks, perms=perms, executability=executability, chmod=chmod, owner=owner, group=group, devices=devices, specials=specials, times=times, omit_dir_times=omit_dir_times, omit_link_times=omit_link_times, _omit_link_copystat=_omit_link_copystat, dry_run=dry_run, ignore_non_existing=ignore_non_existing, ignore_existing=ignore_existing, remove_source_files=remove_source_files, remove_source_dirs=remove_source_dirs, delete=delete, force=force, chown=chown, chown_uid=chown_uid, chown_gid=chown_gid, ignore_times=ignore_times, size_only=size_only, times_only=times_only, modify_window=modify_window, src_time_offset=src_time_offset, exclude=exclude,         include=include,         file_matcher=file_matcher, yield_nodes=yield_nodes, yield_sync=yield_sync, yield_skip=yield_skip, yield_os_calls=yield_os_calls, yield_sync_errors=yield_sync_errors, yield_listdir_errors=yield_listdir_errors, _top_verbose=True,         verbose=verbose, onverbose=onverbose, ignore_errors=ignore_errors, ignore_sync_errors=ignore_sync_errors, ignore_listdir_errors=ignore_listdir_errors, ignore_exdev_errors=ignore_exdev_errors, onerror=onerror, buffer_size=buffer_size, os_module=os_module, _os=_os,  sep=sep,  altsep=altsep):
      return   sync(  # [..] propagating some parameters to `sync()` (parent parameters are kept)
                    # line below produces a very long stacktrace line, prefer to explain with the line just above.
                    srcname, dstname, src_dir=src_dir, dst_dir=dst_dir, src_lstats=src_lstats, dst_lstats=dst_lstats, src_stats=src_stats, dst_stats=dst_stats, _in_delete=_in_delete, _in_backup=_in_backup, follow_symlinks=follow_symlinks, custom_check=custom_check, _src_dirlist=_src_dirlist, _dst_dirlist=_dst_dirlist, source_directory=source_directory, target_directory=target_directory, src_noent_ok=src_noent_ok, content=content, head=head, recursive=recursive, backup=backup, backup_dir=backup_dir, suffix=suffix, inplace=inplace, temp_dir=temp_dir, update=update, dirs=dirs,  links=links, copy_links=copy_links, copy_dirlinks=copy_dirlinks, keep_dirlinks=keep_dirlinks, perms=perms, executability=executability, chmod=chmod, owner=owner, group=group, devices=devices, specials=specials, times=times, omit_dir_times=omit_dir_times, omit_link_times=omit_link_times, _omit_link_copystat=_omit_link_copystat, dry_run=dry_run, ignore_non_existing=ignore_non_existing, ignore_existing=ignore_existing, remove_source_files=remove_source_files, remove_source_dirs=remove_source_dirs, delete=delete, force=force, chown=chown, chown_uid=chown_uid, chown_gid=chown_gid, ignore_times=ignore_times, size_only=size_only, times_only=times_only, modify_window=modify_window, src_time_offset=src_time_offset, exclude=exclude,         include=include,         file_matcher=file_matcher, yield_nodes=yield_nodes, yield_sync=yield_sync, yield_skip=yield_skip, yield_os_calls=yield_os_calls, yield_sync_errors=yield_sync_errors, yield_listdir_errors=yield_listdir_errors, _top_verbose=_top_verbose, verbose=verbose, onverbose=onverbose, ignore_errors=ignore_errors, ignore_sync_errors=ignore_sync_errors, ignore_listdir_errors=ignore_listdir_errors, ignore_exdev_errors=ignore_exdev_errors, onerror=onerror, buffer_size=buffer_size, os_module=os_module, _os=_os,  sep=sep,  altsep=altsep)
    if cast_sync is None: cast_sync = _sync
    def sync(       srcname, dstname, src_dir,         dst_dir,         src_lstats=None,       dst_lstats=None,       src_stats=None,      dst_stats=None,      _in_delete=False,      _in_backup=False,      follow_symlinks=False,           custom_check=False,        _src_dirlist=None,         _dst_dirlist=None,         source_directory=False,            target_directory=False,            src_noent_ok=True,         content=False,   head=None, recursive=False,     backup=False,  backup_dir=False,      suffix=None,   inplace=False,   temp_dir=None,     update=False,  dirs=False, links=False, copy_links=False,      copy_dirlinks=False,         keep_dirlinks=False,         perms=False, executability=False,         chmod=None,  owner=False, group=False, devices=False,   specials=False,    times=False, omit_dir_times=False,          omit_link_times=False,           _omit_link_copystat=True,                dry_run=False,   ignore_non_existing=False,               ignore_existing=False,           remove_source_files=False,               remove_source_dirs=False,              delete=False,  force=False, chown=False, chown_uid=-1,        chown_gid=-1,        ignore_times=False,        size_only=False,     times_only=False,      modify_window=None,          src_time_offset=None,            exclude=lambda _: False, include=lambda _: False, file_matcher=None,         yield_nodes=None,        yield_sync=None,       yield_skip=None,       yield_os_calls=None,           yield_sync_errors=None,              yield_listdir_errors=None,                 _top_verbose=True,         verbose=0,       onverbose=None,      ignore_errors=False,         ignore_sync_errors=None,               ignore_listdir_errors=False,                 ignore_exdev_errors=True,                onerror=None,    buffer_size=None,        os_module=None,      _os=None, sep=None, altsep=None):
      def _sync(    srcname, dstname, src_dir,         dst_dir,         src_lstats=None,       dst_lstats=None,       src_stats=None,      dst_stats=None,      _in_delete=_in_delete, _in_backup=_in_backup, follow_symlinks=False,           custom_check=custom_check, _src_dirlist=None,         _dst_dirlist=None,         source_directory=False,            target_directory=False,            src_noent_ok=True,         content=content, head=head, recursive=recursive, backup=backup, backup_dir=backup_dir, suffix=suffix, inplace=inplace, temp_dir=temp_dir, update=update, dirs=dirs,  links=links, copy_links=copy_links, copy_dirlinks=copy_dirlinks, keep_dirlinks=keep_dirlinks, perms=perms, executability=executability, chmod=chmod, owner=owner, group=group, devices=devices, specials=specials, times=times, omit_dir_times=omit_dir_times, omit_link_times=omit_link_times, _omit_link_copystat=_omit_link_copystat, dry_run=dry_run, ignore_non_existing=ignore_non_existing, ignore_existing=ignore_existing, remove_source_files=remove_source_files, remove_source_dirs=remove_source_dirs, delete=delete, force=force, chown=chown, chown_uid=chown_uid, chown_gid=chown_gid, ignore_times=ignore_times, size_only=size_only, times_only=times_only, modify_window=modify_window, src_time_offset=src_time_offset, exclude=exclude,         include=include,         file_matcher=file_matcher, yield_nodes=yield_nodes, yield_sync=yield_sync, yield_skip=yield_skip, yield_os_calls=yield_os_calls, yield_sync_errors=yield_sync_errors, yield_listdir_errors=yield_listdir_errors, _top_verbose=True,         verbose=verbose, onverbose=onverbose, ignore_errors=ignore_errors, ignore_sync_errors=ignore_sync_errors, ignore_listdir_errors=ignore_listdir_errors, ignore_exdev_errors=ignore_exdev_errors, onerror=onerror, buffer_size=buffer_size, os_module=os_module, _os=_os,  sep=sep,  altsep=altsep):
        return sync(  # [..] propagating some parameters to `sync()` (parent parameters are forgotten)
                    # line below produces a very long stacktrace line, prefer to explain with the line just above.
                    srcname, dstname, src_dir=src_dir, dst_dir=dst_dir, src_lstats=src_lstats, dst_lstats=dst_lstats, src_stats=src_stats, dst_stats=dst_stats, _in_delete=_in_delete, _in_backup=_in_backup, follow_symlinks=follow_symlinks, custom_check=custom_check, _src_dirlist=_src_dirlist, _dst_dirlist=_dst_dirlist, source_directory=source_directory, target_directory=target_directory, src_noent_ok=src_noent_ok, content=content, head=head, recursive=recursive, backup=backup, backup_dir=backup_dir, suffix=suffix, inplace=inplace, temp_dir=temp_dir, update=update, dirs=dirs,  links=links, copy_links=copy_links, copy_dirlinks=copy_dirlinks, keep_dirlinks=keep_dirlinks, perms=perms, executability=executability, chmod=chmod, owner=owner, group=group, devices=devices, specials=specials, times=times, omit_dir_times=omit_dir_times, omit_link_times=omit_link_times, _omit_link_copystat=_omit_link_copystat, dry_run=dry_run, ignore_non_existing=ignore_non_existing, ignore_existing=ignore_existing, remove_source_files=remove_source_files, remove_source_dirs=remove_source_dirs, delete=delete, force=force, chown=chown, chown_uid=chown_uid, chown_gid=chown_gid, ignore_times=ignore_times, size_only=size_only, times_only=times_only, modify_window=modify_window, src_time_offset=src_time_offset, exclude=exclude,         include=include,         file_matcher=file_matcher, yield_nodes=yield_nodes, yield_sync=yield_sync, yield_skip=yield_skip, yield_os_calls=yield_os_calls, yield_sync_errors=yield_sync_errors, yield_listdir_errors=yield_listdir_errors, _top_verbose=_top_verbose, verbose=verbose, onverbose=onverbose, ignore_errors=ignore_errors, ignore_sync_errors=ignore_sync_errors, ignore_listdir_errors=ignore_listdir_errors, ignore_exdev_errors=ignore_exdev_errors, onerror=onerror, buffer_size=buffer_size, os_module=os_module, _os=_os,  sep=sep,  altsep=altsep)

      _noerr = True
      src = pathextend(src_dir, srcname, sep=sep, altsep=altsep)
      dst = pathextend(dst_dir, dstname, sep=sep, altsep=altsep)
      src_is_dst = src == dst
      tmp = tmp_fd = None
      _readlink = None

      ##########################
      # DEFINE THIS SYNC TOOLS #
      ##########################

      def samecontent(src, dst, max_length=None, src_stats=None):
        src_fd = dst_fd = None
        try:
          src_fd = yield from fopen_rb(src)
          dst_fd = yield from fopen_rb(dst)
          same = True
          if max_length is None or max_length < 0:
            bufsize = (getattr(src_stats, 'st_blksize', None) or 4096) if buffer_size is None or buffer_size < 0 else buffer_size
            while 1:
              chunk = yield from fread(src_fd, bufsize); chunklen = len(chunk)
              if chunklen == 0:
                if (yield from fread(dst_fd, 1)): same = False
                break
              if chunk != (yield from fread2(dst_fd, chunklen)):
                same = False
                break
          elif max_length == 0: pass
          else:
            bufsize = (getattr(src_stats, 'st_blksize', None) or 4096) if buffer_size is None or buffer_size < 0 else buffer_size
            while max_length > 0:
              chunk = yield from fread(src_fd, min(bufsize, max_length)); chunklen = len(chunk)
              if chunklen == 0:
                if (yield from fread(dst_fd, 1)): same = False
                break
              if chunk != (yield from fread2(dst_fd, chunklen)):
                same = False
                break
              max_length -= chunklen
          dst_fd = yield from fclose(dst_fd)
          src_fd = yield from fclose(src_fd)
          return same
        finally:  # Never yield in a finally! Because yielding after a GeneratorExit() kills the generator and the parent generators too.
          try:
            if dst_fd is not None: fclose_force(dst_fd)
          finally:
            if src_fd is not None: fclose_force(src_fd)

      # XXX in FAT or exFAT case, mtimes are a multiple of 2 ({,ex}FAT accuracy is 2 = 2s, NTFS accuracy is 0.0000001 = 100ns)
      #     if stat returns 1234.028, in reality, physical mtime is 1236 (eg `ceil(mtime)`). (tested with python 3.10.4)
      #     so a copy between two devices may be lossy!
      #     fs_sync should handle it somehow, think about it. Add option `modify_accuracy=2` or `time_accuracy=2`?
      #         if isinstance(time_accuracy, float): raise XXX  # force time_accuracy to be an integer, else undefined system behavior may occur due to float precision
      #         actual_mtime = mtime + mtime % time_accuracy  # not really precise if time_accuracy is a float : 123.4 % 0.2 => 0.19999999999999885 (instead of 0) => 123.4 + 123.4 % 0.2 => 123.60000000000001 => system could write 123.8 (how to check?), do a time_accuracy_ns?
      #     does it solve if fs_sync acts like rsync? I think not, this a different issue.

      def diffmodifywindow(i, j):
        # here, the behavior is different than rsync,
        # eg for modify_window=2, rsync checks `i in [j - 2, j + 2]`, fs_sync checks `i in ]j - 2, j + 2[`.
        # this is to fix the issue while sync'ing two exFAT devices (which time accuracy is 2s), file A (mtime 12) and file B (mtime 10), with modify_window=2, file B should be updated.
        # https://unix.stackexchange.com/questions/461283/why-modify-window-1-when-using-rsync-command
        # https://rsync.samba.org/doxygen/head/util_8c.html#a35
        if modify_window in (None, 0): return i != j
        if i > j: return i - j >= modify_window
        return j - i >= modify_window

      def supmodifywindow(i, j):
        if modify_window in (None, 0): return i > j
        return i - j >= modify_window

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
          if content or head is not None:
            equals = yield from samecontent(src, dst, max_length=head, src_stats=src_stats)  # compare size if not content and head is not None? I think no.
            if not equals: return 1
          return 0

        if ignore_times: return 1
        # rsync "quick check" is check mod-time & size
        if src_stats.st_size != dst_stats.st_size: return 1
        if diffmodifywindow(src_stats.st_mtime + src_time_offset, dst_stats.st_mtime): return 1
        return 0

      def fopen(path, flags):
        #if verbose >= 3: onverbose('open', path, flags)  # XXX
        if yield_os_calls: yield ('os_call', 'open', (path, flags), {})
        return _os.open(path, flags)

      def fopen_rb(path): return fopen(path, _os.O_RDONLY | getattr(_os, 'O_BINARY', 0) | getattr(_os, 'O_NOINHERIT', 0) | getattr(_os, 'O_CLOEXEC', 0))
      def fopen_wb(path): return fopen(path, _os.O_WRONLY | _os.O_CREAT | _os.O_TRUNC | getattr(_os, 'O_BINARY', 0) | getattr(_os, 'O_NOINHERIT', 0) | getattr(_os, 'O_CLOEXEC', 0))
      def fopen_xb(path): return fopen(path, _os.O_WRONLY | _os.O_CREAT | _os.O_EXCL | getattr(_os, 'O_BINARY', 0) | getattr(_os, 'O_NOINHERIT', 0) | getattr(_os, 'O_CLOEXEC', 0))

      def fclose(fd):
        #if verbose >= 3: onverbose('close', fd)  # XXX
        if yield_os_calls: yield ('os_call', 'close', (fd,), {})
        return _os.close(fd)

      def fclose_force(fd):
        return _os.close(fd)

      def fread(fd, size):
        #if verbose >= 3: onverbose('read', fd, size)  # XXX
        if yield_os_calls: yield ('os_call', 'read', (fd, size), {})
        return _os.read(fd, size)

      def fwrite(fd, chunk):
        #if verbose >= 3: onverbose('read', fd, size)  # XXX
        if yield_os_calls: yield ('os_call', 'write', (fd, chunk), {})
        return _os.write(fd, chunk)

      def fread2(fd, size):
        data = yield from fread(fd, size)
        datalen = len(data)
        while datalen < size:
          d = yield from fread(fd, size - datalen)
          if not d: return data
          data += d
          datalen = len(data)
        if datalen > size: raise RuntimeError(f'fs_sync(): fread2(): datalen > size: {datalen!r} > {size!r}')
        return data

      def softlistdir(*a, **k):
        if verbose >= 3: onverbose('listdir', *a, *((k,) if k else ()))
        if yield_os_calls: yield ('os_call', 'listdir', a, k.copy())
        # XXX if yield_actual_os_call: yield ('actual_os_call', 'listdir', a, k.copy())
        try: return _os.listdir(*a, **k)
        except OSError as e:
          if ignore_listdir_errors: return
          if yield_listdir_errors and _yerr((yield ('listdir_error', a, k.copy(), sys.exc_info()))): return
          raise

      def _stat(*a, **k):
        if verbose >= 3: onverbose('stat', *a, *((k,) if k else ()))
        if yield_os_calls: yield ('os_call', 'stat', a, k.copy())
        # XXX if yield_actual_os_call: yield ('actual_os_call', 'stat', a, k.copy())
        return _os.stat(*a, **k)

      def lstat(*a, **k):
        if verbose >= 3: onverbose('lstat', *a, *((k,) if k else ()))
        if yield_os_calls: yield ('os_call', 'lstat', a, k.copy())
        # XXX if yield_actual_os_call: yield ('actual_os_call', 'lstat', a, k.copy())
        return _os.lstat(*a, **k)

      def readlink(*a, **k):
        if verbose >= 3: onverbose('readlink', *a, *((k,) if k else ()))
        if yield_os_calls: yield ('os_call', 'readlink', a, k.copy())
        # XXX if yield_actual_os_call: yield ('actual_os_call', 'readlink', a, k.copy())
        return _os.readlink(*a, **k)

      def symlink(*a, **k):
        if verbose >= 3: onverbose('symlink', *a, *((k,) if k else ()))
        if yield_os_calls: yield ('os_call', 'symlink', a, k.copy())
        if dry_run: return
        # XXX if yield_actual_os_call: yield ('actual_os_call', 'symlink', a, k.copy())
        return _os.symlink(*a, **k)

      def utime(*a, **k):
        if verbose >= 3: onverbose('utime', *a, *((k,) if k else ()))
        if yield_os_calls: yield ('os_call', 'utime', a, k.copy())
        if dry_run: return
        # XXX if yield_actual_os_call: yield ('actual_os_call', 'utime', a, k.copy())
        return _os.utime(*a, **k)

      def _chmod(*a, **k):
        if verbose >= 3: onverbose('chmod', *a, *((k,) if k else ()))
        if yield_os_calls: yield ('os_call', 'chmod', a, k.copy())
        if dry_run: return
        # XXX if yield_actual_os_call: yield ('actual_os_call', 'chmod', a, k.copy())
        return _os.chmod(*a, **k)

      def _chown(*a, **k):
        if verbose >= 3: onverbose('chown', *a, *((k,) if k else ()))
        if yield_os_calls: yield ('os_call', 'chown', a, k.copy())
        if dry_run: return
        # XXX if yield_actual_os_call: yield ('actual_os_call', 'chown', a, k.copy())
        return _os.chown(*a, **k)

      def mkdir(*a, **k):
        if verbose >= 3: onverbose('mkdir', *a, *((k,) if k else ()))
        if yield_os_calls: yield ('os_call', 'mkdir', a, k.copy())
        if dry_run: return
        # XXX if yield_actual_os_call: yield ('actual_os_call', 'mkdir', a, k.copy())
        return _os.mkdir(*a, **k)

      def unlink(*a, **k):
        if verbose >= 3: onverbose('unlink', *a, *((k,) if k else ()))
        if yield_os_calls: yield ('os_call', 'unlink', a, k.copy())
        if dry_run: return
        # XXX if yield_actual_os_call: yield ('actual_os_call', 'unlink', a, k.copy())
        return _os.unlink(*a, **k)

      def unlink_force(*a, **k):
        if dry_run: return
        return _os.unlink(*a, **k)

      def rmdir(*a, **k):
        if verbose >= 3: onverbose('rmdir', *a, *((k,) if k else ()))
        if yield_os_calls: yield ('os_call', 'rmdir', a, k.copy())
        if dry_run: return
        # XXX if yield_actual_os_call: yield ('actual_os_call', 'rmdir', a, k.copy())
        return _os.rmdir(*a, **k)

      def rm(a, s): return rmdir(a) if stat.S_ISDIR(s.st_mode) else unlink(a)

      def replace(*a, **k):
        if verbose >= 3: onverbose('replace', *a, *((k,) if k else ()))
        if yield_os_calls: yield ('os_call', 'replace', a, k.copy())
        if dry_run: return
        # XXX if yield_actual_os_call: yield ('actual_os_call', 'replace', a, k.copy())
        return _os.replace(*a, **k)

      def softrmdir(a, s=None):  # softrmdir() uses unlink (rm()) for symlinks that point to dirs
        try: yield from (rmdir(a) if s is None else rm(a, s))
        except OSError as err:
          if err.errno == errno.ENOTEMPTY: return
          raise

      def softreplace(*a, **k):
        try: yield from replace(*a, **k)
        except OSError as e:
          if e.errno == errno.EXDEV:
            if ignore_exdev_errors: return False
            if yield_exdev_errors and _yerr((yield ('exdev_error', 'replace', a, k.copy(), sys.exc_info()))): return False
          raise
        return True

      def makedirsfor(path, parent, sep, altsep):
        if altsep: path.replace(altsep, sep)
        split = path.split(sep)
        it = iter(split)
        for _ in it: p = _; break
        for _ in it:
          try: yield from mkdir(pathextend(parent, p, sep=sep, altsep=altsep))
          except FileExistsError: pass
          p += sep + _

      def _copystat(dst, src_stats, dst_stats=None, dst_isdir=False, dst_islnk=False):
        # rsync copies the stats in any cases, without doing backup
        # does not update times if update is True and dst >= src
        if dst_islnk and _omit_link_copystat: return  # XXX the goal is to remove this statement
        opt = {"follow_symlinks": False} if dst_islnk else {}
        if chmod is not None:
          if (not dst_stats or (chmod & 0o777) != (dst_stats.st_mode & 0o777)):
            yield from _chmod(dst, chmod & 0o777, **opt)
        elif perms:
          if (not dst_stats or (src_stats.st_mode & 0o777) != (dst_stats.st_mode & 0o777)):
            yield from _chmod(dst, src_stats.st_mode & 0o777, **opt)
        elif executability:
          if (not dst_stats or (src_stats.st_mode & 0o444) != (dst_stats.st_mode & 0o444)):
            yield from _chmod(dst, (src_stats.st_mode & 0o444) | (dst_stats.st_mode & 0o333), **opt)
        if chown:
          if not dst_stats or (chown_uid >= 0 and chown_uid != dst_stats.st_uid) or (chown_gid >= 0 and chown_gid != dst_stats.st_gid):
            yield from _chown(dst, chown_uid, chown_gid, follow_symlinks=False)
        elif (owner and (not dst_stats or src_stats.st_uid != dst_stats.st_uid)) or \
             (group and (not dst_stats or src_stats.st_gid != dst_stats.st_gid)):
          yield from _chown(dst, src_stats.st_uid if owner else -1, src_stats.st_gid if group else -1, follow_symlinks=False)
        if times:
          if omit_dir_times and stat.S_ISDIR(src_stats.st_mode): pass  # better check dst instead?
          elif omit_link_times and dst_islnk: pass  # better check src instead?
          else:
            diff = supmodifywindow if update else diffmodifywindow
            if (dst_isdir or not dst_stats or diff(src_stats.st_mtime + src_time_offset, dst_stats.st_mtime)):
              yield from utime(dst, (src_stats.st_atime + src_time_offset, src_stats.st_mtime + src_time_offset), **opt)

      # XXX review the two methods below for yield_*{,_errors} and ignore_*_errors legitimity
      def _rmtree(name, dir, lstats, dirlist=None): return sync(name, name, src_dir=dir, dst_dir=dir, src_lstats=lstats, dst_lstats=lstats, src_stats=lstats, dst_stats=lstats, _src_dirlist=dirlist, _dst_dirlist=dirlist, _top_verbose=False, _in_delete=True, remove_source_files=True, remove_source_dirs=True, recursive=True, links=True, devices=True, specials=True, custom_check=True, size_only=True, inplace=True, yield_nodes=yield_nodes, yield_sync=yield_sync, yield_os_calls=yield_os_calls, yield_sync_errors=yield_sync_errors, yield_listdir_errors=yield_listdir_errors, verbose=verbose, onverbose=onverbose, ignore_errors=ignore_errors, ignore_sync_errors=ignore_sync_errors, ignore_listdir_errors=ignore_listdir_errors, onerror=onerror, dry_run=dry_run, buffer_size=buffer_size, os_module=os_module, _os=_os, sep=sep, altsep=altsep)
      def _dobackup(s, d, sd, dd, ls): return sync(s, d, src_dir=sd, dst_dir=dd, src_lstats=ls, src_stats=ls, _top_verbose=True, _in_backup=True, remove_source_files=True, remove_source_dirs=True, force=True, recursive=True, dirs=True, links=True, devices=True, specials=True, perms=perms, times=times, group=group, owner=owner, ignore_times=True, inplace=inplace, yield_nodes=yield_nodes, yield_sync=yield_sync, yield_os_calls=yield_os_calls, yield_sync_errors=yield_sync_errors, yield_listdir_errors=yield_listdir_errors, verbose=verbose, onverbose=onverbose, ignore_exdev_errors=ignore_exdev_errors, ignore_errors=ignore_errors, ignore_sync_errors=ignore_sync_errors, ignore_listdir_errors=ignore_listdir_errors, onerror=onerror, dry_run=dry_run, buffer_size=buffer_size, os_module=os_module, _os=_os, sep=sep, altsep=altsep)

      ##############################
      # HELPER FOR YIELD-FROM MESS #
      ##############################

      def OR(*gg):
        ret = None
        for g in gg:
          ret = yield from g
          if ret: return ret
        return ret

      def diffstat():  # copy/paste from _copystat()
        if chmod is not None:
          if (not dst_stats or (chmod & 0o777) != (dst_stats.st_mode & 0o777)):
            return 1
        elif perms:
          if (not dst_stats or (src_stats.st_mode & 0o777) != (dst_stats.st_mode & 0o777)):
            return 1
        elif executability:
          if (not dst_stats or (src_stats.st_mode & 0o444) != (dst_stats.st_mode & 0o444)):
            return 1
        if chown:
          if not dst_stats or (chown_uid >= 0 and chown_uid != dst_stats.st_uid) or (chown_gid >= 0 and chown_gid != dst_stats.st_gid):
            return 1
        elif (owner and (not dst_stats or src_stats.st_uid != dst_stats.st_uid)) or \
             (group and (not dst_stats or src_stats.st_gid != dst_stats.st_gid)):
          return 1
        if times:
          if omit_dir_times and stat.S_ISDIR(src_stats.st_mode): pass  # better check dst instead?
          elif omit_link_times and stat.S_ISLNK(src_stats.st_mode): pass  # better check dst instead?
          else:
            diff = supmodifywindow if update else diffmodifywindow
            if (not dst_stats or diff(src_stats.st_mtime + src_time_offset, dst_stats.st_mtime)):
              return 1
        return 0

      def difflink():
        nonlocal _readlink
        _readlink = (yield from readlink(src))
        return _readlink != (yield from readlink(dst))

      def diffdir():
        if times and not omit_dir_times:
          if update:
            if supmodifywindow(src_stats.st_mtime + src_time_offset, dst_stats.st_mtime): return 1
            return 0
          if diffmodifywindow(src_stats.st_mtime + src_time_offset, dst_stats.st_mtime): return 1
          return 0
        return 0

      def copystat(dst_stats=None, dst_islnk=False): yield from _copystat(dst, src_stats, dst_stats, dst_islnk=dst_islnk)
      def copystatdir(): yield from _copystat(dst, src_stats, dst_stats, dst_isdir=True)
      def copystattmp(dst_islnk=False): yield from _copystat(tmp, src_stats, dst_islnk=dst_islnk)

      def copylink(intmp=False):
        nonlocal _readlink
        if _readlink is None: _readlink = yield from readlink(src)
        yield from symlink(_readlink, tmp if intmp else dst)

      def dobackup():
        if backup_dir:
          yield from makedirsfor(dstname, backup_dir, sep, altsep)
          yield from _dobackup(dstname, dstname, dst_dir, backup_dir, dst_lstats)
        else:  #if suffix:
          yield from _dobackup(dstname, dstname + suffix, dst_dir, dst_dir, dst_lstats)

      def rmtree():
        return _rmtree(dstname, dst_dir, dst_lstats, _dst_dirlist)

      def rec(): return _sync(srcname, dstname, src_dir, dst_dir, source_directory=True, target_directory=True)
      def recsrc(): return _sync(srcname, dstname, src_dir, dst_dir, source_directory=True)

      def opentmp():
        if dry_run: return
        nonlocal tmp_fd
        nonlocal tmp
        dstdir, dstbase = _os.path.split(dst)
        encode = (lambda e: e.encode()) if isinstance(dst, bytes) else (lambda e: e)
        dot = encode('.')
        _ = _os.path.join(temp_dir, dot + dstbase + dot) if temp_dir else _os.path.join(dstdir, dot + dstbase + dot)
        i = 2
        while 1:
          #if i > 4096: raise RuntimeError('maximum iteration reached')
          # rsync uses   ".{basename(dst)}.{random_6_letters()}"
          # here it uses ".{basename(dst)}.{random_4_or_more_hexdigits}"
          path = _ + encode(''.join(f'{b:02x}' for b in os.urandom(i)))
          try: tmp_fd = yield from fopen_xb(path)
          except FileExistsError: pass
          else: tmp = path; break
          i += 1
      def closetmp():
        nonlocal tmp_fd
        if dry_run: return
        tmp_fd = yield from fclose(tmp_fd)
      def mktmp():
        if dry_run: return
        nonlocal tmp
        encode = (lambda e: e.encode()) if isinstance(dst, bytes) else (lambda e: e)
        dot = encode('.')
        dstdir, dstbase = _os.path.split(dst)
        _ = _os.path.join(temp_dir, dot + dstbase + dot) if temp_dir else _os.path.join(dstdir, dot + dstbase + dot)
        i = 2
        while 1:
          #if i > 4096: raise RuntimeError('maximum iteration reached')
          # rsync uses   ".{basename(dst)}.{random_6_letters()}"
          # here it uses ".{basename(dst)}.{random_4_or_more_hexdigits()}"
          path = _ + encode(''.join(f'{b:02x}' for b in os.urandom(i)))
          try: yield from lstat(path)
          except FileNotFoundError: tmp = path; break
          i += 1
      def replacetmp():
        if dry_run: return
        nonlocal tmp
        _tmp = tmp
        tmp = None  # prevent auto removing tmp file from now, so that tmp file stays if replace() fails
        # tmp_fd is normally already closed by caller  # closing sets mtime
        yield from replace(_tmp, dst)  # do not ignore exdev errors here! If this error is raised, then it might be because temp_dir is outside dst filesystem.

      def copyfileinplace(src, dst, src_fd=None, dst_fd=None):
        if dry_run: return
        src_fd_to_close = dst_fd_to_close = None
        try:
          if src_fd is None: src_fd = src_fd_to_close = yield from fopen_rb(src)
          if dst_fd is None: dst_fd = dst_fd_to_close = yield from fopen_wb(dst)
          bufsize = 4096 if buffer_size is None or buffer_size < 0 else buffer_size
          while 1:
            chunk = yield from fread(src_fd, bufsize)
            if chunk: yield from fwrite(dst_fd, chunk)
            else: break
          if dst_fd_to_close is not None: dst_fd_to_close = yield from fclose(dst_fd_to_close)
          if src_fd_to_close is not None: src_fd_to_close = yield from fclose(src_fd_to_close)
        finally:
          try:
            if dst_fd_to_close is not None: fclose_force(dst_fd_to_close)
          finally:
            if src_fd_to_close is not None: fclose_force(src_fd_to_close)

      def copyfileintmp(src):
        yield from copyfileinplace(src, None, None, tmp_fd)

      def yf(*gg):
        verb_yield = None
        if gg:
          match gg[0]:
            case 'create' | 'update': verb_yield = (2, yield_skip, 'skip', 'backup to', dstname) if _in_backup else (1, yield_sync, 'sync', gg[0], dstname)
            case 'delete':            verb_yield = (1, yield_sync, 'sync', gg[0], dstname)
            case 'skip' | 'uptodate': verb_yield = (1, yield_sync, 'sync', 'delete', srcname) if _in_delete else (2, yield_skip, 'skip', gg[0], dstname)
            case 'absent' | 'exists': verb_yield = (2, yield_skip, 'skip', gg[0], dstname)
          if verb_yield: gg = gg[1:]
        ret = None
        if _top_verbose:
          if verbose >= verb_yield[0]: onverbose(*verb_yield[3:])
          if verb_yield[1]: yield verb_yield[2:]
          for g in gg: ret = yield from g
          if verb_yield[1]: yield ('after_' + verb_yield[2], *verb_yield[3:])  # XXX use specific yield option?
        else:
          for g in gg: ret = yield from g
        return ret

      #####################
      # HANDLE PARAMETERS #
      #####################

      if source_directory or target_directory:
        # XXX use normcase for compare? Add a parameter like use_normcase? XXX or add a custom name_key func?! then how can fs_sync create dst path.txt.lnk from src path.txt?
        g = set()
        if _src_dirlist is not None: g.update(_src_dirlist)
        elif source_directory: _src_dirlist = yield from softlistdir(src); g.update(_src_dirlist)
        if _dst_dirlist is not None: g.update(_dst_dirlist)
        elif target_directory:
          if src_is_dst: _dst_dirlist = _src_dirlist
          else: _dst_dirlist = yield from softlistdir(dst); g.update(_dst_dirlist)
        g = sorted(g)  # XXX it's not mandatory to sort. Add an fs_sync parameter for this?
        #if suffix: g = sorted(g, key=lambda k: countendswith(k, suffix))  # backup files MUST be after update files.
        for name in g:
          args = (pathextend(srcname, name, sep=sep, altsep=altsep), pathextend(dstname, name, sep=sep, altsep=altsep), src_dir, dst_dir)
          try: yield from _sync(*args)
          except OSError:
            if ignore_sync_errors: pass
            else:
              if yield_sync_errors and _yerr((yield ('sync_error', _sync, args, sys.exc_info()))): pass  # XXX check if this yield could raise a RuntimeError: generator ignored GeneratorExit()
              elif onerror is not None: onerror(_sync, args, sys.exc_info())  # onerror() should only be used for `try: _sync()`
              else: raise
        return

      #######################################
      # START SYNC'ING src NODE TO dst NODE #
      #######################################

      if exclude(srcname):
        if not include(srcname):
          #XXX if yield_excluded_nodes: yield('exclude', srcname, dstname, src_dir, dst_dir, src, dst)
          return  # do not sync

      #if yield_nodes: yield ('node', srcname, dstname, src_dir, dst_dir, src, dst)  # XXX too much info yielded?

      if src_lstats is None:
        try: src_lstats = yield from lstat(src)
        except (FileNotFoundError, NotADirectoryError):
          if src_noent_ok: pass
          else: raise
        except OSError as e:
          if e.errno == errno.EIO and ignore_errors: pass
          else: raise
      if src_stats is None:
        src_stats = src_lstats
        if src_lstats and stat.S_ISLNK(src_lstats.st_mode):
          if copy_links or follow_symlinks:
            try: src_stats = yield from _stat(src)
            except (FileNotFoundError, NotADirectoryError): src_stats = None
          elif copy_dirlinks:
            try: _ = yield from _stat(src)
            except (FileNotFoundError, NotADirectoryError): pass
            else:
              if stat.S_ISDIR(_.st_mode): src_stats = _
              del _
          #elif copy_unsafe_links XXX

      if dst_lstats is None:
        if src_is_dst: dst_lstats = src_lstats
        else:
          try: dst_lstats = yield from lstat(dst)
          except (FileNotFoundError, NotADirectoryError): pass
      if dst_stats is None:
        # XXX handle src_is_dst? harder than we think (think about copy_links, follow_symlinks, copy_dirlinks, keep_dirlinks, etc)
        dst_stats = dst_lstats
        if keep_dirlinks and dst_lstats and stat.S_ISLNK(dst_lstats.st_mode):
          try: _ = yield from _stat(dst)
          except (FileNotFoundError, NotADirectoryError): pass
          else:
            if stat.S_ISDIR(_.st_mode): dst_stats = _
            del _

      if yield_nodes: yield ('node', srcname, dstname, src_dir, dst_dir, src, dst, src_lstats, dst_lstats, src_stats, dst_stats)  # XXX too much info yielded?

      try:

        #           dst_noent ignore_non_existing                    : verboseabsent  # remove_source_* has no effect here
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
        if   dst_stats is None and ignore_non_existing: yield from yf('absent'              ); return
        if src_stats is None:
          if dst_stats is None: yield from yf(                        'uptodate'            ); return
          if   ignore_existing: yield from yf(                        'exists'              ); return
          if stat.S_ISDIR(dst_stats.st_mode):
            if dirs:
              if delete:
                if suffix and dstname.endswith(suffix): yield from yf('skip'                ); return
                if backup: yield from yf(                             'delete',  dobackup() ); return
                yield from yf(                                        'delete',  rmtree()   ); return
              yield from yf(                                          'skip'                ); return
            yield from yf(                                            'skip'                ); return
          if     delete:
                if suffix and dstname.endswith(suffix): yield from yf('skip'                ); return
                if backup: yield from yf(                             'delete',  dobackup() ); return
                yield from yf(                                        'delete',  unlink(dst)); return
          yield from yf(                                              'skip'                ); return

        # src_isdir dst_noent remove_source_dirs recursive         : verbosecreate softreplace or (mkdir() rec() copystat() softrmdir(src,lstats))  # copystat() with remove_source_{dirs|files}+recursive might have unexpected behavior.
        # src_isdir dst_noent remove_source_dirs dirs              : verbosecreate                 mkdir()       copystat() softrmdir(src,lstats)
        # src_isdir dst_noent remove_source_dirs                   : verboseskip                                            softrmdir(src,lstats)
        # src_isdir dst_noent                    recursive         : verbosecreate mkdir() rec() copystat()
        # src_isdir dst_noent                    dirs              : verbosecreate mkdir()       copystat()
        # src_isdir dst_noent                                      : verboseskip
        # src_isdir dst_isdir ignore_existing    recursive         : verboseexists   rec copystatdir()  # copystat() on ignore_existing? yes, rsync behavior.
        # src_isdir dst_isdir ignore_existing    dirs              : verboseexists
        # src_isdir dst_isdir ignore_existing                      : verboseskip
        # src_isdir dst_isdir remove_source_dirs recursive diffdir : verboseupdate   rec copystatdir() softrmdir(src,lstats)
        # src_isdir dst_isdir remove_source_dirs recursive         : verboseuptodate rec copystatdir() softrmdir(src,lstats)
        # src_isdir dst_isdir remove_source_dirs dirs      diffdir : verboseupdate       copystatdir() softrmdir(src,lstats)
        # src_isdir dst_isdir remove_source_dirs dirs              : verboseuptodate     copystatdir() softrmdir(src,lstats)
        # src_isdir dst_isdir remove_source_dirs                   : verboseskip                       softrmdir(src,lstats)
        # src_isdir dst_isdir                    recursive diffdir : verboseupdate   rec copystatdir()
        # src_isdir dst_isdir                    recursive         : verboseuptodate rec copystatdir()
        # src_isdir dst_isdir                    dirs      diffdir : verboseupdate       copystatdir()
        # src_isdir dst_isdir                    dirs              : verboseuptodate     copystatdir()
        # src_isdir dst_isdir                                      : verboseskip
        # src_isdir           ignore_existing                      : verboseexists  # with recursive and when src_isdir, rsync goes down src dir... but why?
        # src_isdir           remove_source_dirs recursive backup  : verboseupdate dobackup()  softreplace() or (mkdir() rec() copystat() softrmdir(src,lstats))
        # src_isdir           remove_source_dirs recursive         : verboseupdate unlink(dst) softreplace() or (mkdir() rec() copystat() softrmdir(src,lstats))  # copytree before replace? inplace does not matter for src_isdir?
        # src_isdir           remove_source_dirs dirs      backup  : verboseupdate dobackup()                    mkdir()       copystat() softrmdir(src,lstats)   # XXX softreplace if src dir is empty?
        # src_isdir           remove_source_dirs dirs              : verboseupdate unlink(dst)                   mkdir()       copystat() softrmdir(src,lstats)   # XXX softreplace if src dir is empty?
        # src_isdir           remove_source_dirs                   : verboseskip                                                          softrmdir(src,lstats)
        # src_isdir                              recursive backup  : verboseupdate dobackup()                    mkdir() rec() copystat()
        # src_isdir                              recursive         : verboseupdate unlink(dst)                   mkdir() rec() copystat()
        # src_isdir                              dirs      backup  : verboseupdate dobackup()                    mkdir()       copystat()
        # src_isdir                              dirs              : verboseupdate unlink(dst)                   mkdir()       copystat()
        # src_isdir                                                : verboseskip
        if stat.S_ISDIR(src_stats.st_mode):
          if dst_stats is None:
            if remove_source_dirs:
              if recursive: yield from yf(    'create',              OR(softreplace(src, dst), yf(mkdir(dst), recsrc(), copystat(),    softrmdir(src, src_lstats)))); return
              if dirs: yield from yf(         'create',                                           mkdir(dst), recsrc(), copystat(),    softrmdir(src, src_lstats)  ); return
              yield from yf(                  'skip',                                                                                  softrmdir(src, src_lstats)  ); return
            if   recursive: yield from yf(    'create',                                           mkdir(dst), recsrc(), copystat()                                 ); return
            if   dirs: yield from yf(         'create',                                           mkdir(dst),           copystat()                                 ); return
            yield from yf(                    'skip'                                                                                                               ); return
          if stat.S_ISDIR(dst_stats.st_mode):
            if ignore_existing:
              if recursive: yield from yf(    'exists',                                                       rec(),    copystatdir()                              ); return
              if dirs: yield from yf(         'exists',                                                                                                            ); return
              yield from yf(                  'skip',                                                                                                              ); return
            if remove_source_dirs:
              if recursive:
                if diffdir(): yield from yf(  'update',                                                       rec(),    copystatdir(), softrmdir(src, src_lstats)  ); return
                yield from yf(                'uptodate',                                                     rec(),    copystatdir(), softrmdir(src, src_lstats)  ); return
              if dirs:
                if diffdir(): yield from yf(  'update',                                                                 copystatdir(), softrmdir(src, src_lstats)  ); return
                yield from yf(                'uptodate',                                                               copystatdir(), softrmdir(src, src_lstats)  ); return
              yield from yf(                  'skip',                                                                                  softrmdir(src, src_lstats)  ); return
            if   recursive:
                if diffdir(): yield from yf(  'update',                                                       rec(),    copystatdir()                              ); return
                yield from yf(                'uptodate',                                                     rec(),    copystatdir()                              ); return
            if   dirs:
                if diffdir(): yield from yf(  'update',                                                                 copystatdir()                              ); return
                yield from yf(                'uptodate',                                                               copystatdir()                              ); return
            yield from yf(                    'skip'                                                                                                               ); return
          if   ignore_existing: yield from yf('exists'                                                                                                             ); return
          if   remove_source_dirs:
            if recursive:
              if backup: yield from yf(       'update', dobackup(),  OR(softreplace(src, dst), yf(mkdir(dst), recsrc(), copystat(),    softrmdir(src, src_lstats)))); return
              yield from yf(                  'update', unlink(dst), OR(softreplace(src, dst), yf(mkdir(dst), recsrc(), copystat(),    softrmdir(src, src_lstats)))); return
            if dirs:
              if backup: yield from yf(       'update', dobackup(),                               mkdir(dst),           copystat(),    softrmdir(src, src_lstats)  ); return
              yield from yf(                  'update', unlink(dst),                              mkdir(dst),           copystat(),    softrmdir(src, src_lstats)  ); return
            yield from yf(                    'skip',                                                                                  softrmdir(src, src_lstats)  ); return
          if   recursive:
              if backup: yield from yf(       'update', dobackup(),                               mkdir(dst), recsrc(), copystat()                                 ); return
              yield from yf(                  'update', unlink(dst),                              mkdir(dst), recsrc(), copystat()                                 ); return
          if   dirs:
              if backup: yield from yf(       'update', dobackup(),                               mkdir(dst),           copystat()                                 ); return
              yield from yf(                  'update', unlink(dst),                              mkdir(dst),           copystat()                                 ); return
          yield from yf(                      'skip'                                                                                                               ); return

        # src_isreg dst_noent remove_source_files inplace                 : verbosecreate softreplace() or (        copyfile          copystat            unlink(src))
        # src_isreg dst_noent remove_source_files                         : verbosecreate softreplace() or (opentmp copyfile closetmp copystat replacetmp unlink(src))
        # src_isreg dst_noent                     inplace                 : verbosecreate                           copyfile          copystat
        # src_isreg dst_noent                                             : verbosecreate                   opentmp copyfile closetmp copystat replacetmp
        # src_isreg           ignore_existing                             : verboseexists
        # src_isreg dst_isdir remove_source_files backup       inplace    : verboseupdate dobackup softreplace or (        copyfile          copystat            unlink(src))
        # src_isreg dst_isdir remove_source_files backup                  : verboseupdate dobackup softreplace or (opentmp copyfile closetmp copystat replacetmp unlink(src))  # do backup/rmtree before copy because if softreplace works and backup fails, src doesn't exist anymore.
        # src_isreg dst_isdir remove_source_files force|delete inplace    : verboseupdate rmtree   softreplace or (        copyfile          copystat            unlink(src))
        # src_isreg dst_isdir remove_source_files force|delete            : verboseupdate rmtree   softreplace or (opentmp copyfile closetmp copystat replacetmp unlink(src))
        # src_isreg dst_isdir remove_source_files              inplace    : verboseupdate rm       softreplace or (        copyfile          copystat            unlink(src))  # cannot delete non-empty directory: {dst!r} & could not make way for new regular file: {src!r}
        # src_isreg dst_isdir remove_source_files                         : verboseupdate rm       softreplace or (opentmp copyfile closetmp copystat replacetmp unlink(src))  # cannot delete non-empty directory: {dst!r} & could not make way for new regular file: {src!r}
        # src_isreg dst_isdir                     backup       inplace    : verboseupdate dobackup                         copyfile          copystat
        # src_isreg dst_isdir                     backup                  : verboseupdate dobackup                 opentmp copyfile closetmp copystat replacetmp               # do backup/rmtree before copy? safer than copy before backup/rmtree?
        ## src_isreg dst_isdir                     backup                  : verboseupdate                          opentmp copyfile closetmp copystat dobackup replacetmp      # do copy before backup/rmtree? takes more space on device. and if backup fails, we have copied file for nothing.
        # src_isreg dst_isdir                     force|delete inplace    : verboseupdate rmtree                           copyfile          copystat
        # src_isreg dst_isdir                     force|delete            : verboseupdate rmtree                   opentmp copyfile closetmp copystat replacetmp
        # src_isreg dst_isdir                                  inplace    : verboseupdate rm                               copyfile          copystat                          # cannot delete non-empty directory: {dst!r} & could not make way for new regular file: {src!r}
        # src_isreg dst_isdir                                             : verboseupdate rm                       opentmp copyfile closetmp copystat replacetmp               # cannot delete non-empty directory: {dst!r} & could not make way for new regular file: {src!r}
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
              if inplace: yield from yf(       'create',                      OR(softreplace(src, dst), yf(           copyfileinplace(src, dst),               copystat(),                  unlink(src)))); return
              yield from yf(                   'create',                      OR(softreplace(src, dst), yf(opentmp(), copyfileintmp(src),        closetmp(),   copystattmp(), replacetmp(), unlink(src)))); return
            if   inplace: yield from yf(       'create',                                                              copyfileinplace(src, dst),               copystat()                                ); return
            yield from yf(                     'create',                                                   opentmp(), copyfileintmp(src),        closetmp(),   copystattmp(), replacetmp()               ); return
          if   ignore_existing: yield from yf ('exists'                                                                                                                                                  ); return
          if stat.S_ISDIR(dst_stats.st_mode):
            if remove_source_files:
              if backup:
                if inplace: yield from yf(     'update', dobackup(),          OR(softreplace(src, dst), yf(           copyfileinplace(src, dst),               copystat(),                  unlink(src)))); return
                yield from yf(                 'update', dobackup(),          OR(softreplace(src, dst), yf(opentmp(), copyfileintmp(src),        closetmp(),   copystattmp(), replacetmp(), unlink(src)))); return
              if force:
                if inplace: yield from yf(     'update', rmtree(),            OR(softreplace(src, dst), yf(           copyfileinplace(src, dst),               copystat(),                  unlink(src)))); return
                yield from yf(                 'update', rmtree(),            OR(softreplace(src, dst), yf(opentmp(), copyfileintmp(src),        closetmp(),   copystattmp(), replacetmp(), unlink(src)))); return
              if   inplace: yield from yf(     'update', rm(dst, dst_lstats), OR(softreplace(src, dst), yf(           copyfileinplace(src, dst),               copystat(),                  unlink(src)))); return
              yield from yf(                   'update', rm(dst, dst_lstats), OR(softreplace(src, dst), yf(opentmp(), copyfileintmp(src),        closetmp(),   copystattmp(), replacetmp(), unlink(src)))); return
            if   backup:
                if inplace: yield from yf(     'update', dobackup(),                                                  copyfileinplace(src, dst),               copystat()                                ); return
                yield from yf(                 'update', dobackup(),                                       opentmp(), copyfileintmp(src),        closetmp(),   copystattmp(), replacetmp()               ); return
                #yield from yf(                 'update',                                                   opentmp(), copyfileintmp(src),        closetmp(),   copystattmp(), dobackup(), replacetmp()   ); return
            if   force:
                if inplace: yield from yf(     'update', rmtree(),                                                    copyfileinplace(src, dst),               copystat()                                ); return
                yield from yf(                 'update', rmtree(),                                         opentmp(), copyfileintmp(src),        closetmp(),   copystattmp(), replacetmp()               ); return
                #yield from yf(                 'update',                                                   opentmp(), copyfileintmp(src),        closetmp(),   copystattmp(), rmtree(),    replacetmp()  ); return
            if     inplace: yield from yf(     'update', rm(dst, dst_lstats),                                         copyfileinplace(src, dst),               copystat()                                ); return
            yield from yf(                     'update', rm(dst, dst_lstats),                              opentmp(), copyfileintmp(src),        closetmp(),   copystattmp(), replacetmp()               ); return
          if stat.S_ISREG(dst_stats.st_mode):
            if remove_source_files:
              if (yield from difffile()):
                if backup:
                  if inplace: yield from yf(   'update', dobackup(),          OR(softreplace(src, dst), yf(           copyfileinplace(src, dst),               copystat(),                  unlink(src)))); return
                  yield from yf(               'update', dobackup(),          OR(softreplace(src, dst), yf(opentmp(), copyfileintmp(src),        closetmp(),   copystattmp(), replacetmp(), unlink(src)))); return
                if   inplace: yield from yf(   'update',                      OR(softreplace(src, dst), yf(           copyfileinplace(src, dst),               copystat(),                  unlink(src)))); return
                yield from yf(                 'update',                      OR(softreplace(src, dst), yf(opentmp(), copyfileintmp(src),        closetmp(),   copystattmp(), replacetmp(), unlink(src)))); return
              if diffstat(): yield from yf(    'update',                                                                                                       copystat(),                  unlink(src)  ); return
              yield from yf(                   'uptodate',                                                                                                                                  unlink(src)  ); return
            if   (yield from difffile()):
                if backup:
                  if inplace: yield from yf(   'update', dobackup(),                                                  copyfileinplace(src, dst),               copystat()                                ); return
                  yield from yf(               'update', dobackup(),                                       opentmp(), copyfileintmp(src),        closetmp(),   copystattmp(), replacetmp()               ); return
                if   inplace: yield from yf(   'update',                                                              copyfileinplace(src, dst),               copystat()                                ); return
                yield from yf(                 'update',                                                   opentmp(), copyfileintmp(src),        closetmp(),   copystattmp(), replacetmp()               ); return
            if   diffstat(): yield from yf(    'update',                                                                                                       copystat()                                ); return
            yield from yf(                     'uptodate'                                                                                                                                                ); return
          if   remove_source_files:
                if backup:
                  if inplace: yield from yf(   'update', dobackup(),          OR(softreplace(src, dst), yf(           copyfileinplace(src, dst),               copystat(),                  unlink(src)))); return
                  yield from yf(               'update', dobackup(),          OR(softreplace(src, dst), yf(opentmp(), copyfileintmp(src),        closetmp(),   copystattmp(), replacetmp(), unlink(src)))); return
                if   inplace: yield from yf(   'update',                      OR(softreplace(src, dst), yf(           copyfileinplace(src, dst),               copystat(),                  unlink(src)))); return
                yield from yf(                 'update',                      OR(softreplace(src, dst), yf(opentmp(), copyfileintmp(src),        closetmp(),   copystattmp(), replacetmp(), unlink(src)))); return
          if       backup:
                  if inplace: yield from yf(   'update', dobackup(),                                                  copyfileinplace(src, dst),               copystat()                                ); return
                  yield from yf(               'update', dobackup(),                                       opentmp(), copyfileintmp(src),        closetmp(),   copystattmp(), replacetmp()               ); return
          if         inplace: yield from yf(   'update',                                                              copyfileinplace(src, dst),               copystat()                                ); return
          yield from yf(                       'update',                                                   opentmp(), copyfileintmp(src),        closetmp(),   copystattmp(), replacetmp()               ); return

        # src_islnk links dst_noent remove_source_files                         : verbosecreate softreplace or (symlink copystat unlink(src))
        # src_islnk links dst_noent                                             : verbosecreate                 symlink copystat
        # src_islnk links           ignore_existing                             : verboseexists
        # src_islnk links dst_isdir remove_source_files backup       inplace    : verboseupdate dobackup softreplace or (      symlink copystat            unlink(src))
        # src_islnk links dst_isdir remove_source_files backup                  : verboseupdate dobackup softreplace or (mktmp symlink copystat replacetmp unlink(src))  # do backup/rmtree before copy because if softreplace works and backup fails, src doesn't exist anymore.
        # src_islnk links dst_isdir remove_source_files force|delete inplace    : verboseupdate rmtree   softreplace or (      symlink copystat            unlink(src))
        # src_islnk links dst_isdir remove_source_files force|delete            : verboseupdate rmtree   softreplace or (mktmp symlink copystat replacetmp unlink(src))
        # src_islnk links dst_isdir remove_source_files              inplace    : verboseupdate rm       softreplace or (      symlink copystat            unlink(src))  # cannot delete non-empty directory: {dst!r}
        # src_islnk links dst_isdir remove_source_files                         : verboseupdate rm       softreplace or (mktmp symlink copystat replacetmp unlink(src))  # cannot delete non-empty directory: {dst!r}
        # src_islnk links dst_isdir                     backup       inplace    : verboseupdate dobackup symlink copystat
        # src_islnk links dst_isdir                     backup                  : verboseupdate dobackup symlink copystat replacetmp
        # src_islnk links dst_isdir                     force|delete inplace    : verboseupdate rmtree   symlink copystat
        # src_islnk links dst_isdir                     force|delete            : verboseupdate rmtree   symlink copystat replacetmp
        # src_islnk links dst_isdir                                  inplace    : verboseupdate rm                             symlink copystat            unlink(src)   # cannot delete non-empty directory: {dst!r}
        # src_islnk links dst_isdir                                             : verboseupdate rm                       mktmp symlink copystat replacetmp unlink(src)   # cannot delete non-empty directory: {dst!r}
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
              if remove_source_files: yield from yf('create',                      OR(softreplace(src, dst), yf(         copylink(),        copystat(dst_islnk=True),                  unlink(src)))); return
              yield from yf(                        'create',                                                            copylink(),        copystat(dst_islnk=True)                                ); return
            if   ignore_existing: yield from yf(    'exists'                                                                                                                                        ); return
            if stat.S_ISDIR(dst_stats.st_mode):
              if remove_source_files:
                if backup:
                  if inplace: yield from yf(        'update', dobackup(),          OR(softreplace(src, dst), yf(         copylink(),        copystat(dst_islnk=True),                  unlink(src)))); return
                  yield from yf(                    'update', dobackup(),          OR(softreplace(src, dst), yf(mktmp(), copylink(intmp=1), copystattmp(dst_islnk=True), replacetmp(), unlink(src)))); return
                if force:
                  if inplace: yield from yf(        'update', rmtree(),            OR(softreplace(src, dst), yf(         copylink(),        copystat(dst_islnk=True),                  unlink(src)))); return
                  yield from yf(                    'update', rmtree(),            OR(softreplace(src, dst), yf(mktmp(), copylink(intmp=1), copystattmp(dst_islnk=True), replacetmp(), unlink(src)))); return
                if   inplace: yield from yf(        'update', rm(dst, dst_lstats), OR(softreplace(src, dst), yf(         copylink(),        copystat(dst_islnk=True),                  unlink(src)))); return
                yield from yf(                      'update', rm(dst, dst_lstats), OR(softreplace(src, dst), yf(mktmp(), copylink(intmp=1), copystattmp(dst_islnk=True), replacetmp(), unlink(src)))); return
              if   backup:
                  if inplace: yield from yf(        'update', dobackup(),                                                copylink(),        copystat(dst_islnk=True)                                ); return
                  yield from yf(                    'update', dobackup(),                                       mktmp(), copylink(intmp=1), copystattmp(dst_islnk=True), replacetmp()               ); return
                  #yield from yf(                    'update',                                                   mktmp(), copylink(intmp=1), copystattmp(dst_islnk=True), dobackup(), replacetmp()   ); return
              if   force:
                  if inplace: yield from yf(        'update', rmtree(),                                                  copylink(),        copystat(dst_islnk=True)                                ); return
                  yield from yf(                    'update', rmtree(),                                         mktmp(), copylink(intmp=1), copystattmp(dst_islnk=True), replacetmp()               ); return
                  #yield from yf(                    'update',                                                   mktmp(), copylink(intmp=1), copystattmp(dst_islnk=True), rmtree(),   replacetmp()   ); return
              if     inplace: yield from yf(        'update', rm(dst, dst_lstats),                                       copylink(),        copystat(dst_islnk=True)                                ); return
              yield from yf(                        'update', rm(dst, dst_lstats),                              mktmp(), copylink(intmp=1), copystattmp(dst_islnk=True), replacetmp()               ); return
            if stat.S_ISLNK(dst_stats.st_mode):
              if remove_source_files:
                if (yield from difflink()):
                  if backup:
                    if inplace: yield from yf(      'update', dobackup(),          OR(softreplace(src, dst), yf(         copylink(),        copystat(dst_islnk=True),                  unlink(src)))); return
                    yield from yf(                  'update', dobackup(),          OR(softreplace(src, dst), yf(mktmp(), copylink(intmp=1), copystattmp(dst_islnk=True), replacetmp(), unlink(src)))); return
                  if   inplace: yield from yf(      'update',                      OR(softreplace(src, dst), yf(         copylink(),        copystat(dst_islnk=True),                  unlink(src)))); return
                  yield from yf(                    'update',                      OR(softreplace(src, dst), yf(mktmp(), copylink(intmp=1), copystattmp(dst_islnk=True), replacetmp(), unlink(src)))); return
                yield from yf(                      'uptodate',                                                                                                                        unlink(src)  ); return
              if   (yield from difflink()):
                  if backup:
                    if inplace: yield from yf(      'update', dobackup(),                                                copylink(),        copystat(dst_islnk=True)                                ); return
                    yield from yf(                  'update', dobackup(),                                       mktmp(), copylink(intmp=1), copystattmp(dst_islnk=True), replacetmp()               ); return
                  if   inplace: yield from yf(      'update',                                                            copylink(),        copystat(dst_islnk=True)                                ); return
                  yield from yf(                    'update',                                                   mktmp(), copylink(intmp=1), copystattmp(dst_islnk=True), replacetmp()               ); return
              yield from yf(                        'uptodate'                                                                                                                                      ); return
            if   remove_source_files:
                  if backup:
                    if inplace: yield from yf(      'update', dobackup(),          OR(softreplace(src, dst), yf(         copylink(),        copystat(dst_islnk=True),                  unlink(src)))); return
                    yield from yf(                  'update', dobackup(),          OR(softreplace(src, dst), yf(mktmp(), copylink(intmp=1), copystattmp(dst_islnk=True), replacetmp(), unlink(src)))); return
                  if   inplace: yield from yf(      'update',                      OR(softreplace(src, dst), yf(         copylink(),        copystat(dst_islnk=True),                  unlink(src)))); return
                  yield from yf(                    'update',                      OR(softreplace(src, dst), yf(mktmp(), copylink(intmp=1), copystattmp(dst_islnk=True), replacetmp(), unlink(src)))); return
            if       backup:
                    if inplace: yield from yf(      'update', dobackup(),                                                copylink(),        copystat(dst_islnk=True)                                ); return
                    yield from yf(                  'update', dobackup(),                                       mktmp(), copylink(intmp=1), copystattmp(dst_islnk=True), replacetmp()               ); return
            if         inplace: yield from yf(      'update',                                                            copylink(),        copystat(dst_islnk=True)                                ); return
            yield from yf(                          'update',                                                   mktmp(), copylink(intmp=1), copystattmp(dst_islnk=True), replacetmp()               ); return
          yield from yf(                            'skip'                                                                                                                                          ); return

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
          if not specials: yield from yf('skip'); return
          t = "special"
        elif stat.S_ISBLK(src_stats.st_mode) or stat.S_ISCHR(src_stats.st_mode):
          if not devices: yield from yf('skip'); return
          t = "device"
        if t:
          if dst_stats is None: yield from yf('create'); raise NotImplementedError(f"don't know how to copy {t}: {src!r}")
          if   ignore_existing: yield from yf('exists'); return
          if stat.S_ISDIR(dst_stats.st_mode):
            if remove_source_files:
              if backup: yield from yf(       'update', dobackup(),          OR(softreplace(src, dst), _raise(NotImplementedError(f"don't know how to copy {t}: {src!r}")))); return
              if force: yield from yf(        'update', rmtree(),            OR(softreplace(src, dst), _raise(NotImplementedError(f"don't know how to copy {t}: {src!r}")))); return
              yield from yf(                  'update', rm(dst, dst_lstats), OR(softreplace(src, dst), _raise(NotImplementedError(f"don't know how to copy {t}: {src!r}")))); return
            yield from yf(                    'update'); raise NotImplementedError(f"don't know how to copy {t}: {src!r}")
          if   remove_source_files:
            if     backup: yield from yf(     'update', dobackup(),          OR(softreplace(src, dst), _raise(NotImplementedError(f"don't know how to copy {t}: {src!r}")))); return
            yield from yf(                    'update',                      OR(softreplace(src, dst), _raise(NotImplementedError(f"don't know how to copy {t}: {src!r}")))); return
          yield from yf(                      'update'); raise NotImplementedError(f"don't know how to copy {t}: {src!r}")

        raise NotImplementedError(f'unhandled node for copy: {src!r}')

      except:
        _noerr = False
        raise
      finally:  # never yield in a finally, but it's ok if it is for a return (not for a raise)
        try:
          if _noerr:
            if tmp_fd is not None: tmp_fd = yield from fclose(tmp_fd)
            if tmp is not None: tmp = yield from unlink(tmp)
        finally:
          try:
            if tmp_fd is not None: fclose_force(tmp_fd)
          finally:
            if tmp is not None: unlink_force(tmp)
      # End def sync()

    if as_func: return cast_sync

    if source_directory:  # implies target_directory
      return cast_sync(src[:0], dst[:0], src, dst, source_directory=True, target_directory=True, follow_symlinks=follow_symlinks, src_noent_ok=src_noent_ok)

    if target_directory:
      src_dir, srcname = _os.path.split(src)
      return cast_sync(src[:0], dst[:0], src_dir, dst, _src_dirlist=(srcname,), _dst_dirlist=(), source_directory=True, target_directory=True, follow_symlinks=follow_symlinks, src_noent_ok=src_noent_ok)

    src_dir, srcname = _os.path.split(src)
    dst_dir, dstname = _os.path.split(dst)
    return cast_sync(srcname, dstname, src_dir, dst_dir, follow_symlinks=follow_symlinks, src_noent_ok=src_noent_ok)
    # End def fs_sync()

  def merge(src, dst, **kw):
    return fs_sync(src, dst, **(dict(archive=True) | kw))

  def mirror(src, dst, **kw):
    return fs_sync(src, dst, **(dict(archive=True, delete=True) | kw))

  def clean(src, dst, **kw):
    return fs_sync(src, dst, **(dict(recursive=True, delete=True, ignore_non_existing=True, ignore_existing=True, links=True, devices=True, specials=True) | kw))

  def move(src, dst, **kw):
    return fs_sync(src, dst, **(dict(recursive=True, remove_source_files=True, remove_source_dirs=True, links=True, devices=True, specials=True) | kw))

  def remove(dst, **kw):
    return fs_sync(dst, dst, **(dict(remove_source_files=True, remove_source_dirs=True, links=True, devices=True, specials=True) | kw))

  fs_sync.merge = merge
  fs_sync.mirror = mirror
  fs_sync.clean = clean
  fs_sync.move = move
  fs_sync.remove = remove
  return fs_sync

fs_sync = fs_sync()
fs_sync._required_globals = ['errno', 'os', 'stat', 'sys']
