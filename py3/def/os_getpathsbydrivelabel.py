# os_getpathsbydrivelabel.py Version 1.1.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_getpathsbydrivelabel():
  if sys.platform == "win32":
    labels = os_win32_getlettersbydrivelabel()
    return {label: letter + b"\\" for label, letter in labels.items() if letter}
  else:
    mountpoints = os_posix_getmountpointsbydrivelabel()
    return {label: mountpoint for label, mountpoint in mountpoints.items() if mountpoint}
os_getpathsbydrivelabel._required_globals = [
  "sys",
  "os_win32_getlettersbydrivelabel",
  "os_posix_getmountpointsbydrivelabel",
]
