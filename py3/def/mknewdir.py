# mknewdir.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def mknewdir(path, *args, base_format="{basename}_{index}", start_index=1, first_open=True, os_module=None, **opt):
  """\
mknewdir(path, *args, **opt) -> newpath
  baseformat => "{base}_{index}"  (bytes or custom formatter are allowed)
  first_open => True : try to create `path` before generating new names (default)
                False: start directly to create generated named files
  start_index : sets the first value of {index} (defaults to 1)
  os_module   : the os module to work with (if None, defaults to os)
  Other opt and args are propagated to the mkdir method.

>>> newdirname = mknewdir("Downloads/mydir", base_format="{b} ({i})")
>>> newdirname
"Downloads/mydir (1)"
"""
  # This function is a big copy/paste of opennewfile() code
  if os_module is None: os_module = os
  encoding = ("UTF-8", "surrogateescape")  # lossless encoding, just used to convert str <-> bytes if no custom formatter is provided
  if isinstance(base_format, bytes): base_format = base_format.decode(*encoding)
  path = os_module.fspath(path)
  if isinstance(path, bytes) and isinstance(base_format, str):
    def _format(f, **k): return f.format(**{k: (v.decode(*encoding) if isinstance(v, bytes) else v) for k, v in k.items()}).encode(*encoding)
  else:
    def _format(f, **k): return f.format(**k)
  if first_open:
    try: return os_module.mkdir(path, *args, **opt)
    except FileExistsError: pass
  dir, base = os_module.path.split(path)
  name, ext = os_module.path.splitext(base)
  format_dict = {
    "basename": base, "base": base, "b": base,
    "name": name,                   "n": name,
    "index": start_index,           "i": start_index,
    "extension": ext, "ext": ext,   "e": ext,
  }
  prev_base, new_base = base, _format(base_format, **format_dict)
  while True:
    new_path = os_module.path.join(dir, new_base)
    try: return os_module.mkdir(new_path, *args, **opt)
    except FileExistsError: pass
    format_dict["i"] = format_dict["index"] = format_dict["index"] + 1
    prev_base, new_base = new_base, _format(base_format, **format_dict)
    if prev_base == new_base:  # XXX check all previously generated values ?
      raise ValueError("base_format.format() returned the same value as a previous one")

mknewdir._required_globals = ["os"]
