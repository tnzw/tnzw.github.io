# printb.py Version 1.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def printb(*objects, sep=b" ", end=b"\n", encoding=None, file=None, flush=False):
  if file is None: file = sys.stdout.buffer
  file.write(bprint(*objects, sep=sep, end=end, encoding=encoding))
  if flush: file.flush()

printb._required_globals = ["sys", "bprint"]
