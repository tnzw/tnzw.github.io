# SftpOs.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class SftpOs(object):
  # sftp_os = SftpOs(pysftp.Connection(…))
  # sftp_os._close_conn_on_del = True

  # https://docs.python.org/3/library/os.html
  # https://bitbucket.org/dundeemt/pysftp/src/master/pysftp/__init__.py

  # SFTPAttributes → (st_mode=16895, st_ino=4222124650991797, st_uid=0, st_gid=0, st_size=20480, st_atime=1601902565, st_mtime=1601902565)

  _pysftp_conn = None
  _close_conn_on_del = False
  _proc_fd = None
  name = None
  path = None
  _last_fd_id = 3

  ##windows ex: os.stat_result(st_mode=16895, st_ino=4222124650991797, st_dev=813348024, st_nlink=1, st_uid=0, st_gid=0, st_size=20480, st_atime=1601902565, st_mtime=1601902565, st_ctime=1593107313)
  #class os_stat_result(tuple):  # same as : os_stat_result = collections.namedtuple("os_stat_result", fields, defaults=(0,)*len(fields))
  #  _fields = tuple("st_mode, st_ino, st_dev, st_nlink, st_uid, st_gid, st_size, st_atime, st_mtime".split(", "))
  #  def __new__(cls, *a, **k):
  #    la = len(a)
  #    return tuple.__new__(cls, ((a[i] if i < la else k.get(field, 0)) for i, field in enumerate(cls._fields)))
  #  def __repr__(self): return "SftpOs." + self.__class__.__name__ + "(" + ", ".join(_ + "=" + repr(getattr(self, _)) for _ in self._fields) + ")"
  #  def __getattr__(self, name):
  #    for i, field in enumerate(self._fields):
  #      if field == name: return self[i]
  #    raise AttributeError(repr("SftpOs." + self.__class__.__name__) + " object has no attribute " + repr(name))
  #  def __setattr__(self, name, value):
  #    if name in self._fields: raise AttributeError("readonly attribute")
  #    raise AttributeError(repr("SftpOs." + self.__class__.__name__) + " object has no attribute " + repr(name))
  #  def __delattr__(self, name):
  #    if name in self._fields: raise AttributeError("readonly attribute")
  #    raise AttributeError(repr("SftpOs." + self.__class__.__name__) + " object has no attribute " + repr(name))

  def __init__(self, pysftp_conn, *, cwd=None, path=None, name=None):
    self._pysftp_conn = pysftp_conn
    if name is None: name = "sftp"
    if not isinstance(name, str): raise TypeError("expected str for sftpos.name")
    self.name = name
    self.path = path or posixpath
    if cwd is not None: self._pysftp_conn.chdir(cwd)
    self._proc_fd = {}
  def __del__(self):
    for fd in self._proc_fd:
      self.close(fd)
    if self._close_conn_on_del:
      self._pysftp_conn.close()
  @property
  def sep(self): return "/"
  @property
  def sepb(self): return b"/"
  def _encode_mode(self, mode): return int(oct(mode).lstrip("0o") or 0, 10)
  def _next_fd_id(self):
    self._last_fd_id = self._last_fd_id + 1
    return self._last_fd_id
  def getcwd  (self): return self.fsdecode(self._pysftp_conn.getcwd())
  def getcwdb (self): return self.fsencode(self._pysftp_conn.getcwd())
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
  def fspath(self, path): return os_fspath(path)
  def chdir(self, path): self._pysftp_conn.chdir(path)

  def stat(self, path, *, dir_fd=None, follow_symlinks=True):
    if not follow_symlinks: return self.lstat(path, dir_fd=dir_fd)
    # dir_fd are not handled by pysftp
    if dir_fd is not None: raise NotImplementedError("cannot handle 'dir_fd'")
    return self._pysftp_conn.stat(self.fspath(path))
  def lstat(self, path, *, dir_fd=None):
    # dir_fd are not handled by pysftp
    if dir_fd is not None: raise NotImplementedError("cannot handle 'dir_fd'")
    return self._pysftp_conn.lstat(self.fspath(path))
  def chmod(self, path, mode, *, dir_fd=None, follow_symlinks=True):
    # dir_fd and follow_symlinks are not handled by pysftp
    if dir_fd is not None: raise NotImplementedError("cannot handle 'dir_fd'")
    if not follow_symlinks: raise NotImplementedError("cannot handle follow_symlinks=False")
    self._pysftp_conn.chmod(self.fspath(path), self._encode_mode(mode))
  def chown(self, path, uid, gid, *, dir_fd=None, follow_symlinks=True):
    # dir_fd and follow_symlinks are not handled by pysftp
    if dir_fd is not None: raise NotImplementedError("cannot handle 'dir_fd'")
    if not follow_symlinks: raise NotImplementedError("cannot handle follow_symlinks=False")
    self._pysftp_conn.chown(self.fspath(path), uid, gid)
  def mkdir(self, path, mode=0o777, *, dir_fd=None):
    # dir_fd is not handled by pysftp
    if dir_fd is not None: raise NotImplementedError("cannot handle 'dir_fd'")
    self._pysftp_conn.mkdir(self.fspath(path), self._encode_mode(mode))
  def rmdir(self, path, *, dir_fd=None):
    # dir_fd is not handled by pysftp
    if dir_fd is not None: raise NotImplementedError("cannot handle 'dir_fd'")
    self._pysftp_conn.rmdir(self.fspath(path))
  def utime(self, path, times=None, *, ns=None, dir_fd=None, follow_symlinks=True):
    # ns, dir_fd and follow_symlinks are not handled by pysftp
    if ns is not None: raise NotImplementedError("cannot handle 'ns'")
    if dir_fd is not None: raise NotImplementedError("cannot handle 'dir_fd'")
    if not follow_symlinks: raise NotImplementedError("cannot handle follow_symlinks=False")
    with self._pysftp_conn.open(self.fspath(path), "rb") as f: f.utime(times)
  def remove(self, path, *, dir_fd=None):
    # dir_fd is not handled by pysftp
    if dir_fd is not None: raise NotImplementedError("cannot handle 'dir_fd'")
    self._pysftp_conn.remove(self.fspath(path))
  def unlink(self, path, *, dir_fd=None):
    # dir_fd is not handled by pysftp
    if dir_fd is not None: raise NotImplementedError("cannot handle 'dir_fd'")
    self._pysftp_conn.unlink(self.fspath(path))
  def symlink(self, src, dst, target_is_directory=False, *, dir_fd=None):
    # target_is_directory and dir_fd are not handled by pysftp
    if target_is_directory: raise NotImplementedError("cannot handle 'target_is_directory'")
    if dir_fd is not None: raise NotImplementedError("cannot handle 'dir_fd'")
    self._pysftp_conn.symlink(self.fspath(src), self.fspath(dst))
  def readlink(self, path, *, dir_fd=None):
    # dir_fd is not handled by pysftp
    if dir_fd is not None: raise NotImplementedError("cannot handle 'dir_fd'")
    self._pysftp_conn.readlink(self.fspath(path))
  def truncate(self, path, length):
    if isinstance(path, int): return self.ftruncate(path, length)
    self._pysftp_conn.truncate(self.fspath(path), length)
  def listdir(self, path="."): return self._pysftp_conn.listdir(self.fspath(path))
  #def scandir(self, path="."): XXX use self._pysftp_conn.listdir_attr(self.fspath(path))
  #def access(self, path, mode, *, dir_fd=None, effective_ids=False, follow_symlinks=True): XXX
  #@property
  #def F_OK(self): return os.F_OK
  #@property
  #def R_OK(self): return os.R_OK
  #@property
  #def W_OK(self): return os.W_OK
  #@property
  #def X_OK(self): return os.X_OK
  def rename(self, src, dst, *, src_dir_fd=None, dst_dir_fd=None):
    # dir_fd is not handled by pysftp
    if src_dir_fd is not None or dst_dir_fd is not None: raise NotImplementedError("cannot handle 'dir_fd'")
    self._pysftp_conn.rename(self.fspath(src), self.fspath(dst))
  def open(self, path, flags, mode=0o777, *, dir_fd=None,
           bufsize=-1):
    if mode != 0o777: raise NotImplementedError("cannot handle 'mode'")
    flags = convert_open_flags_to_mode(flags, os_module=self)
    o = self._pysftp_conn.open(self.fspath(path), flags, bufsize=bufsize)
    fd = self._next_fd_id()
    self._proc_fd[fd] = o
    return fd
  def fdopen(self, fd, mode="r", buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    if buffering != -1: raise NotImplementedError("cannot handle 'buffering'")
    if encoding is not None: raise NotImplementedError("cannot handle 'encoding'")
    if errors is not None: raise NotImplementedError("cannot handle 'errors'")
    if newline is not None: raise NotImplementedError("cannot handle 'newline'")
    if not closefd: raise NotImplementedError("cannot handle closefd=False")
    if opener is not None: raise NotImplementedError("cannot handle 'opener'")
    # XXX check already open fd mode
    return self._proc_fd[fd]
  def io_open(self, file, mode="r", buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    if encoding is not None: raise NotImplementedError("cannot handle 'encoding'")
    if errors is not None: raise NotImplementedError("cannot handle 'errors'")
    if newline is not None: raise NotImplementedError("cannot handle 'newline'")
    if not closefd: raise NotImplementedError("cannot handle closefd=False")
    if opener is not None: raise NotImplementedError("cannot handle 'opener'")
    return self._pysftp_conn.open(file, mode=mode, bufsize=buffering)
  @property
  def O_RDONLY(self): return 0
  @property
  def O_WRONLY(self): return 1
  @property
  def O_RDWR  (self): return 2
  @property
  def O_APPEND(self): return 8
  @property
  def O_CREAT (self): return 256
  @property
  def O_TRUNC (self): return 512
  @property
  def O_EXCL  (self): return 1024
  @property
  def O_BINARY(self): return 32768
  def close(self, fd):
    o = self._proc_fd[fd]
    o.close()
    del self._proc_fd[fd]
  def read(self, fd, n):
    io = self._proc_fd[fd]
    read1 = getattr(io, "read1", None)
    if callable(read1): return read1(n)
    return io.read(n)
  def write(self, fd, str):
    l = self._proc_fd[fd].write(str)
    if l is None and isinstance(str, bytes): return len(str)  # XXX We only know the length when its bytes ?
    return l
  def fstat(self, fd):
    io = self._proc_fd[fd]
    return io.stat()
  def fsync(self, fd):
    io = self._proc_fd[fd]
    io.flush()
  def ftruncate(self, fd, length):
    io = self._proc_fd[fd]
    io.truncate(length)
  def lseek(self, fd, pos, how): return self._proc_fd[fd].seek(pos, how)
  @property
  def SEEK_SET(self): return 0
  @property
  def SEEK_CUR(self): return 1
  @property
  def SEEK_END(self): return 2
  @property
  def supports_dir_fd(self): return ()
  @property
  def supports_fd(self): return ()
  @property
  def supports_follow_symlinks(self): return (stat,)
SftpOs._required_globals = ["posixpath", "os_path", "convert_open_flags_to_mode"]