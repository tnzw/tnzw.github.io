# iter_inspect.py Version 1.0.0
# Copyright (c) 2024 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def iter_inspect(iterable, fn):
  """\
Usage example:

    def counter(_): counter.count += 1
    counter.count = 0
    result = process_stream(iter_inspect(stream, counter))
    print(f'{counter.count} elements processed to produce result {result!r}')
"""
  for v in iterable:
    fn(v)
    yield v
