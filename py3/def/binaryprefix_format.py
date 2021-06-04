# binaryprefix_format.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def binaryprefix_format(number, format="{value:.0f}{prefix}", *, exclude_prefixes=()):
  """\
binaryprefix_format(number[, format], **opt)

format => "{value:.0f}{prefix}"
opt
  exclude_prefixes => (): a set of prefixes to not use

>>> binaryprefix_format(123456789)
'118Mi'
>>> binaryprefix_format(1234, "{value:.1f} {prefix_name}byte(s)")
'1.2 kibibyte(s)'
>>> binaryprefix_format(1234, exclude_prefixes=("Ki",))
'1234'
"""
  # https://en.wikipedia.org/wiki/Binary_prefix
  prefixes = ((2**80, "Yi", "yobi"), (2**70, "Zi", "zebi"),
              (2**60, "Ei", "exbi"), (2**50, "Pi", "pebi"), (2**40, "Ti", "tebi"),
              (2**30, "Gi", "gibi"), (2**20, "Mi", "mebi"), (2**10, "Ki", "kibi"),
              (2** 0,   "",     ""))
  v, prefix, prefix_name = 1, "", ""
  if number != 0:
    for _ in prefixes:
      if _[1] in exclude_prefixes: pass
      else:
        v, prefix, prefix_name = _
        if number >= v: break
  if v != 1: number /= v
  return format.format(value=number, prefix=prefix, prefix_name=prefix_name, prefix_symbol=prefix)
