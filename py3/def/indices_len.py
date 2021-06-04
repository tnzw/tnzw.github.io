# indices_len.py Version 1.0.1
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def indices_len(indices):
  # indices_len(slice(0, 20, 2).indices(10)) -> 5
  start, stop, step = indices
  if step < 0:
    delta = start - stop
    if step < -1:
      d,m = divmod(delta, -step)
      delta = d + (1 if m else 0)
  else:
    delta = stop - start
    if step > 1:
      d,m = divmod(delta, step)
      delta = d + (1 if m else 0)
  return delta if delta > 0 else 0
