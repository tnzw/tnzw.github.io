# difflines.py Version 1.0.0
# Copyright (c) 2018, 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def difflines(text1, text2, parsed_line_listener=None):

  def rec(matrix, a1, a2, x, y, parsed_line_listener):
    if (x > 0 and y > 0 and a1[y - 1] == a2[x - 1]):
      rec(matrix, a1, a2, x - 1, y - 1, parsed_line_listener)
      return parsed_line_listener((x, y, " ", a1[y - 1]))
    if (x > 0 and (y == 0 or matrix[y][x - 1] >= matrix[y - 1][x])):
      rec(matrix, a1, a2, x - 1, y, parsed_line_listener)
      return parsed_line_listener((x, None, "+", a2[x - 1]))
    if (y > 0 and (x == 0 or matrix[y][x - 1] < matrix[y - 1][x])):
      rec(matrix, a1, a2, x, y - 1, parsed_line_listener)
      return parsed_line_listener((None, y, "-", a1[y - 1]))

  a1, a2 = text1.split("\n"), text2.split("\n")
  matrix = [None] * (len(a1) + 1)
  r = []

  for y in range(len(matrix)):
    matrix[y] = [0] * (len(a2) + 1)

  for y in range(1, len(matrix)):
    for x in range(1, len(matrix[y])):
      if (a1[y - 1] == a2[x - 1]): matrix[y][x] = 1 + matrix[y - 1][x - 1]
      else: matrix[y][x] = max(matrix[y - 1][x], matrix[y][x - 1])

  rec(matrix, a1, a2, x, y, parsed_line_listener or (lambda e: r.append(e[2] + e[3])))
  return "\n".join(r)
