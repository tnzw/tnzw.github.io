# assert_notequal.py Version 1.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def assert_notequal(a, b, message=None):
  if message is None:
    message = "{} == {}".format(pprint.pformat(a), pprint.pformat(b))
  assert a != b, message

assert_notequal._required_globals = ["pprint"]
