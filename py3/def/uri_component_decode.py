# uri_component_decode.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def uri_component_decode(bb):
  if isinstance(bb, str): bb = bb.encode("UTF-8", "surrogateescape")
  parts = bb.split(b"%")
  res = [parts[0]]
  app = res.append
  for part in parts[1:]:
    try: _ = bytes((int(part[:2], 16),))
    except ValueError: app(b"%"), app(part)
    else: app(_), app(part[2:])
  return b"".join(res)
