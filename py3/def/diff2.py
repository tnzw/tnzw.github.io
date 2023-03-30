# diff2.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def diff2(iterable, *iterables, key=None, default=None):
  """\
can do classic diff: `diff2(a, b)`, but can also do triple or more diff: `diff2(a, b, c, d, …)`.
usage:
  for line_a, line_b in diff(open("a"), open("b")):
    if   line_a is None: print(f'-{line_b}', end='\n\\ No newline at end of file\n' if line_b[-1] != '\n' else ''
    elif line_b is None: print(f'+{line_a}', end='\n\\ No newline at end of file\n' if line_a[-1] != '\n' else ''
    else:                print(f' {line_a}', end='\n\\ No newline at end of file\n' if line_a[-1] != '\n' else ''
"""
  iterables = (iterable,) + iterables
  if key is None: key = lambda v: v
  l = len(iterables)
  if l == 1:
    for _ in iterable: yield (0,), _
    return
  stacks = [[] for _ in range(l)]
  sii = set(range(l))
  matching = False
  match = [None for _ in range(l)]
  match_value = None; match_value_key = None
  undefined = []
  for row in zip2(*iterables, default=undefined):
    excluded = set()  # stack indices that have no row value to check for match
    # push in stacks
    for si, s, rv in zip(range(l), stacks, row):
      if rv is undefined:
        excluded.add(si)
      else:
        rv_key = key(rv)
        s.append((rv, rv_key))
        # check for similar match
        if matching and match_value_key == rv_key and match[si] is None:
          match[si] = s[:] ; s[:] = ()
          excluded.add(si)
    # looping through stacks to check for matches
    for si1, s1 in enumerate(stacks):
      svi1 = -1
      while svi1 + 1 < len(s1):
        svi1 += 1
        sv1, sv1_key = s1[svi1]
        # looping through eligible row values to check for matches
        for si2 in sii - {si1}:
          if si2 in excluded: continue
          s2 = stacks[si2]
          sv2, sv2_key = s2[-1]
          if sv1_key == sv2_key:  # new match !!
            if matching:
              # flush
              for mi, m in enumerate(match):
                if m is not None:
                  t = [default] * l
                  for mv, mvk in m[:-1]: _[mi] = mv; yield tuple(t)
                  t = None
              yield (*(default if m is None else m[-1][0] for m in match),)
            matching = True
            match_value = sv1; match_value_key = sv1_key
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
        _ = [default] * l
        for mv, mvk in m[:-1]: _[mi] = mv; yield tuple(_)
        _ = None
    yield (*(default if m is None else m[-1][0] for m in match),)
  for si, s in enumerate(stacks):
    t = [default] * l
    for sv, svk in s: t[si] = sv; yield tuple(t)
    t = None
diff2._required_globals = ['zip2']
