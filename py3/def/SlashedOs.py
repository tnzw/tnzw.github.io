# SlashedOs.py Version 1.0.0
#   This is free and unencumbered software released into the public domain.
#   SPDX: Unlicense <http://unlicense.org/>
#   Contributors: 2024 <tnzw@github.triton.ovh>

class SlashedOs:
  """\
A way to use common path separator "/" in a windows environment.

Usage:
  os_module = SlashedOs() if os.name == 'nt' else os

- Windows absolute path example: `C:/Users/me/AppData/Roaming`
- Not tested with UNC paths yet
"""

  class Path:
    def __init__(self, os, *, __name__='path'):
      self.__name__ = __name__
      self._cache = {}
      self.os = os
      self.sep = '/'
      if os._os.sep != '/': self.altsep = os._os.sep
      else: self.altsep = None
    def __dir__(self):
      return [
        '__name__', '_cache', 'os', 'sep', 'altsep', '_slashed'] # XXX
    def _slashed(self, path):
      sep = self.os._os.sep
      if sep == '/': return path
      if isinstance(path, bytes): return path.replace(sep.encode('ascii'), b'/')
      if isinstance(path, str): return path.replace(sep, '/')
      raise TypeError(f"cannot handle path with type {type(path)}")
    def __getattr__(self, name):
      if name in self._cache: return self._cache[name]
      if name in [
        'abspath', 'basename', 'commonpath', 'commonprefix', 'dirname',
        'expanduser', 'expandvars', 'isabs', 'join',
        'normcase', 'normpath', 'split', 'splitdrive', 'splitext',
        'exists', 'lexists', 'islink', 'isdir', 'isfile', 'ismount',
        'getsize', 'getmtime', 'getatime', 'getctime',
        'samefile', 'sameopenfile', 'samestat',
        'realpath', 'relpath',
        # 'expandvars', XXX
      ]:
        missing = []
        orig = getattr(self.os._os.path, name, missing)
        if orig is missing: raise AttributeError(f"no such attribute {name!r}")
        fn = lambda *a, **k: self._slashed(orig(*a, **k))
        self._cache[name] = fn
        return fn
      if name in ['supports_unicode_filenames']: return getattr(self.os.path, name)
      raise AttributeError(f"no such attribute {name!r}")

  def __init__(self, os_module=None, *, __name__='slashedos', name=None):
    self.__name__ = __name__
    # self.name = 'slashed_' + self._os.name  XXX if _os name is None then just 'slashedos'
    self._cache = {}
    self._os = os if os_module is None else os_module
    self.path = SlashedOs.Path(self)
  def __dir__(self):
    return [
      '__name__', '_os', 'path', 'sep', 'altsep']  # XXX
  def __getattr__(self, name):
    if name in self._cache: return self._cache[name]
    if name in [
      'fsencode', 'fsdecode', 'fspath',
      'open', 'access', 'chdir', 'chflags', 'chmod', 'chown', 'chroot',
      'lchflags', 'lchmod', 'lchown', 'link', 'listdir', 'lstat', 'mkdir',
      'makedirs', 'mkfifo', 'mknod', 'remove', 'removedirs', 'rename', 'renames',
      'replace', 'rmdir',
      # 'scandir', 'DirEntry', XXX
      'stat', 'statvfs_result',
      # 'symlink', XXX
      'truncate', 'unlink', 'utime',
      # 'walk', 'fwalk', XXX
      'getxattr', 'listxattr', 'removexattr', 'setxattr',
      'add_dll_directory',
      'execl', 'execle', 'execlp', 'execlpe',
      'execv', 'execve', 'execvp', 'execvpe',
      'posix_spawn', 'posix_spawnp',
      'spawnl', 'spawnle', 'spawnlp', 'spawnlpe',
      'spawnv', 'spawnve', 'spawnvp', 'spawnvpe',
      'startfile',
    ]: return getattr(self._os, name)
    if name in [
      'getcwd', 'getcwdb', 'readlink',
    ]:
      missing = []
      orig = getattr(self._os, name, missing)
      if orig is missing: raise AttributeError(f"no such attribute {name!r}")
      fn = lambda *a, **k: self.path._slashed(orig(*a, **k))
      self._cache[name] = fn
      return fn
    if name in [
      'get_exec_path', 'listdrives', 'listmounts', 'listvolumes',
    ]:
      missing = []
      orig = getattr(self._os, name, missing)
      if orig is missing: raise AttributeError(f"no such attribute {name!r}")
      fn = lambda *a, **k: [self.path._slashed(_) for _ in orig(*a, **k)]
      self._cache[name] = fn
      return fn
    if name in [
      'ctermid',
      'getegid', 'geteuid', 'getgid', 'getgrouplist', 'getgroups', 'getlogin',
      'getpgid', 'getpgrp', 'getpid', 'getppid', 'getpriority',
      'getresuid', 'getresgid', 'getuid', 'initgroups',
      'setegid', 'seteuid', 'setgid', 'setgroups', 'setns', 'setpgrp', 'setpgid',
      'setpriority', 'setregid', 'setresgid', 'setresuid', 'setreuid', 'getsid',
      'setsid',
      'strerror',
      'umask', 'uname', 'unshare',
      'fdopen', 'close', 'closerange', 'copy_file_range', 'device_encoding',
      'dup', 'dup2', 'fchmod', 'fchown', 'fdatasync', 'fstat', 'fstatvfs',
      'fsync', 'ftruncate', 'get_blocking', 'grantpt', 'isatty', 'lockf',
      'login_tty', 'lseek', 'openpty', 'pipe', 'pipe2',
      'posix_fallocate', 'posix_fadvise', 'pread', 'posix_openpt', 'preadv',
      'ptsname', 'pwrite', 'pwritev', 'read', 'sendfile', 'set_blocking',
      'splice', 'readv', 'tcgetpgrp', 'tcsetpgrp', 'ttyname', 'unlockpt',
      'write', 'writev',
      'get_terminal_size',
      'get_inheritable', 'set_inheritable', 'get_handle_inheritable',
      'set_handle_inheritable',
      'fchdir', 'major', 'minor', 'makedev', 'sync',
      'memfd_create', 'eventfd', 'eventfd_read', 'eventfd_write',
      'timerfd_create', 'timerfd_settime', 'timerfd_settime_ns',
      'timerfd_gettime', 'timerfd_gettime_ns',
      'abort', '_exit', 'fork', 'forkpty', 'kill', 'killpg', 'nice', 'pidfd_open',
      'plock', 'register_at_fork', 'times', 'wait', 'waitid', 'waitpid', 'wait3',
      'wait4', 'waitstatus_to_exitcode',
      'sched_get_priority_min', 'sched_get_priority_max', 'sched_getscheduler',
      'sched_setparam', 'sched_getparam', 'sched_rr_get_interval', 'sched_yield',
      'sched_setaffinity', 'sched_getaffinity',
      'cpu_count', 'getloadavg', 'process_cpu_count',
      'getrandom', 'urandom',
    ]: return getattr(self._os, name)
    # XXX pathconf fpathconf pathconf_names
    # XXX getenv getenvb putenv unsetenv environ environb
    # XXX popen system
    # XXX confstr confstr_names
    # XXX sysconf sysconf_names
    # 'supports_dir_fd', XXX
    # 'supports_effective_fd', XXX
    # 'supports_fd', XXX
    # 'supports_follow_symlinks', XXX
    if name in ['sep', 'altsep']: return getattr(self.path, name)
    if name in ['devnull']: return self.path._slashed(getattr(self._os, name))
    if name in [
      'error', 'name', 'PathLike', 'linesep', 'suppports_bytes_environ',
      'terminal_size', 'F_OK', 'R_OK', 'W_OK', 'X_OK', 'stat_result',
      'sched_param',
      'extsep', 'pathsep',
      # 'defpath', XXX
    ] or name.startswith((
      'PRIO_', 'RTLD_', 'CLONE_', 'F_', 'SEEK_', 'O_', 'POSIX_',
      'RWF_', 'SF_', 'SPLICE_', 'MFD_', 'EFD_', 'TFD_', 'XATTR_',
      'EX_', 'P_', 'W', 'CLD_', 'SCHED_', 'GRND_',
    )): return getattr(self._os, name)
    raise AttributeError(f"no such attribute {name!r}")

SlashedOs._required_globals = ['os']

# # XXX test SlashedOs!
# import os
# sos = SlashedOs()
# print(sos.path.sep)
# print(sos.path.altsep)
# print(sos.path.abspath('test'))
# print(sos.listdir())
# print(sos.O_CREAT)
# print(sos.devnull)
# print(sos.sep)
# print(repr(sos.linesep))
# print(sos.write is os.write)
# print(sos.getcwd())
# print(sos.getcwd is not os.getcwd)
