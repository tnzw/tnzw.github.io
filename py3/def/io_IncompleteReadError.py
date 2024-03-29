# io_IncompleteReadError.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class io_IncompleteReadError(Exception):
  def __init__(self, partial, expected):
    self.partial = partial
    self.expected = expected
    self.message = f"{len(partial)} bytes read on a total of {expected!r} expected bytes"
    super().__init__(self.message)
