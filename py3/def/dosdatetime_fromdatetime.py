# dosdatetime_fromdatetime.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def dosdatetime_fromdatetime(dt):
  """converts a non-naive datetime to a dosdatetime (naive)"""
  return dosdatetime(*dt.timetuple()[:6])
dosdatetime_fromdatetime._required_globals = ['dosdatetime']
