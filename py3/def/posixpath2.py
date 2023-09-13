# posixpath2.py Version 1.2.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def posixpath2(os_module=None, *, supports_unicode_filenames=False, use_environ=True, get_user_home=None, keep_double_initial_slashes=True, lowercase=False):
  _module__func = posixpath2
  _module__name__ = _module__func.__name__ if __name__ == '__main__' else (__name__ + '.' + _module__func.__name__)
  #if __name__ != '__main__': _module__name__ = __name__ + '.' + _module__name__
  try: export = __builtins__.__class__(_module__name__)
  except AttributeError:
    class _module__class__: pass
    export = _module__class__()
    export.__name__ = _module__name__
  export.__doc__ = _module__func.__doc__
  export._mk_module = _module__func

  _use_environ = True if use_environ else False; del use_environ
  _keep_double_initial_slashes = True if keep_double_initial_slashes else False; del keep_double_initial_slashes
  _lowercase = True if lowercase else False; del lowercase

  # beginning of module #

  __all__ = [
    'curdir', 'pardir', 'sep', 'altsep', 'extsep', 'pathsep',
    'basename', 'commonpath', 'commonprefix', 'dirname', 'isabs', 'join',
    'normcase', 'normpath', 'relpath', 'split', 'splitdrive', 'splitext',
    'supports_unicode_filenames', 'samestat',
  ]

  # https://docs.python.org/3/library/os.path.html

  export.os = os_module
  curdir = '.'
  pardir = '..'
  sep = '/'
  altsep = None
  extsep = '.'
  pathsep = ':'

  def _check_arg_types(funcname, *args):
    # Copied from https://github.com/python/cpython/blob/3.11/Lib/genericpath.py#L144
    hasstr = hasbytes = False
    for s in args:
      if isinstance(s, str): hasstr = True
      elif isinstance(s, bytes): hasbytes = True
      else: raise TypeError(f'{funcname}() argument must be str, bytes, or os.PathLike object, not {s.__class__.__name__!r}') from None
    if hasstr and hasbytes: raise TypeError("Can't mix strings and bytes in path components") from None

  if os_module is None:
    def _fspath(path):
      # Inspired by https://github.com/python/cpython/blob/3.11/Lib/os.py#L1036
      if isinstance(path, (str, bytes)): return path
      path_type = type(path)
      try: fspath_func = path_type.__fspath__
      except AttributeError: raise TypeError('expected str, bytes or os.PathLike object, not ' + path_type.__name__) from None
      path_repr = fspath_func(path)
      if isinstance(path_repr, (str, bytes)): return path_repr
      raise TypeError(f'expected {path_type.__name__}.__fspath__() to return str or bytes, not {type(path_repr).__name__}')
    export._fspath = _fspath
  else:
    def _fspath(s): return os_module.fspath(s)  # do not use `_fspath = os_module.fspath`

  # Pure path operations (uses os.fspath anyway which is part of os module but not a syscall actualy)
  def basename(path):
    # Algorithm copied from https://github.com/python/cpython/blob/3.11/Lib/posixpath.py#L140
    # `PurePosixPath(...).name` returns different result than `posixpath.basename()`.
    """Returns the final component of a pathname"""
    path = _fspath(path)
    sep = b'/' if isinstance(path, bytes) else '/'
    i = path.rfind(sep) + 1
    return path[i:]
  def commonpath(paths):
    # Algorithm copied from https://github.com/python/cpython/blob/3.11/Lib/posixpath.py#L527
    """Given a sequence of path names, returns the longest common sub-path."""
    if not paths: raise ValueError('commonpath() arg is an empty sequence')
    paths = (*(_fspath(p) for p in paths),)  # use our custom fspath
    if isinstance(paths[0], bytes): sep = b'/'; curdir = b'.'
    else: sep = '/'; curdir = '.'
    try:
      if _lowercase: split_paths = [p.lower().split(sep) for p in paths]
      else:          split_paths = [        p.split(sep) for p in paths]
      try: isabs, = {p[:1] == sep for p in paths}
      except ValueError: raise ValueError("Can't mix absolute and relative paths") from None
      split_paths = [[c for c in s if c and c != curdir] for s in split_paths]  # removes empty names, curdir names and root
      s1 = min(split_paths); s2 = max(split_paths)
      if _lowercase:
        common = paths[0].split(sep)
        common = [c for i, c in zip(range(len(s1)), common) if c and c != curdir]  # removes empty names, curdir names and root
      else:
        common = s1
      for i, c in enumerate(s1):
        if c != s2[i]:
          common = common[:i]
          break
      return (sep if isabs else sep[:0]) + sep.join(common)
    except (TypeError, AttributeError):
      _check_arg_types('commonpath', *paths)
      raise
  def _commonprefix(m):
    # Algorithm copied from https://github.com/python/cpython/blob/3.11/Lib/genericpath.py#L69
    # PurePath() is useless here as this method does not care of path mechanism.
    s1 = min(m); s2 = max(m)
    for i, c in enumerate(s1):
      if c != s2[i]: return s1[:i]
    return s1
  def commonprefix(m):
    """Given a list of pathnames, returns the longest common leading component"""
    if not m: return ''
    if not isinstance(m[0], (list, tuple)): m = (*(_fspath(_) for _ in m),)
    return _commonprefix(m)
  def dirname(path):
    # Algorithm copied from https://github.com/python/cpython/blob/3.11/Lib/posixpath.py#L150
    # `PurePosixPath(...).parent.as_posix()` returns different result than `posixpath.dirname()` does.
    """Returns the directory component of a pathname"""
    path = _fspath(path)
    sep = b'/' if isinstance(path, bytes) else '/'
    i = path.rfind(sep) + 1
    head = path[:i]
    if head and head != sep * len(head): head = head.rstrip(sep)
    return head
  def _isabs(fspath): return fspath.startswith(b'/' if isinstance(fspath, bytes) else '/')  #return PurePosixPath(path).is_absolute()
  def isabs(path): return _isabs(_fspath(path))
  def _join(fspath, *fspaths):
    # Algorithm copied from https://github.com/python/cpython/blob/3.11/Lib/posixpath.py#L71
    # `PurePosixPath(...).joinpath(...).as_posix()` returns different result than `posixpath.join()` does.
    sep = b'/' if isinstance(fspath, bytes) else '/'
    path = fspath
    try:
      if not fspaths: path[:0] + sep  #23780: Ensure compatible data type even if p is null.
      for b in fspaths:
        if b.startswith(sep): path = b
        elif not path or path.endswith(sep): path += b
        else: path += sep + b
      return path
    except (TypeError, AttributeError, BytesWarning):
      _check_arg_types('join', fspath, *fspaths)
      raise
  def join(path, *paths):
    """Join two or more pathname components, inserting '/' as needed.
If any component is an absolute path, all previous path components
will be discarded.  An empty last part will result in a path that
ends with a separator."""
    return _join(*(_fspath(p) for p in (path,) + paths))
  def normcase(path):
    if _lowercase: return _fspath(path).lower()
    return _fspath(path)
  def _normpath(fspath):
    # Algorithm copied from https://github.com/python/cpython/blob/3.11/Lib/posixpath.py#L350
    if isinstance(fspath, bytes): sep = b'/'; empty = b''; dot = b'.'; dotdot = b'..'
    else:                         sep =  '/'; empty =  ''; dot =  '.'; dotdot =  '..'
    if fspath == empty: return dot
    if fspath.startswith(sep): initial_slashes = 2 if _keep_double_initial_slashes and fspath.startswith(sep * 2) and not fspath.startswith(sep * 3) else 1
    else: initial_slashes = 0
    comps = fspath.split(sep)
    new_comps = []
    for comp in comps:
      if comp in (empty, dot): pass
      elif comp != dotdot or (not initial_slashes and not new_comps) or (new_comps and new_comps[-1] == dotdot): new_comps.append(comp)
      elif new_comps: new_comps.pop()
    comps = new_comps
    fspath = sep.join(comps)
    if initial_slashes: fspath = sep * initial_slashes + fspath
    return fspath or dot
  def normpath(path):
    """Normalize path, eliminating double slashes, etc."""
    return _normpath(_fspath(path))
  def relpath(path, start=None):
    # Algorithm adapted from https://github.com/python/cpython/blob/3.11/Lib/posixpath.py#L486
    # Handles a pure path version of relpath() if os_module is None.
    # /!\ On windows: posixpath.abspath('..') returns '..'! So we can't compare abspath nor relpath from original behavior!
    """Return a relative version of a path"""
    if not path: raise ValueError('no path specified')
    path = _fspath(path)
    if isinstance(path, bytes): curdir = b'.'; sep = b'/'; pardir = b'..'
    else:                       curdir =  '.'; sep =  '/'; pardir =  '..'
    start = curdir if start is None else _fspath(start)
    try:
      if _isabs(path) != _isabs(start):
        if os_module is None: raise ValueError("Can't mix absolute and relative paths")
        path = _abspath(path); start = _abspath(start)
      else:
        path = _normpath(path); start = _normpath(start)
      start_list = [x for x in start.split(sep) if x and x != curdir]  # removes empty names, curdir names and root
      path_list = [x for x in path.split(sep) if x and x != curdir]  # removes empty names, curdir names and root
      i = len(_commonprefix([start_list, path_list]))
      rel_list = [pardir] * (len(start_list) - i) + path_list[i:]
      if not rel_list: return curdir
      return _join(*rel_list)
    except (TypeError, AttributeError, BytesWarning, DeprecationWarning):
      _check_arg_types('relpath', path, start)
      raise
  def split(path):
    # Algorithm copied from https://github.com/python/cpython/blob/3.11/Lib/posixpath.py#L100
    """Split a pathname.  Returns tuple "(head, tail)" where "tail" is
everything after the final slash.  Either part may be empty."""
    path = _fspath(path)
    sep = b'/' if isinstance(path, bytes) else '/'
    i = path.rfind(sep) + 1
    head, tail = path[:i], path[i:]
    if head and head != sep * len(head): head = head.rstrip(sep)
    return head, tail
  def splitdrive(path):
    """Split a pathname into drive and path. On Posix, drive is always empty."""
    path = _fspath(path)
    return path[:0], path
  def splitext(path):
    # Algorithm refactored from https://github.com/python/cpython/blob/3.11/Lib/genericpath.py#L121
    """Split the extension from a pathname.
Extension is everything from the last dot to the end, ignoring
leading dots.  Returns "(root, ext)"; ext may be empty."""
    path = _fspath(path)
    if isinstance(path, bytes): sep = b'/'; dot = b'.'
    else:                       sep =  '/'; dot =  '.'
    si = path.rfind(sep)
    di = path.rfind(dot)
    if di > si:
      fi = si + 1
      while fi < di:
        if path[fi:fi + 1] != dot: return path[:di], path[di:]
        fi += 1
    return path, path[:0]

  # Non-OS operations
  def samestat(s1, s2): return s1.st_ino == s2.st_ino and s1.st_dev == s2.st_dev

  if os_module is not None:
    __all__ += [
      'abspath', 'exists', 'lexists', 'isfile', 'isdir', 'islink',
      'getatime', 'getmtime', 'getctime', 'getsize',
      'samefile', 'sameopenfile',
      'realpath', 'expanduser',
      # defpath, ismount, expandvars
    ]

    if hasattr(os_module, 'devnull'):
      __all__ += ['devnull']
      devnull = os_module.devnull

    # OS operations
    # FileNotFoundError happens when a node does not exists while traversing a path
    #   ex: /dir/dir/noent/noent
    #                ^
    # NotADirectoryError happens when a file is traversed like a dir
    #   ex: /dir/dir/file/noent
    #                ^
    def _abspath(fspath):
      cwd = os_module.getcwdb() if isinstance(fspath, bytes) else os_module.getcwd()
      return _normpath(_join(cwd, fspath))
    def abspath(path): return _abspath(os_module.fspath(path))
    def exists(path):
      try: s = os_module.stat(path)
      except (NotADirectoryError, FileNotFoundError): return False
      return True
    def lexists(path):
      try: s = os_module.lstat(path)
      except (NotADirectoryError, FileNotFoundError): return False
      return True
    def isfile(path):
      try: s = os_module.stat(path)
      except (NotADirectoryError, FileNotFoundError): return False
      return stat.S_ISREG(s.st_mode)
    def isdir(path):
      try: s = os_module.stat(path)
      except (NotADirectoryError, FileNotFoundError): return False
      return stat.S_ISDIR(s.st_mode)
    def islink(path):
      try: s = os_module.lstat(path)
      except (NotADirectoryError, FileNotFoundError): return False
      return stat.S_ISLNK(s.st_mode)
    def getatime(path): return os_module.stat(path).st_atime
    def getctime(path): return os_module.stat(path).st_ctime  # caution! windows ctime != linux ctime
    def getmtime(path): return os_module.stat(path).st_mtime
    def getsize(path): return os_module.stat(path).st_size
    def samefile(f1, f2): return samestat(os_module.stat(f1), os_module.stat(f2))
    def sameopenfile(f1, f2): return samestat(os_module.fstat(f1), os_module.fstat(f2))
    def realpath(path, *, strict=False):  # documentation says that we "should not" use this function anyway
      return os_realpath(path, strict=strict, os_module=os_module)

    def expanduser(path):
      # Algorithm adapted from https://github.com/python/cpython/blob/3.11/Lib/posixpath.py#L229
      # Handles more options from module configuration, like the use of get_user_home().
      """Expand ~ and ~user constructions."""
      path = os_module.fspath(path)
      is_bytes = isinstance(path, bytes)
      if is_bytes: tilde = b'~'; sep = b'/'
      else:        tilde =  '~'; sep =  '/'
      if not path.startswith(tilde): return path
      i = path.find(sep, 1)
      if i < 0: i = len(path)
      if i == 1:
        if _use_environ and hasattr(os_module.environ) and 'HOME' in os_module.environ: userhome = os_module.environ['HOME']
        # XXX also use a fake pwd module?
        elif get_user_home is not None: userhome = get_user_home(path[1:1])
        else: return path
      else:
        # XXX also use a fake pwd module?
        if get_user_home is not None: userhome = get_user_home(path[1:i])
        else: return path
      if userhome is None: return path
      if is_bytes:
        if not isinstance(userhome, bytes): userhome = os_module.fsencode(userhome)
      else:
        if not isinstance(userhome,   str): userhome = os_module.fsdecode(userhome)
      userhome = userhome.rstrip(sep)
      return (userhome + path[i:]) or sep

  __export__ = ['__all__', *__all__]

  # end of module #

  _module__locals = locals()
  for _ in _module__locals.get('__export__', _module__locals):
    if not hasattr(export, _): setattr(export, _, _module__locals[_])
  return export
posixpath2 = posixpath2()
posixpath2._required_globals = ['stat', 'os_realpath']
