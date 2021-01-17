# os_fwalk.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_fwalk(top=".", topdown=True, onerror=None, follow_symlinks=False, *, dir_fd=None, os_module=None):
  return os_walk(top, topdown=topdown, onerror=onerror, followlinks=follow_symlinks, dir_fd=dir_fd, open_tops=True, os_module=os_module)
os_fwalk._required_globals = ["os_walk"]
