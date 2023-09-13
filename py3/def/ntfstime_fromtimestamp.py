# ntfstime_fromtimestamp.py Version 1.1.1
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def ntfstime_fromtimestamp(ts, ceil=False):
  # an ntfs time is an amount of 100 nanoseconds since 1 Jan 1601
  # 116444736000000000 is "1 Jan 1970" - "1 Jan 1601" in 100ns
  if type(ts) is int: return ts * 10000000 + 116444736000000000
  # I have better precision using divmod()
  #                                        922337203680.4775801 * 10000000 => 9223372036804774912
  #   divmod(922337203680.4775801, 1) => $div * 10000000 + $mod * 10000000 => 9223372036804775390
  ts, mod = divmod(ts, 1)
  mod *= 10000000
  intmod = int(mod)
  ts = int(ts) * 10000000 + intmod
  if ceil and mod - intmod > 0: ts += 1
  return ts + 116444736000000000
