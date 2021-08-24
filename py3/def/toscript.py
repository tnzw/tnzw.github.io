# toscript.py Version 0.1.3
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def toscript(desired_globals, keep_banners=True, keep_source=False):
  imports = set()
  script = ""
  required_globals_set = set()
  required_globals_found = list(desired_globals)
  for _ in required_globals_found:
    if _ in required_globals_set:
      continue
    required_globals_set.add(_)
    if not re.match("[_a-z][_a-z0-9]*(\\.[_a-z][_a-z0-9]*)*", _, re.I):
      raise ValueError(f"invalid global name {_}")
    var = eval(_)
    if inspect.ismodule(var): imports.add(_)
    elif isinstance(getattr(var, "_source", None), str):
      if keep_banners:
        script += var._source.strip("\n") + "\n"
      else:
        it = io.StringIO(var._source.strip("\n"))
        for line in it:
          if line[:1] not in ("#", "\n"):
            script += line
            break
        for line in it: script += line
        script += "\n"
      if keep_source:  # XXX it keeps banner, is ok ?
        script += f'{_}._source = """' + re.sub('"', '\\"', re.sub("\\\\", "\\\\\\\\", var._source)) + '"""\n'
      required_globals_found += getattr(var, "_required_globals", [])
    else:
      script += _ + " = " + repr(var) + "\n"
  return "".join(f"import {_}\n" for _ in imports) + script
toscript._required_globals = ["re", "inspect"]
