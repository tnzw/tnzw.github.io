# os_path_split.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_path_split(path, n=1, *, os_module=None):
  """\
os_path_split(path, n, **opt)
An enhanced version of os.path.split
see https://docs.python.org/3/library/os.path.html#os.path.split

os_path_split(path) : acts like os.path.split
os_path_split("a/b/c", 1) → ("a/b", "c")
os_path_split("a/b/c/d", 2) → ("a/b", "c", "d")
"""
  if os_module is None: os_module = os
  if n is None: n = 1
  (path, t) = os_module.path.split(path)
  r = (t,)
  n -= 1
  while n:
    (path, t), p = os_module.path.split(path), path
    if path == p: return path, *r
    r = (t,) + r
    n -= 1
  return path, *r
os_path_split._required_globals = ["os"]
