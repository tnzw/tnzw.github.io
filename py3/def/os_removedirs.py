# os_removedirs.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_removedirs(name, *, parents=-1, os_module=None):
  """\
os_removedirs(path, **opt)
  parents => -1     : Control the amount of parent to create.
                      N=0 => will only try removing "/dir/a/b/c"
                      N=1 => will try removing "/dir/a/b/c" and "/dir/a/b"
                      N=2 => will try removing "/dir/a/b/c", "/dir/a/b" and "/dir/a"
                      ...
                      N<=1 => will try removing all folders (ie. "/dir/a/b/c", "/dir/a/b", "/dir/a", "/dir")
  os_module => None : The module to use as os (if None, it uses the 'os' module)
"""
  if os_module is None: os_module = os
  if parents is None: parents = -1
  split = os_path_split(name, parents + 1, os_module=os_module) if parents else ()
  os_module.rmdir(name)
  i = len(split) - 1
  while i > 1:
    try: os_module.rmdir(os_module.path.join(*split[:i]))
    except OSError as e:
      if errno.ENOTEMPTY != e.errno: raise
      break
    i -= 1
os_removedirs._required_globals = ["os", "errno", "os_path_split"]
