# zipfile_archive_genfromtree.py Version 1.0.1
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def zipfile_archive_genfromtree(path, basename, *, follow_symlinks=False):
  """\
Usage:
    # Saving my stuff in a zip file
    with open('save.zip', 'wb') as f:
      for chunk in zipfile_archive_genfromtree('/home/me/my_stuff', 'my_stuff'):
        f.write(chunk)
"""
  # I don't use the stat module as zip format handles these fixed constants
  # (which are incidentally the same as in UNIX)
  S_IFMT  = 0o170000  # 0xF000
  S_IFDIR = 0o040000  # 0x4000
  S_IFREG = 0o100000  # 0x8000
  S_IFLNK = 0o120000  # 0xA000
  splitall = [basename]
  zipsep = b'/' if isinstance(basename, bytes) else '/'
  if follow_symlinks: inodes = set()
  def walk(p, sa):
    lst = os.lstat(p)
    if follow_symlinks:
      try: wst = os.stat(p) if lst.st_mode & S_IFLNK == S_IFLNK else lst
      except FileNotFoundError: wst = None
      else:  # try to prevent fs loop ELOOP
        if wst.st_ino > 0:
          key = (wst.st_dev, wst.st_ino)
          if key in inodes: return
          inodes.add(key)
    else:
      wst = lst
    yield p, sa, lst, wst
    if wst is not None and wst.st_mode & S_IFMT == S_IFDIR:
      for name in os.listdir(p):
        yield from walk(os.path.join(p, name), sa + [name])  # don't use sep.join() instead of os.path.join(), because "\\".join(["\\", "hello"]) -> "\\\\hello" which is network path.
  g = zipfile_archive_pipegen(); next(g)
  for p, sa, lst, wst in walk(path, splitall):
    if wst is None:  # is broken symlink
      pass
    else:
      fmt = wst.st_mode & S_IFMT
      if fmt == S_IFREG:
        yield g.send(('entry', {'path': zipsep.join(sa), 'st_mode': wst.st_mode, 'st_mtime': wst.st_mtime}))
        with open(p, 'rb') as f:
          for chunk in io_iterread1(f):
            yield g.send(('data', chunk))
      elif fmt == S_IFDIR:
        yield g.send(('entry', {'path': zipsep.join(sa) + zipsep, 'st_mode': wst.st_mode, 'st_mtime': wst.st_mtime}))
      elif fmt == S_IFLNK:
        yield g.send(('entry', {'path': zipsep.join(sa), 'st_mode': wst.st_mode, 'st_mtime': wst.st_mtime}))
        data = os.readlink(p)
        yield g.send(('data', data))
      else:
        raise NotImplementedError(f"unhandled node type 0o{fmt:o}: {p}")
  yield g.send(('close',))
zipfile_archive_genfromtree._required_globals = ['os', 'io_iterread1', 'zipfile_archive_pipegen']
