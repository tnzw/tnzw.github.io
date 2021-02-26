# assert_is.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def assert_is(a, b, message=None, info=None):
  if message is None:
    message = "{} is not {}".format(pprint.pformat(a), pprint.pformat(b))
  if info is None: info = ""
  else: info = f", {info}"
  assert a is b, str(message) + str(info)

assert_is._required_globals = ["pprint"]
