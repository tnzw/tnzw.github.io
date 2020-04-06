# byteprefix_dd_multiplyint.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def byteprefix_dd_multiplyint(value, prefix):
  """\
possible prefixes : c w b B kB K MB M xM GB G TB T PB P EB E ZB Z YB Y
    value = byteprefix_dd_multiplyint(3.1, "G")
"""
  unit = str(prefix)
  if unit ==   "": return value * 1
  if unit ==  "c": return value * 1
  if unit ==  "w": return value * 2
  if unit ==  "b": return value * 512
  if unit ==  "B": return value * 1
  if unit == "kB": return value * 1000
  if unit ==  "K": return value * 1024
  if unit == "MB": return value * 1000 * 1000
  if unit ==  "M": return value * 1024 * 1024
  if unit == "xM": return value * 1024 * 1024
  if unit == "GB": return value * 1000 * 1000 * 1000
  if unit ==  "G": return value * 1024 * 1024 * 1024
  if unit == "TB": return value * 1000 * 1000 * 1000 * 1000
  if unit ==  "T": return value * 1024 * 1024 * 1024 * 1024
  if unit == "PB": return value * 1000 * 1000 * 1000 * 1000 * 1000
  if unit ==  "P": return value * 1024 * 1024 * 1024 * 1024 * 1024
  if unit == "EB": return value * 1000 * 1000 * 1000 * 1000 * 1000 * 1000
  if unit ==  "E": return value * 1024 * 1024 * 1024 * 1024 * 1024 * 1024
  if unit == "ZB": return value * 1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000
  if unit ==  "Z": return value * 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024
  if unit == "YB": return value * 1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000
  if unit ==  "Y": return value * 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024
  raise ValueError("invalid prefix: " + repr(prefix))
