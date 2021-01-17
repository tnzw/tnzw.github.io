# data_iswapcase.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def data_iswapcase(data):
  def swapcase(value):
    def swapcase_byte(value):
      if 0x41 <= value <= 0x5A: return value + 0x20
      if 0x61 <= value <= 0x7A: return value - 0x20
      return value 
    def swapcase_str(value): return value.swapcase()
    if isinstance(v, int): swapcase.brain = swapcase_byte
    else: swapcase.brain = swapcase_str
    return swapcase.brain(value)
  swapcase.brain = swapcase
  for i, v in enumerate(data): data[i] = swapcase.brain(v)
