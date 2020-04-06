# binaryprefix_multiplyint.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def binaryprefix_multiplyint(value, prefix):
  """\
possible prefixes : k Ki M Mi G Gi T Ti P Pi E Ei Z Zi Y Yi
    value = binaryprefix_multiplyint(3.1, "G")
"""
  unit = str(prefix)
  if unit ==   "": return value * 1
  if unit ==  "k": return value * 1000
  if unit == "Ki": return value * 1024
  if unit ==  "M": return value * 1000 * 1000
  if unit == "Mi": return value * 1024 * 1024
  if unit ==  "G": return value * 1000 * 1000 * 1000
  if unit == "Gi": return value * 1024 * 1024 * 1024
  if unit ==  "T": return value * 1000 * 1000 * 1000 * 1000
  if unit == "Ti": return value * 1024 * 1024 * 1024 * 1024
  if unit ==  "P": return value * 1000 * 1000 * 1000 * 1000 * 1000
  if unit == "Pi": return value * 1024 * 1024 * 1024 * 1024 * 1024
  if unit ==  "E": return value * 1000 * 1000 * 1000 * 1000 * 1000 * 1000
  if unit == "Ei": return value * 1024 * 1024 * 1024 * 1024 * 1024 * 1024
  if unit ==  "Z": return value * 1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000
  if unit == "Zi": return value * 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024
  if unit ==  "Y": return value * 1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000
  if unit == "Yi": return value * 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024
  raise ValueError("invalid prefix: " + repr(prefix))
