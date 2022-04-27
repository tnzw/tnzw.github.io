# zip2.py Version 1.0.0
# Copyright (c) 2022 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def zip2(*iterables, default=None):
  """\
zip2(*iterables, default=None) --> a generator yielding tuples until all inputs are exhausted.

    >>> list(zip2('abcde', range(3), range(4)))
    [('a', 0, 0), ('b', 1, 1), ('c', 2, 2), ('d', None, 3), ('e', None, None)]

This generator yields n-length tuples, where n is the number of iterables
passed as positional arguments to zip2(). The i-th element in every tuple
comes from the i-th iterable argument to zip2(). This continues until the
longest argument is exhausted.  Shorter iterables are padded with a given
default value which defaults to None.
"""
  pack = [default] * len(iterables)
  # benchmarck this fonction using (unordered) set() or (ordered) dict() : seem that using dict() is a little bit quicker than set(), which is a bit quicker than list().
  #iterators = [(i, iter(it)) for i, it in enumerate(iterables)]  # list()
  #iterators = {(i, iter(it)) for i, it in enumerate(iterables)}  # unordered set() : https://docs.python.org/3/tutorial/datastructures.html#sets
  iterators = {i: iter(it) for i, it in enumerate(iterables)}  # ordered dict() : https://docs.python.org/3/tutorial/datastructures.html#dictionaries
  todel = []  # using set() or dict()
  while True:
    #oi = 0  # using list()
    #for ii, (i, it) in enumerate(iterators):  # using list()
    #for i, it in iterators:  # using set()
    for i, it in iterators.items():  # using dict()
      for v in it:
        pack[i] = v
        break
      else:
        pack[i] = default
        #iterators.pop(ii - oi) ; oi += 1  # using list()
        #todel.append((i, it))  # using set()
        todel.append(i)  # using dict()
    if todel:
      #for i in todel: iterators.remove(i)  # using set()
      for i in todel: del iterators[i]  # using dict()
      todel[:] = ()
    if iterators: yield tuple(pack)
    else: break
