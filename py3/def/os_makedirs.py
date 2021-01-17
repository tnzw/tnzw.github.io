# os_makedirs.py Version 1.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_makedirs(name, mode=0o777, exist_ok=False, *, parents=-1, os_module=None):
  """\
os_makedirs(path, **opt)
  mode => 0o777     : The mode to apply to the leaf
  exist_ok => False : Do not raise FileExistsError if leaf already exists
  parents => -1     : Control amount of parent dir creation.
                      N=0 => will only create "/dir/a/b/c"
                      N=1 => will create "/dir/a/b" and "/dir/a/b/c"
                      N=2 => will create "/dir/a", "/dir/a/b" and "/dir/a/b/c"
                      ...
                      N<=1 => will create all folders (eg. "/dir", "/dir/a", "/dir/a/b", "/dir/a/b/c")
  os_module => None : The module to use as os (if None, it uses the 'os' module)
"""
  if os_module is None: os_module = os
  if parents is None: parents = -1
  if mode is None: mode = 0o777
  split = os_path_split(name, parents + 1, os_module=os_module) if parents else ()
  i, l = 2, len(split)
  while i < l:
    try: os_module.mkdir(os_module.path.join(*split[:i]))
    except FileExistsError: pass
    i += 1
  try: os_module.mkdir(name, mode=mode)
  except FileExistsError:
    if not exist_ok or not stat.S_ISDIR(os_module.lstat(name).st_mode): raise
os_makedirs._required_globals = ["os", "stat", "os_path_split"]
