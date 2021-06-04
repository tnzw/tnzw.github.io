# js_parse_int.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def js_parse_int():
  NaN = float("nan")
  def js_parse_int(string, radix=None):
    """\
Parses a string argument and returns an integer of the specified radix (the base
in mathematical numeral systems).

string
    The value to parse. If this argument is not a string, then it is converted
    to one using the ToString abstract operation. Leading whitespace in this
    argument is ignored.
radix=None
    An integer between 2 and 36 that represents the radix (the base in
    mathematical numeral systems) of the string. Be careful—this does not
    default to 10! If the radix value is not of the Number type it will be
    coerced to a Number

See orignal documentation :
https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/parseInt
"""
    string = str(string)  # force to be an str
    string = string.lstrip()
    sign = 1
    if string[:1] == "-": string, sign = string[1:], -1
    elif string[:1] == "+": string = string[1:]
    if radix is None:
      if string[:2].lower() == "0x": string, radix = string[2:], 16
      else: radix = 10
    elif radix == 16 and string[:2].lower() == "0x": string = string[2:]
    elif radix < 2 or 36 < radix: return NaN  # … sigh
    nums = []
    symbols = "0123456789abcdefghijklmnopqrstuvxyz"[:radix]
    for c in string:
      c = c.lower()
      if c in symbols:
        if c <= "9": nums.append(ord(c) - 0x30)
        else: nums.append(ord(c) - 0x57)
      else: break
    if nums:
      return sum(num * (radix ** coef) for num, coef in zip(nums, range(len(nums) - 1, -1, -1))) * sign
    return NaN  # it's a float, yes… javascript.

  js_parse_int.NaN = NaN
  return js_parse_int

js_parse_int = js_parse_int()
