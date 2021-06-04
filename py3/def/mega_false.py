# mega_false.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def mega_false():
  class MegaFalse(int):
    for _ in ("bool", "eq", "ge", "gt", "le", "lt", "ne"):
      exec(f"def __{_}__(self, *a, **k): return False", globals(), locals())
    del _
    for _ in ("repr", "str", "format"):
      exec(f"def __{_}__(self, *a, **k): return 'False'", globals(), locals())
    del _
  return MegaFalse(0)
mega_false = mega_false()
