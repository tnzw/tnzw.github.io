# sh_find.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def sh_find(path=".", controller=None, os_module=None):
  def printpath(direntry): print(direntry.path)
  if os_module is None: os_module = os
  if controller is None: controller = printpath
  def rec(de):
    ctl = controller(de)
    if ctl not in ("exit", "break", "nofollow") and de.is_dir(follow_symlinks=False):
      try: scan = os_module.scandir(de.path)
      except FileNotFoundError: pass
      else:
        for _ in scan:  # XXX does for...in...break automaticaly closes scan ?
          ctl2 = rec(_)
          if ctl2 == "exit": ctl = "exit"
          if ctl2 in ("exit", "break"):
            scan.close()
            break
    return ctl
  return rec(DirEntry(path, os_module=os_module, _lstat=os_module.lstat(path)))

sh_find._required_globals = ["os", "DirEntry"]
