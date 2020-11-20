# MemOs.py Version 1.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class MemOs(object):  # XXX TEST THE WHOLE CLASS !
  """\
An os module like object that only act in memory in a virtual file system
"""
  # https://docs.python.org/3/library/os.html

  _fs = None
  _meta = None
  _last_ino = None
  _last_fd = None
  _proc_fd = None
  _proc_cwd = None
  _proc_cwd_ino = None
  _umask = 0o022
  _ROOT_INO = 3

  error = OSError
  name = None
  path = None

  uid = 0
  gid = 0

  def __init__(self, *, name=None, path=None):
    if name is None: name = "_mem_os"
    if not isinstance(name, str): raise TypeError("expected str for mem_os.name")
    self.name = name
    self.path = posixpath if path is None else path
    self._fs = {self._ROOT_INO: {b".": self._ROOT_INO, b"..": self._ROOT_INO}}
    now = time.time()
    self._meta = {self._ROOT_INO: {"st_mode": self.T_DIR | 0o755, "st_ino": self._ROOT_INO, "st_uid": int(self.uid), "st_gid": int(self.gid), "st_nlink": 1, "st_size": 4096, "st_atime": now, "st_mtime": now}}
    self._last_ino = self._ROOT_INO
    self._last_fd = 3
    self._proc_cwd = (b"/",)
    self._proc_cwd_ino = (self._ROOT_INO,)
    self._proc_fd = {}

  # File Names, Command Line Arguments, and Environment Variables

  def fsencode(self, filename):
    filename = self.fspath(filename)
    if isinstance(filename, bytes): return filename
    if isinstance(filename, str): return filename.encode("UTF-8")
    raise TypeError("expected str, bytes or os.PathLike, not " + type(filename))

  def fsdecode(self, filename):
    filename = self.fspath(filename)
    if isinstance(filename, str): return filename
    if isinstance(filename, bytes): return filename.decode("UTF-8", "strict")
    raise TypeError("expected str, bytes or os.PathLike, not " + type(filename))

  def fspath(self, path): return os_fspath(path)

  def umask(self, mask):
    p, self._umask = self._umask, 0o777 & mask
    return p

  # File Object Creation  

  def fdopen(self, fd, mode="r", buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    # XXX compare os.fdopen behavior ! with opener or not
    if buffering not in (None, -1): raise NotImplementedError()
    if encoding is not None: raise NotImplementedError()
    if opener is not None:
      return FileIO(None, mode, closefd=closefd, opener=opener, os_module=self)
    else:
      fds = self._getcheck_fd(fd, fmt="reg")
      mode_flags = convert_open_mode_to_flags(mode, os_module=self)
      if fds["flags"] not in (mode_flags, mode_flags | self.O_NOINHERIT): raise XXX
      #if opener is not None: raise NotImplementedError()  # XXX
      return FileIO(fds["path"], mode, closefd=closefd, opener=lambda *a: fd, os_module=self)

  # File Descriptor Operations

  o_noatime = False  # XXX not used, please check every method that should update atime !

  T_FIFO = 0x1000
  T_CHR  = 0x2000
  T_DIR  = 0x4000
  T_BLK  = 0x6000
  T_REG  = 0x8000
  T_LNK  = 0xA000
  T_SOCK = 0xC000

  def close(self, fd):
    fds = self._getcheck_fd(fd)
    fds["closed"] = True
    del self._proc_fd[fd]

  #def copy_file_range(self, src, dst, count, offset_src=None, offset_dst=None): XXX
  #def dup(self, fd): XXX
  #def dup2 XXX ?

  def fchmod(self, fd, mode): return self._hchmod(self._getcheck_fd(fd)["meta"], mode)

  def fchown(self, fd, uid, gid): return self._hchown(self._getcheck_fd(fd)["meta"], uid, gid)

  def fstat(self, fd): return self.stat_result(**self._getcheck_fd(fd)["meta"])

  def fdatasync(self, fd): self._getcheck_fd(fd)

  def fsync(self, fd): self._getcheck_fd(fd)

  def ftruncate(self, fd, length):
    if length < 0: raise OSError(errno.EINVAL, "Invalid argument")
    fds = self._getcheck_fd(fd, fmt="reg")
    if not fds["flags"] & self.O_RDWR and not fds["flags"] & self.O_WRONLY: raise PermissionError(errno.EACCES, "Permission denied")  # not the same error as in _getcheck_fd
    return self._htruncate(fds["data"], fds["meta"])

  def isatty(self, fd):
    self._getcheck_fd(fd)
    return False

  def lseek(self, fd, pos, how):
    if not isinstance(pos, int): raise TypeError("an integer is required")
    fds = self._getcheck_fd(fd, fmt="reg")
    if   how == self.SEEK_SET: pass
    elif how == self.SEEK_CUR: pos += fds["seek"]
    elif how == self.SEEK_END: pos += len(fds["data"])
    else: raise OSError(errno.EINVAL, "Invalid argument")
    if pos < 0: raise OSError(errno.EINVAL, "Invalid argument")
    return pos

  SEEK_SET = 0
  SEEK_CUR = 1
  SEEK_END = 2

  def open(self, path, flags, mode=0o777, *, dir_fd=None):
    if dir_fd is not None: raise NotImplementedError()
    p_ino, p = self._traverse(path, not_found_as_none=True)
    w,rw,a,c,t,x = (flags & getattr(self, "O_" + _) for _ in "WRONLY RDWR APPEND CREAT TRUNC EXCL".split())
    r = 0 if w or rw else 1
    if x and p_ino[-1] is not None: raise FileExistsError(errno.EEXIST, "File exists", path)
    now = time.time()
    if c:
      dir = self._fs[p_ino[-2]]
      now = time.time()
      ino = self._next_ino()
      data, meta = bytearray(), {"st_mode": self.T_REG | (mode & (0o777 - self._umask)), "st_uid": int(self.uid), "st_gid": int(self.gid), "st_ino": ino, "st_nlink": 1, "st_size": 0, "st_atime": now, "st_mtime": now}
      if p_ino[-1] is not None:
        if not stat.S_ISREG(meta["st_mode"]): raise OSError(errno.EINVAL, "Invalid argument")  # XXX I just guessed the error...
        self._hunlink(dir, p[-1], p_ino[-1], self._meta[p_ino[-1]])
      dir[p[-1]], self._fs[ino], self._meta[ino] = ino, data, meta
    else:
      if p_ino[-1] is None: raise FileNotFoundError(errno.ENOENT, "No such file or directory", path)  # XXX windows error ?
      data, meta = self._fs[p_ino[-1]], self._meta[p_ino[-1]]
      if stat.S_ISDIR(meta["st_mode"]) and (w or rw): raise IsADirectoryError(errno.EISDIR, "Is a directory", path)  # XXX windows error ?
      elif not stat.S_ISREG(meta["st_mode"]): raise OSError(errno.EINVAL, "Invalid argument")  # XXX I just guessed the error...
    fds = {
      "data": data, "meta": meta, "path": path, "flags": flags, "seek": 0, "closed": False, "fmt": stat.S_IFMT(meta["st_mode"]),
    }
    fd = self._next_fd()
    # XXX does O_TRUNC updates mtime on opening ?
    if t: data[:], meta["st_size"], self._proc_fd[fd], meta["st_atime"], meta["st_mtime"] = b"", 0, fds, now, now
    else: self._proc_fd[fd], meta["st_atime"] = fds, now
    # XXX does O_WRONLY or O_RDWR updates mtime on opening ?
    return fd

  O_RDONLY    = 0
  O_WRONLY    = 1
  O_RDWR      = 2
  O_APPEND    = 8
  O_CREAT     = 256
  O_EXCL      = 1024
  O_TRUNC     = 512

  O_BINARY    = 32768
  O_NOINHERIT = 128

  O_NOATIME   = 262144  # XXX

  #def pread(self, fd, n, offset): XXX
  #def preadv(self, fd, buffers, offset, flags=0): XXX
  #def pwrite(self, fd, str, offset): XXX
  #def pwritev(self, fd, buffers, offset, flags=0): XXX

  def read(self, fd, n):
    # this method works with linesep = "\r\n" or one byte linesep
    if n < 0: raise OSError(errno.EINVAL, "Invalid argument")
    fds = self._getcheck_fd(fd, readable=True, fmt="reg")
    fds = self._proc_fd[fd]
    data, meta, pos = fds["data"], fds["meta"], fds["seek"]
    d = bytes(data[pos:n])
    fds["seek"], meta["st_atime"] = pos + len(d), time.time()
    if fds["flags"] & self.O_BINARY: return d
    if self.linesepb == b"\r\n": return d.replace(b"\r", b"")
    if len(self.linesepb) == 1: return d.replace(self.linesepb, b"\n")
    raise NotImplementedError()

  #def readv(self, fd, buffers): XXX

  def write(self, fd, str):
    fds = self._getcheck_fd(fd, writable=True, fmt="reg")
    data, meta, pos = fds["data"], fds["meta"], fds["seek"]
    lstr = len(str)
    actual_str = str if fds["flags"] & self.O_BINARY else str.replace(b"\n", self.linesepb)
    alstr = len(actual_str)
    if fds["flags"] & self.O_APPEND: pos = len(data)
    size = max(pos+alstr, len(data))
    now = time.time()
    data[pos:pos+alstr], fds["seek"], meta["st_size"], meta["st_atime"], meta["st_mtime"] = actual_str, pos + alstr, size, now, now
    return lstr

  #def writev(self, fd, buffers): XXX

  # Querying the size of a terminal
  # - no terminal here, of course

  # Inheritance of File Descriptors
  # XXX

  # Files and Directories

  #def access

  def chdir(self, path):
    cwd_ino, cwd = self._traverse(path)
    meta = self._meta[cwd_ino[-1]]
    if not stat.S_ISDIR(meta["st_mode"]): raise NotADirectoryError(errno.ENOTDIR, "Not a directory", path, 2)  # FileNotFoundError on windows
    self._proc_cwd_ino, self._proc_cwd = cwd_ino, cwd

  def chmod(self, path, mode, *, dir_fd=None, follow_symlinks=True):
    if isinstance(path, int): return self.fchmod(path, uid, gid)
    if dir_fd is not None: raise NotImplementedError()
    return self._hchmod(self._meta[self._traverse(path, follow_symlinks=follow_symlinks)[0][-1]], mode)

  def chown(self, path, uid, gid, *, dir_fd=None, follow_symlinks=True):
    if isinstance(path, int): return self.fchown(path, uid, gid)
    if dir_fd is not None: raise NotImplementedError()
    return self._hchown(self._meta[self._traverse(path, follow_symlinks=follow_symlinks)[0][-1]], uid, gid)

  def chroot(self, path):
    # it is impossible to go back to previous root ;)
    ino = self._traverse(path)[0][-1]
    meta = self._meta[ino]
    if not stat.S_ISDIR(meta["st_mode"]): raise NotADirectoryError(errno.ENOTDIR, "Not a directory", path)  # chroot not available on windows
    for i, cwd_ino in enumerate(self._proc_cwd_ino):
      if cwd_ino == ino:
        self._proc_cwd_ino, self._proc_cwd = self._proc_cwd_ino[i:], self._proc_cwd[i:]
        return
    self._proc_cwd_ino, self._proc_cwd = (ino,), (b"/",)

  #def fchdir(self, fd)

  def getcwd(self): return self.fsdecode(self.getcwdb())
  def getcwdb(self): return self.path.join(*self._proc_cwd)

  def lchmod(self, path, mode): return self.chmod(path, mode, follow_symlinks=False)

  def lchown(self, path, uid, gid): return self.chown(path, uid, gid, follow_symlinks=False)

  def link(self, src, dst, *, src_dir_fd=None, dst_dir_fd=None, follow_symlinks=True):
    if src_dir_fd is not None or dst_dir_fd is not None: raise NotImplementedError()
    s_ino, s = self._traverse(src, follow_symlinks=follow_symlinks, error_path=src, error_dst=dst)
    s_meta = self._meta[s_ino[-1]]
    if stat.S_ISDIR(s_meta["st_mode"]): raise PermissionError(errno.EPERM, "Permission denied", src, 5, dst)
    d_ino, d = self._traverse(dst, follow_symlinks=False, not_found_as_none=True, error_path=src, error_dst=dst)
    if d_ino[-1] is not None: raise FileExistsError(errno.EEXIST, "File exists", src, 183, dst)
    dir = self._fs[d_ino[-2]]
    s_meta["st_nlink"], dir[d[-1]] = s_meta["st_nlink"] + 1, s_ino[-1]

  def listdir(self, path="."):
    ino = self._traverse(path)[0][-1]
    dir, meta = self._fs[ino], self._meta[ino]
    if not stat.S_ISDIR(meta["st_mode"]): raise NotADirectoryError(errno.ENOTDIR, "Not a directory", path, 267)
    if isinstance(path, str): return [self.fsdecode(_) for _ in dir if _ not in (b"..", b".", b"")]
    return [_ for _ in dir if _ not in (b"..", b".", b"")]

  def lstat(self, *a, **k): return self.stat(*a, follow_symlinks=False, **k)

  def mkdir(self, path, mode=0o777, *, dir_fd=None):
    if dir_fd is not None: raise NotImplementedError()
    p_ino, p = self._traverse(path, not_found_as_none=True)
    if p_ino[-1] is not None: raise FileExistsError(errno.EEXIST, "File already exists", path, 183)
    dir = self._fs[p_ino[-2]]
    newdirino = self._next_ino()
    newdir = {b".": newdirino, b"..": p_ino[-2]}
    now = time.time()
    newmeta = {"st_mode": self.T_DIR | (mode & (0o777 - self._umask)), "st_uid": int(self.uid), "st_gid": int(self.gid), "st_ino": newdirino, "st_nlink": 1, "st_size": 4096, "st_atime": now, "st_mtime": now}
    dir[p[-1]], self._fs[newdirino], self._meta[newdirino] = newdirino, newdir, newmeta

  #def makedirs(self, mode=0o777, exist_ok=False):
  #  XXX os_makedirs(name, mode=0o777, exist_ok=False, *, os_module=None)
  #  return os_makedirs(name, mode=mode, exist_ok=exist_ok, os_module=self)

  def readlink(self, path, *, dir_fd=None):
    if dir_fd is not None: raise NotImplementedError()
    p_ino, _ = self._traverse(path, follow_symlinks=False)
    p_meta = self._meta[p_ino[-1]]
    if not stat.S_ISLNK(p_meta["st_mode"]): raise OSError(errno.EINVAL, "Invalid argument", path)  # XXX windows error ?
    return self._hreadlink(self._fs[p_ino[-1]], reflect_type=path)

  def remove(self, path, *, dir_fd=None):
    if dir_fd is not None: raise NotImplementedError()
    p_ino, p = self._traverse(path, follow_symlinks=False)
    #if not p_ino[1:2]: raise OSError(errno.EBUSY, "Device or resource busy", path, 32)  # PermissionError on windows
    _, meta = self._fs[p_ino[-1]], self._meta[p_ino[-1]]
    if stat.S_ISDIR(meta["st_mode"]): raise IsADirectoryError(errno.EISDIR, "Is a directory", path, 5)  # PermissionError on windows
    self._hunlink(self._fs[p_ino[-2]], p[-1], p_ino[-1], meta)

  #def removedirs(self, name): XXX

  def rename(self, src, dst, *, src_dir_fd=None, dst_dir_fd=None):
    # windows cannot replace, but unix can
    if src_dir_fd is not None or dst_dir_fd is not None: raise NotImplementedError()
    s_ino, s = self._traverse(src, follow_symlinks=False, not_found_as_none=False, error_path=src, error_dst=dst)
    d_ino, d = self._traverse(dst, follow_symlinks=False, not_found_as_none=True , error_path=src, error_dst=dst)
    s_dir, d_dir = self._fs[s_ino[-2]], self._fs[d_ino[-2]]
    if d_ino[-1] is None:
      d_dir[d[-1]] = s_dir[s[-1]]
      del s_dir[s[-1]]
      return
    s_meta, d_meta = self._meta[s_ino[-1]], self._meta[d_ino[-1]]
    if stat.S_ISDIR(s_meta["st_mode"]):  # windows does not accept replacing any dir : PermissionError WinError 5
      if not stat.S_ISDIR(d_meta["st_mode"]): raise NotADirectoryError(errno.ENOTDIR, "Not a directory", src, 5, dst)
      for name in self._fs[d_ino[-1]]:
        if name not in (b"", b".", b".."): raise OSError(errno.ENOTEMPTY, "Directory not empty", src, 5, dst)
    if stat.S_ISDIR(d_meta["st_mode"]): raise IsADirectoryError(errno.EISDIR, "Is a directory", src, 5, dst)
    self._hunlink(d_dir, d[-1], d_ino[-1], d_meta)
    d_dir[d[-1]] = s_dir[s[-1]]
    del s_dir[s[-1]]

  #def renames(self, old, new): XXX

  replace = rename

  def rmdir(self, path, *, dir_fd=None):
    if dir_fd is not None: raise NotImplementedError()
    p_ino, p = self._traverse(path, follow_symlinks=False)
    #if p_ino[-1] in self._proc_cwd_ino: raise OSError(errno.EBUSY, "Device or resource busy", path, 32)  # PermissionError on windows
    rmdir, meta = self._fs[p_ino[-1]], self._meta[p_ino[-1]]
    if not stat.S_ISDIR(meta["st_mode"]): raise NotADirectoryError(errno.ENOTDIR, "Not a directory", path, 267)
    for n in rmdir:
      if n in (b"", b".", b".."): pass
      else: raise OSError(errno.ENOTEMPTY, "Non empty directory", path, 145)
    self._hunlink(self._fs[p_ino[-2]], p[-1], p_ino[-1], meta)

  #def scandir(self, path="."): XXX

  def stat(self, path, *, dir_fd=None, follow_symlinks=True):
    if isinstance(path, int): return self.fstat(path)
    if dir_fd is not None: raise NotImplementedError()
    return self.stat_result(**self._meta[self._traverse(path, follow_symlinks=follow_symlinks)[0][-1]])

  #windows ex: os.stat_result(st_mode=16895, st_ino=4222124650991797, st_dev=813348024, st_nlink=1, st_uid=0, st_gid=0, st_size=20480, st_atime=1601902565, st_mtime=1601902565, st_ctime=1593107313)
  class stat_result(tuple):  # same as : os_stat_result = collections.namedtuple("os_stat_result", fields, defaults=(0,)*len(fields))
    _fields = tuple("st_mode, st_ino, st_nlink, st_size, st_atime, st_mtime".split(", "))
    def __new__(cls, *a, **k):
      la = len(a)
      return tuple.__new__(cls, ((a[i] if i < la else k.get(field, 0)) for i, field in enumerate(cls._fields)))
    def __repr__(self): return "MemOs." + self.__class__.__name__ + "(" + ", ".join(_ + "=" + repr(getattr(self, _)) for _ in self._fields) + ")"
    def __getattr__(self, name):
      for i, field in enumerate(self._fields):
        if field == name: return self[i]
      raise AttributeError(repr("MemOs." + self.__class__.__name__) + " object has no attribute " + repr(name))
    def __setattr__(self, name, value):
      if name in self._fields: raise AttributeError("readonly attribute")
      raise AttributeError(repr("MemOs." + self.__class__.__name__) + " object has no attribute " + repr(name))
    def __delattr__(self, name):
      if name in self._fields: raise AttributeError("readonly attribute")
      raise AttributeError(repr("MemOs." + self.__class__.__name__) + " object has no attribute " + repr(name))

  def symlink(self, src, dst, target_is_directory=False, *, dir_fd=None):
    # target_is_directory is ignored on non-windows platforms
    if dir_fd is not None: raise NotImplementedError()
    d_ino, d = self._traverse(dst, follow_symlinks=False, not_found_as_none=True, error_path=src, error_dst=dst)
    if d_ino[-1] is not None: raise FileExistsError(errno.EEXIST, "File exists", src, 183, dst)  # XXX windows error is 183 ?
    dir = self._fs[d_ino[-2]]
    n = self.fsencode(src)
    n_ino = self._next_ino()
    now = time.time()
    n_meta = {"st_mode": self.T_LNK | (0o777 - self._umask), "st_uid": int(self.uid), "st_gid": int(self.gid), "st_ino": n_ino, "st_nlink": 1, "st_size": len(n), "st_atime": now, "st_mtime": now}
    dir[d[-1]], self._fs[n_ino], self._meta[n_ino] = n_ino, n, n_meta

  def sync(self):
    for fd in self._proc_fd: self.fsync(fd)

  def truncate(self, path, length):
    if isinstance(path, int): return self.ftruncate(path, length)
    if length < 0: return
    ino = self._traverse(path)[0][-1]
    return self._htruncate(self._fs[ino], self._meta[ino])

  unlink = remove

  def utime(self, path, times=None, *, ns=None, dir_fd=None, follow_symlinks=True):
    if dir_fd is not None: raise NotImplementedError()
    if times is not None and ns is not None: raise ValueError("utime: you may specify either 'times' or 'ns' but not both")
    if ns is not None: times = (int(ns[0]) / 1000000000, int(ns[1]) / 1000000000)  # ns is nanosecond
    if times is None:
      now = time.time()
      time = (now, now)
    if isinstance(path, int):
      meta = self._getcheck_fd(path)["meta"]
    else:
      meta = self._meta[self._traverse(path, follow_symlinks=follow_symlinks)[0][-1]]
    if not isinstance(times[0], (int, float)) or not isinstance(times[1], (int, float)): TypeError("an integer is required")
    meta["st_atime"], meta["st_mtime"] = times[0:2]

  #def walk(self, top, topdown=True, onerror=True, followlinks=False): XXX
  #def fwalk(self, top=".", topdown=True, onerror=True, *, follow_symlinks=False, dir_fd=None): XXX

  supports_dir_fd = ()
  supports_effective_ids = ()
  supports_fd = (chmod, chown, stat, truncate, utime)
  supports_follow_symlinks = (chmod, chown, stat, utime, link)

  # Linux extended attributes
  # - none

  # Process Management
  # - none

  # Interface to the scheduler
  # - none

  # Miscellaneous System Information

  @property
  def curdir(self): return self.path.curdir
  @property
  def curdirb(self): return self.fsencode(self.curdir)
  @property
  def pardir(self): return self.path.pardir
  @property
  def pardirb(self): return self.fsencode(self.pardir)
  @property
  def sep(self): return self.path.sep
  @property
  def sepb(self): return self.fsencode(self.sep)
  @property
  def altsep(self): return self.path.altsep
  @property
  def altsepb(self): return self.fsencode(self.altsep)
  @property
  def extsep(self): return self.path.extsep
  @property
  def extsepb(self): return self.fsencode(self.extsep)
  @property
  def pathsep(self): return self.path.pathsep
  @property
  def pathsepb(self): return self.fsencode(self.pathsep)
  linesep = "\n"
  @property
  def linesepb(self): return self.fsencode(self.linesep)

  # Random numbers
  # - none

  # Helpers

  def _traverse(self, path, cwd_ino=None, cwd=None, *, follow_symlinks=True, follow_dots=False, not_found_as_none=False, error_path=None, error_dst=None):
    split = os_path_split(self.fsencode(path), -1, os_module=self)
    if split[0]:  # isabs
      cwd_ino, cwd = self._proc_cwd_ino[:1], self._proc_cwd[:1]
    else:
      if cwd_ino is None: cwd_ino = self._proc_cwd_ino
      if cwd is None: cwd = self._proc_cwd
    l = len(split) - 2
    for i, name in enumerate(split[1:]):
      if name == b"": continue
      if not follow_dots:
        if name == b".": continue
        if name == b"..":
          if cwd[1:]: cwd_ino, cwd = cwd_ino[:-1], cwd[:-1]
          continue
      cwn, cwm = self._fs[cwd_ino[-1]], self._meta[cwd_ino[-1]]
      if not stat.S_ISDIR(cwm["st_mode"]): raise NotADirectoryError(errno.ENOTDIR, "Not a directory", path if error_path is None else error_path, 3, error_dst)  # FileNotFoundError on windows
      if name not in cwn:
        if i == l and not_found_as_none: return cwd_ino + (None,), cwd + (name,)
        raise FileNotFoundError(errno.ENOENT, "No such file or directory", path if error_path is None else error_path, 2 if i == l else 3, error_dst)
      ino = cwn[name]
      nn, nm = self._fs[ino], self._meta[ino]
      if i != l or follow_symlinks:
        while stat.S_ISLNK(nm["st_mode"]):
          cwd_ino_lnk, _ = self._traverse(self._hreadlink(nn), cwd_ino=cwd_ino, cwd=cwd, error_path=error_path, error_dst=error_dst)  # follow_dots for symlinks ?
          cwd_ino = cwd_ino[:-1] + cwd_ino_lnk[-1]
          nn, nm = self._fs[cwd_ino[-1]], self._meta[cwd_ino[-1]]
      cwd_ino, cwd = cwd_ino + (ino,), cwd + (name,)
    return cwd_ino, cwd

  def _next_ino(self):
    i = self._last_ino + 1
    while i in self._fs: i += 1
    self._last_ino = i
    return i

  def _next_fd(self):
    self._last_fd = self._last_fd + 1
    return self._last_fd

  def _getcheck_fd(self, fd, readable=False, writable=False, fmt=None):
    ok, fds = True, None
    if fd in self._proc_fd:
      fds = self._proc_fd[fd]
      if readable and not fds["flags"] & self.O_RDWR and     fds["flags"] & self.O_WRONLY: ok = False
      if writable and not fds["flags"] & self.O_RDWR and not fds["flags"] & self.O_WRONLY: ok = False
      isdir = stat.S_ISDIR(fds["fmt"])
      if fmt == "dir" and not isdir: raise NotADirectoryError(errnor.ENOTDIR, "Not a directory")  # windows cannot open dir
      if fmt == "reg" and not stat.S_ISREG(fds["fmt"]):
        if isdir: raise IsADirectoryError(errno.EISDIR, "Is a directory")  # windows cannot open dir
        raise OSError(errno.EBADF, "Bad file descriptor")  # XXX I just guessed the error...
      if fds["closed"]: ok = False
    else: ok = False
    if ok: return fds
    raise OSError(errno.EBADF, "Bad file descriptor")

  def _hchmod(self, meta, mode):
    meta["st_mode"] = (meta["st_mode"] & 0xFFFFFE00) | (mode & 0o777)  # is 0xFFFFFE00 ok ? Do not use umask

  def _hchown(self, meta, uid, gid):
    if not isinstance(uid, int): raise TypeError("uid should be integer")
    if not isinstance(gid, int): raise TypeError("gid should be integer")
    if uid >= 0: meta["st_uid"] = uid
    if gid >= 0: meta["st_gid"] = gid

  def _hreadlink(self, data, reflect_type=b""):
    data = bytes(data)
    if isinstance(reflect_type, str): return self.fsdecode(data)
    return data

  def _htruncate(self, data, meta):
    ldata = len(data)
    now = time.time()
    if ldata < length: data[ldata:], meta["st_size"], meta["st_atime"], meta["st_mtime"] = b"\x00" * (length - ldata), length, now, now
    else             : data[     :], meta["st_size"], meta["st_atime"], meta["st_mtime"] =              data[:length], length, now, now    

  def _hunlink(self, dir, name, ino, meta):
    if meta["st_nlink"] > 1:
      meta["st_nlink"] = meta["st_nlink"] - 1
      del dir[name]
    else:
      meta["st_nlink"] = 0
      del dir[name]
      del self._fs[ino]
      del self._meta[ino]

MemOs._required_globals = ["posixpath", "errno", "time", "stat", "os_fspath", "os_path_split", "FileIO", "convert_open_mode_to_flags"]
