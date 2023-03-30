# ntpath_splitall.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def ntpath_splitall():
  def _isletterdrive(drive, _letters, _colon): return drive[1:] == _colon and drive[:1] in _letters
  def _hasletterdrive(path, _letters, _colon): return path[1:2] == _colon and path[:1] in _letters
  def _splitletterdrive(path, _letters, _colon): return (path[:2], path[2:]) if _hasletterdrive(path, _letters, _colon) else (path[:0], path)
  def _splituncdrive(path, _sep, _altsep, _empty):
    if path[:1] in (_sep, _altsep) and path[1:2] in (_sep, _altsep) and path[2:3] not in (_sep, _altsep):
      index = find2(path, (_sep, _altsep), 2)
      if index == -1: return (path[:0], path)
      # algo differs from _isuncdrive() to allow to reproduce pathlib.PureWindowsPath('//./') inconsistency
      if not path[index + 1:index + 2]: return (path[:index + 1], path[:0])
      if path[index + 1:index + 2] in (_sep, _altsep): return (path[:0], path)
      index2 = find2(path, (_sep, _altsep), index + 1)
      # what algo "should" be :
      #if path[index + 1:index + 2] in (_empty, _sep, _altsep): return (path[:0], path)
      #index2 = find2(path, (_sep, _altsep), index + 2)
      if index2 == -1: return (path, path[:0])
      return (path[:index2], path[index2:])
    return (path[:0], path)
  def _splitdrive(path, _sep, _altsep, _empty, _letters, _colon):
    drive, path = _splitletterdrive(path, _letters, _colon)
    if drive: return drive, path
    return _splituncdrive(path, _sep, _altsep, _empty)
  def _splitall(fspath):
    if isinstance(fspath, bytes): drive = root = _empty = b''; _sep = b'\\'; _altsep = b'/'; _dot = b'.'; _letters = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'; _colon = b':'
    else:                         drive = root = _empty =  ''; _sep =  '\\'; _altsep =  '/'; _dot =  '.'; _letters =  'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'; _colon =  ':'
    names = []
    if len(fspath):
      # parse drive
      drive, fspath = _splitdrive(fspath, _sep, _altsep, _empty, _letters, _colon)
      # parse root
      if fspath[:1] in (_sep, _altsep): l = 1; root = fspath[:l]
      else: l = 0
      # parse names (without normalising anything)
      names = fspath[l:]
      if names: names = split2(names, (_sep, _altsep))
      else: names = []
    return drive, root, names
  def ntpath_splitall_from_fspath(path):
    try: return _splitall(path)
    except (TypeError, ValueError):
      if not isinstance(path, (str, bytes)): raise TypeError('path must be of type str or bytes') from None
      raise
  def ntpath_splitall(path):
    """\
Splits a windows path into a triplet (drive, root, names) without
normalizing.  (ie. names could have empty names and dots.)
"""
    return _splitall(os_fspath(path))
  ntpath_splitall.from_fspath = ntpath_splitall_from_fspath
  return ntpath_splitall
ntpath_splitall = ntpath_splitall()
ntpath_splitall._required_globals = ['find2', 'os_fspath', 'split2']
