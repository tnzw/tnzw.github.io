# bprint.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def bprint(*objects, sep=b" ", end=b"\n", encoding=None):
  if encoding is None: encoding = (sys.getdefaultencoding(), "replace")
  elif not isinstance(encoding, (tuple, list)): encoding = (encoding, "replace")
  elif len(encoding) and encoding[0] is None: encoding = sys.getdefaultencoding(), *encoding[1:]
  def enc(v):
    if isinstance(v, str): return v.encode(*encoding)
    if isinstance(v, (bytes, bytearray)): return bytes(v)
    return repr(v).encode(*encoding)
  return sep.join(enc(o) for o in objects) + end

bprint._required_globals = ["sys"]
