# os_joinrealpath.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

# algorithm copied from posixpath.py (python 3.11)
# see https://github.com/python/cpython/blob/3.11/Lib/posixpath.py#L421

def os_joinrealpath(path, rest, *, strict=False, os_module=None, _seen=None, _use_fspath=True, _sep=None, _altsep=None, _curdir=None, _pardir=None):
  # uses os_module.fspath, os_module.fsencode, os_module.path.isabs, os_module.path.split, os_module.path.join
  if os_module is None: os_module = os
  path_module = os_module.path
  if _seen is None: _seen = {}
  if _use_fspath:
    path = os_module.fspath(path)
    rest = os_module.fspath(rest)
  if _sep is None:
    _altsep = getattr(os_module, 'altsep', None)
    if isinstance(path, bytes):
      _sep = os_module.fsencode(os_module.sep)
      _curdir = os_module.fsencode(os_module.curdir)
      _pardir = os_module.fsencode(os_module.pardir)
      if _altsep: os_module.fsencode(_altsep)
    else:
      _sep = os_module.sep
      _curdir = os_module.curdir
      _pardir = os_module.pardir
  parts = []; prev_par = par = rest
  while 1:
    par, cur = path_module.split(par)
    if par == prev_par: parts.insert(0, par); break
    prev_par = par
    parts.insert(0, cur)
  if path_module.isabs(rest):
    drive, _ = path_module.splitdrive(rest)
    if drive: path = parts[0]
    else:
      drive, _ = path_module.splitdrive(path)
      if drive: path = drive + parts[0]
      else: path = parts[0]
    if _altsep: path = path.replace(_altsep, _sep)
  for name in parts[1:]:
    if not name or name == _curdir: continue
    if name == _pardir:
      if path:
        path, name = path_module.split(path)
        if name == _pardir: path = path_module.join(path, _pardir, _pardir)
      else: path = _pardir
      continue
    newpath = path_module.join(path, name)
    try: st = os_module.lstat(newpath)
    except OSError:
      if strict: raise
      is_link = False
    else: is_link = stat.S_ISLNK(st.st_mode)
    if not is_link:
      path = newpath
      continue
    # Resolve the symbolic link
    if newpath in _seen:
      path = _seen[newpath]
      if path is not None: continue  # use cached value
      # The symlink is not resolved, so we must have a symlink loop.
      if strict: os_module.stat(newpath)  # Raise OSError(errno.ELOOP)
      else: return path_module.join(newpath, rest), False  # Return already resolved part + rest of the path unchanged.
    _seen[newpath] = None
    path, ok = os_joinrealpath(path, os_module.readlink(newpath), strict=strict, os_module=os_module, _seen=_seen, _use_fspath=False, _sep=_sep, _altsep=_altsep, _curdir=_curdir, _pardir=_pardir)
    if not ok: return path_module.join(path, rest), False
    _seen[newpath] = path
  return path, True
os_joinrealpath._required_globals = ['os', 'stat']
