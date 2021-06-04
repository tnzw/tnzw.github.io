# AltOs.py Version 1.1.5
# Copyright (c) 2020-2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class AltOs(object):
  """\
Same as os module but with:
- fsdecode uses str.decode("UTF-8", "strict") on every platform
- chdir / chroot does not check if directory exists
- chdir / chroot are using a fake process chdir / chroot
- chroot works on windows
- chroot automatically changes cwd to b"/" if chroot is child of cwd
- chown is equal to noop on windows (but can still use chown on mounted OSes)
- you can mount other "os" with alt_os.mount("/mnt", FtpOs("url", "usr", "pwd"))
    however, "/mnt" is still part of os, not FtpOs.
- symlinks are followed to the same mount point (os following) instead of following in AltOs moint points
"""
  # https://docs.python.org/3/library/os.html

  _proc_fd = None
  _proc_cwd = None
  _proc_root = None
  _proc_mounts = None
  _umask = 0o000
  _FD_START = 3

  error = OSError
  name = None
  path = None

  def __init__(self, *, name=None, path=None, cwd=None, umask=0o000, root=None, os_module=None):
    self.os = os if os_module is None else os_module
    if name is None: name = self.os.name
    if not isinstance(name, str): raise TypeError("expected str for alt_os.name")
    self.name = name
    self.path = self.os.path if path is None else path
    self._proc_fd = {}
    if cwd is None: cwd = self.os.getcwdb()
    if umask is None: umask = 0o000
    self._umask = umask & 0o777
    self._proc_cwd = self._tuplepath(cwd).fsencode().norm()
    self._proc_root = self._tuplepath(b"") if root is None else self._tuplepath(root).fsencode().norm()
    self._proc_mounts = {}

  def __del__(self):
    for fd in self._proc_fd:
      self.close(fd)

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

  def fdopen(self, fd, *a, **k): return self._call_fd("fdopen", fd, *a, **k)

  # File Descriptor Operations

  def close(self, fd):
    self._call_fd("close", fd)
    #XXXfds = self._getcheck_fd(fd)
    #else: fds["os"].close(fds["fd"])
    del self._proc_fd[fd]

  #def copy_file_range(self, src, dst, count, offset_src=None, offset_dst=None): XXX
  #def dup(self, fd): XXX
  #def dup2 XXX ?

  def fchmod(self, fd, mode): return self._call_fd("fchmod", fd, mode)
  def fchown(self, fd, uid, gid): return self._call_fd("fchown", fd, uid, gid)
  def fstat(self, fd): return self._call_fd("fstat", fd)
  def fdatasync(self, fd): return self._call_fd("fdatasync", fd)
  def fsync(self, fd): return self._call_fd("fsync", fd)
  def ftruncate(self, fd, length): return self._call_fd("ftruncate", fd, length)
  def isatty(self, fd): return self._call_fd("isatty", fd)

  def lseek(self, fd, pos, how):
    fds = self._getcheck_fd(fd)
    return fds["os"].lseek(fds["fd"], pos, self._convert_lseek_how(how, fds["os"]))

  SEEK_SET = 0
  SEEK_CUR = 1
  SEEK_END = 2

  def open(self, path, flags, mode=0o777, *, dir_fd=None):
    mode = mode & (0o777 - self._umask)  # XXX I think umask is applied, right ?
    subpath, os = self._traverse(path, dir_fd=dir_fd)
    ofd = os.open(subpath, self._convert_open_flags(flags, os, 0), mode=mode)
    fds = {
      "fd": ofd, "os": os,
      "traversed": subpath,  # used by dir_fd functions
    }
    fd = self._next_fd()
    self._proc_fd[fd] = fds
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

  #def pread(self, fd, n, offset): XXX
  #def preadv(self, fd, buffers, offset, flags=0): XXX
  #def pwrite(self, fd, str, offset): XXX
  #def pwritev(self, fd, buffers, offset, flags=0): XXX
  def read(self, fd, n): return self._call_fd("read", fd, n)
  #def readv(self, fd, buffers): XXX
  def write(self, fd, str): return self._call_fd("write", fd, str)
  #def writev(self, fd, buffers): XXX

  # Querying the size of a terminal
  # - no terminal here, of course

  # Inheritance of File Descriptors
  # XXX

  # Files and Directories

  #def access

  def chdir(self, path): self._proc_cwd = self._abspath(path)

  def chmod(self, path, mode, *, dir_fd=None, follow_symlinks=True): return self._call_pathorfd("chmod", path, mode, dir_fd=dir_fd, follow_symlinks=follow_symlinks)
  def chown(self, path, uid, gid, *, dir_fd=None, follow_symlinks=True): return self._call_pathorfd("chown", path, mode, dir_fd=dir_fd, follow_symlinks=follow_symlinks)

  def chroot(self, path):
    if not path: raise FileNotFoundError(errno.ENOENT, "No such file or directory", path)
    abspath = self._abspath(path)
    try: common = self._proc_cwd.commonpath((abspath,))
    except ValueError: cwd = self._proc_cwd[:0].root(self._proc_cwd.rootname[len(self._proc_cwd.drivename):])
    else:
      if abspath == common: cwd = self._proc_cwd[len(common):].root(self._proc_cwd.sep).norm()
      else: cwd = self._proc_cwd.root().root(self._proc_cwd.sep)
    newroot = self._realpath(abspath)
    self._proc_root, self._proc_cwd = newroot, cwd

  def mount(self, path, os):
    realpath = self._realpath(path).pathname
    if realpath in self._proc_mounts: raise OSError(errno.EINVAL, "Mountpoint already exists")
    self._proc_mounts[realpath] = os
  def unmount(self, path):
    realpath = self._realpath(path).pathname
    if realpath not in self._proc_mounts: raise OSError(errno.EINVAL, "Mountpoint does not exist")
    del self._proc_mounts[realpath]

  def getcwd(self): return self.fsdecode(self.getcwdb())
  def getcwdb(self): return self._proc_cwd.pathname
  def lchmod(self, path, mode): return self.chmod(path, mode, follow_symlinks=False)
  def lchown(self, path, uid, gid): return self.chown(path, uid, gid, follow_symlinks=False)
  def link(self, src, dst, *, src_dir_fd=None, dst_dir_fd=None, follow_symlinks=True): return self._call_srcdst("link", src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd, follow_symlinks=follow_symlinks)
  def listdir(self, path="."): return self._call_path("listdir", path)
  def lstat(self, path, *, dir_fd=None): return self.stat(path, dir_fd=dir_fd, follow_symlinks=False)
  def mkdir(self, path, mode=0o777, *, dir_fd=None):
    mode = mode & (0o777 - self._umask)
    return self._call_path("mkdir", path, mode=mode, dir_fd=dir_fd)
  def makedirs(self, name, mode=0o777, exist_ok=False): return os_makedirs(name, mode=mode, exist_ok=exist_ok, os_module=self)
  def readlink(self, path, *, dir_fd=None): return self._call_path("readlink", path, dir_fd=dir_fd)
  def remove(self, path, *, dir_fd=None): return self._call_path("remove", path, dir_fd=dir_fd)
  def removedirs(self, name): return os_removedirs(name, os_module=self)
  def rename(self, src, dst, *, src_dir_fd=None, dst_dir_fd=None): return self._call_srcdst("rename", src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)
  def replace(self, src, dst, *, src_dir_fd=None, dst_dir_fd=None): return self._call_srcdst("replace", src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)
  def rmdir(self, path, *, dir_fd=None): return self._call_path("rmdir", path, dir_fd=dir_fd)
  def scandir(self, path="."): return self._call_path("scandir", path)
  def stat(self, path, *, dir_fd=None, follow_symlinks=True): return self._call_pathorfd("stat", path, dir_fd=dir_fd, follow_symlinks=follow_symlinks)
  def symlink(self, src, dst, target_is_directory=False, *, dir_fd=None): return self._call_srcdst("symlink", src, dst, target_is_directory=target_is_directory, dst_dir_fd=dir_fd)
  def sync(self):
    self.os.sync()
    for mos in self._proc_mounts.values(): mos.sync()
  def truncate(self, path, length): return self._call_pathorfd("truncate", path, length)
  def unlink(self, path, *, dir_fd=None): return self._call_path("unlink", path, dir_fd=dir_fd)
  def utime(self, *a, **k):
    def param_checker(path, times=None, *, ns=None, dir_fd=None, follow_symlinks=True): pass
    param_checker(*a, **k)  # to avoid -> ValueError: utime: you may specify either 'times' or 'ns' but not both
    return self._call_pathorfd("utime", *a, **k)
  def walk(self, top, topdown=True, onerror=True, followlinks=False):
    return os_walk(top, topdown=topdown, onerror=onerror, followlinks=followlinks, os_module=self)
  def fwalk(self, top=".", topdown=True, onerror=True, *, follow_symlinks=False, dir_fd=None):
    return os_fwalk(top, topdown=topdown, onerror=onerror, follow_symlinks=follow_symlinks, dir_fd=dir_fd, os_module=self)

  supports_dir_fd = (chmod, chown, fwalk, link, lstat, mkdir, open, readlink, remove, rename, rmdir, stat, symlink, unlink, utime)
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

  def _next_fd(self):  # XXX not cocurrent safe
    fd = self._FD_START
    while fd in self._proc_fd: fd += 1
    return fd

  def _tuplepath(self, path):
    if isinstance(path, tuplepath): return tuplepath(path.tuple, os_module=self)
    return tuplepath(path, os_module=self)

  def _realpath(self, path, in_chroot=False):
    tpath = self._proc_cwd.join(path).fsencode().norm()
    if not in_chroot and self._proc_root: tpath = self._proc_root.extend(tpath).norm()
    return tpath

  def _abspath(self, path): return self._realpath(path, in_chroot=True)

  def _traverse(self, path, *, normpath=True, dir_fd=None, error_path=None, error_dst=None):
    if error_path is None: error_path = path
    if not self.path.isabs(path) and dir_fd is not None:
      fd_realpath = self._getcheck_fd(fd)["realpath"]
      if self._proc_root and self._proc_root.commonpath((fd_realpath,)) != self._proc_root: raise FileNotFoundError(errno.ENOENT, "No such file or directory", error_path)
      realpath = self._proc_root.join(fd_realpath[len(self._proc_root):].join(path).norm())
    else:
      realpath = self._realpath(path)
    for i in range(len(realpath), 0, -1):
      m = realpath[:i].pathname
      if m in self._proc_mounts: return realpath[i:], self._proc_mounts[m]
    return realpath, self.os

  def _getcheck_fd(self, fd):
    if fd in self._proc_fd: return self._proc_fd[fd]
    raise OSError(errno.EBADF, "Bad file descriptor")

  def _call_fd(self, *a, **k):
    method, fd = a[:2]
    fds = self._getcheck_fd(fd)
    return getattr(fds["os"], method)(fds["fd"], *a[2:], **k)

  def _call_path(self, *a, dir_fd=None, **k):
    method, path = a[:2]
    path = self.fspath(path)
    subpath, os = self._traverse(path, dir_fd=dir_fd)
    if isinstance(path, str): subpath = subpath.fsdecode()
    return getattr(os, method)(subpath.pathname, *a[2:], **k)

  def _call_pathorfd(self, *a, dir_fd=None, **k):
    method, pathorfd = a[:2]
    if isinstance(pathorfd, int): return self._call_fd(*a, dir_fd=dir_fd, **k)
    return self._call_path(*a, dir_fd=dir_fd, **k)

  def _call_srcdst(self, *a, dir_fd=None, src_dir_fd=None, dst_dir_fd=None, **k):
    method, src, dst = a[:3]
    src, dst = self.fspath(src), self.fspath(dst)
    subsrc, ossrc = self._traverse(src, dir_fd=src_dir_fd, error_path=src, error_dst=dst)
    subdst, osdst = self._traverse(dst, dir_fd=dst_dir_fd, error_path=src, error_dst=dst)
    if ossrc is not osdst: raise OSError(errno.EXDEV, "Invalid cross-device link", src, 17, dst)
    if isinstance(src, str): subsrc = subsrc.fsdecode()
    if isinstance(dst, str): subdst = subdst.fsdecode()
    return getattr(ossrc, method)(subsrc.pathname, subdst.pathname, *a[3:], **k)

  def _convert_lseek_how(self, how, os):
    how = (self.SEEK_SET, self.SEEK_CUR, self.SEEK_END).index(how)
    return (os.SEEK_SET, os.SEEK_CUR, os.SEEK_END)[how]

  def _convert_open_flags(self, flags, os, *soft):
    if os.O_RDONLY != 0: raise NotImplementedError("cannot handle O_RDONLY != 0")
    new_flags = 0
    for attr in "WRONLY RDWR APPEND CREAT EXCL TRUNC BINARY NOINHERIT".split():
      new_flags |= getattr(os, "O_" + attr, *soft) if flags & getattr(self, "O_" + attr) else 0
    return new_flags

AltOs._required_globals = ["os", "errno", "tuplepath", "os_fspath", "os_fwalk", "os_makedirs", "os_path_split", "os_removedirs", "os_walk"]
