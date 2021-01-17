# assert_notequal.py Version 1.1.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def assert_notequal(a, b, message=None, info=None):
  if message is None:
    message = "{} == {}".format(pprint.pformat(a), pprint.pformat(b))
  if info is None: info = ""
  else: info = f", {info}"
  assert a != b, str(message) + str(info)

assert_notequal._required_globals = ["pprint"]
