# os_path_splitall.py Version 1.1.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_path_splitall(path, *, os_module=None):
  """\
os_path_splitall(path) -> tuple that can be restored as valid path by doing os.path.join.

    os_path_splitall("a/b/c") -> ("a", "b", "c")
    os_path_splitall("/a/b/c") -> ("/a", "b", "c")
"""
  if os_module is None: os_module = os
  pp = os_module.path.split(path)
  if not pp[1]: return pp[0]
  ppp = (pp[1],)
  while pp[0]:
    pp = os_module.path.split(pp[0])
    if not pp[1]: return pp[0] + ppp[0], *ppp[1:]
    ppp = (pp[1],) + ppp
  return ppp
os_path_splitall._required_globals = ["os"]
