# os_posix_getmountpointsbydrivelabel.py Version 2.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_posix_getmountpointsbydrivelabel():
  # try with https://stackoverflow.com/questions/8319264/how-can-i-get-the-name-of-a-drive-in-python
  # try with labels = os.listdir("/dev/disk/by-label")
  cp = subprocess.run(["lsblk", "-o", "LABEL,MOUNTPOINT"], input=b"", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
#  cp.stdout = """LABEL    MOUNTPOINT
#SYSTEM   /boot/efi
#         
#OS       
#RECOVERY 
#         /
#         
#MYUSB    /media/user/MyUsb
#"""
  o = {}
  lines = cp.stdout.split(b"\n")
  label_length = len(re.match(b"^(LABEL\s+)MOUNTPOINT$", lines[0]).group(1))
  matcher = re.compile(b"^(.{" + str(label_length).encode("ascii") + b"})(.*)$")
  for line in lines[1:]:
    m = matcher.match(line)
    if not m: continue
    o[m.group(1).rstrip()] = m.group(2) if re.search(b"\\S", m.group(2)) else None
  return o
os_posix_getmountpointsbydrivelabel._required_globals = ["re", "subprocess"]
