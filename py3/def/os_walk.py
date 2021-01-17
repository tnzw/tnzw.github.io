# os_walk.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_walk(top, topdown=True, onerror=None, followlinks=False, *, dir_fd=None, open_tops=False, os_module=None):
  # https://docs.python.org/3/library/os.html#os.walk
  # Uses scandir if possible, else fallsback to listdir
  # Returns tuple with dirpath, dirnames, nondirnames[, dirfd].
  # The encoding of names depends of the type of 'top'.
  if os_module is None: os_module = os
  def rec(path):
    dirnames, nondirnames = [], []
    top_fd = None
    try:
      if open_tops: top_fd = os_module.open(path, os_module.O_RDONLY, dir_fd=dir_fd)
      scandir = getattr(os_module, "scandir", None)
      if scandir is None:
        listdir = os_module.listdir
        try: names = listdir(path if top_fd is None else top_fd)
        except OSError as e:
          if onerror is None: raise
          onerror(e)
          return
        for name in names:
          stats = os_module.stat(os_module.path.join(path, name), follow_symlinks=followlinks, dir_fd=dir_fd)
          if stat.S_ISDIR(stats.st_mode): dirnames.append(name)
          else: nondirnames.append(name)
      else:
        try: entries = scandir(path if top_fd is None else top_fd)
        except OSError as e:
          if onerror is None: raise
          onerror(e)
          return
        for entry in entries:
          if entry.is_dir(follow_symlinks=followlinks): dirnames.append(entry.name)
          else: nondirnames.append(entry.name)
      if not topdown:
        for name in dirnames:
          yield from rec(os_module.path.join(path, name))
      if open_tops: yield path, dirnames, nondirnames, top_fd
      else: yield path, dirnames, nondirnames
    finally:
      if top_fd is not None: os_module.close(top_fd)
    if topdown:
      for name in dirnames:
        yield from rec(os_module.path.join(path, name))
  return rec(top)

os_walk._required_globals = ["os", "stat"]
