# fs_synctree.py Version 3.3.2
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def fs_synctree(src, dst,
                action="merge", move=False,
                compare_mtime=1, compare_size=True, compare_head_n=0, compare_content=False, compare_symlink=True,
                preserve_timestamps=True, preserve_mode=True, preserve_ownership=False,
                dryrun=False,
                backup_directory=None, backup_updates=True, backup_deletions=True,
                buffer_size=None,
                onerror=None, onfilter=None, onprogress=None):
  """\
fs_synctree(src, dst, **options) -> Error
  action => "merge"
    merge : Copy SRC files in DST. Existing files are overwritten.
    update : Copy SRC files in DST. Existing files are overwritten only if files are not equal.
    mirror : Copy SRC files in DST and remove DST files that don't exist in SRC. Existing files are overwritten only if files are not equal.
    clean : Remove DST files that don't exist in SRC.
  move => 0                   : XXX NIY
  compare_mtime => 1          : Compare the modification time of each files. This is used to check if two files are "equal".
                                0 => do not compare, N>0 => compare mtime with N accuracy in seconds. (ex: 2 => for FAT32 file system.)
  compare_size => True        : Compare the size of each files.
  compare_head_n => 0         : XXX NIY Compare the first n bytes. Ex: compare_head_n => 4096
  compare_content => False    : XXX NIY Nearly as long as direct copying without comparing. At least, it avoids to write for nothing.
  compare_symlink => True
  preserve_timestamps => True
  preserve_mode => True
  preserve_ownership => False : (Works only on non-Windows OS)
  dryrun => False             : Do not write/delete anything
  backup_directory => None    : Could be a path_str pointing to a folder where deleted files are moved.
  backup_updates => True
  backup_deletions => True
  buffer_size => None         : Used for copying file. Could be either an int or None.
  onerror => lambda err: err
  onfilter => lambda path: (None, 1)
  onprogress => lambda action, path: None
    ex: onprogress("create", "common/path/of/file")  # create, delete, update
"""

  def catch(fn,**k):
    try: fn()
    except Exception as e:
      for p,v in k.items(): setattr(e,p,v)
      return onerror(e)
  def catch2(fn,*d,oe=True,**k):
    try: return None, fn()
    except Exception as e:
      for p,v in k.items(): setattr(e,p,v)
      if oe: e = onerror(e)
      return e, d[0] if d else None
  def mkerr(E,*a,**k):
    e = E(*a)
    for p,v in k.items(): setattr(e,p,v)
    return e

  action = action.lower()

  if src == "": src = "."
  if dst == "": dst = "."
  if src == b"": src = b"."
  if dst == b"": dst = b"."

  if compare_mtime is True: compare_mtime = 1

  if onerror is None: onerror = lambda err: err
  if onfilter is None: onfilter = lambda path: (None, 1)
  if onprogress is None: onprogress = lambda action, path: None

  mtimeaccuracy = 0 if compare_mtime < 2 else compare_mtime // 2;

  for _ in (src, dst):
    if not os.path.isdir(_):
      return mkerr(NotADirectoryError, errno.ENOTDIR, "Not a directory", filename=_)

  compare_file = True if compare_mtime or compare_size or compare_head_n > 0 or compare_content else False
  compare_link = True if compare_symlink else False

  srcl, dstl = len(src), len(dst)
  sep = os.sep
  if isinstance(src, bytes): sep = bytes(sep, "ascii")
  sepl = len(sep)

  sharedlink = [None]

  def mkdir(new):
    err = None if dryrun else catch(lambda: os.mkdir(new), syscall="mkdir")
    if err: return err
    return None

  def backupnode(curstat, cur, new, comdir):
    err, newstat = catch2(lambda: os.lstat(new), oe=False, syscall="lstat")
    if err and err.errno == errno.ENOENT: err = None
    if err: err = onerror(err)
    if err: return err

    if newstat:
      if stat.S_ISDIR(newstat.st_mode):
        err = None if dryrun else catch(lambda: os.utime(new, (curstat.st_atime, curstat.st_mtime)), syscall="utime")
        if err: return err
        err = None if dryrun else catch(lambda: os.chmod(new, curstat.st_mode & 0o777), syscall="chmod")
        if err: return err
        err = None if dryrun else catch(lambda: getattr(os, "chown", lambda *_: None)(new, curstat.st_uid, curstat.st_gid), syscall="chown")
        if err: return err
        return None if dryrun else catch(lambda: os.rmdir(cur), syscall="rmdir")
      return mkerr(FileExistsError, errno.EEXIST, "backup file already exists", filename=new)  # XXX is it realy expected behavior ?

    err = fs_mkdir(backup_directory + sep + comdir, parents=-comdir.count(sep), exist_ok=True)
    if err: err = onerror(err)
    if err: return err

    err = fs_move(cur, new)
    if err: err = onerror(err)
    return err

  def removenode(newstat, new, bak, comdir):
    if backup_directory and backup_deletions:
      return backupnode(newstat, new, bak, comdir)
    if stat.S_ISDIR(newstat.st_mode):
      err = None if dryrun else catch(lambda: os.rmdir(new), syscall="rmdir")
      if err: return err
    else:
      err = None if dryrun else catch(lambda: os.unlink(new), syscall="unlink")
      if err: return err
    return None

  def comparenode(curstat, cur, newstat, new):
    if not curstat or not newstat: return None, 0
    if (curstat.st_mode & 0xF000) != (newstat.st_mode & 0xF000): return None, 0
    if stat.S_ISLNK(curstat.st_mode):
      if not compare_link: return None, 0
      if compare_symlink:
        err, sharedlink[0] = catch2(lambda: os.readlink(cur), syscall="readlink")
        if err: return err
        err, newlink = catch2(lambda: os.readlink(new), syscall="readlink")
        if err: return err
        if sharedlink[0] != newlink: return None, 0
      return None, 1
    elif stat.S_ISREG(curstat.st_mode):
      if not compare_file: return None, 0
      if compare_size and curstat.st_size != newstat.st_size: return None, 0
      if compare_mtime and (curstat.st_mtime > newstat.st_mtime + mtimeaccuracy or curstat.st_mtime + mtimeaccuracy < newstat.st_mtime):
        return None, 0
      # XXX do other comparison methods
      if (compare_head_n > 0):
        #my ($d1, $d2);
        #($err, $d1) = fs_readfile($cur, {end=>$optcmphead});
        #$err = &$onerror($err, "fs_readfile", $cur) if $err;
        #return $err if $err;
        #($err, $d2) = fs_readfile($new, {end=>$optcmphead});
        #$err = &$onerror($err, "fs_readfile", $new) if $err;
        #return $err if $err;
        #$equal = 0 unless $d1 eq $d2;
        # XXX use fs_diff($cur, $new, {end=>$optcmpheadn}) instead.
        pass
      if (compare_content):
        # XXX use a kind of fs_diff($cur, $new)
        pass
      # XXX &$optcmp(...)
      return None, 1;
    elif stat.S_ISDIR(curstat.st_mode): return None, 1
    return None, 0

  def copynode(curstat, cur, newstat, new, bak, comdir, equal):
    # here, $new is the same type as $cur, or non existing.
    written = 0
    if newstat and curstat.st_mode & 0xF000 != newstat.st_mode & 0xF000 and stat.S_ISDIR(curstat.st_mode):
      # do not remove if $cur is a directory, as it is removed while descending the tree
      err = removenode(newstat, new)
      if err: return err
    if stat.S_ISLNK(curstat.st_mode):
      if equal: return None
      if newstat:
        if backup_directory and backup_updates:
          err = backupnode(newstat, new, bak, comdir)
          if err: return err
        else:
          err = None if dryrun else catch(lambda: os.unlink(new), syscall="unlink")
          if err: return err
      if sharedlink[0] is None:
        err, sharedlink[0] = catch2(lambda: os.readlink(cur), syscall="readlink")
        if err: return err
      err = None if dryrun else catch(lambda: os.symlink(sharedlink[0], new), syscall="symlink")
      if err: return err
      #if preserve_timestamps and (not newstat or curstat.st_mtime != newstat.st_mtime):
      #  err = None if dryrun else catch(lambda: os.utime(new, (curstat.st_atime, curstat.st_mtime), follow_symlinks=False), syscall="utime")
      #  if err: return err
      #if preserve_mode and (not newstat or curstat.st_mode != newstat.st_mode):
      #  err = None if dryrun else catch(lambda: os.chmod(new, curstat.st_mode & 0o777, follow_symlinks=False), syscall="chmod")
      #  if err: return err
      #if preserve_ownership and (not newstat or curstat.st_uid != newstat.st_uid or curstat.st_gid != newstat.st_gid):
      #  err = None if dryrun else catch(lambda: getattr(os, "chown", lambda *a,**k: None)(new, curstat.st_uid, curstat.st_gid, follow_symlinks=False), syscall="chown")
      #  if err: return err
    elif stat.S_ISDIR(curstat.st_mode):
      #if not newstat:  # Folders are created while descending in the tree
      #  $err = $optdryrun ? "" : fs_mkdir($new); if ($err) { $err = &$onerror($err, "fs_mkdir", $new); return $err if $err; }
      if preserve_timestamps and (not newstat or curstat.st_mtime != newstat.st_mtime):
        err = None if dryrun else catch(lambda: os.utime(new, (curstat.st_atime, curstat.st_mtime)), syscall="utime")
        if err: return err
      if preserve_mode and (not newstat or curstat.st_mode != newstat.st_mode):
        err = None if dryrun else catch(lambda: os.chmod(new, curstat.st_mode & 0o777), syscall="chmod")
        if err: return err
      if preserve_ownership and (not newstat or curstat.st_uid != newstat.st_uid or curstat.st_gid != newstat.st_gid):
        err = None if dryrun else catch(lambda: getattr(os, "chown", lambda *_: None)(new, curstat.st_uid, curstat.st_gid), syscall="chown")
        if err: return err
    elif stat.S_ISREG(curstat.st_mode):
      if not equal:
        if newstat and backup_directory and backup_updates:
          err = backupnode(newstat, new, bak, comdir)
          if err: return err
        err = None if dryrun else fs_copyfile(cur, new, buffer_size=buffer_size)
        if err:
          err = onerror(err)
          if err: return err
        written = 1
      if preserve_timestamps and (written or not newstat or curstat.st_mtime != newstat.st_mtime):
        err = None if dryrun else catch(lambda: os.utime(new, (curstat.st_atime, curstat.st_mtime)), syscall="utime")
        if err: return err
      if preserve_mode and (written or not newstat or curstat.st_mode != newstat.st_mode):
        err = None if dryrun else catch(lambda: os.chmod(new, curstat.st_mode & 0o777), syscall="chmod")
        if err: return err
      if preserve_ownership and (written or not newstat or curstat.st_uid != newstat.st_uid or curstat.st_gid != newstat.st_gid):
        err = None if dryrun else catch(lambda: getattr(os, "chown", lambda *_: None)(new, curstat.st_uid, curstat.st_gid), syscall="chown")
        if err: return err
    else:
      return onerror(mkerr(LookupError("Unhandled node", filename=cur)))
    return None

  if action not in ("merge", "update", "mirror"): mkdir = lambda *a: None
  if action not in ("mirror", "clean"): removenode = lambda *a: None
  if action not in ("update", "mirror"): comparenode = lambda *a: (None, 0)
  if action not in ("merge", "update", "mirror"): copynode = lambda *a: None

  progressupdate = lambda *a: onprogress("update", *a)
  progresscreate = lambda *a: onprogress("create", *a)
  progressdelete = lambda *a: onprogress("delete", *a)

  if backup_directory and backup_deletions:
    progressdelete = lambda *a: onprogress("backup", *a)

  if action not in ("merge", "update", "mirror"): progressupdate = lambda: None
  if action not in ("merge", "update", "mirror"): progresscreate = lambda: None
  if action not in ("mirror", "clean"): progressdelete = lambda: None

  def rec(err, name, roots):
    if err:
      err = onerror(err)
      return err
    curdir, newdir = roots
    comdir = curdir[srcl+sepl:] if curdir else newdir[dstl+sepl:]
    com = comdir + sep + name if comdir else name
    cur, new, bak = src+sep+com, dst+sep+com, (backup_directory+sep+com if backup_directory else None)
    statss = []
    for _, _dir in ((cur, curdir), (new, newdir)):
      stats = None
      if _dir:
        err, stats = catch2(lambda: os.lstat(_), syscall="lstat")
        if err: return err
      statss.append(stats)
    curstat, newstat = statss
    statss = None

    err, unfiltered = onfilter(com)
    if err: return err
    if not unfiltered: curstat = None

    if curstat and stat.S_ISDIR(curstat.st_mode):
      if not newstat:
        err = mkdir(new)
        if err: return err
      elif not stat.S_ISDIR(newstat.st_mode):
        err = removenode(newstat, new, bak, comdir)
        if err: return err
        err = mkdir(new)
        if err: return err

    # recursive
    err = fs_iterdirsdiff(rec, [cur if curstat and not stat.S_ISLNK(curstat.st_mode) else None,
                                new if newstat and not stat.S_ISLNK(newstat.st_mode) else None])
    if err: return err

    sharedlink[0] = None

    if curstat and newstat:
      err, cmp = comparenode(curstat, cur, newstat, new)
      if err: return err
      if not cmp:
        err = progressupdate(com)
        if err: return err
      err = copynode(curstat, cur, newstat, new, bak, comdir, cmp)
      if err: return err
    elif curstat:
      err = progresscreate(com)
      if err: return err
      err = copynode(curstat, cur, newstat, new, bak, comdir, 0)
      if err: return err
    elif newstat:
      err = progressdelete(com)
      if err: return err
      err = removenode(newstat, new, bak, comdir)
      if err: return err
    return None
  return fs_iterdirsdiff(rec, [src, dst]);
fs_synctree._required_globals = [
  "errno",
  "os",
  "stat",
  "sys",
  "fs_copyfile",
  "fs_mkdir",
  "fs_move",
]
