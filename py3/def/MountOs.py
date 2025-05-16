# MountOs.py Version 1.0.0
#   This is free and unencumbered software released into the public domain.
#   SPDX: Unlicense <http://unlicense.org/>
#   Contributors: 2024 <tnzw@github.triton.ovh>

class MountOs:
  """\
Usage:
  mos = MountOs()
  mos.mount('mount_point_id', os)
  mos.open('mount_point_id/sub/path/to/source/file.txt', mos.O_RDONLY | mos.O_BINARY)

- Contains only necessary functions to manipulate nodes inside the mounted OSes.
- Does not contain any path mechanism except for the first separator of the path
  to extract the mount point ID.
- Given paths must be PathLike objects, str or bytes.
"""
  # https://docs.python.org/3/library/os.html

  def __init__(self, *, __name__='mountos', name=None, sep='/', altsep=None):
    self.__name__ = __name__
    assert len(sep) == 1
    assert altsep is None or len(altsep) == 1
    self.name = __name__ if name is None else name
    self.sep = sep
    self.altsep = altsep
    # self.path = posixpath2._mk_module(os_module=module, use_environ=False, keep_double_initial_slashes=False)
    self._mounts = {}  # {id: (os, fds)}
    self._last_fd = 3
    self._fds = {}  # {local_fd: (mount_id, mount_fd)}

  def __dir__(self):
    return [
      '__name__', 'sep', 'altsep']  # XXX

  def mount(self, id, os):  # not thread safe
    if not id.isidentifier(): raise ValueError('invalid mount name')
    if id in self._mounts: raise ValueError('mount already exists')
    self._mounts[id] = (os, set())

  def unmount(self, id):  # not thread safe
    if id not in self._mounts: raise ValueError('mount does not exist')
    os, fds = self._mounts[id]
    if fds: raise OSError(errno.EBUSY, 'mount is in use')
    del self._mounts[id]

  def _splitmount(self, path):
    sep, altsep = self.sep, self.altsep
    sepb, altsepb = sep.encode('ascii'), altsep.encode('ascii') if altsep else None
    i = 0
    for i, c in enumerate(path):
      if c in (sep, sepb, altsep, altsepb):
        break
    else: return path[:0], path[0:]
    return path[:i], path[i + 1:]

  def _call_path(self, method, path, *a, dir_fd=None, **k):
    if dir_fd is not None: raise TypeError('dir_fd not supported')
    mount_id, subpath = self._splitmount(path)
    if mount_id not in self._mounts: raise FileNotFoundError(errno.ENOENT, 'mount point not found', path)
    os, fds = self._mounts[mount_id]
    return getattr(os, method)(subpath, *a, **k)

  def _call_fd(self, method, fd, *a, **k):
    if fd not in self._fds: raise OSError(errno.EBADF, 'bad file descriptor')
    mount_id, mount_fd = self._fds[fd]
    if mount_id not in self._mounts: raise RuntimeError('corrupted mount_os')
    os, fds = self._mounts[mount_id]
    return getattr(os, method)(mount_fd, *a, **k)

  def _call_pathorfd(self, method, path, *a, **k):
    if isinstance(path, int): return self._call_fd(method, path, *a, **k)
    return self._call_path(method, path, *a, **k)

  for m in ['stat', 'utime', 'chmod', 'chown']:
    exec(f'def {m}(self, *a, **k): return self._call_pathorfd("{m}", *a, **k)')
  for m in ['lstat', 'readlink', 'mkdir', 'unlink', 'rmdir', 'listdir']:
    exec(f'def {m}(self, *a, **k): return self._call_path("{m}", *a, **k)')
  for m in ['read', 'write']:
    exec(f'def {m}(self, *a, **k): return self._call_fd("{m}", *a, **k)')
  del m

  def open(self, path, flags, mode=0o777, *, dir_fd=None):  # not thread-safe
    # almost copied from _call_path
    if dir_fd is not None: raise TypeError('dir_fd not supported')
    mount_id, subpath = self._splitmount(path)
    if mount_id not in self._mounts: raise FileNotFoundError(errno.ENOENT, 'mount point not found', path)
    os, fds = self._mounts[mount_id]
    # converting flags
    new_flags = 0
    for oflag in self._O_FLAGS:
      sflag = getattr(self, oflag, None)
      if sflag is None or sflag == 0: continue
      # if (sflag & flags) == sflag: print('found flag', oflag, sflag, 'to', getattr(os, oflag, 0))
      if (sflag & flags) == sflag: new_flags |= getattr(os, oflag, 0)
    mount_fd = os.open(subpath, new_flags, mode=mode)
    new_fd = self._last_fd + 1
    self._last_fd = new_fd
    fds.add(mount_fd)
    self._fds[new_fd] = (mount_id, mount_fd)
    return new_fd

  _O_FLAGS = ('O_RDONLY', 'O_WRONLY', 'O_CREAT', 'O_TRUNC', 'O_EXCL', 'O_BINARY', 'O_NOINHERIT', 'O_CLOEXEC')
  # O_RDONLY MUST be 0
  i = 0
  for o in _O_FLAGS:
    exec(f'{o} = {i!r}')
    if i == 0: i = 1
    else: i *= 2
  del i
  del o

  def close(self, fd):  # not thread safe
    # almost copied from _call_fd
    if fd not in self._fds: raise OSError(errno.EBADF, 'bad file descriptor')
    mount_id, mount_fd = self._fds[fd]
    if mount_id not in self._mounts: raise RuntimeError('corrupted mount_os')
    os, fds = self._mounts[mount_id]
    os.close(mount_fd)
    fds.remove(mount_fd)
    del self._fds[fd]

  def symlink(self, src, dst, target_is_directory=False, *, dir_fd=None):
    # Does not morph the `src` value (ie does not morph the symlink content). XXX ok?
    # almost copied from _call_path
    if target_is_directory: raise TypeError("target_is_directory not supported")
    if dir_fd is not None: raise TypeError("dir_fd not supported")
    mount_id, subdst = self._splitmount(dst)
    if mount_id not in self._mounts: raise FileNotFoundError(errno.ENOENT, "mount point not found", dst)
    os, fds = self._mounts[mount_id]
    return os.symlink(src, subdst)

  def _replace(self, method, src, dst, *, src_dir_fd=None, dst_dir_fd=None):
    # almost copied from _call_path
    if src_dir_fd is not None or dst_dir_fd is not None: raise TypeError("*_dir_fd not supported")
    src_mount_id, subsrc = self._splitmount(src)
    if src_mount_id not in self._mounts: raise FileNotFoundError(errno.ENOENT, "mount point not found", src)
    dst_mount_id, subdst = self._splitmount(dst)
    if dst_mount_id not in self._mounts: raise FileNotFoundError(errno.ENOENT, "mount point not found", dst)
    src_os, src_fds = self._mounts[src_mount_id]
    dst_os, dst_fds = self._mounts[dst_mount_id]
    if src_os is not dst_os: raise OSError(errno.EXDEV, "Invalid cross-device link", src, 17, dst)
    return getattr(src_os, method)(subsrc, subdst)

  def replace(self, *a, **k): return self._replace('replace', *a, **k)
  def rename(self, *a, **k): return self._replace('rename', *a, **k)

MountOs._required_globals = ['errno', 'os']

# # #!python3 -i
# # exec(open('pythoncustom.py', 'rb').read())

# # XXX test MountOs!
# import os, errno
# mos = MountOs()
# mos.mount('here', os)
# mos.mount('hoy', os)
# fd = mos.open('here/pythoncustom.py', mos.O_RDONLY | mos.O_BINARY | mos.O_CLOEXEC | mos.O_NOINHERIT)
# print(mos.read(fd, 2))
# print(mos.read(fd, 2))
# mos.close(fd)
# # mos.replace('here/pythoncustom.py', 'hoy/pythoncustom2.py')
