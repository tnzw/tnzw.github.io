# fs_iterdirsdiff.py Version 1.1.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

# XXX do not return error anymore (action could be wrapped in try/except, use ignore_listdir_errors=None)
def fs_iterdirsdiff(action, paths, *, os_modules=None):
  """\
fs_iterdirsdiff(action, paths, **opt) -> Error
  import os
  def rec(err, name, roots):
    if err: raise err
    a, b, c = roots
    # Do some stuff here...
    print("name='" + str(name) + "' exists in folder", [str(p) for p in roots if p]);
    # A var is defined if a node exists in its associated folder.
    # e.g. *a* is defined if the node exists in folder "a".
    #      If *b* is also defined then the node with the same name exists in folder "b" as well.
    #      If *c* is not defined then a node with the same name does not exist in folder "c".
    return fs_iterdirsdiff(rec, [p and p + b"/" + name for p in roots])  # recursive
  err = fs_iterdirsdiff(rec, [b"a", b"b", b"c"])
  print(err)
"""
  def get(l, i, default=None):
    try: return l[i]
    except IndexError: return default

  l = len(paths)
  if os_modules is None: os_modules = [os] * l
  dirpaths = []
  subpaths = []
  for _,o in zip(paths, os_modules):
    dirs = None
    try: dirs = None if _ is None else o.listdir(_)
    except (NotADirectoryError, FileNotFoundError): pass
    except OSError as err:
      err = action(err, None, None)
      if err: return err
    dirpaths.append(None if dirs is None else _)
    subpaths.append(None if dirs is None else sorted(dirs))

  indices = [0] * l
  while 1:
    firstpaths = [None] * l
    for i in range(l):
      dirs = subpaths[i]
      if dirs is not None:
        firstpaths[i] = get(dirs, indices[i])

    winners = sorted(firstpaths, key=lambda v: (0 if v is None else 1, v))
    winner = None
    for _ in winners:
      if _ is not None:
        winner = _
        break

    if winner is None: return None

    params = [None] * l
    for i in range(l):
      if subpaths[i] is None: continue
      if get(subpaths[i], indices[i]) == winner:
        params[i] = paths[i]
        indices[i] = indices[i] + 1

    err = action(None, winner, params)
    if err: return err

  return None
fs_iterdirsdiff._required_globals = ["os"]
