# dosdatetime_utcfromtimestamp.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def dosdatetime_utcfromtimestamp(ts):
  return dosdatetime(*time.gmtime(ts)[:6])  # /!\ naive
dosdatetime_utcfromtimestamp._required_globals = ['time', 'dosdatetime']
