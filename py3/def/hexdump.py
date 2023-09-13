# hexdump.py Version 1.1.1
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def hexdump():
  def hexdump_iter(data):
    # 00000000  63 6f 75 63 6f 75 63 6f  75 63 6f 75 63 6f 75 63  |coucoucoucoucouc|
    # 00000010  6f 75                                             |ou|
    mi = 0
    while 1:
      d = data[mi:mi + 16]
      if not d: break
      line = f'{mi:08X}  '
      for b in d[:8]: line += f'{b:02X} '
      line += ' '
      for b in d[8:]: line += f'{b:02X} '
      line += ' ' * (60 - len(line)) + '|'
      for b in d:
        if 0x20 <= b < 0x7f: line += chr(b)
        else: line += '.'
      line += '|'
      yield line
      mi += 16
  def hexdumps(data): return '\n'.join(hexdump_iter(data))
  def hexdump(data, end='\n', sep='\n', **print_opt):
    i = hexdump_iter(data)
    for line in i: print(line, **print_opt, end=''); break
    for line in i: print(sep + line, **print_opt, end='')
    print(end=end)
  hexdump.iter = hexdump_iter
  hexdump.s = hexdumps
  return hexdump
hexdump = hexdump()
