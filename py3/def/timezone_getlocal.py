# timezone_getlocal.py Version 1.1.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def timezone_getlocal():
  return datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

timezone_getlocal._required_globals = ['datetime']
