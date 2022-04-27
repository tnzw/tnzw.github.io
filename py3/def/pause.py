# pause.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def pause(prompt=None):
  if prompt is None: prompt = "Press any key to continue... "
  def fallback_pause():
    if prompt.endswith("\r\n"): input(prompt[:-2] + " ")
    elif prompt.endswith("\n"): input(prompt[:-1] + " ")
    else: input(prompt)
  def win_pause():
    if prompt:
      sys.stdout.write(prompt)
      sys.stdout.flush()
    c = msvcrt.getwch()
    if c == "\003": raise KeyboardInterrupt
    sys.stdout.write("\r\n")
  def unix_pause():
    fd = sys.stdin.fileno()
    if prompt:
      sys.stdout.write(prompt)
      sys.stdout.flush()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~termios.ICANON & ~termios.ECHO  # lflag
    new[6][termios.VMIN] = 1
    new[6][termios.VTIME] = 0
    termios.tcsetattr(fd, termios.TCSANOW, new)
    try:
      os.read(fd, 1)  # blocking if no input given
    finally:
      termios.tcsetattr(fd, termios.TCSAFLUSH, old)
    sys.stdout.write("\n")

  # inspired by getpass.py
  try: termios.tcgetattr, termios.tcsetattr
  except (NameError, AttributeError):
    try: msvcrt
    except NameError: fallback_pause()
    else: win_pause()
  else: os, unix_pause()

pause._required_globals = ["os", "sys", "termios", "msvcrt"]
