# metricprefix_format.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def metricprefix_format(number, format="{value:.0f}{prefix}", exclude_prefixes=set(("h", "da", "d", "c"))):
  """\
metricprefix_format(number[, format], **opt)

format => "{value:.0f}{prefix}"
opt
  exclude_prefixes => set(("h", "da", "d", "c")): a set of prefixes to not use

>>> metricprefix_format(123456789)
'123M'
>>> metricprefix_format(1234, "{value:.1f} {prefix_name}meter(s)")
'1.2 kilometer(s)'
>>> metricprefix_format(1234, exclude_prefixes=("k",))
'1234'
"""
  # https://en.wikipedia.org/wiki/Metric_prefix
  prefixes = ((10** 24, "Y", "yotta"), (10** 21, "Z", "zetta"),
              (10** 18, "E",   "exa"), (10** 15, "P",  "peta"), (10** 12, "T", "tera"),
              (10**  9, "G",  "giga"), (10**  6, "M",  "mega"), (10**  3, "k", "kilo"),
              (10**  2, "h", "hecto"), (10**  1,"da",  "deca"),
              (10**  0,  "",      ""),
              (10** -1, "d",  "deci"), (10** -2, "c", "centi"),
              (10** -3, "m",  "mili"), (10** -6, "µ", "micro"), (10** -9, "n", "nano"),
              (10**-12, "p",  "pico"), (10**-15, "f", "femto"), (10**-18, "a", "atto"),
              (10**-21, "z", "zepto"), (10**-24, "y", "yocto"))
  v, prefix, prefix_name = 1, "", ""
  if number != 0:
    for _ in prefixes:
      if _[1] in exclude_prefixes: pass
      else:
        v, prefix, prefix_name = _
        if number >= v: break
  if v != 1: number /= v
  return format.format(value=number, prefix=prefix, prefix_name=prefix_name, prefix_symbol=prefix)
