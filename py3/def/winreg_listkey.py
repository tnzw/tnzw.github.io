# winreg_listkey.py Version 1.0.0
# Copyright (c) 2022 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def winreg_listkey(key, sub_key, *, filter_keys=False, filter_values=False):
  with winreg_scankey(key, sub_key, filter_keys=filter_keys, filter_values=filter_values) as scan:
    return [_.name for _ in scan]
winreg_listkey._required_globals = ['winreg_scankey']
