# os_walk.py Version 1.0.2
# Copyright (c) 2020-2021, 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_walk(top, topdown=True, onerror=None, followlinks=False, *, dir_fd=None, open_tops=False, os_module=None):
  # https://docs.python.org/3/library/os.html#os.walk
  # Uses scandir if possible, else fallsback to listdir
  # Returns tuple with (dirpath, dirnames, nondirnames[, dirfd]).
  # The encoding of names depends of the type of 'top'.
  if os_module is None: os_module = os
  if open_tops:
    os_open = os_module.open
    os_close = os_module.close
    O_RDONLY = os_module.O_RDONLY
  os_path_join = os_module.path.join
  os_stat = os_module.stat
  os_lstat = os_module.lstat
  os_scandir = getattr(os_module, 'scandir', None)
  if os_scandir is None:
    os_listdir = os_module.listdir
  else:
    def os_listdir(p):
      with os_scandir(p) as scan:
        return [e.name for e in scan]
  if dir_fd is None: o_dir_fd = {}
  else: o_dir_fd = {'dir_fd': dir_fd}
  def rec(path):
    dirnames = []; nondirnames = []
    top_fd = None
    try:
      if open_tops: top_fd = os_open(path, O_RDONLY, **o_dir_fd)
      try: names = os_listdir(path if top_fd is None else top_fd)
      except OSError as e:
        if onerror is None: raise
        onerror(e)
        return
      for name in names:
        subpath = os_path_join(path, name)
        stats = os_stat(subpath, dir_fd=dir_fd)
        if stat.S_ISDIR(stats.st_mode): dirnames.append(name)
        else: nondirnames.append(name)
      if not topdown:
        for name in dirnames:
          subpath = os_path_join(path, name)
          if followlinks or not stat.S_ISLNK(os_lstat(subpath, **o_dir_fd).st_mode):
            yield from rec(subpath)
      if open_tops: yield path, dirnames, nondirnames, top_fd
      else: yield path, dirnames, nondirnames
    finally:
      if top_fd is not None: os_close(top_fd)
    if topdown:
      for name in dirnames:
        subpath = os_path_join(path, name)
        if followlinks or not stat.S_ISLNK(os_lstat(subpath, **o_dir_fd).st_mode):
          yield from rec(subpath)
  return rec(top)
os_walk._required_globals = ['os', 'stat']
