# next2.py Version 1.0.0
# Copyright (c) 2024 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def next2(iterator):  # -> (iterator_value: any, is_ok: bool)
  try: return (next(iterator), True)
  except StopIteration as e: return (e.value, False)
