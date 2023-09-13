# zipfile_archive_pipegen.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def zipfile_archive_pipegen():
  state = None
  sent = yield b''
  while 1:
    state, result, end = zipfile_archive_pipealgo(state, sent)
    if end: return
    sent = yield result
zipfile_archive_pipegen._required_globals = ['zipfile_archive_pipealgo']
