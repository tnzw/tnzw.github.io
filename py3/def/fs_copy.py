# fs_copy.py Version 1.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def fs_copy(src, dst, **opt):
  """\
Copy src file tree to dst. If dst already exists, it attemps to overwrite only if clobber is set.
If src and dst are two directories, it merges the content of src to dst.

It is an alias for `fs_move(src, dst, auto_remove=False, **opt)` however some default arguments differ.

fs_copy(src, dst, **opt) -> Error
  opt
    preserve_ownership => False
    auto_remove => False
    Other arguments are the same as for fs_move
"""
  if "preserve_ownership" not in opt: opt["preserve_ownership"] = False
  if "auto_remove" not in opt: opt["auto_remove"] = False
  return fs_move(src, dst, **opt)
fs_copy._required_globals = ["fs_move"]
