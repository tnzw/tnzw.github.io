# ScandirIterator.py Version 1.1.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class ScandirIterator(object):
  def __init__(self, iterator_to_close, other_iterator):
    # scan = os.scandir(...)
    # ScandirIterator(scan, (CustomDirEntry(...) for entry in scan))
    self._itc = iterator_to_close
    self._ito = other_iterator
  def __iter__(self): return self
  def __next__(self): return self._ito.__next__()
  def __enter__(self): return self
  def __exit__(self, *a): self.close()
  def close(self):
    if self._itc is not None:
      return self._itc.close()
