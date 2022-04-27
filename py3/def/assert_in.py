# assert_in.py Version 1.0.0
# Copyright (c) 2022 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def assert_in(a, b, message=None, info=None):
  if message is None:
    message = "{} not in {}".format(pprint.pformat(a), pprint.pformat(b))
  if info is None: info = ""
  else: info = f", {info}"
  assert a in b, str(message) + str(info)

assert_in._required_globals = ["pprint"]
