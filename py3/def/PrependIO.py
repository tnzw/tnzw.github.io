# PrependIO.py Version 1.1.1
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class PrependIO(tuple):
  """\
PrependIO(io)

pio = PrependIO(io.BytesIO(b"abc"))
pio.prepend(b"def")
pio.read() → b"defabc"

/!\\ CAUTION
The use of writable and seekable methods may lead to inconsistencies.
"""

  def __new__(cls, io, lwriter=None): return tuple.__new__(cls, (io, PipeIO() if lwriter is None else lwriter))
  def __repr__(self): return f"{self.__class__.__name__}({self.io!r}, {self.lwriter!r})"

  @property
  def io(self): return super().__getitem__(0)
  @property
  def lwriter(self): return super().__getitem__(1)

  # io.IOBase
  #   mixins ["close", "closed", "__enter__", "__exit__", "flush", "isatty",
  #           "__iter__", "__next__", "readable", "readline", "readlines",
  #           "seekable", "tell", "writable", "writelines"]
  #   stubs  ["fileno", "seek", "truncate"]

  for _ in ("close", "closed", "__enter__", "__exit__", "flush", "isatty",
            "readable",
            "seekable", "tell", "writable", "writelines",
            "fileno", "seek", "truncate",
            "write"):
    exec(f"@property\ndef {_}(self): return self.io.{_}", {}, locals())
  del _
  for _ in ("__iter__", "__next__", "readline", "readlines"):
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

  def read1(self, size=-1):
    def read1(r, *s):
      if hasattr(r, "read1"): return r.read1(*s)
      if s: return r.read(*s)
      return r.read(DEFAULT_BUFFER_SIZE)
    if size is None or size < 0: size = ()
    else: size = (size,)
    data = read1(self.lwriter, *size)
    if data: return data
    return read1(self.io, *size)

  def read(self, size=-1):
    if size is None or size < 0: return self.readall()
    if size == 0: return self.lwriter.read(0)
    data = self.lwriter.read(size)
    l = len(data)
    if l < size: data += self.io.read(size - l)
    return data

  def readall(self):
    data = self.lwriter.read()
    data += self.io.read()
    return data

  def prepend(self, b): return self.lwriter.lwrite(b)

  def prependable(self): return True

PrependIO._required_globals = ["PipeIO", "RawIOBase", "DEFAULT_BUFFER_SIZE"]
