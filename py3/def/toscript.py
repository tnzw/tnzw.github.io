# toscript.py Version 0.1.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def toscript(desired_globals, keep_banners=True):
  imports = ""
  script = ""
  required_globals_set = set()
  required_globals_found = list(desired_globals)
  for _ in required_globals_found:
    if _ in required_globals_set:
      continue
    if not re.match("[_a-z][_a-z0-9]*", _, re.I):
      raise ValueError(f"invalid global name {_}")
    var = eval(_)
    if inspect.ismodule(var):
      imports += "import " + _ + "\n"
    elif isinstance(getattr(var, "_source", None), str):
      if keep_banners:
        script += var._source + "\n"
      else:
        it = io.StringIO(var._source)
        for line in it:
          if line[:1] not in ("#", "\n"):
            script += line
            break
        for line in it: script += line
        script += "\n"
      required_globals_found += getattr(var, "_required_globals", [])
    else:
      script += _ + " = " + repr(var) + "\n"
  return imports + script
toscript._required_globals = ["inspect"]
