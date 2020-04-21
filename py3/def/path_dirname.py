# path_dirname.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def path_dirname():
  def _path_dirname(*a,**k):
    _path_dirname.fn = path_win32_dirname if sys.platform == "win32" else path_posix_dirname
    return _path_dirname.fn(*a,**k)
  def path_dirname(*a,**k):
    return _path_dirname.fn(*a,**k)
  _path_dirname.fn = _path_dirname
  return path_dirname
path_dirname = path_dirname()
path_dirname._required_globals = [
  "sys",
  "path_posix_dirname",
  "path_win32_dirname",
]
