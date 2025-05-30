# SftpOs.py Version 3.0.0
# Copyright (c) 2020, 2023-2024 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class SftpOs:
  """\
A wrapper class to provide an os module like API over a pysftp connection.
"""
  # https://docs.python.org/3/library/os.html
  # https://bitbucket.org/dundeemt/pysftp/src/master/pysftp/__init__.py

  def __init__(self, pysftp_conn, *, __name__='sftpos', closeconn=False, name=None):
    self.__name__ = __name__
    self.name = __name__ if name is None else name
    if type(self.name) is not str: raise TypeError(f"name must be a str")
    self._pysftp_conn = pysftp_conn
    self._closeconn = closeconn
    self._proc_fd = {}  # {fd: SftpFile}
    self._last_fd_id = 3
    # self.__all__ = []
    self.path = posixpath2._mk_module(os_module=self, use_environ=False, keep_double_initial_slashes=False)

  def __del__(self):
    if self._proc_fd:
      for conn in self._proc_fd.values():
        conn.close()
      if self._closeconn:
        self._pysftp_conn.close()

  def _next_fd_id(self):
    self._last_fd_id = self._last_fd_id + 1
    return self._last_fd_id

  _fsencoding = 'utf8'
  _fsencodeerrors = 'strict'

  linesep = '\n'

  # XXX def __dir__(self):
  def __getattr__(self, name):
    if name in ('curdir', 'pardir', 'sep', 'altsep', 'extsep'): return getattr(self.path, name)
    raise AttributeError(f"module '{self.__name__}' has no attribute '{name}'")

  def fspath(self, path): return os_fspath(path)

  def fsencode(self, filename):
    filename = self.fspath(filename)
    t = type(filename)
    if t is str: return filename.encode(self._fsencoding, self._fsencodeerrors)
    if t is bytes: return filename
    raise TypeError(f"expected str, bytes or os.PathLike, not {t.__name__}")

  def fsdecode(self, filename):
    filename = self.fspath(filename)
    t = type(filename)
    if t is bytes: return filename.decode(self._fsencoding, self._fsencodeerrors)
    if t is str: return filename
    raise TypeError(f"expected str, bytes or os.PathLike, not {t.__name__}")

  def getcwd (self): return self.fsdecode(self._pysftp_conn.getcwd())
  def getcwdb(self): return self.fsencode(self._pysftp_conn.getcwd())
  def chdir(self, path): self._pysftp_conn.chdir(path)

  # SFTPAttributes → (st_mode=16895, st_ino=4222124650991797, st_uid=0, st_gid=0, st_size=20480, st_atime=1601902565, st_mtime=1601902565)

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

  def stat(self, path, *, dir_fd=None, follow_symlinks=True):
    if follow_symlinks:
      # dir_fd are not handled by pysftp
      if dir_fd is not None: raise NotImplementedError("dir_fd is not implemented on this module")
      # XXX could I use file descriptors on pysftp stat()? check with other methods.
      if isinstance(path, int): raise NotImplementedError("file descriptors not handled")
      return self._pysftp_conn.stat(self.fspath(path))
    return self.lstat(path)

  def lstat(self, path, *, dir_fd=None):
    # dir_fd are not handled by pysftp
    if dir_fd is not None: raise NotImplementedError("dir_fd is not implemented on this module")
    return self._pysftp_conn.lstat(self.fspath(path))

  @staticmethod
  def _encode_mode(mode): return int(oct(mode)[2:], 10)

  def chmod(self, path, mode, *, dir_fd=None, follow_symlinks=True):
    # dir_fd and follow_symlinks are not handled by pysftp
    if dir_fd is not None: raise NotImplementedError("dir_fd is not implemented on this module")
    if not follow_symlinks: raise NotImplementedError("follow_symlinks is not implemented on chmod()")
    self._pysftp_conn.chmod(self.fspath(path), SftpOs._encode_mode(mode))

  def chown(self, path, uid, gid, *, dir_fd=None, follow_symlinks=True):
    # dir_fd and follow_symlinks are not handled by pysftp
    if dir_fd is not None: raise NotImplementedError("dir_fd is not implemented on this module")
    if not follow_symlinks: raise NotImplementedError("follow_symlinks is not implemented on chmod()")
    self._pysftp_conn.chown(self.fspath(path), uid, gid)

  def mkdir(self, path, mode=0o777, *, dir_fd=None):
    # dir_fd is not handled by pysftp
    if dir_fd is not None: raise NotImplementedError("dir_fd is not implemented on this module")
    self._pysftp_conn.mkdir(self.fspath(path), SftpOs._encode_mode(mode))

  def rmdir(self, path, *, dir_fd=None):
    # dir_fd is not handled by pysftp
    if dir_fd is not None: raise NotImplementedError("dir_fd is not implemented on this module")
    self._pysftp_conn.rmdir(self.fspath(path))

  def utime(self, path, times=None, *, ns=None, dir_fd=None, follow_symlinks=True):
    # ns, dir_fd and follow_symlinks are not handled by pysftp
    if ns is not None: raise NotImplementedError("ns is not implemented on utime()")
    if dir_fd is not None: raise NotImplementedError("dir_fd is not implemented on this module")
    if not follow_symlinks: raise NotImplementedError("follow_symlinks is not implemented on chmod()")
    with self._pysftp_conn.open(self.fspath(path), 'rb') as f: f.utime(times)

  def remove(self, path, *, dir_fd=None):
    # dir_fd is not handled by pysftp
    if dir_fd is not None: raise NotImplementedError("dir_fd is not implemented on this module")
    self._pysftp_conn.remove(self.fspath(path))

  def unlink(self, path, *, dir_fd=None):
    # dir_fd is not handled by pysftp
    if dir_fd is not None: raise NotImplementedError("dir_fd is not implemented on this module")
    self._pysftp_conn.unlink(self.fspath(path))

  def symlink(self, src, dst, target_is_directory=False, *, dir_fd=None):
    # target_is_directory and dir_fd are not handled by pysftp
    if target_is_directory: raise NotImplementedError("target_is_directory is not implemented on symlink()")
    if dir_fd is not None: raise NotImplementedError("dir_fd is not implemented on this module")
    self._pysftp_conn.symlink(self.fspath(src), self.fspath(dst))

  def readlink(self, path, *, dir_fd=None):
    # dir_fd is not handled by pysftp
    if dir_fd is not None: raise NotImplementedError("dir_fd is not implemented on this module")
    return self._pysftp_conn.readlink(self.fspath(path))

  def truncate(self, path, length):
    if isinstance(path, int): return self.ftruncate(path, length)
    self._pysftp_conn.truncate(self.fspath(path), length)

  def listdir(self, path='.'): return self._pysftp_conn.listdir(self.fspath(path))
  #def scandir(path='.'): XXX use pysftp_conn.listdir_attr(fspath(path))
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
    if src_dir_fd is not None or dst_dir_fd is not None: raise NotImplementedError('dir_fd is not implemented on this module')
    self._pysftp_conn.rename(self.fspath(src), self.fspath(dst))
  def replace(self, src, dst, *, src_dir_fd=None, dst_dir_fd=None):
    # dir_fd is not handled by pysftp
    if src_dir_fd is not None or dst_dir_fd is not None: raise NotImplementedError('dir_fd is not implemented on this module')
    fdst = self.fspath(dst)
    if self._pysftp_conn.lexists(fdst): self._pysftp_conn.unlink(fdst)  # required as rename() does not overwrite dst reg files XXX ok?
    self._pysftp_conn.rename(self.fspath(src), fdst)

  def open(self, path, flags, mode=0o777, *, dir_fd=None, bufsize=-1):
    # https://pysftp.readthedocs.io/en/release_0.2.9/pysftp.html#pysftp.Connection.open
    if mode != 0o777: raise NotImplementedError('mode is not implemented on open()')
    flags = convert_open_flags_to_mode(flags, os_module=self)
    if 'x' in flags and 'w' not in flags: flags += 'w'  # well...
    o = self._pysftp_conn.open(self.fspath(path), flags, bufsize=bufsize)
    fd = self._next_fd_id()
    self._proc_fd[fd] = o
    return fd

  # def fdopen(self, fd, mode="r", buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    # if buffering != -1: raise NotImplementedError("cannot handle 'buffering'")
    # if encoding is not None: raise NotImplementedError("cannot handle 'encoding'")
    # if errors is not None: raise NotImplementedError("cannot handle 'errors'")
    # if newline is not None: raise NotImplementedError("cannot handle 'newline'")
    # if not closefd: raise NotImplementedError("cannot handle closefd=False")
    # if opener is not None: raise NotImplementedError("cannot handle 'opener'")
    # # XXX check already open fd mode
    # return self._proc_fd[fd]
  # def io_open(self, file, mode="r", buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    # if encoding is not None: raise NotImplementedError("cannot handle 'encoding'")
    # if errors is not None: raise NotImplementedError("cannot handle 'errors'")
    # if newline is not None: raise NotImplementedError("cannot handle 'newline'")
    # if not closefd: raise NotImplementedError("cannot handle closefd=False")
    # if opener is not None: raise NotImplementedError("cannot handle 'opener'")
    # return self._pysftp_conn.open(file, mode=mode, bufsize=buffering)

  O_RDONLY    = 0x00000
  O_WRONLY    = 0x00001
  O_RDWR      = 0x00002
  O_APPEND    = 0x00008  # 0x400
  O_CREAT     = 0x00100  # 0x040
  O_EXCL      = 0x00400  # 0x080
  O_TRUNC     = 0x00200

  # O_NOINHERIT = 0x00080
  # O_BINARY    = 0x08000

  # O_CLOEXEC   = 0x80000

  def close(self, fd):
    o = self._proc_fd[fd]
    o.close()
    del self._proc_fd[fd]
  def read(self, fd, n):
    io = self._proc_fd[fd]
    read1 = getattr(io, 'read1', None)
    if read1 is not None: return read1(n)
    return io.read(n)
  def write(self, fd, str):
    l = self._proc_fd[fd].write(str)
    if l is None:
      if isinstance(str, bytes): return len(str)  # XXX We only know the length when its bytes ?
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
  SEEK_SET = 0
  SEEK_CUR = 1
  SEEK_END = 2
  supports_dir_fd = ()
  supports_fd = ()
  supports_follow_symlinks = (stat,)

SftpOs._required_globals = ['convert_open_flags_to_mode', 'os_fspath', 'posixpath2']
