# opennewfile.py Version 3.0.0
# Copyright (c) 2018-2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def opennewfile(path, mode="x", *args, base_format="{name}_{index}{extension}", start_index=1, first_open=True, os_module=None, **opt):
  """\
opennewfile(path, *args, **opt) -> file_object
  baseformat => "{name}_{index}{extension}"  (bytes or custom formatter are allowed)
  first_open => True : try to open `path` before generating new names (default)
                False: start directly to open generated named files
  start_index : sets the first value of {index} (defaults to 1)
  os_module   : the os module to work with (if None, defaults to os)
                if defined, the method uses 'open2' to open file instead of using the 'open' builtin
  Other opt and args are propagated to the open method.

>>> f = opennewfile("Downloads/myfile.txt", base_format="{n} ({i}){e}")
>>> f.name
"Downloads/myfile (1).txt"
"""
  if os_module is None: os_module, _open = os, open
  else: opt["os_module"], _open = os_module, open2
  encoding = ("UTF-8", "surrogateescape")  # lossless encoding, just used to convert str <-> bytes if no custom formatter is provided
  if isinstance(base_format, bytes): base_format = base_format.decode(*encoding)
  path = os_module.fspath(path)
  if isinstance(path, bytes) and isinstance(base_format, str):
    def _format(f, **k): return f.format(**{k: (v.decode(*encoding) if isinstance(v, bytes) else v) for k, v in k.items()}).encode(*encoding)
  else:
    def _format(f, **k): return f.format(**k)
  if "r" in mode or "a" in mode or "w" in mode: raise ValueError("must not have one of read/write/append mode")
  if "x" not in mode: mode += "x"
  if first_open:
    try: return _open(path, mode, *args, **opt)
    except FileExistsError: pass
  dir, base = os_module.path.split(path)
  name, ext = os_module.path.splitext(base)
  format_dict = {
    "basename": base, "base": base, "b": base,
    "name": name,                   "n": name,
    "index": start_index - 1,       "i": start_index - 1,
    "extension": ext, "ext": ext,   "e": ext,
  }
  prev_base = _format(base_format, **format_dict)
  format_dict["i"] = format_dict["index"] = format_dict["index"] + 1
  new_base = _format(base_format, **format_dict)
  if prev_base == new_base:
    raise ValueError("base_format should at least handle '{index}'")
  prev_base = base
  while True:
    new_path = os_module.path.join(dir, new_base)
    try: return _open(new_path, mode, *args, **opt)
    except FileExistsError: pass
    format_dict["i"] = format_dict["index"] = format_dict["index"] + 1
    prev_base, new_base = new_base, _format(base_format, **format_dict)
    if prev_base == new_base:  # XXX check all previously generated values ?
      raise ValueError("base_format.format() returned the same value as a previous one")
opennewfile._required_globals = ["os", "open2"]
