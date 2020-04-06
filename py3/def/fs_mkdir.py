# fs_mkdir.py Version 1.1.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def fs_mkdir(path, mode=0o777, parents=False, exist_ok=False):
  """\
fs_mkdir(path, mode=0o777, parents=False)
  mode => 0o777
  parents => False : Also creates parent dirs. This could be an index from where to start creating dirs. ex:
                       fs_mkdir("/dir/a/b/c", parents=N)
                     N=0 => will only create "/dir/a/b/c"
                     N=-1 => will create "/dir/a/b" and "/dir/a/b/c"
                     N=-2 => will create "/dir/a", "/dir/a/b" and "/dir/a/b/c"
                     ...
                     N>=1 => will create all folders (ie. "/dir", "/dir/a", "/dir/a/b", "/dir/a/b/c")
"""
  if isinstance(parents, bool): parents = 1 if parents else 0
  if parents == 0:
    try: os.mkdir(path, mode=mode)
    except FileExistsError as e:
      if not exist_ok: return e
    except Exception as e: return e
    return None
  dir, sep = "", os.sep
  if isinstance(path, bytes): dir, sep = b"", sep.encode("ascii")
  path = path.split(sep)
  if parents < 0: root = []
  else: root, path = path[:parents-1], path[parents-1:]
  for i in range(len(path) - 1):
    try: os.mkdir(os.path.join(*root + path[:i + 1]), mode=mode)
    except FileExistsError: pass
    except Exception as e: return e
  try: os.mkdir(os.path.join(*root + path), mode=mode)
  except FileExistsError as e:
    if not exist_ok: return e
  except Exception as e: return e
  return None
fs_mkdir._required_globals = ["os"]