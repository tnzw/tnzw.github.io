# ntpath_checkbasename.py Version 1.0.2
# Copyright (c) 2021, 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def ntpath_checkbasename():
  def _checkbasename(basename, *, strict=True):
    ubasename = basename.upper()
    if isinstance(ubasename, bytes): ubasename = ''.join(chr(_) for _ in ubasename)
    if not ubasename: return "basename must not be empty"
    for _ in ''.join(chr(_) for _ in range(32)) + '\\/:*?<>|"':
      if _ in basename:
        return f"invalid character in basename: {_!r}"
    # basename like 'A:' is handled by forbidden ':'
    doti = ubasename.find('.')
    noextubasename = ubasename if doti == -1 else ubasename[:doti]
    if (noextubasename in ('CON', 'PRN', 'AUX', 'NUL') or
        noextubasename.startswith(('COM', 'LPT')) and noextubasename[3:] in ('0','1','2','3','4','5','6','7','8','9')):
      return f"reserved basename: {basename!r}"
    # the checks bellow are invalid for explorer and other windows softwares,
    # but are valid for python and linux.
    if strict:
      if ubasename.startswith(' '): return "basename should not start with spaces"  # XXX other kind of whitespaces?
      if ubasename.endswith(' '): return "basename should not end with spaces"  # XXX other kind of whitespaces?
      if ubasename.endswith('.'): return "basename should not end with dots"
  def ntpath_checkbasename(basename, *, strict=True):
    e = _checkbasename(os_fspath(basename))
    if e: raise ValueError(e)
  def ntpath_checkbasename_from_fspath(basename):
    try: e = _checkbasename(basename)
    except (TypeError, ValueError):
      if not isinstance(basename, (str, bytes)): raise TypeError('basename must be of type str or bytes') from None
      raise
    if e: raise ValueError(e)
  def ntpath_checkbasename_catch(basename):
    e = _checkbasename(os_fspath(basename))
    if e: return ValueError(e)
  def ntpath_checkbasename_catch_from_fspath(basename):
    try: e = _checkbasename(basename)
    except (TypeError, ValueError):
      if not isinstance(basename, (str, bytes)): raise TypeError('basename must be of type str or bytes') from None
      raise
    if e: return ValueError(e)
  def ntpath_checkbasename_bool(basename): return not _checkbasename(os_fspath(basename))
  def ntpath_checkbasename_bool_from_fspath(basename):
    try: return not _checkbasename(basename)
    except (TypeError, ValueError):
      if not isinstance(basename, (str, bytes)): raise TypeError('basename must be of type str or bytes') from None
      raise
  ntpath_checkbasename.from_fspath = ntpath_checkbasename_from_fspath
  ntpath_checkbasename.catch = ntpath_checkbasename_catch
  ntpath_checkbasename.catch.form_fspath = ntpath_checkbasename_catch_from_fspath
  ntpath_checkbasename.bool = ntpath_checkbasename_bool
  ntpath_checkbasename.bool.from_fspath = ntpath_checkbasename_bool_from_fspath
  return ntpath_checkbasename
ntpath_checkbasename = ntpath_checkbasename()
ntpath_checkbasename._required_globals = ['os_fspath']
