# data_iupper.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def data_iupper(data):
  def upper(value):
    def upper_byte(value):
      if 0x41 <= value <= 0x5A: return value + 0x20
      return value 
    def upper_str(value): return value.upper()
    if isinstance(v, int): upper.brain = upper_byte
    else: upper.brain = upper_str
    return upper.brain(value)
  upper.brain = upper
  for i, v in enumerate(data): data[i] = upper.brain(v)
