# Path_walk.py Version 2.1.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def Path_walk(top, topdown=True, onerror=None, followlinks=False, *, relative_root=False, _relroot=None, depth=None):
  dirs = []; files = []; new_depth = None
  if depth is not None: new_depth = depth + 1
  if relative_root:
    if _relroot is None: root = _relroot = top.relative_to(top)  # '.'
    else: root = _relroot
  else: root = top
  try: children = list(top.iterdir())
  except OSError as e:
    if onerror is None: raise
    onerror(e)
    return
  for child in children:
    st_mode = child.stat(follow_symlinks=followlinks).st_mode
    if stat.S_ISDIR(st_mode): dirs.append(child)
    else: files.append(child)
  if topdown:
    yield (root, dirs, files, *(() if depth is None else (depth,)))
    for child in dirs: yield from Path_walk(child, topdown=topdown, followlinks=followlinks, relative_root=relative_root, _relroot=None if _relroot is None else _relroot.joinpath(child.name), depth=new_depth)
  else:
    for child in dirs: yield from Path_walk(child, topdown=topdown, followlinks=followlinks, relative_root=relative_root, _relroot=None if _relroot is None else _relroot.joinpath(child.name), depth=new_depth)
    yield (root, dirs, files, *(() if depth is None else (depth,)))
Path_walk._required_globals = ['stat']
