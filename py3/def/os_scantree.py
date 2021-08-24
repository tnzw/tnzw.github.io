# os_scantree.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_scantree(path, topdown=True, *, scan_top=False, filter=None, leaves_only=False, follow_symlinks=False, os_module=None):
  """\
os_scantree(path, **opt) -> ScandirIterator

opt:
  topdown          yield entries before subdirectories ones.
  scan_top         first iteration is `path` entry.
  filter=FUNC      skip entry `if not filter(entry)`.
  leaves_only      doesn't yield non-empty dir entries (making topdown option useless).
                   if a dir has all its entries skipped, then the dir is concidered as a leaf.
  follow_symlinks  follow symlinks (/!\\ no symlink attack protection, please keep it False).
  os_module        use another os module.
"""
  if os_module is None: os_module = os
  if filter is None: filter = lambda de: True
  def closer(): pass
  closer.closed = False
  def close():
    closer.closed = True
    try: next(closer.g)
    except StopIteration: pass
    else: raise RuntimeError("Bad implementation of rec()")
  closer.close = close
  def rec(path, if_empty=None):
    with os_module.scandir(path) as scan:
      for entry in scan:
        if filter(entry):
          if_empty = None
          if entry.is_dir(follow_symlinks=follow_symlinks):
            if leaves_only:
              yield from rec(entry.path, if_empty=entry)
              if closer.closed: return
            elif topdown:
              yield entry
              if closer.closed: return
              yield from rec(entry.path)
              if closer.closed: return
            else:
              yield from rec(entry.path)
              if closer.closed: return
              yield entry
              if closer.closed: return
          else:
            yield entry
            if closer.closed: return
      if if_empty: yield if_empty
  def toprec(path):
    p = os_module.fspath(path)
    b = os_module.path.basename(p)
    entry = DirEntry(p, name=b, os_module=os_module)
    if leaves_only:
      yield from rec(entry.path, if_empty=entry)
    elif topdown:
      yield entry
      if closer.closed: return
      yield from rec(path)
    else:
      yield from rec(path)
      if closer.closed: return
      yield entry
  closer.g = toprec(path) if scan_top else rec(path)
  return ScandirIterator(closer, closer.g)
os_scantree._required_globals = ["os", "stat", "ScandirIterator", "DirEntry"]
