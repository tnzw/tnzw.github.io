# fs_diff.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def fs_diff(path, *paths,
            compare_mode=False, compare_mtime=False, compare_owner=False, compare_group=False, compare_size=True, compare_content=True, max_length=None,
            follow_symlinks=False, stats=None,
            os_modules=None):
  """\
fs_diff(*paths, **opt) -> True if equals, else False
  opt
    compare_mode => False
    compare_mtime => False
    compare_owner => False
    compare_group => False
    compare_size => True
    compare_content => True
    max_length => None or < 0 : compares all files content
                            0 : useless, compares no data
                          > 0 : compares only `length` first content data
    follow_symlinks => False  : used to stat files
    stats => None             : preloaded stats (amount of stats must be equal to amount of paths)
"""
  if max_length is None: max_length = -1
  if len(paths) < 1: return True
  paths = (path,) + paths
  if os_modules is None: os_modules = (os,) * len(paths)

  if stats is None:
    fstats, *stats = (os_modules[i].stat(path, follow_symlinks=follow_symlinks) for i, path in enumerate(paths))
  else:
    if len(stats) != len(paths): raise ValueError("not enough stat result passed through 'stats'")
    fstats, *stats = stats
  fmt = stat.S_IFMT(fstats.st_mode)
  for _stat in stats:
    if fmt != stat.S_IFMT(_stat.st_mode): return False
    if compare_size and fstats.st_size != _stat.st_size: return False
    if compare_mode and fstats.st_mode != _stat.st_mode: return False
    if compare_mtime and fstats.st_mtime != _stat.st_mtime: return False
    if compare_owner and fstats.st_uid != _stat.st_uid: return False
    if compare_group and fstats.st_gid != _stat.st_gid: return False

  if compare_content and stat.S_ISREG(fstats.st_mode):
    fds = []
    try:
      for i, path in enumerate(paths): fds.append(os_modules[i].open(path, os_modules[i].O_RDONLY | os_modules[i].O_BINARY))
      l = 0
      for data in os_iterread(fds[0], length=max_length, os_module=os_modules[0]):
        data_len = len(data)
        l += data_len
        for i, fd in enumerate(fds[1:]):
          s = 0
          while s < data_len:
            cmp_data = os_modules[i + 1].read(fd, data_len - s)
            e = len(cmp_data)
            if not e or data[s:s+e] != cmp_data: return False
            s += e
      if l != max_length:
        for i, fd in enumerate(fds[1:]):
          if os_modules[i + 1].read(fd, 1): return False
    finally:
      for i, fd in enumerate(fds):
        os_modules[i].close(fd)  # XXX ouh it must not raise here, some fd might stay in memory forever
  return True

fs_diff._required_globals = ["os", "stat", "os_iterread"]
