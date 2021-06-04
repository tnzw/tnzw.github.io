# io_chain.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class io_chain(tuple):
  """\
io_chain(*readables)
io_chain(io.BytesIO(b"abc"), io.BytesIO(b"def")).read() → b"abcdef"

Considered closed if one of the readables is close.
`close()` closes all readables.
`unclosed_chained = io_chain(*(_ for _ in chained.ios if not _.closed))`.
"""

  # io.IOBase
  #   mixins ["close", "closed", "__enter__", "__exit__", "flush", "isatty",
  #           "__iter__", "__next__", "readable", "readline", "readlines",
  #           "seekable", "tell", "writable", "writelines"]
  #   stubs  ["fileno", "seek", "truncate"]

  @property
  def closed(self):
    for r in self.ios:
      if r.closed: return True
    return False
  def close(self):
    for r in self.ios: r.close()

  def readable(self): return True
  def seekable(self): return False
  def writable(self): return False

  for _ in ("__enter__", "__exit__", "flush", "isatty",
            "__iter__", "__next__", "readline", "readlines",
            "fileno", "_checkClosed"):
    exec(f"def {_}(self, *a, **k): return RawIOBase.{_}(self, *a, **k)", globals(), locals())
  del _

  # io.RawIOBase
  #   mixins IOBase + ["read", "readall"]
  #   stubs  ["readinto", "write"]
  #   others ["raw"]

  # io.BufferedIOBase
  #   mixins IOBase + ["readinto", "readinto1"]
  #   stubs  ["detach", "read", "read1", "write"]
  #   others ["buffer"]

  def __del__(self): pass  # children have their own way to close on __del__

  @property
  def ios(self): return super().__getitem__(0)

  def __new__(cls, readable, *readables):
    readables = (readable,) + readables
    for r in readables:
      if callable(getattr(r, "readable", None)) and not r.readable():
        try: Error = io.UnsupportedOperation
        except NameError: Error = ValueError
        raise Error("File or stream is not readable.")
    return tuple.__new__(cls, (readables,))

  def readinto1(self, b):
    self._checkClosed()
    for r in self.ios:
      _ = (getattr(r, "readinto1") or r.readinto)(b)
      if _ > 0: return _
    return 0

  def read(self, size=-1):
    self._checkClosed()
    if size is None or size < 0:
      it = iter(self.ios)
      for r in it:
        data = r.read()
        break
      else: return data
      for r in it: data += r.read()
      return data
    if size == 0:
      for r in self.ios: return r.read(0)
      raise RuntimeError("unexpected error")
    it = iter(self.ios)
    for r in it:
      data = r.read(size)
      l = len(data)
      if l >= size: return data
      break
    for r in it:
      data += r.read(size - l)
      l = len(data)
      if l >= size: return data
    return data

  def read1(self, size=-1):
    self._checkClosed()
    def read1(r, *a): return (getattr(r, "read1") or r.read)(*a)
    if size is None or size < 0:
      for r in self.ios:
        data = read1(r)
        if data: return data
      return data
    if size == 0:
      for r in self.ios: return read1(r, 0)
      raise RuntimeError("unexpected error")
    for r in self.ios:
      data = read1(r, size)
      if data: return data
    return data

  def readinto(self, b):
    # XXX really not optimized…
    d = self.read(len(b))
    l = len(d)
    b[:l] = d
    return l

  def readall(self):
    r, c = b"", self.read()
    while c: r, c = r + c, self.read()
    return r

io_chain._required_globals = ["RawIOBase"]
