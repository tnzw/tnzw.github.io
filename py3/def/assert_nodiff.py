# assert_nodiff.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def assert_nodiff(a, b, t1='', t2=''):
  t1 = f'{t1}'; t2 = f'{t2}'
  it_diffs = False
  s = f'diff\n---{" " if t1 else ""}{t1}\n+++{" " if t2 else ""}{t2}\n@@\n'
  for ii, line in diff(a, b):
    if ii == (0, 1): s += f' {line!r}\n'
    elif ii == (0,): s += f'-{line!r}\n'; it_diffs = True
    elif ii == (1,): s += f'+{line!r}\n'; it_diffs = True
    else:            s += f'?{line!r}\n'; it_diffs = True
  if it_diffs: assert_equal(0, 1, s)
assert_nodiff._required_globals = ['assert_equal', 'diff']
