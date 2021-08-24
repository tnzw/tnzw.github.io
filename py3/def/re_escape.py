# re_escape.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def re_escape(text):
  if isinstance(text, str):
    return re.sub( "([\\\\\\[\\]\\{\\}\\(\\)\\.\\?\\*\\+\\^\\$])",  "\\\\\\1", text)
  return   re.sub(b"([\\\\\\[\\]\\{\\}\\(\\)\\.\\?\\*\\+\\^\\$])", b"\\\\\\1", text)
re_escape._required_globals = ["re"]
