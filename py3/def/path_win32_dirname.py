# path_win32_dirname.py Version 2.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def path_win32_dirname(path):
  if isinstance(path, bytes):
    if path == b"": return b"."
    root = path[:1]
    path = path.rstrip(b"/\\")
    if path == b"": return root
    root = b""
    if b"a"[0] <= path[0] <= b"z"[0] or b"A"[0] <= path[0] <= b"Z"[0]:
      if path[1:3] == b":": return path
      if path[1:3] in (b":/", b":\\"):
        root, path = path[:2], path[2:]
    i = max(path.rfind(b"/"), path.rfind(b"\\"))
    if i == 0: return root or path[0:1]
    if i > 0: return root + path[:i]
    return b"."
  else:
    if path == "": return "."
    root = path[:1]
    path = path.rstrip("/\\")
    if path == "": return root
    root = ""
    if "a" <= path[0] <= "z" or "A" <= path[0] <= "Z":
      if path[1:3] == ":": return path
      if path[1:3] in (":/", ":\\"):
        root, path = path[:2], path[2:]
    i = max(path.rfind("/"), path.rfind("\\"))
    if i == 0: return root or path[0:1]
    if i > 0: return root + path[:i]
    return "."
