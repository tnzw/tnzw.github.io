# diff.py Version 1.1.0
# Copyright (c) 2022-2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

# Maybe I should take a look some diff algorithm, well... later, my implementation works so far.
# - https://stackoverflow.com/questions/805626/diff-algorithm#1313218
# - http://ftp.gnu.org/gnu/diffutils/
# - https://github.com/google/diff-match-patch

def diff(iterable, *iterables, key=None, default=None, algo=0, yieldtype=0, use_no_hash=False):
  """\
Can do classic diff: `diff(a, b)`, but can also do triple or more diff: `diff(a, b, c, d, …)`.
usage:
  for ii, line in diff(open('a'), open('b')):
    end = '\n\\ No newline at end of file\n' if line[-1] != '\n' else ''
    if   ii == (0, 1): print(f' {line}', end=end)
    elif ii == (0,):   print(f'-{line}', end=end)
    elif ii == (1,):   print(f'+{line}', end=end)
    else:              print(f'?{line}', end=end)

algo: diff.A_CLASSIC_MATCH: yields items once several possible matches are found (default)
      diff.A_LONGEST_MATCH: yields unmatched items once any match is found (XXX not implemented yet)
      diff.A_PER_ROW_MATCH: yields on every row of items
yieldtype: diff.Y_MATCHING_INDICES_FIRST_VALUE               : usage `for ii, line in diff(open('a'), open('b'))`
           diff.Y_MATCHING_VALUES_OR_DEFAULT                 : usage `for line_a, line_b in diff(open('a'), open('b'), default=None)`
           diff.Y_MATCHING_INDICES_MATCHING_VALUES_OR_DEFAULT: usage `for ii, (line_a, line_b) in diff(open('a'), open('b'), default=None)`
use_no_hash: do not use hash() in the algo (increases computing time a lot).
             This might be useful when using `diff(custom_magic_object, custom_magic_object)`.
"""
  # il -> indexed list
  if use_no_hash:
    def il_new(): return []
    def il_bool(il): return bool(il)
    def il_len(il): return len(il)
    def il_add(il, vk, *v):
      if v: v, = v
      else: v = vk
      il.append((vk, v))
    def il_in(il, vk): return any(vk == _[0] for _ in il)  # slow!!
    def il_getall(il, vk): return [_[1] for _ in il if _[0] == vk]  # slow!!
    def il_shift2(il): return il.pop(0)
    def il_shift(il): return il.pop(0)[1]
  else:
    def il_new(): return ([], {})
    #def il_clear(il): il[0].clear(); il[1].clear()
    def il_bool(il): return bool(il[0])
    def il_len(il): return len(il[0])
    def il_add(il, vk, *v):
      l, d = il
      if v: v, = v
      else: v = vk
      #li = len(l)
      #if vk in d: d[vk].append((li, vk, v))
      #else: d[vk] = [(li, vk, v)]
      if vk in d: d[vk].append((vk, v))
      else: d[vk] = [(vk, v)]
      l.append((vk, v))
    def il_in(il, vk): return vk in il[1]
    #def il_iget(il, i): return il[0][i][1]
    #def il_kget(il, vk): return il[1][vk][2]
    #def il_kget(il, vk): return il[1][vk][1]
    def il_getall(il, vk): return [_[1] for _ in il[1].get(vk, [])]
    #def il_keyindex(il, vk):
    #  try: return il[1][vk][0]
    #  except KeyError: return -1
    def il_shift2(il):
      l, d = il
      vk, v = l.pop(0)
      d[vk].pop(0)
      if not d[vk]: del d[vk]
      return vk, v
    def il_shift(il): return il_shift2(il)[1]
    #def il_pop(il):
    #  l, d = il
    #  vk, v = l.pop()
    #  d[vk].pop()
    #  if not d[vk]: del d[vk]
    #  return v
    #def il_values(il):
    #  for vk, v in il[0]:
    #    yield v
  # ill -> indexed list list
  #def ill_new(size): return [il_new() for _ in range(size)]
  #def ill_newil(ill): il = il_new(); ill.append(il); return il
  #def ill_popil(ill): return ill.pop(0)
  #def ill_addvalue(ill, vk, *v):
  #  if not ill: ill_newil(ill)
  #  il_add(ill[-1], vk, *v)
  def ill_search(ill, vk):
    res = []
    for ili, il in enumerate(ill):
      #i = il_keyindex(il, vk)
      #if i != -1: res.append((ili, i))
      if il_in(il, vk): res.append(ili)
    return res
  iterables = (iterable,) + iterables
  if key is None: key = lambda v: v
  if algo is None: algo = 0
  if yieldtype is None: yieldtype = 0
  l = len(iterables)
  rl = range(l)
  def y_iv0(i, v):
    return tuple(v if _ == i else default for _ in rl)
  def y_iivv0(ii, vv):
    rr = [default] * l
    for _, i in enumerate(ii): rr[i] = vv[_]
    return tuple(rr)
  yielders = {
    0: (lambda i, v: ((i,), v), lambda ii, vv: (tuple(ii), vv[0])),  # returns ((i, ...), v), very quick
    1: (lambda i, v: tuple(v if i == _ else default for _ in rl), y_iivv0),  # returns (v, ...), pretty inefficient
    2: (lambda i, v: ((i,), y_iv0(i, v)), lambda ii, vv: (tuple(ii), y_iivv0(ii, vv))),  # returns ((i, ...), (v, ...)), pretty inefficient
  }
  if algo not in {0, 1, 2}: raise ValueError('invalid algo parameter')
  if yieldtype not in yielders: raise ValueError('invalid yield type parameter')
  y_iv, y_iivv = yielders[yieldtype]
  if l == 1:
    for _ in iterable: yield y_iv(0, _)
    return
  undefined = []
  if algo == 1:
    for row in zip2(*iterables, default=undefined):
      matches = {}
      for si, rv in zip(rl, row):
        if rv is not undefined:
          rvk = key(rv)
          if rvk in matches: m = matches[rvk]; m[0].append(si); m[1].append(rv)
          else: matches[rvk] = ([si], [rv])
      for rvk, (msii, mvv) in matches.items():
        yield y_iivv(msii, mvv)
    return
  # we can imagine -> diff('aZY','bZc','Yde') yielding: 'a--' '-b-' '--Y', 'ZZ-' '--d' 'Y--' '-c-' '--e'  (PER_ROW_MATCH)  (use very few memory)
  # we can imagine -> diff('aZY','YZc','Yde') yielding: '-YY' 'a--' 'ZZ-' 'Y--' '-c-' '--d' '--e'  (CLASSIC_MATCH)  (may use less memory in worst case)
  # we can imagine -> diff('aZY','YZc','Yde') yielding: 'a--' 'Z--' 'YYY' '-Z-' '-c-' '--d' '--e'  (LONGEST_MATCH)  (may use high memory in worst case)
  #   Feed until I find 3 (n-0) matches with ill_search or end of rows, find 2 (n-1) matches from the previous unmatched part, same thing (n-2) recursively

  # CLASSIC MATCH (pretty good algo, but not perfect for more than 2 iterables)
  def iterchain(*it):
    for _ in it:
      yield from _
  rows = [il_new() for si in rl]
  matches = il_new()
  for ri, row in enumerate(iterchain(zip2(*iterables, default=undefined), ([undefined] * l,))):
    is_last_row = True
    # push row in rows
    row2 = []
    for si, rv in zip(rl, row):
      if rv is not undefined:
        is_last_row = False
        rr = rows[si]
        rvk = key(rv)
        il_add(rr, rvk, (rvk, rv))
        row2.append((si, rvk))
    # find match
    for si, rvk in row2:
      sii = ill_search(rows, rvk)
      if len(sii) >= 2:
        dd = il_getall(matches, rvk)
        for d in dd:
          if si not in d:
            d[si] = True
            break
        else:
          il_add(matches, rvk, {si: True})
    # flush
    end = 0 if is_last_row else 1
    while il_len(matches) > end:
      rvk, d = il_shift2(matches)
      sii = ill_search(rows, rvk)
      vv = []
      for si in sii:
        rr = rows[si]
        while il_bool(rr):
          rvk2, rv2 = il_shift(rr)
          if rvk2 != rvk:
            yield y_iv(si, rv2)
          else:
            vv.append(rv2)
            break
      yield y_iivv(sii, vv)
      # XXX now matches may be inconsistent as we might have remove some cross match
      #     do our best by refreshing matches
      matches2 = il_new()
      while il_len(matches):
        rvk, d = il_shift2(matches)
        sii = ill_search(rows, rvk)
        if len(sii) >= 2: il_add(matches2, rvk, d)
      matches = matches2
      del matches2
    # flush remaining
    if is_last_row:
      for si in rl:
        rr = rows[si]
        while il_bool(rr):
          rvk2, rv2 = il_shift(rr)
          yield y_iv(si, rv2)

diff.A_CLASSIC_MATCH = 0
diff.A_PER_ROW_MATCH = 1
diff.Y_MATCHING_INDICES_FIRST_VALUE = 0
diff.Y_MATCHING_VALUES_OR_DEFAULT = 1
diff.Y_MATCHING_INDICES_MATCHING_VALUES_OR_DEFAULT = 2
diff._required_globals = ['zip2']
