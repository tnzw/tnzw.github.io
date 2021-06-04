# tuplepath.py Version 1.2.3
# Copyright (c) 2020-2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class tuplepath(tuple):
  # https://docs.python.org/fr/3/library/os.path.html
  # https://docs.python.org/3/reference/datamodel.html

  def __new__(cls, path="", os_module=None):
    if os_module is None: os_module = os
    if hasattr(path, "__fstuple__"):
      t = path.__fstuple__()
      if not isinstance(t, tuple): raise TypeError("__fstuple__ returned non-tuple (type " + type(t).__name__ + ")")
      return tuple.__new__(cls, (t, os_module))
    if isinstance(path, tuple): return tuple.__new__(cls, (path, os_module))
    if isinstance(path, list): return tuple.__new__(cls, (tuple(path), os_module))
    path = os_module.fspath(path)
    split = os_module.path.split
    prevsplit = split(path)
    path = ()
    nextsplit = split(prevsplit[0])
    while prevsplit != nextsplit:
      path = prevsplit[1:2] + path
      prevsplit, nextsplit = nextsplit, split(nextsplit[0])
    path = prevsplit[:1] + path
    return tuple.__new__(cls, (path, os_module))

  def __repr__(self):
    repr_os = "" if self.os is os else f", os_module={self.os!r}"
    return self.__class__.__name__ + f"({self.tuple!r}{repr_os})"

  def __str__(self): return str(self.pathname)

  def __bytes__(self): return self.pathname if isinstance(self.rootname, bytes) else self.fsencode().pathname

  def __eq__(self, path): return self.tuple == self._new(path).tuple

  def __bool__(self):
    if self.tuple[2:3]: return True
    for _ in self.tuple:
      if _: return True
    return False

  def __len__(self): return len(self.names) if self else 0

  def __getitem__(self, key):
    # there is no sens to use self.tuple[key]
    # because `len(self[1:])` would be equal to `len(self)`.
    if isinstance(key, slice):
      if key.start in (0, None) or key.start <= -len(self): return self._new((self.rootname,) + self.names[key])
      return self._new((self.emptyname,) + self.names[key])
    l = -len(self)
    if l == 0: raise IndexError("index out of range")
    if key in (0, None, l): return self[:1].pathname
    return self.names[key]

  def __iter__(self): return iter((self[0],) + self.names[1:])

  def __add__(self, other): return self.append(other)

  def __radd__(self, other): return self._new(other) + self

  def __fspath__(self): return self.pathname

  def __fstuple__(self): return self.tuple

  def _new(self, path=""): return self.__class__(path, os_module=self.os)

  for _ in "sep altsep curdir pardir pathsep extsep".split():
    exec(f"""@property\ndef {_}(self):\n os = self.os\n p = os.path.{_}\n if p is None: return p\n if isinstance(self.rootname, bytes): return os.fsencode(p)\n return p\n""", globals(), locals())
  del _

  @property
  def tuple(self): return tuple.__getitem__(self, 0)
  @property
  def os(self): return tuple.__getitem__(self, 1)
  @property
  def names(self): return self.tuple[1:]

  @property
  def drivename(self): return self.splitdrive()[0]
  @property
  def rootname(self): return self.tuple[0] if self.tuple else ""
  @property
  def pathname(self): return self.rootname + self.sep.join(self.normtype().names)
  @property
  def dirname(self): return self.dir().pathname
  @property
  def basename(self): return self.names[-1] if self.names else self.emptyname
  @property
  def extname(self): return self.splitext()[1]
  @property
  def emptyname(self): return self.rootname[:0]

  def root(self, newroot=None):
    if newroot is None: return self._new((self.rootname,))
    return self._new((newroot,) + self.names)  # kind of confusing ?
  def dir(self): return self._new((self.rootname,) + self.names[:-1])
  def base(self): return self._new((self.emptyname,) + self.names[-1:])
  def ext(self):
    e = self.extname
    if e: return self._new((self.emptyname,) + (e,))
    return self.empty()
  def drive(self): return self._new((self.drivename,))
  def empty(self): return self._new((self.emptyname,))

  def append(self, path, *paths):
    # kind of act like str/bytes __add__ -> tuplepath("C:/a") + "D:/b" -> "C:/aD:/b"
    # use join for such a result -> tuplepath("C:/a").join("D:/b") -> "D:/b"
    dec = self.os
    dec, enc = dec.fsdecode, dec.fsencode
    fs = None
    for path in (path,) + paths:
      path = self._new(path)
      if not self:
        self = path
        continue
      if fs is None: fs = dec if isinstance(self.sep, str) else enc
      psep, paltsep = fs(path.sep), path.altsep and fs(path.altsep)
      prootname, pnames = fs(path.rootname), path.names
      if pnames:
        _, pnames = pnames[0], pnames[1:]
        prootname += fs(_)
      if paltsep: prootname = prootname.replace(paltsep, psep)
      ssep, saltsep = self.sep, self.altsep
      names = self.names
      if psep != ssep:
        prootname = prootname.replace(psep, ssep)
      if names:
        _, names = names[-1], names[:-1]
        prootname = fs(_) + prootname
      if saltsep: prootname = prootname.replace(saltsep, ssep)
      prootname = tuple(prootname.split(ssep)) if prootname else ()
      self = self._new((self.rootname,) + names + prootname + pnames)

      # The algo below is really not fast due to serialisation + parsing
      #if isinstance(self.rootname, bytes):
      #  path = self.os.fsencode(path)
      #  return self._new(self.pathname + path)
      #path = self.os.fsdecode(path)
      #return self._new(self.pathname + path)
    return self

  def commonpath(self, paths):
    # it normaly raises when types are mixed : TypeError: Can't mix strings and bytes in path component
    common_tuple = ()
    paths = tuple(self._new(_).tuple for _ in paths)
    for _ in zip(*(self.tuple,) + paths):
      for i in range(len(_) - 1):
        if _[i] != _[i + 1]: break
      else:
        common_tuple = common_tuple + (_[0],)
        continue
      break
    if common_tuple: return self._new(common_tuple)
    raise ValueError("Can't mix absolute and relative paths or paths don't have the same drive")

  def extend(self, path, *paths):
    # kind of act like str/bytes __add__ with additional separator -> tuplepath("C:/a").extend("D:/b") -> "C:/a/D:/b"
    # tuplepath("C:/a/").extend("D:/b" ) -> "C:/a/D:/b"
    # tuplepath("C:/a" ).extend("/D:/b") -> "C:/a/D:/b"
    # tuplepath("C:/a/").extend("/D:/b") -> "C:/a/D:/b"
    # use join for such a result -> tuplepath("C:/a").join("D:/b") -> "D:/b"
    dec = self.os
    dec, enc = dec.fsdecode, dec.fsencode
    fs = None
    for path in (path,) + paths:
      path = self._new(path)
      if not self:
        self = path
        continue
      if fs is None: fs = dec if isinstance(self.sep, str) else enc
      psep, paltsep = fs(path.sep), path.altsep and fs(path.altsep)
      prootname, pnames = fs(path.rootname), path.names
      if prootname[:1] in (psep, paltsep): prootname = prootname[1:]
      if pnames:
        _, pnames = pnames[0], pnames[1:]
        prootname += fs(_)
      if paltsep: prootname = prootname.replace(paltsep, psep)
      prootname = tuple(prootname.split(psep)) if prootname else ()
      stuple = self.tuple
      if stuple[1:] and not stuple[-1]: stuple = stuple[:-1]
      self = self._new(stuple + prootname + pnames)
    return self

  def fsdecode(self):
    a = self.os.fsdecode
    return self._new(tuple(a(_) for _ in self.tuple) or ("",))

  def fsencode(self):
    a = self.os.fsencode
    return self._new(tuple(a(_) for _ in self.tuple) or (b"",))

  def isabs(self): return True if self.rootname else False

  def join(self, path, *paths):
    new = self.tuple
    for path in (path,) + paths:
      for i in range(len(new) - 1, 0, -1):
        if not new[i]: new = new[:-1]
      path = self._new(path)
      if path.isabs(): new = path.tuple
      else: new = new + path.names
    return self._new(new)

  def norm(self):
    # try to act like self._new(self.os.path.normpath(self.pathname))
    # but avoid stringifying and parsing.
    self = self.normtype()
    rootname = self.rootname
    normpath = self.os.path.normpath
    altsep, sep = self.altsep, self.sep
    if normpath: rootname = normpath(rootname)
    elif altsep: rootname = rootname.replace(altsep, sep)
    names = ()
    for name in self.names:
      if not name or name in (".", b".", "", b""): pass
      elif name in ("..", b".."):
        if not rootname and (names and names in (("..",), (b"..",)) or not names): names = names + (name,)
        else: names = names[:-1]
      else:
        if altsep: name = name.replace(altsep, sep)
        names = names + tuple(name.split(sep))
    return self._new((rootname,) + names)

  normpath = norm

  def normtype(self):
    if isinstance(self.rootname, bytes): return self.fsencode()
    return self.fsdecode()

  def sibling(self, path, *paths): return self.dir().join(path, *paths)

  def split(self): return self.dir(), self.basename

  def splitall(self): return self.tuple

  def splitdrive(self):
    drive, rootname = self.os.path.splitdrive(self.rootname)
    return drive, self.root(rootname)  # this might be changed to relative path, as original os.path.splidrive can do

  def splitext(self):
    basename = self.basename
    l = -1
    for i,c in enumerate(basename):
      if c in (".", b".", 0x2e): l = i
    if l <= 0: return basename, basename[:0]
    return basename[:i], basename[i:]

tuplepath._required_globals = ["os"]
