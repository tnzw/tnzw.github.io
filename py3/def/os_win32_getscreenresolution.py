# os_win32_getscreenresolution.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_win32_getscreenresolution():
  return ctypes.windll.user32.GetSystemMetrics(78), ctypes.windll.user32.GetSystemMetrics(79)
os_win32_getscreenresolution._required_globals = ["ctypes"]
