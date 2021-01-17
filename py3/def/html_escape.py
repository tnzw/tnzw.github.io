# html_escape.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def html_escape(s, quote=True):
  """
  Enhanced version of html.escape to allow escaping bytes.

  Replace special characters "&", "<" and ">" to HTML-safe sequences.
  If the optional flag quote is true (the default), the quotation mark
  characters, both double quote (") and single quote (') characters are also
  translated.
  """
  if isinstance(s, (bytes, bytearray)):
    s, amp, lt, gt, quot, squot = bytes(s), (b"&", b"&amp;"), (b"<", b"&lt;"), (b">", b"&gt;"), (b'"', b"&quot;"), (b'\'', b"&#x27;")
  else:
    amp, lt, gt, quot, squot = ("&", "&amp;"), ("<", "&lt;"), (">", "&gt;"), ('"', "&quot;"), ('\'', "&#x27;")
  s = s.replace(*amp)  # Must be done first!
  s = s.replace(*lt)
  s = s.replace(*gt)
  if quote:
    s = s.replace(*quot)
    s = s.replace(*squot)
  return s
