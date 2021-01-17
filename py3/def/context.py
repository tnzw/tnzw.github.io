# context.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class context(object):
  # see https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers
  # and inspired by https://docs.python.org/3/library/functions.html#property
  def __init__(self, shared, enter, exit): self._enter, self._exit, self._shared = enter, exit, shared
  def __enter__(self): return self._enter(self._shared)
  def __exit__(self, type, value, traceback): return self._exit(self._shared, type, value, traceback)
