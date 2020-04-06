# os_win32_getlettersbydrivelabel.py Version 2.0.3
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_win32_getlettersbydrivelabel():
  # try with https://stackoverflow.com/questions/8319264/how-can-i-get-the-name-of-a-drive-in-python
  cp = subprocess.run(["wmic", "volume", "get", "DriveLetter,Label"], input=b"", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
#  cp.stdout = """DriveLetter  Label
#C:           OS
#             RECOVERY
#D:           MYUSB
#             SYSTEM
#
#
#"""
  o = {}
  lines = [l for ll in cp.stdout.split(b"\n") for l in ll.split(b"\r")]
  driveletter_length = len(re.match(b"^(DriveLetter\s+)Label\s*$", lines[0]).group(1))
  matcher = re.compile(b"^(.{" + str(driveletter_length).encode("ascii") + b"})(.*)$")
  for line in lines[1:]:
    m = re.match(b"^([A-Z]:|\\s{2})\\s{11}(.*)$", line)
    if not m: continue
    o[m.group(2).rstrip()] = m.group(1) if re.search(b"\\S", m.group(1)) else None
  return o
os_win32_getlettersbydrivelabel._required_globals = ["re", "subprocess"]
