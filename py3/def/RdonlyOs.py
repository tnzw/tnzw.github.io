# RdonlyOs.py Version 2.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def RdonlyOs(*, os_module=None):
  """\
Same as os module but disallow writing the file system
"""
  _module__name__ = 'rdonlyos'
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

  if os_module is None: os_module = os
  _os = os_module
  del os_module
  undefined = []
  for _ in ('error', 'name', 'path', 'SEEK_SET', 'SEEK_CUR', 'SEEK_END', 'O_RDONLY', 'O_WRONLY', 'O_RDWR', 'O_APPEND', 'O_CREAT', 'O_EXCL', 'O_TRUNC', 'O_BINARY', 'O_NOINHERIT', 'curdir', 'pardir', 'sep', 'altsep', 'exstep', 'pathsep', 'linesep'):
    v = getattr(_os, _, undefined)
    if v is not undefined: setattr(export, _, v)
  for _ in ('fsencode', 'fsdecode', 'fspath', 'umask', 'close', 'dup', 'dup2', 'fstat', 'isatty', 'lseek', 'pread', 'preadv', 'read', 'readv', 'chdir', 'chroot', 'getcwd', 'getcwdb', 'listdir', 'lstat', 'readlink', 'scandir', 'stat', 'walk', 'fwalk'):
    v = getattr(_os, _, undefined)
    if v is not undefined: setattr(export, _, v)
  def mknop(_):
    def fn(*a,**k): raise OSError(errno.EROFS, "Read-only file system")
    fn.__name__ = _
    return fn
  for _ in ('copy_file_range', 'fchmod', 'fchown', 'fdatasync', 'fsync', 'ftruncate', 'pwrite', 'pwritev', 'write', 'writev', 'chmod', 'chown', 'lchmod', 'lchown', 'link', 'mkdir', 'makedirs', 'remove', 'removedirs', 'rename', 'replace', 'rmdir', 'symlink', 'sync', 'truncate', 'unlink', 'utime'):
    setattr(export, _, mknop(_))
  # for _ in "supports_dir_fd supports_effective_ids supports_fd supports_follow_symlinks".split(): XXX
  def open(self, path, flags, mode=0o777, *, dir_fd=None):
    if flags & sum(getattr(self, _, 0) for _ in "O_WRONLY O_RDWR O_APPEND O_CREAT O_TRUNC".split()): raise OSError(errno.EROFS, "Read-only file system")
    return _os.open(path, flags, mode=mode, dir_fd=dir_fd)
  def fdopen(self, fd, mode="r", *a, **k):
    if "r" not in mode or "+" in mode: raise OSError(errno.EROFS, "Read-only file system")
    return _os.fdopen(fd, mode=mode, *a, **k)
  del undefined

  # end of module #
  _module__locals = locals()  # is not exported
  for _ in _module__locals:
    if not _.startswith('_module_') and not hasattr(export, _):
      setattr(export, _, _module__locals[_])
  #del export.__priv__
  del export.export
  return export
RdonlyOs._required_globals = ['os', 'errno']
