# posixpath_splitall.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def posixpath_splitall():
  def _splitall(fspath):
    if isinstance(fspath, bytes): root = empty = b''; sep = b'/'; dot = b'.'
    else:                         root = empty =  ''; sep =  '/'; dot =  '.'
    names = []
    if len(fspath):
      # parse root
      if fspath[:1] == sep:
        if fspath[1:2] == sep and (fspath[2:3] != sep or fspath[2:3] == empty): l = 2
        else: l = 1
        root = fspath[:l]
      else: l = 0
      # parse names (without normalising anything)
      names = fspath[l:]
      if names: names = names.split(sep)
      else: names = []
    return empty, root, names
  def posixpath_splitall_from_fspath(path):
    try: return _splitall(path)
    except (TypeError, ValueError):
      if not isinstance(path, (str, bytes)): raise TypeError('path must be of type str or bytes') from None
      raise
  def posixpath_splitall(path):
    """\
Splits a posix path into a triplet (drive, root, names) without
normalizing.  (ie. names could have empty names and dots.)
"""
    return _splitall(os_fspath(path))
  posixpath_splitall.from_fspath = posixpath_splitall_from_fspath
  return posixpath_splitall
posixpath_splitall = posixpath_splitall()
posixpath_splitall._required_globals = ['os_fspath']
