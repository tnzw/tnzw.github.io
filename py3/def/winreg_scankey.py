# winreg_scankey.py Version 1.0.0
# Copyright (c) 2022 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def winreg_scankey(key, sub_key, *, filter_keys=False, filter_values=False):
  def winreg_scankey_generator():
    with winreg.OpenKey(key, sub_key) as access_key:
      yield
      # getting values before keys, like a dump → [key]\n values\n [key\\subkey]\n …
      if not filter_values:
        i = 0
        while 1:
          try: yield winreg_KeyEntry('value', *winreg.EnumValue(access_key, i))
          except OSError as e:
            if e.errno == 22 and e.winerror == 259: break
            raise
          i += 1
      if not filter_keys:
        i = 0
        while 1:
          try: yield winreg_KeyEntry('key', winreg.EnumKey(access_key, i))
          except OSError as e:
            if e.errno == 22 and e.winerror == 259: break
            raise
          i += 1
  g = winreg_scankey_generator()
  next(g)
  return winreg_ScankeyIterator(g)
winreg_scankey._required_globals = ['winreg', 'winreg_KeyEntry', 'winreg_ScankeyIterator']
