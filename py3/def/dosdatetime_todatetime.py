# dosdatetime_todatetime.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def dosdatetime_todatetime(ddt):
  # bits YYYYYYYMMMMDDDDDhhhhhmmmmmmsssss
  return datetime.datetime((ddt >> 25) + 1980, (ddt >> 21) & 0xF, (ddt >> 16) & 0x1F, (ddt >> 11) & 0x1F, (ddt >> 5) & 0x3F, (ddt & 0x1F) * 2)
dosdatetime_todatetime._required_globals = ['datetime']
