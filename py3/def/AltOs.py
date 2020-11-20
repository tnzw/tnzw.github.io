# AltOs.py Version 1.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class AltOs(object):  # XXX TEST THE WHOLE CLASS !
  """\
Same as os module but with:
- fsdecode uses str.decode("UTF-8", "strict") every time
- chdir / chroot does not check if directory exists
- chdir / chroot are using a fake process chdir / chroot
- chroot works on windows
- chroot automatically changes cwd to b"/" if chroot is child of cwd
- XXX chown is equal to noop on windows
- you can mount other "os" with alt_os.mount("/mnt", Ftp_Os("url", "usr", "pwd"))
- symlinks are followed to the same mount point (os following) instead of following in AltOs moint points
"""
  # https://docs.python.org/3/library/os.html
  _proc_root = None
  _proc_cwd = None
  _proc_mounts = None
  _proc_fd = None
  name = None
  path = None
  def __init__(self, *, cwd=None, root=b"", path=None, name=None, mounts=None):
    if name is None: name = os.name
    if not isinstance(name, str): raise TypeError("expected str for alt_os.name")
    self.name = name
    self.path = path or os.path
    if cwd is None: cwd = self.path.normpath(os.getcwdb())
    self._proc_root = self.fsencode(self.path.normpath(root)) if root else root
    self._proc_cwd = self.fsencode(cwd)
    self._proc_mounts = {} if mounts is None else mounts.copy()
    self._proc_fd = {}
  def __del__(self):
    for fd in self._proc_fd:
      self.close(fd)
  def new_from_here(self):
    return self.__class__(cwd=self._proc_cwd, root=self._proc_root, path=self.path, name=self.name, mounts=self._proc_mounts)
  @property
  def sep(self): return self.path.sep
  @property
  def sepb(self): return self.path.sep.encode("UTF-8", "strict")
  def _realpath(self, path):
    if self._proc_root.endswith(self.sepb):
      XXX_is_this_block_really_used
      return self._proc_root + self.path.normpath(self.path.join(self._proc_cwd, self.fsencode(path))).lstrip(self.sepb)
    if self._proc_cwd.startswith(self.sepb):
      return self._proc_root + self.path.normpath(self.path.join(self._proc_cwd, self.fsencode(path)))
    if self._proc_root:
      return self._proc_root + self.sepb + self.path.normpath(self.path.join(self._proc_cwd, self.fsencode(path)))
    return self.path.normpath(self.path.join(self._proc_cwd, self.fsencode(path)))
    #if type is bytes: return res
    #return self.fsdecode(res)
  def _call_os_method_path_a_k(self, *a, **k):
    method, path = a[0:2]
    pathb = self._realpath(path)
    for m, o in self._proc_mounts.items():
      if (pathb + self.sepb).startswith(m + self.sepb):
        pathb = pathb[len(m) + len(self.sepb):]
        if isinstance(path, str): path = self.fsdecode(pathb)
        return getattr(o, method)(path, *a[2:], **k)
    if isinstance(path, str): path = self.fsdecode(pathb)
    return getattr(os, method)(path, *a[2:], **k)
  def _call_os_method_fd_a_k(self, *a, **k):
    method, fd = a[0:2]
    o = self._proc_fd[fd]
    if o is self: return getattr(os, method)(fd, *a[2:], **k)
    return getattr(o, method)(fd, *a[2:], **k)
  def _convert_open_flags(self, flags, os):
    if os.O_RDONLY != 0: raise NotImplementedError("cannot handle O_RDONLY != 0")
    new_flags = 0
    for attr in "O_WRONLY O_RDWR O_APPEND O_CREAT O_EXCL O_TRUNC O_BINARY".split():
      new_flags |= getattr(os, attr) if flags & getattr(self, attr) else 0
    return new_flags
  def _convert_lseek_how(self, how, os):
    how = (self.SEEK_SET, self.SEEK_CUR, self.SEEK_END).index(how)
    return (os.SEEK_SET, os.SEEK_CUR, os.SEEK_END)[how]
  def getcwd  (self): return self.fsdecode(self._proc_cwd)
  def getcwdb (self): return self._proc_cwd
  def fsencode(self, filename):
    filename = self.fspath(filename)
    if isinstance(filename, bytes): return filename
    if isinstance(filename, str): return filename.encode("UTF-8")
    raise TypeError("expected str or bytes, not " + type(filename))
  def fsdecode(self, filename):
    filename = self.fspath(filename)
    if isinstance(filename, str): return filename
    if isinstance(filename, bytes): return filename.decode("UTF-8", "strict")
    raise TypeError("expected str or bytes, not " + type(filename))  # XXX os.PathLike
  def fspath(self, path): return os.fspath(path)
  def chdir(self, path): self._proc_cwd = self.path.normpath(self.path.join(self._proc_cwd, self.fsencode(path)))
  def chroot(self, path):
    path = self.fspath(path)
    path = self._realpath(path)
    self._proc_root = path
    self._proc_cwd = (self._proc_cwd[len(path):] or self.sepb) if self._proc_cwd.startswith(path) else self.sepb
  def mount(self, path, os):
    path = self.fspath(path)
    path = self._realpath(path)
    self._proc_mounts[path] = os
  def stat(self, path, *a, **k): return self._call_os_method_path_a_k("stat", path, *a, **k)
  def lstat(self, path, *a, **k): return self._call_os_method_path_a_k("lstat", path, *a, **k)
  def chmod(self, path, *a, **k): return self._call_os_method_path_a_k("chmod", path, *a, **k)
  def chown(self, path, *a, **k): return self._call_os_method_path_a_k("chown", path, *a, **k)  # XXX do it after checking mount point : if self.name != "nt" else None
  def mkdir(self, path, *a, **k): return self._call_os_method_path_a_k("mkdir", path, *a, **k)
  def rmdir(self, path, *a, **k): return self._call_os_method_path_a_k("rmdir", path, *a, **k)
  def utime(self, path, *a, **k): return self._call_os_method_path_a_k("utime", path, *a, **k)
  def remove(self, path, *a, **k): return self._call_os_method_path_a_k("remove", path, *a, **k)
  def unlink(self, path, *a, **k): return self._call_os_method_path_a_k("unlink", path, *a, **k)
  def symlink(self, src, dst, *a, **k):
    pathb = self._realpath(dst)
    for m, o in self._proc_mounts.items():
      if (pathb + self.sepb).startswith(m + self.sepb):
        pathb = pathb[len(m) + len(self.sepb):]
        if isinstance(dst, str): dst = self.fsdecode(pathb)
        return o.symlink(src, dst, *a[3:], **k)
    if isinstance(dst, str): dst = self.fsdecode(pathb)
    return os.symlink(src, dst, *a[3:], **k)
  def readlink(self, path, *a, **k): return self._call_os_method_path_a_k("readlink", path, *a, **k)
  def truncate(self, path, *a, **k): return self._call_os_method_path_a_k("truncate", path, *a, **k)
  def listdir(self, path=".", *a, **k): return self._call_os_method_path_a_k("listdir", path, *a, **k)
  def scandir(self, path=".", *a, **k): return self._call_os_method_path_a_k("scandir", path, *a, **k)
  def access(self, path, *a, **k): return self._call_os_method_path_a_k("access", path, *a, **k)
  @property
  def F_OK(self): return os.F_OK
  @property
  def R_OK(self): return os.R_OK
  @property
  def W_OK(self): return os.W_OK
  @property
  def X_OK(self): return os.X_OK
  def rename(self, src, dst):#, *, src_dir_fd=None, dst_dir_fd=None):
    # XXX how to handle dir_fds ?!
    src = self.fspath(src)
    dst = self.fspath(dst)
    srcb = self._realpath(src)
    dstb = self._realpath(dst)
    for srcm, srco in self._proc_mounts.items() + [("", None)]:
      if (srcb + self.sepb).startswith(srcm + self.sepb):
        break
    for dstm, dsto in self._proc_mounts.items() + [("", None)]:
      if (dstb + self.sepb).startswith(dstm + self.sepb):
        break
    if isinstance(src, str): srcb = self.fsdecode(srcb)
    if isinstance(dst, str): dstb = self.fsdecode(dstb)
    if srco is None and dsto is None:
      return os.rename(srcb, dst)
    if srco is dsto:
      return srco.rename(srcb, dst)
    raise OSError(errno.EXDEV, "Cannot move file to a mountpoint", src, 17, dst)  # EXDEV = 18
  def open(self, path, flags, *a, **k):
    method = "open"
    path = self._realpath(path)
    for m, o in self._proc_mounts.items():
      if (path + self.sepb).startswith(m + self.sepb):
        path = path[len(m) + len(self.sepb):]
        flags = self._convert_open_flags(flags, o)
        fd = getattr(o, method)(path, flags, *a, **k)
        self._proc_fd[fd] = o
        return fd
    fd = getattr(os, method)(path, flags, *a, **k)
    self._proc_fd[fd] = self
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
  def close(self, fd):
    o = self._proc_fd[fd]
    if o is self: os.close(fd)
    else: o.close(fd)
    del self._proc_fd[fd]
  def read(self, fd, *a, **k): return self._call_os_method_fd_a_k("read", fd, *a, **k)
  def write(self, fd, *a, **k): return self._call_os_method_fd_a_k("write", fd, *a, **k)
  def fstat(self, fd, *a, **k): return self._call_os_method_fd_a_k("fstat", fd, *a, **k)
  def fsync(self, fd, *a, **k): return self._call_os_method_fd_a_k("fsync", fd, *a, **k)
  def fdopen(self, fd, *a, **k): return self._call_os_method_fd_a_k("fdopen", fd, *a, **k)
  def ftruncate(self, fd, *a, **k): return self._call_os_method_fd_a_k("ftruncate", fd, *a, **k)
  def lseek(self, fd, pos, how):
    method = "lseek"
    o = self._proc_fd[fd]
    if o is self: return getattr(os, method)(fd, pos, how)
    how = self._convert_lseek_how(how, o)
    return getattr(o, method)(fd, pos, how)
  SEEK_SET = 0
  SEEK_CUR = 1
  SEEK_END = 2

AltOs._required_globals = ["os", "errno"]
