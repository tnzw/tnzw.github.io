# fs_readfile.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def fs_readfile(path, *, os_module=None):
  if os_module is None:
    with open(path, "rb") as f:
      return f.read()
  else:
    fd = None
    try:
      fd = os_module.open(path, os_module.O_RDONLY | getattr(os_module, "O_BINARY", 0))
      return b"".join(_ for _ in os_iterread(fd, os_module=os_module))
    finally:
      if fd is not None: os_module.close(fd)

fs_readfile._required_globals = ["os_iterread"]
