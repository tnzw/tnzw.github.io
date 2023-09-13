# dosdatetime.py Version 1.0.1
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def dosdatetime(year, month, day, hour=0, minute=0, second=0):
  # A dosdatetime is a uint32 (or larger)
  # https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-dosdatetimetofiletime
  # 0 <= second < 32 * 2, 0 <= minutes < 64, 0 <= hour < 32, 0 <= day < 32, 0 <= month < 16, 1980 <= year < 2108
  # bits YYYYYYYMMMMDDDDDhhhhhmmmmmmsssss
  #if not (1980 <= year < 2108): raise ValueError(...)  # 2107 is spec max year
  if year < 1980: raise ValueError("year must be >= 1980")
  if month & -0x10: raise ValueError("month must be in 1..12")
  if day & -0x20: raise ValueError("day must be in 1..31")
  if hour & -0x20: raise ValueError("hour must be in 0..23")
  if minute & -0x40: raise ValueError("minute must be in 0..59")
  if second & -0x40: raise ValueError("second must be in 0..59")
  return ((year - 1980) << 25) | (month << 21) | (day << 16) | (hour << 11) | (minute << 5) | second // 2
