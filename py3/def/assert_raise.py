# assert_raise.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def assert_raise(E, fn, message=None):
  try: val = fn()
  except E: return
  if message is None:
    val = repr(val)
    if len(val) > 100: val = val[:100] + "..."
    message = "returned value : " + val
  assert False, message
