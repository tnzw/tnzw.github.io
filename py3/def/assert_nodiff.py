# assert_nodiff.py Version 1.0.1
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def assert_nodiff():
  def diff_key(o):
    t = type(o)
    m = getattr(t, '__key__', None)
    if m is None:
      return ({
        tuple: lambda o: tuple(diff_key(_) for _ in o),
        list: lambda o: [diff_key(_) for _ in o],
        dict: lambda o: repr({diff_key(k): diff_key(v) for k, v in o.items()}),
      }).get(t, lambda _: _)(o)
    return m(o)
  def assert_nodiff(a, b, t1='', t2='', *, key=None, use_no_hash=None):
    if key is None and not use_no_hash: key = diff_key
    t1 = f'{t1}'; t2 = f'{t2}'
    it_diffs = False
    s = f'diff\n---{" " if t1 else ""}{t1}\n+++{" " if t2 else ""}{t2}\n@@\n'
    for ii, line in diff(a, b, key=key, use_no_hash=use_no_hash):
      if ii == (0, 1): s += f' {line!r}\n'
      elif ii == (0,): s += f'-{line!r}\n'; it_diffs = True
      elif ii == (1,): s += f'+{line!r}\n'; it_diffs = True
      else:            s += f'?{line!r}\n'; it_diffs = True
    if it_diffs: assert_equal(0, 1, s)
  assert_nodiff.key = diff_key
  return assert_nodiff
assert_nodiff = assert_nodiff()
assert_nodiff._required_globals = ['assert_equal', 'diff']
