# iter_join.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def iter_join(sep, iterables):
  """\
bytes(iter_join(b", ", (b"ab", b"cd", b"e"))) → b"ab, cd, e"
"""
  it = iter(iterables)
  for _ in it:
    yield from _
    break
  for _ in it:
    yield from sep
    yield from _
