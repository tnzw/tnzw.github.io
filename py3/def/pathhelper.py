# pathhelper.py Version 1.1.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class pathhelper(tuple):
  # https://docs.python.org/fr/3/library/os.path.html
  # https://docs.python.org/3/reference/datamodel.html

  def __new__(cls, path="", os_module=None):
    if os_module is None: os_module = os
    return tuple.__new__(cls, (os_module.fspath(path), os_module))

  def __repr__(self):
    repr_os = "os" if self.os is os else repr(self.os)
    return self.__class__.__name__ + f"({self.pathname!r}, os_module={repr_os})"

  def __str__(self): return str(self.pathname)

  def __bytes__(self): return self.pathname if isinstance(self.pathname, bytes) else self.fsencode().pathname

  def __eq__(self, path): return self.pathname == (path.pathname if isinstance(path, self.__class__) else path)

  def __bool__(self): return True if self.pathname else False

  def __len__(self): return len(self.pathname)

  def __getitem__(self, key): return self.pathname[key]

  def __iter__(self): return iter(self.pathname)

  def __add__(self, other): return self.append(other)

  def __radd__(self, other): return self._new(other) + self

  def __fspath__(self): return self.pathname

  def _new(self, path=""): return self.__class__(path, os_module=self.os)

  for _ in "sep altsep curdir pardir pathsep extsep".split(): exec(f"""@property\ndef {_}(self):\n os = self.os\n p = os.path.{_}\n if p is None: return p\n if isinstance(self.pathname, bytes): return os.fsencode(p)\n return p\n""", globals(), locals())
  for _ in "isabs".split(): exec(f"""def {_}(self, *a, **k):\n return self.os.path.{_}(self.pathname, *a, **k)\n""", globals(), locals())
  #for _ in "basename dirname".split(): exec(f"""@property\ndef {_}(self):\n return self._new(self.os.path.{_}(self.pathname))\n""", globals(), locals())
  for _ in "basename dirname".split(): exec(f"""@property\ndef {_}(self):\n return self.os.path.{_}(self.pathname)\n""", globals(), locals())
  for _ in "normcase normpath join".split(): exec(f"""def {_}(self, *a, **k):\n return self._new(self.os.path.{_}(self.pathname, *a, **k))\n""", globals(), locals())
  for _ in "split splitext".split(): exec(f"""def {_}(self, *a, **k):\n _ = self.os.path.{_}(self.pathname, *a, **k)\n return self._new(_[0]), _[1]\n""", globals(), locals())
  for _ in "splitdrive".split(): exec(f"""def {_}(self, *a, **k):\n _ = self.os.path.{_}(self.pathname, *a, **k)\n return _[0], self._new(_[1])\n""", globals(), locals())
  #for _ in "split splitdrive splitext".split(): exec(f"""def {_}(self, *a, **k):\n return self.os.path.{_}(self.pathname, *a, **k)\n""", globals(), locals())
  def commonpath(self, paths): return self.os.path.commonpath((self.pathname, *paths))

  for _ in "fsdecode fsencode".split(): exec(f"""def {_}(self, *a, **k):\n return self._new(self.os.{_}(self.pathname, *a, **k))\n""", globals(), locals())
  for _ in "chmod chown stat lchmod lchown lstat utime truncate".split(): exec(f"""def {_}(self, *a, **k):\n return self.os.{_}(self.pathname, *a, **k)\n""", globals(), locals())
  del _

  @property
  def os(self): return tuple.__getitem__(self, 1)

  @property
  def drivename(self): return self.splitdrive()[0]
  @property
  def rootname(self):
    dirname = self.os.path.dirname
    ssep, saltsep = self.sep, self.altsep
    p = self.pathname
    l = len(p)
    i,j = 0,0
    for i in range(0, l):
      if p[i:i+1] in (ssep, saltsep): break
      j=i
    for i in range(j, l):
      if p[i:i+1] not in (ssep, saltsep): break
    p = p[:i]
    # `p` is now reduce to limit the number of `dirname` call.
    n = dirname(p)
    while p != n: p, n = n, dirname(p)
    return p
  @property
  def pathname(self): return tuple.__getitem__(self, 0)
  @property
  def extname(self): return self.splitext()[1]
  @property
  def emptyname(self): return self.pathname[:0]

  def root(self, newroot=None):
    if newroot is None: return self._new(self.rootname)
    return self._new(newroot).append(self.pathname[len(self.rootname):])  # kind of confusing ?
  def dir(self): return self._new(self.dirname)
  def base(self): return self._new(self.basename)
  def ext(self):
    e = self.extname
    if e: return self._new(e)
    return self.empty()
  def drive(self): return self._new(self.drivename)
  def empty(self): return self._new(self.emptyname)

  def append(self, path, *paths):
    # kind of act like str/bytes __add__ -> tuplepath("C:/a") + "D:/b" -> "C:/aD:/b"
    # use join for such a result -> tuplepath("C:/a").join("D:/b") -> "D:/b"
    dec = self.os
    dec, enc = dec.fsdecode, dec.fsencode
    for path in (path,) + paths:
      pathname = self.pathname
      pathname += enc(path) if isinstance(pathname, bytes) else dec(path)
      self = self._new(pathname)
    return self

  def extend(self, path, *paths):
    # kind of act like str/bytes __add__ with additional separator -> tuplepath("C:/a").extend("D:/b") -> "C:/a/D:/b"
    # tuplepath("C:/a/").extend("D:/b" ) -> "C:/a/D:/b"
    # tuplepath("C:/a" ).extend("/D:/b") -> "C:/a/D:/b"
    # tuplepath("C:/a/").extend("/D:/b") -> "C:/a/D:/b"
    # use join for such a result -> tuplepath("C:/a").join("D:/b") -> "D:/b"
    dec = self.os
    dec, enc = dec.fsdecode, dec.fsencode
    ssep, saltsep = self.sep, self.altsep
    for path in (path,) + paths:
      pathname = self.pathname
      if not pathname:
        self = self._new(path)
        continue
      path = enc(path) if isinstance(pathname, bytes) else dec(path)
      if not path: continue
      if path[:1] in (ssep, saltsep): path = path[1:]
      if pathname[-1:] in (ssep, saltsep) or self.rootname == pathname: pathname += path
      else: pathname += ssep + path
      self = self._new(pathname)
    return self

  norm = normpath

  def sibling(self, path, *paths): return self.dir().join(path, *paths)

  def splitall(self):
    split = self.os.path.split
    p = split(self.pathname)
    s = ()
    n = split(p[0])
    while p != n:
      s = p[1:2] + s
      p, n = n, split(n[0])
    s = p[:1] + s
    return s

pathhelper._required_globals = ["os", "os_path_split"]
