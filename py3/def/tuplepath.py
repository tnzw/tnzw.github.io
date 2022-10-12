# tuplepath.py Version 2.1.2
# Copyright (c) 2020-2022 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class tuplepath(tuple):
  """\
tuplepath(fspath, **opt)

opt
  (keyword arguments are operated in this order)
  os_module: the module to use for `fspath()`, `fsdecode()`, `fsencode()` and
             `path`.
  path : parse the path to set the tuplepath pathname.
  root : sets the rootname.
  drive: sets the drivename.
  names: sets all the names composing the tuplepath.
  dir  : sets all the names composing the tuplepath before the basename.
  base : sets the basename.
  ext  : sets the extension.

Enhance an fspath to have better control over elements that compose the path
such as the names between separators, the root name or the extension, etc.
`tuplepath` is an immutable PathLike object.

A `tuplepath` contains all shortcuts method that exists in `os.path` to
manipulate and return modified version of the path, such as `join()`. Same
for `path` properties and `os` `fsencode()` and `fsdecode()`.

You can replace elements of a `tuplepath` by calling its `replace()` method.
The keywords arguments are the same as in the constructor (see above).

You can compare to pathes by using `==`, it compares rootnames and names even
on different representation of the path. Exemple on windows :

    >>> tuplepath("a\\b\\c") == tuplepath("a/b/c")
    True

You can iter through the path components:

    >>> print(" / ".join(tuplepath("/a/b/c")))
    /a / b / c

Or get the names directly:

    >>> tuplepath("/a/b/c")[0]
    "/a"
    >>> tuplepath("/a/b/c")[1]
    "b"
    >>> tuplepath("/a/b/c")[:2]
    "/a/b"
    >>> tuplepath("/a/b/c")[1:]
    "b/c"
    >>> tuplepath("/a/b/c").names
    ('a', 'b', 'c')
"""
  __slots__ = ()
  # ((rootname, *names), os_module)
  # https://docs.python.org/3/library/os.path.html
  # https://docs.python.org/3/reference/datamodel.html

  @classmethod
  def fromrootnames(cls, *rootnames, os_module=None):
    "fromrootnames(*fstuple)"
    if rootnames: return cls(root=rootnames[0], names=rootnames[1:], os_module=os_module)
    return cls(os_module=os_module)

  def __new__(cls, *a, **opt):
    if a[1:]: raise TypeError(f"tuplepath() takes 1 positional argument but {len(a)} were given")
    if a:
      if "path" in opt: raise TypeError(f"tuplepath() got multiple values for argument 'path'")
      opt["path"] = a[0]
    fslist = []
    os_module = None
    if "os" in opt: os_module = opt.pop("os")
    elif "os_module" in opt: os_module = opt.pop("os_module")
    _os = os if os_module is None else os_module
    def fspath_to_fstuple(path):
      split = _os.path.split
      prevsplit = split(path)
      path = ()
      nextsplit = split(prevsplit[0])
      while prevsplit != nextsplit:
        path = prevsplit[1:2] + path
        prevsplit, nextsplit = nextsplit, split(nextsplit[0])
      return prevsplit[:1] + path
    def fstuple(o):
      t = o.__fstuple__()
      if type(t) is not tuple: raise TypeError(f"__fstuple__ returned non-tuple (type {type(t).__name__!r})")
      return t
    if "path" in opt:
      path = opt.pop("path")
      if hasattr(path, "__fstuple__"): fslist = list(_os.fspath(_) for _ in fstuple(path))
      else: fslist = list(fspath_to_fstuple(_os.fspath(path)))
    if "root" in opt:
      root = _os.fspath(opt.pop("root"))
      if not fslist: fslist = [root]
      else: fslist[0] = root
    if "drive" in opt:
      drive = _os.fspath(opt.pop("drive"))
      if fslist and fslist[0]:
        _, root = _os.path.splitdrive(fslist[0])
        fslist[0] = drive + root  # this may raise TypeError: can't concat str to bytes, I'm ok with it
      #else: raise ValueError("cannot change drive of relative path")  # fail silently
    if "names" in opt:
      names = list(_os.fspath(_) for _ in opt.pop("names"))
      if names:
        if fslist: fslist = fslist[:1] + names
        else: fslist = [names[0][:0]] + names
      else:
        fslist = fslist[:1]
    if "dir" in opt:
      dir = opt.pop("dir")
      if hasattr(dir, "__fstuple__"): dir = list(_os.fspath(_) for _ in fstuple(dir))
      else: dir = list(fspath_to_fstuple(_os.fspath(dir)))
      base = fslist[1:][-1:] or ([dir[0][:0]] if dir else [""])
      fslist = dir + base
    if "base" in opt:
      base = _os.fspath(opt.pop("base"))
      if fslist:
        if fslist[1:]: fslist[-1] = base
        else: fslist.append(base)
      else:
        fslist.extend((base[:0], base))
    if "ext" in opt:
      ext = opt.pop("ext")
      if ext is not None: ext = _os.fspath(ext)
      if fslist and fslist[1:]:
        newbase, _ = _os.path.splitext(fslist[-1])
        if ext is None: fslist[-1] = newbase
        else: fslist[-1] = newbase + ext  # this may raise TypeError: can't concat str to bytes, I'm ok with it
    if opt: raise TypeError(f"replace() got an unexpected keyword argument {opt.popitem()[0]!r}")
    return tuple.__new__(cls, (tuple(fslist or ("",)), os_module))

  def __repr__(self):
    o = self._os
    repr_os = "" if o is None else f", os_module={o!r}"
    return f"{self.__class__.__name__}(root={self.rootname!r}, names={self.names!r}{repr_os})"

  def __str__(self): return str(self.pathname)

  def __bytes__(self): return self.pathname if isinstance(self.rootname, bytes) else self.fsencode().pathname

  def __eq__(self, path): return self.tuple == self.replace(path=path).tuple

  def __bool__(self):
    if self.tuple[2:3]: return True
    for _ in self.tuple:
      if _: return True
    return False

  # The code of __len__ __getitem__ and __iter__ could be confusing but is very useful.
  # To use len() normaly, better use len(my_tuplepath.pathnames) or len(my_tuplepath.names).
  # Same thing for __getitem__ and __iter__.

  def __len__(self): return len(self.names) if self else 0

  def __getitem__(self, key):
    # there is no sens to use self.tuple[key]
    # because `len(self[1:])` would be equal to `len(self)`.
    if isinstance(key, slice):
      if key.start in (0, None) or key.start <= -len(self): return self.replace(names=self.names[key])
      return self.replace(root=self.emptyname, names=self.names[key])
    l = -len(self)
    if l == 0: raise IndexError("index out of range")
    if key in (0, None, l): return self[:1].pathname
    return self.names[key]

  def __iter__(self): return iter((self[0],) + self.names[1:])

  def __add__(self, other): return self.append(other)

  def __radd__(self, other): return self.replace(path=other) + self

  def __fspath__(self): return self.pathname

  def __fstuple__(self): return self.tuple or ("",)

  for _ in "sep altsep curdir pardir pathsep extsep".split():
    exec(f"""@property\ndef {_}(self):\n os = self.os\n p = os.path.{_}\n if p is None: return p\n if isinstance(self.rootname, bytes): return os.fsencode(p)\n return p\n""", globals(), locals())
  del _

  @property
  def tuple(self): return tuple.__getitem__(self, 0)
  @property
  def _os(self): return tuple.__getitem__(self, 1)
  @property
  def names(self): return self.tuple[1:]
  @property
  def os(self):
    o = self._os
    if o is None: return os
    return o

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

  def root(self): return self.replace(names=())
  def dir(self): return self.replace(names=self.names[:-1])
  def base(self): return self.replace(root=self.emptyname, names=self.names[-1:])
  def ext(self):
    e = self.extname
    if e: return self.replace(root=self.emptyname, names=(e,))
    return self.empty()
  def drive(self): return self.replace(root=self.drivename, names=())
  def empty(self): return self.replace(root=self.emptyname, names=())

  def append(self, path, *paths):
    """\
Act like str/bytes __add__ -> tuplepath("C:/a") + "D:/b" -> "C:/aD:/b"
use join for such a result -> tuplepath("C:/a").join("D:/b") -> "D:/b"
"""
    dec = self.os
    dec, enc = dec.fsdecode, dec.fsencode
    fs = None
    for path in (path,) + paths:
      path = self.replace(path=path)
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
      self = self.replace(root=self.rootname, names=names + prootname + pnames)

      # The algo below is really not fast due to serialisation + parsing
      #if isinstance(self.rootname, bytes):
      #  path = self.os.fsencode(path)
      #  return self.replace(path=self.pathname + path)
      #path = self.os.fsdecode(path)
      #return self.replace(path=self.pathname + path)
    return self

  def commonpath(self, paths):
    # it normaly raises when types are mixed : TypeError: Can't mix strings and bytes in path component
    common_tuple = ()
    paths = tuple(self.replace(path=_).tuple for _ in paths)
    for _ in zip(*(self.tuple or ("",),) + paths):
      for i in range(len(_) - 1):
        if _[i] != _[i + 1]: break
      else:
        common_tuple = common_tuple + (_[0],)
        continue
      break
    if common_tuple: return self.replace(root=common_tuple[0], names=common_tuple[1:])
    raise ValueError("Can't mix absolute and relative paths or paths don't have the same drive")

  def extend(self, path, *paths):
    """\
Acts like str/bytes __add__ with additional separator -> tuplepath("C:/a").extend("D:/b") -> "C:/a/D:/b"
tuplepath("C:/a/").extend("D:/b" ) -> "C:/a/D:/b"
tuplepath("C:/a" ).extend("/D:/b") -> "C:/a/D:/b"
tuplepath("C:/a/").extend("/D:/b") -> "C:/a/D:/b"
use join for such a result -> tuplepath("C:/a").join("D:/b") -> "D:/b"
"""
    dec = self.os
    dec, enc = dec.fsdecode, dec.fsencode
    fs = None
    for path in (path,) + paths:
      path = self.replace(path=path)
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
      srootname, snames = self.rootname, self.names
      if snames and not snames[-1]: snames = snames[:-1]
      self = self.replace(root=srootname, names=snames + prootname + pnames)
    return self

  def fsdecode(self):
    a = self.os.fsdecode
    t = tuple(a(_) for _ in self.tuple) or ("",)
    return self.replace(root=t[0], names=t[1:])

  def fsencode(self):
    a = self.os.fsencode
    t = tuple(a(_) for _ in self.tuple) or (b"",)
    return self.replace(root=t[0], names=t[1:])

  def isabs(self): return True if self.rootname else False

  def join(self, path, *paths):
    sdrivename = self.drivename
    srootname, snames = self.rootname[len(sdrivename):], self.names
    for path in (path,) + paths:
      path = self.replace(path=path)
      if path.isabs():
        pdrivename = path.drivename
        if pdrivename:
          sdrivename = pdrivename
          srootname, snames = path.rootname[len(pdrivename):], path.names
        else:
          srootname, snames = path.rootname, path.names
      elif path.names:
        if snames and not snames[-1]: snames = snames[:-1] + path.names
        else: snames += path.names
    anchor = sdrivename + srootname if sdrivename else srootname
    return self.replace(root=anchor, names=snames)

  def norm(self):
    return self.replace(path=self.os.path.normpath(self))
    # Code below tries to act like self.replace(path=self.os.path.normpath(self.pathname))
    # but avoid stringifying and parsing.
    # However, we cannot guess what could be other `os` path normalization style.
    # So, we have to use self.os.normpath(self).
    #self = self.normtype()
    #rootname = self.rootname
    #normpath = self.os.path.normpath
    #altsep, sep = self.altsep, self.sep
    #if normpath: rootname = normpath(rootname)
    #elif altsep: rootname = rootname.replace(altsep, sep)
    #names = ()
    #for name in self.names:
    #  if not name or name in (".", b".", "", b""): pass  # use self.os.path.curdir?
    #  elif name in ("..", b".."):  # use self.os.path.pardir?
    #    if not rootname and (names and names in (("..",), (b"..",)) or not names): names = names + (name,)
    #    else: names = names[:-1]
    #  else:
    #    if altsep: name = name.replace(altsep, sep)
    #    names = names + tuple(name.split(sep))
    #return self.replace(root=rootname, names=names)

  def normcase(self):
    # self.replace(path=self.os.path.normcase(self)) could lead to inconsistencies ?
    return self.replace(root=self.os.path.normcase(self.rootname), names=(self.os.path.normcase(_) for _ in self.names))

  normpath = norm

  def normtype(self):
    if isinstance(self.rootname, bytes): return self.fsencode()
    return self.fsdecode()

  def replace(self, **opt):
    if "os_module" not in opt: opt["os_module"] = self._os
    if "path" not in opt: opt["path"] = self
    return tuplepath(**opt)

  def sibling(self, path, *paths): return self.dir().join(path, *paths)

  def split(self): return self.dir(), self.basename

  def splitall(self): return self.tuple or ("",)

  def splitdrive(self):
    drive, rootname = self.os.path.splitdrive(self.rootname)
    return drive, self.replace(root=rootname)  # this might be changed to relative path, as original os.path.splitdrive can do

  def splitext(self):
    newbase, ext = self.os.path.splitext(self.basename)
    return self.replace(base=newbase), ext
    # the extsep could be different than "."… so don't use code below
    #basename = self.basename
    #l = -1
    #for i,c in enumerate(basename):
    #  if c in (".", 0x2e, b"."): l = i
    #if l <= 0: return basename, basename[:0]
    #return basename[:l], basename[l:]

tuplepath._required_globals = ["os"]
