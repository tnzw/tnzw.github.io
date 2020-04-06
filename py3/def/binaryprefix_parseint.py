# binaryprefix_parseint.py Version 1.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def binaryprefix_parseint(string):
  """\
binaryprefix_parseint("1000k") -> 1000000
binaryprefix_parseint("1000Ki") -> 1024000
"""
  m = re.match("^\\s*([-+]?)([0-9]+)([KMGTPEZY]i|[kMGTPEZY]|)\\s*$", str(string))
  if m: return binaryprefix_multiplyint(int(m.group(1) + m.group(2)), m.group(3))
  raise ValueError("invalid litteral for binaryprefix_parseint(): " + repr(string))
binaryprefix_parseint._required_globals = ["binaryprefix_multiplyint"]
