# ntpath_checkbasename.py Version 1.0.1
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def ntpath_checkbasename():
  def ntpath_checkbasename(basename, *, strict=True):
    basename = os_fspath(basename)
    ubasename = basename.upper()
    if isinstance(ubasename, bytes): ubasename = "".join(chr(_) for _ in ubasename)
    if not ubasename: raise ValueError("basename must not be empty")
    for _ in "".join(chr(_) for _ in range(32)) + '\\/:*?<>|"':
      if _ in basename:
        raise ValueError(f"invalid character in basename: {_!r}")
    # basename like 'A:' is handled by forbidden ':'
    doti = ubasename.find(".")
    noextubasename = ubasename if doti == -1 else ubasename[:doti]
    if noextubasename in ("CON", "PRN", "AUX", "NUL"): raise ValueError(f"reserved basename: {basename!r}")
    if noextubasename in (f"COM{_}" for _ in range(10)): raise ValueError(f"reserved basename: {basename!r}")
    if noextubasename in (f"LPT{_}" for _ in range(10)): raise ValueError(f"reserved basename: {basename!r}")
    # the checks bellow are invalid for explorer and other windows softwares,
    # but are valid for python and linux.
    if strict:
      if ubasename.strip(" ") != ubasename: raise ValueError("basename should not start or end with spaces")  # XXX other kind of whitespaces?
      if ubasename.rstrip(".") != ubasename: raise ValueError("basename should not end with dots")
  def ntpath_checkbasename_catch(basename):
    try: ntpath_checkbasename(basename)
    except ValueError as e: return e
  def ntpath_checkbasename_bool(basename):
    try: ntpath_checkbasename(basename)
    except ValueError as e: return False
    return True
  ntpath_checkbasename.catch = ntpath_checkbasename_catch
  ntpath_checkbasename.bool = ntpath_checkbasename_bool
  return ntpath_checkbasename
ntpath_checkbasename = ntpath_checkbasename()
ntpath_checkbasename._required_globals = ["os_fspath"]
