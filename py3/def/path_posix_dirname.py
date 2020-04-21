# path_posix_dirname.py Version 2.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def path_posix_dirname(path):
  if isinstance(path, bytes):
    if path == b"": return b"."
    path = path.rstrip(b"/")
    if path == b"": return b"/"
    i = path.rfind(b"/")
    if i == 0: return b"/"
    if i > 0: return path[:i]
    return b"."
  else:
    if path == "": return "."
    path = path.rstrip("/")
    if path == "": return "/"
    i = path.rfind("/")
    if i == 0: return "/"
    if i > 0: return path[:i]
    return "."
