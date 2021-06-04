# datetime_is_summer_time.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def datetime_is_summer_time(datetime):
  """\
datetime_is_summer_time(datetime)

Return True if the given `datetime` is in summer time, else False.

Winter time is before last sunday from a complete week-end of march, 2am is 3am.
/!\ between 2am and 3am ? `>= 2am` is summer time.
Summer time is before last sunday from a complete week-end of october, 3am is 2am.
**/!\** between 3am and 2am ? `>= 2am` is winter time.
"""
  if 4 <= datetime.month <= 9: return True
  if datetime.month == 3:
    if datetime.weekday() == 6: return datetime.day >= 25 and datetime.hour >= 2
    return datetime.day >= 26 + datetime.weekday()
  elif datetime.month == 10:
    if datetime.weekday() == 6: return datetime.day < 25 or datetime.hour < 2
    return datetime.day < 26 + datetime.weekday()
  return False
