# opennewfile.py Version 2.0.1
# Copyright (c) 2018-2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def opennewfile(path, mode="x", **opt):
  """\
opennewfile(path, **opt) -> file_object
  baseformat => (b)"%(name)s_%(index)d%(extension)s"
  other args are the same as the 'open' builtin

Example:
  f = opennewfile("Downloads/myfile.txt", baseformat="%(n)s (%(i)d)%(e)s")
  new_path = f.name
  # f.write(...)
  f.close()
"""
  if "baseformat" not in opt:
    baseformat = b"%(name)s_%(index)d%(extension)s" if isinstance(path, bytes) else "%(name)s_%(index)d%(extension)s"
  else:
    baseformat = opt.pop("baseformat")
  if "opener" in opt: raise NotImplementedError
  if "r" in mode or "a" in mode or "w" in mode: raise ValueError("must not have one of read/write/append mode")
  if "x" not in mode: mode += "x"
  try:
    f = open(path, mode, **opt)
  except OSError as e:
    if e.errno != errno.EEXIST: raise
  else:
    return f
  dir, base = os.path.split(path)
  name, ext = os.path.splitext(base)
  format_dict = {
    "b": base,
    "base": base,
    "basename": base,
    "n": name,
    "name": name,
    "i": 0,
    "index": 0,
    "e": ext,
    "ext": ext,
    "extension": ext,
  }
  format_dict.update({k.encode("ascii"): v for k, v in format_dict.items()})
  check_format = baseformat % format_dict  # cannot use str.format with bytes
  format_dict["index"] += 1
  format_dict[b"i"] = format_dict[b"index"] = format_dict["i"] = format_dict["index"]
  if check_format == baseformat % format_dict:
    raise ValueError("baseformat should at least contain '%(index)d'")
  while 1:
    new_path = os.path.join(dir, baseformat % format_dict)
    try:
      f = open(new_path, mode, **opt)
    except OSError as e:
      if e.errno != errno.EEXIST: raise
      format_dict["index"] += 1
      format_dict[b"i"] = format_dict[b"index"] = format_dict["i"] = format_dict["index"]
    else:
      return f
opennewfile._required_globals = ["os"]
