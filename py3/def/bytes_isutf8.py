# bytes_isutf8.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def bytes_isutf8(data, errors=None, truncated_end=False, truncated_start=False):
  # UTF-8 BOM is handled (ef bb bf)
  i = 0; l = len(data)
  if truncated_start:
    l3 = 3 if l >= 3 else l
    while i < l3:
      code = data[i]
      if (0x80 & code) == 0: i += 1; break
      if (0xc0 & code) != 0x80: break
      i += 1
  while i < l:
    code = data[i]
    if   (0x80 & code) == 0: i += 1
    elif (0xe0 & code) == 0xc0:  # two bytes required
      #if code < 0xc2  # overlong encoding
      if i + 1 >= l: return True if truncated_end else False  # end of data
      a = code; code = data[i + 1]
      if (0xc0 & code) != 0x80: return False  # invalid continuation byte
      i += 2
    elif (0xf0 & code) == 0xe0:  # three bytes required
      if i + 1 >= l: return True if truncated_end else False  # end of data
      a = code; code = data[i + 1]
      if (0xc0 & code) != 0x80: return False  # invalid continuation byte
      #if a == 0xe0 and code <= 0x9f  # overlong encoding
      a = (a << 6) | (code & 0x3f)
      if i + 2 >= l: return True if truncated_end else False  # end of data
      code = data[i + 2]
      if (0xc0 & code) != 0x80: return False  # invalid continuation byte
      #c = ((a << 6) | (code & 0x3f)) & 0xffff; if 0xd800 <= c <= 0xdfff  # reserved code point
      i += 3
    elif (0xf8 & code) == 0xf0:  # four bytes required
      if code >= 0xf5: return False  # invalid start byte
      if i + 1 >= l: return True if truncated_end else False  # end of data
      a = code; code = data[i + 1]
      if (0xc0 & code) != 0x80: return False  # invalid continuation byte
      #if a == 0xf0 and code <= 0x8f  # overlong encoding
      a = (a << 6) | (code & 0x3f)
      if i + 2 >= l: return True if truncated_end else False  # end of data
      code = data[i + 2]
      if (0xc0 & code) != 0x80: return False  # invalid continuation byte
      a = (a << 6) | (code & 0x3F)
      if i + 3 >= l: return True if truncated_end else False  # end of data
      code = data[i + 3]
      if (0xc0 & code) != 0x80: return False  # invalid continuation byte
      #c = ((a << 6) | (code & 0x3f)) & 0x1fffff; if c > 0x10ffff  # invalid code point
      i += 4
    else: return False  # invalid start byte
  return True
