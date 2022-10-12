# os_win32_getlettersbydrivelabel.py Version 2.0.4
# Copyright (c) 2020, 2022 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_win32_getlettersbydrivelabel():
  # https://ardamis.com/2012/08/21/getting-a-list-of-logical-and-physical-drives-from-the-command-line/
  # try with https://stackoverflow.com/questions/8319264/how-can-i-get-the-name-of-a-drive-in-python
  cp = subprocess.run(["wmic", "volume", "get", "DriveLetter,Label", "/format:list"], input=b"", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
  pattern = re.compile(b'(?:\\r*\\n)*DriveLetter=([^\\r\\n]*)\\r*\\nLabel=([^\\r\\n]*)\\r*\\n')
  o = {}
  m = pattern.match(cp.stdout)
  while m:
    o[m.group(2)] = m.group(1) or None
    m = pattern.match(cp.stdout, m.end())
  return o
os_win32_getlettersbydrivelabel._required_globals = ["re", "subprocess"]
