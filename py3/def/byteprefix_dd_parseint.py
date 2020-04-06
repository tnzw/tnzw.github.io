# byteprefix_dd_parseint.py Version 1.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def byteprefix_dd_parseint(string):
  """\
byteprefix_dd_parseint("1000K") -> 1024000
byteprefix_dd_parseint("1000kB") -> 1000000
"""
  m = re.match("^\\s*([-+]?)([0-9]+)(xM|[kMGTPEZY]B|[cwbBKMGTPEZY]|)\\s*$", str(string))
  if m: return byteprefix_dd_multiplyint(int(m.group(1) + m.group(2)), m.group(3))
  raise ValueError("invalid litteral for byteprefix_dd_parseint(): " + repr(string))
byteprefix_dd_parseint._required_globals = ["byteprefix_dd_multiplyint"]
