# stat_type.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def stat_type(mode):
  """Convert a file’s mode to a string of the form ‘symbolic_link’."""
  mode = mode & 0xF000
  if mode == 0x8000: return "file"
  if mode == 0x4000: return "directory"
  if mode == 0xA000: return "symbolic_link"
  if mode == 0xC000: return "socket"
  if mode == 0x1000: return "fifo"
  if mode == 0x6000: return "block_device"
  if mode == 0x2000: return "character_device"
  return "unknown"
