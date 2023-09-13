# SftpOs.py Version 2.1.0
# Copyright (c) 2020, 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def SftpOs(pysftp_conn, *, closeconn=False, name=None):
  _proc_fd = {}
  class __del__:
    def __del__(self): self()
    def __call__(self):
      if _proc_fd:
        for conn in _proc_fd.values():
          conn.close()
      if closeconn:
        pysftp_conn.close()
  __del__ = __del__()

  _module__name__ = 'sftpos'
  _module__doc__ = f"""A module instance of {_module__name__}, please see {_module__name__}.__doc__ for more information."""
  _module__name__ = _module__name__ if __name__ == '__main__' else (__name__ + '.' + _module__name__)
  try: _module__class__ = __builtins__.__class__
  except AttributeError:
    class _module__class__:
      def __init__(self, name): self.__name__ = name
  export = _module__class__(_module__name__)
  export.__doc__ = _module__doc__

  # beginning of module #

  # https://docs.python.org/3/library/os.html
  # https://bitbucket.org/dundeemt/pysftp/src/master/pysftp/__init__.py

  __all__ = []  # XXX
  if name is None: name = 'sftpos'
  elif type(name) is not str: raise TypeError("name must be str")

  _last_fd_id = 3

  def _next_fd_id():
    nonlocal _last_fd_id
    _last_fd_id = _last_fd_id + 1
    return _last_fd_id

  _fsencoding = 'utf-8'
  _fsencodeerrors = 'strict'

  linesep = '\n'
  linesepb = b'\n'

  path = _module_path = posixpath2._mk_module(export, use_environ=False, keep_double_initial_slashes=False)

  # XXX check if str?
  curdir = _module_path.curdir
  pardir = _module_path.pardir
  sep    = _module_path.sep
  altsep = _module_path.altsep
  extsep = _module_path.extsep

  curdirb = curdir.encode('ascii')
  pardirb = pardir.encode('ascii')
  sepb = sep.encode('ascii')
  altsepb = None if altsep is None else altsep.encode('ascii')
  extsep = extsep.encode('ascii')

  def fspath(path): return os_fspath(path)

  def fsencode(filename):
    filename = fspath(filename)
    t = type(filename)
    if t is str: return filename.encode(_fsencoding, _fsencodeerrors)
    if t is bytes: return filename
    raise TypeError(f"expected str, bytes or os.PathLike, not {t.__name__}")

  def fsdecode(filename):
    filename = fspath(filename)
    t = type(filename)
    if t is bytes: return filename.decode(_fsencoding, _fsencodeerrors)
    if t is str: return filename
    raise TypeError(f"expected str, bytes or os.PathLike, not {t.__name__}")

  def getcwd (): return fsdecode(pysftp_conn.getcwd())
  def getcwdb(): return fsencode(pysftp_conn.getcwd())
  def chdir(path): pysftp_conn.chdir(path)

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

  # stat() has the same name as stat module...
  def _module_stat():
    def stat(path, *, dir_fd=None, follow_symlinks=True):
      if follow_symlinks:
        # dir_fd are not handled by pysftp
        if dir_fd is not None: raise NotImplementedError('dir_fd is not implemented on this module')
        #if isinstance(path, int): return pysftp_conn.stat(XXX)
        return pysftp_conn.stat(fspath(path))
      return lstat(path)
    return stat
  export.stat = _module_stat = _module_stat()

  def lstat(path, *, dir_fd=None):
    # dir_fd are not handled by pysftp
    if dir_fd is not None: raise NotImplementedError('dir_fd is not implemented on this module')
    return pysftp_conn.lstat(fspath(path))

  def _encode_mode(mode): return int(oct(mode)[2:], 10)

  def chmod(path, mode, *, dir_fd=None, follow_symlinks=True):
    # dir_fd and follow_symlinks are not handled by pysftp
    if dir_fd is not None: raise NotImplementedError('dir_fd is not implemented on this module')
    if not follow_symlinks: raise NotImplementedError('follow_symlinks is not implemented on chmod()')
    pysftp_conn.chmod(fspath(path), _encode_mode(mode))

  def chown(path, uid, gid, *, dir_fd=None, follow_symlinks=True):
    # dir_fd and follow_symlinks are not handled by pysftp
    if dir_fd is not None: raise NotImplementedError('dir_fd is not implemented on this module')
    if not follow_symlinks: raise NotImplementedError('follow_symlinks is not implemented on chmod()')
    pysftp_conn.chown(fspath(path), uid, gid)

  def mkdir(path, mode=0o777, *, dir_fd=None):
    # dir_fd is not handled by pysftp
    if dir_fd is not None: raise NotImplementedError('dir_fd is not implemented on this module')
    pysftp_conn.mkdir(fspath(path), _encode_mode(mode))

  def rmdir(path, *, dir_fd=None):
    # dir_fd is not handled by pysftp
    if dir_fd is not None: raise NotImplementedError('dir_fd is not implemented on this module')
    pysftp_conn.rmdir(fspath(path))

  def utime(path, times=None, *, ns=None, dir_fd=None, follow_symlinks=True):
    # ns, dir_fd and follow_symlinks are not handled by pysftp
    if ns is not None: raise NotImplementedError('ns is not implemented on utime()')
    if dir_fd is not None: raise NotImplementedError('dir_fd is not implemented on this module')
    if not follow_symlinks: raise NotImplementedError('follow_symlinks is not implemented on chmod()')
    with pysftp_conn.open(fspath(path), 'rb') as f: f.utime(times)

  def remove(path, *, dir_fd=None):
    # dir_fd is not handled by pysftp
    if dir_fd is not None: raise NotImplementedError('dir_fd is not implemented on this module')
    pysftp_conn.remove(fspath(path))

  def unlink(path, *, dir_fd=None):
    # dir_fd is not handled by pysftp
    if dir_fd is not None: raise NotImplementedError('dir_fd is not implemented on this module')
    pysftp_conn.unlink(fspath(path))

  def symlink(src, dst, target_is_directory=False, *, dir_fd=None):
    # target_is_directory and dir_fd are not handled by pysftp
    if target_is_directory: raise NotImplementedError('target_is_directory is not implemented on symlink()')
    if dir_fd is not None: raise NotImplementedError('dir_fd is not implemented on this module')
    pysftp_conn.symlink(fspath(src), fspath(dst))

  def readlink(path, *, dir_fd=None):
    # dir_fd is not handled by pysftp
    if dir_fd is not None: raise NotImplementedError('dir_fd is not implemented on this module')
    return pysftp_conn.readlink(fspath(path))

  def truncate(path, length):
    if isinstance(path, int): return ftruncate(path, length)
    pysftp_conn.truncate(fspath(path), length)

  def listdir(path='.'): return pysftp_conn.listdir(fspath(path))
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
  def rename(src, dst, *, src_dir_fd=None, dst_dir_fd=None):
    # dir_fd is not handled by pysftp
    if src_dir_fd is not None or dst_dir_fd is not None: raise NotImplementedError('dir_fd is not implemented on this module')
    pysftp_conn.rename(fspath(src), fspath(dst))
  def replace(src, dst, *, src_dir_fd=None, dst_dir_fd=None):
    # dir_fd is not handled by pysftp
    if src_dir_fd is not None or dst_dir_fd is not None: raise NotImplementedError('dir_fd is not implemented on this module')
    if pysftp_conn.lexists(dst): pysftp_conn.unlink(fspath(dst))  # required as rename() does not overwrite dst reg files XXX ok?
    pysftp_conn.rename(fspath(src), fspath(dst))

  def open(path, flags, mode=0o777, *, dir_fd=None, bufsize=-1):
    # https://pysftp.readthedocs.io/en/release_0.2.9/pysftp.html#pysftp.Connection.open
    if mode != 0o777: raise NotImplementedError('mode is not implemented on open()')
    flags = convert_open_flags_to_mode(flags, os_module=export)
    if 'x' in flags and 'w' not in flags: flags += 'w'  # well...
    o = pysftp_conn.open(fspath(path), flags, bufsize=bufsize)
    fd = _next_fd_id()
    _proc_fd[fd] = o
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

  #O_NOINHERIT = 0x00080
  O_BINARY    = 0x08000

  #O_CLOEXEC   = 0x80000

  def close(fd):
    o = _proc_fd[fd]
    o.close()
    del _proc_fd[fd]
  def read(fd, n):
    io = _proc_fd[fd]
    read1 = getattr(io, 'read1', None)
    if read1 is not None: return read1(n)
    return io.read(n)
  def write(fd, str):
    l = _proc_fd[fd].write(str)
    if l is None:
      if isinstance(str, bytes): return len(str)  # XXX We only know the length when its bytes ?
    return l
  def fstat(fd):
    io = _proc_fd[fd]
    return io.stat()
  def fsync(fd):
    io = _proc_fd[fd]
    io.flush()
  def ftruncate(fd, length):
    io = _proc_fd[fd]
    io.truncate(length)
  def lseek(fd, pos, how): return _proc_fd[fd].seek(pos, how)
  SEEK_SET = 0
  SEEK_CUR = 1
  SEEK_END = 2
  supports_dir_fd = ()
  supports_fd = ()
  supports_follow_symlinks = (_module_stat,)

  # end of module #
  _module__locals = locals()  # is not exported
  for _ in _module__locals:
    if not _.startswith('_module_') and not hasattr(export, _):
      setattr(export, _, _module__locals[_])
  #del export.__priv__
  del export.export
  return export
SftpOs._required_globals = ['convert_open_flags_to_mode', 'os_fspath', 'posixpath2']
