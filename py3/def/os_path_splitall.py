# os_path_splitall.py Version 1.2.0
# Copyright (c) 2020, 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_path_splitall(path, splitroot=False, splitdrive=False, *, os_module=None):
  """\
os_path_splitall(path) -> returns a list that can be restored as valid path using os.path.join().

  path       : str|bytes|PathLike -> the fs path to split using os.path.split()
  splitroot  : bool -> also extract the root
  splitdrive : bool -> use os.path.splitdrive() to extract the drive

/!\\ Caution when using os.path.join() while using options splitroot or splitdrive!

    os_path_splitall('a/b/c') -> ['a', 'b', 'c']
    os_path_splitall('/a/b/c') -> ['/a', 'b', 'c']

Other examples on windows:

    os_path_splitall('C:\\a\\b\\c') -> ['C:\\a', 'b', 'c']
    os_path_splitall('C:\\a\\b\\c', splitroot=True) -> ['C:\\', 'a', 'b', 'c']
    os_path_splitall('C:\\a\\b\\c', splitdrive=True) -> ['C:', '\\a', 'b', 'c']
    os_path_splitall('C:\\a\\b\\c', splitroot=True, splitdrive=True) -> ['C:', '\\', 'a', 'b', 'c']
"""
  if os_module is None: os_module = os
  if splitdrive: drive, path = os_module.path.splitdrive(path)
  split = os_module.path.split
  ph, t = split(path)
  r = [t]
  while 1:
    h, t = split(ph)
    if ph == h:
      if splitroot: r.insert(0, h)
      else: r[0] = h + r[0]
      if splitdrive: r.insert(0, drive)
      return r
    r.insert(0, t)
    ph = h
os_path_splitall._required_globals = ['os']
