# iter_chain.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def iter_chain(iterable, *iterables):
  """\
bytes(iter_chain(b"abc", b"def")) → b"abcdef"
"""
  for _ in iterable: yield _
  for i in iterables:
    for _ in i: yield _
