# diff.py Version 1.0.0
# Copyright (c) 2022 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def diff(iterable, *iterables):
  """\
can do classic diff: `diff(a, b)`, but can also do triple or more diff: `diff(a, b, c, d, …)`.
usage:
  for ii, line in diff(open("a"), open("b")):
    end = "\n\\ No newline at end of file\n" if line[-1] != "\n" else ""
    if ii == (0, 1): print(f" {line}", end=end)
    elif ii == (0,): print(f"-{line}", end=end)
    elif ii == (1,): print(f"+{line}", end=end)
    else: print(f"?{line}", end=end)
"""
  iterables = (iterable,) + iterables
  l = len(iterables)
  if l == 1:
    for _ in iterable: yield (0,), _
    return
  stacks = [[] for _ in range(l)]
  sii = set(range(l))
  matching = False
  match = [None for _ in range(l)]
  match_value = None
  undefined = []
  for row in zip2(*iterables, default=undefined):
    excluded = set()  # stack indices that have no row value to check for match
    # push in stacks
    for si, s, rv in zip(range(l), stacks, row):
      if rv is undefined:
        excluded.add(si)
      else:
        s.append(rv)
        # check for similar match
        if matching and match_value == rv and match[si] is None:
          match[si] = s[:] ; s[:] = ()
          excluded.add(si)
    # looping through stacks to check for matches
    for si1, s1 in enumerate(stacks):
      svi1 = -1
      while svi1 + 1 < len(s1):
        svi1 += 1
        sv1 = s1[svi1]
        # looping through eligible row values to check for matches
        for si2 in sii - {si1}:
          if si2 in excluded: continue
          s2 = stacks[si2]
          sv2 = s2[-1]
          if sv1 == sv2:  # new match !!
            if matching:
              # flush
              for mi, m in enumerate(match):
                if m is not None:
                  for mv in m[:-1]: yield (mi,), mv
              yield tuple(mi for mi, m in enumerate(match) if m is not None), match_value
            matching = True
            match_value = sv1
            match[:] = (None for _ in range(l))
            match[si1] = s1[:svi1 + 1] ; s1[:] = s1[svi1 + 1:] ; svi1 = -1
            match[si2] = s2[:] ; s2[:] = ()
            if not s1: excluded.add(si1)
            excluded.add(si2)
            for si3 in sii - {si1} - excluded:
              s3 = stacks[si3]
              sv3 = s3[-1]
              if sv1 == sv3:
                match[si3] = s3[:] ; s3[:] = ()
                excluded.add(si3)
  if matching:
    # flush
    for mi, m in enumerate(match):
      if m is not None:
        for mv in m[:-1]: yield (mi,), mv
    yield tuple(mi for mi, m in enumerate(match) if m is not None), match_value
  for si, s in enumerate(stacks):
    for sv in s:
      yield (si,), sv
diff._required_globals = ["zip2"]
