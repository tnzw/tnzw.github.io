# bytes_format.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def bytes_format(format, *a, **k):
  """\
Acts like str.format on bytes. Every byte-array like arguments are converted to
str using a lossless encoding (here is ('UTF-8', 'surrogateescape')), then an
str.format is applied, then converted again to bytes.

>>> bytes_format(b"{} {my_str} {value:.1f}", b"hello", my_str="world", value=12.3456)
b'hello world 12.3'
"""
  encoding = ("UTF-8", "surrogateescape")  # lossless encoding  # XXX hardcoded
  def tof(v):
    if isinstance(v, (bytes, bytearray)): return v.decode(*encoding)
    return v
  return format.decode(*encoding).format(
    *(tof(_) for _ in a),
    **{k: tof(v) for k, v in k.items()}
  ).encode(*encoding)
