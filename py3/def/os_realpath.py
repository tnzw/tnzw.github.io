# os_realpath.py Version 1.0.1
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

# algorithm copied from posixpath.py (python 3.11)
# see https://github.com/python/cpython/blob/3.11/Lib/posixpath.py#L412

def os_realpath(path, *, strict=False, os_module=None):
  """\
Return the canonical path of the specified filename, eliminating any symbolic links encountered in the path.

This method does not use os.path.realpath() as if os.path was a pure path module.
"""
  if os_module is None: os_module = os
  path = os_module.fspath(path)
  path, ok = os_joinrealpath(os_module.getcwdb() if isinstance(path, bytes) else os_module.getcwd(), path, strict=strict, os_module=os_module, _use_fspath=False)
  return path
os_realpath._required_globals = ['os', 'os_joinrealpath']
