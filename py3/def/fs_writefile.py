# fs_writefile.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def fs_writefile(path, data, *, os_module=None):
  if os_module is None:
    with open(path, "wb") as f:
      return f.write(data)
  else:
    fd = None
    try:
      fd = os_module.open(path, os_module.O_WRONLY | os_module.O_CREAT | os_module.O_TRUNC | getattr(os_module, "O_BINARY", 0))
      return os_module.write(fd, data)  # XXX check length written ?
    finally:
      if fd is not None: os_module.close(fd)
