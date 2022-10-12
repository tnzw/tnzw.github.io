# PurePosixPath2.py Version 1.1.0
# Copyright (c) 2022 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class PurePosixPath2(tuple):
  '''\
PurePosixPath2(*pathsegments, **replacements)

Handles posix paths like pathlib.PurePosixPath does but with an extended api.

- PurePosixPath2.names                  → gets parts without anchor
- PurePosixPath2('hello') // 'world'    → PurePosixPath2('hello/world')
- PurePosixPath2('hello') // 'my/world' → raises ValueError
- PurePosixPath2('hello') + 'world'     → PurePosixPath2('helloworld')
- PurePosixPath2('hello/').extra        → '/'  XXX Not implemented yet

In addition to PurePath(), PurePosixPath2() handles bytes path.

You can convert from any PurePath-like by doing:

    >>> pp = PurePath(…)
    >>> PurePosixPath2(pp, anchor='/' if pp.is_absolute() else '')
'''
  # https://docs.python.org/3/library/pathlib.html
  # https://docs.python.org/3/reference/datamodel.html

  # (parts, root, stem, suffix, suffixes, extra) nb: drive and anchor are not necessary in PurePosixPath2 but could be necessary in PureWindowsPath2
  #   parts contains anchor if anchor is not empty
  #   eg '/hello/world' -> ('/', 'hello', 'world')
  #      'hello/world' -> ('hello', 'world')

  __slots__ = ()
  def __new__(cls, *pathsegments, **replacements):

    def isvaliddrive(drive):
      return drive in (None, '', b'')

    def isvalidroot(root):
      return root in ('', b'', '/', b'/', '//', b'//')

    def isroot(root):
      return root in ('/', b'/', '//', b'//')

    #def splitext(path):  # returns (path_without_suffix, suffix)
    #  # splitext('/..a') → ('/.', '.a') is legit
    #  if isinstance(path, bytes): _sep = b'/'; _dot = b'.'; _ddot = b'..'; _empty = b''
    #  else:                       _sep =  '/'; _dot =  '.'; _ddot =  '..'; _empty =  ''
    #  if path[-1:] == _dot: return (path, path[:0])  # splitext('/a.b.') → ('/a.b.', '')
    #  if path[-2:] == _ddot and path[-3:-2] in (_empty, _sep): return (path, path[:0])  # splitext('/..') → ('/..', '')
    #  i = len(path)
    #  while i > 0 and path[i-1:i] != _dot: i -= 1
    #  if i > 0 and path[i-1:i] == _dot: i -= 1
    #  if i == 0 or path[i-1:i] == _sep: return (path, path[:0])
    #  return (path[:i], path[i:])
    def name_splitext(name):  # returns (stem, suffix)
      # splitext('..a') → ('.', '.a') is legit
      if isinstance(name, bytes): _dot = b'.'; _ddot = b'..'
      else:                       _dot =  '.'; _ddot =  '..'
      if name[-1:] == _dot: return (name, name[:0])  # name_splitext('a.b.') → ('a.b.', '')
      if name == _ddot: return (name, name[:0])  # name_splitext('..') → ('..', '')
      i = len(name) - 1
      while i > 0 and name[i-1:i] != _dot: i -= 1
      if i > 0 and name[i-1:i] == _dot: i -= 1
      if i == 0: return (name, name[:0])
      return (name[:i], name[i:])
    def name_splitsuffixes(name):
      # unfortunately, pathlib.Pure{Posix,Windows}Path has inconsistent behavior on spliting name parts
      # → PurePosixPath('..a').stem → '.'
      # → PurePosixPath('..a').suffix → '.a'
      # → PurePosixPath('..a').suffixes → [] ???
      # so we use this method only for suffixes, not stem or suffix
      if not name: return [name]
      _dot = b'.' if isinstance(name, bytes) else '.'
      if name[-1:] == _dot: return [name]
      nameparts = []
      i = 0; l = len(name)
      while i < l and name[i:i+1] == _dot: i += 1
      #l = len(name); i = min(1, l)
      while i < l and name[i:i+1] != _dot: i += 1
      nameparts.append(name[:i])
      last = i
      while i < l:
        if              name[i:i+1] == _dot: i += 1
        while i < l and name[i:i+1] != _dot: i += 1
        nameparts.append(name[last:i])
        last = i
      return nameparts

    def check_name(name):  # PurePath().with_name() behavior
      if isinstance(name, bytes): _sep = b'/'; _dot = b'.'
      else:                       _sep =  '/'; _dot =  '.'
      # '\0' char is allowed in Pure{Posix,Windows}Path
      # XXX add a parameter to disallow special chars? or add a method ppp.has_reserved_char()?
      # None raises ValueError: Invalid name None
      if name and _sep not in name and name != _dot: return name
      raise ValueError(f'Invalid name {name!r}')
    def check_suffix(s):  # PurePath().with_suffix() behavior
      if isinstance(s, bytes): _sep = b'/'; _dot = b'.'
      else:                    _sep =  '/'; _dot =  '.'
      if s and s[:1] == _dot and s[1:] and _sep not in s[1:]: return s
      raise ValueError(f'Invalid suffix {s!r}')
    def check_suffixes(ss):
      si = iter(ss)
      for s in si:
        if isinstance(ss, bytes): _sep = b'/'; _dot = b'.'
        else:                     _sep =  '/'; _dot =  '.'
        for si in ((s,), si):
          for s in si:
            if s and s[:1] == _dot and _sep not in s[1:] and _dot not in s[1:]: yield s
            else: raise ValueError(f'Invalid suffix {s!r}')
        break

    def extract_purepath_parts(purepath, ex):
      try: drv = purepath.drive; rt = purepath.root; pts = purepath.parts
      except AttributeError: return False
      ex[:] = drv, rt, [*(pts[1:] if drv or rt else pts)]
      return True

    def from_fspath(fspath):
      if isinstance(fspath, bytes): root = empty = b''; sep = b'/'; dot = b'.'
      else:                         root = empty =  ''; sep =  '/'; dot =  '.'
      names = []
      if len(fspath):
        # parse root
        if fspath[:1] == sep:
          if fspath[1:2] == sep and (fspath[2:3] != sep or fspath[2:3] == empty): l = 2
          else: l = 1
          root = fspath[:l]
        else: l = 0
        # parse names
        i = fspath.find(sep, l)
        while i >= 0:
          name = fspath[l:i]
          if name and name != dot: names.append(name)  # normalises original path
          l = i + 1
          i = fspath.find(sep, l)
        name = fspath[l:]
        if name and name != dot: names.append(name)  # normalises original path
      return empty, root, names

    def parse(pathsegment):
      ex = []
      if type(pathsegment) == PurePosixPath2:
        return pathsegment.drive, pathsegment.root, list(pathsegment.names)
      elif isinstance(pathsegment, (str, bytes)):
        return from_fspath(pathsegment)
      elif extract_purepath_parts(pathsegment, ex):
        return ex
      elif hasattr(pathsegment, '__fspath__'):
        return from_fspath(pathsegment.__fspath__())
      else:
        raise ValueError('invalid path')

    final_check_anchor = final_check_names = False
    drive, root, names = None, None, []

    def make_emptyname_error(msg='has an empty name'):
      if isvalidroot(root): return ValueError(f'{cls(root=root)!r} {msg}')
      return ValueError(f'{cls.__name__}(root={root!r}) {msg}')

    if pathsegments:
      final_check_anchor = final_check_names = True
      drv, root, names = parse(pathsegments[0])
      if drv: drive = drv
      for _ in pathsegments[1:]:
        # joinpath()
        drv, rt, nn = parse(_)
        if drv: drive = drv; root = rt; names = nn
        if rt: root = rt; names = nn
        else: names.extend(nn)

    if replacements:
      if 'parsed_parts' in replacements:  # this is a bit like PurePath._from_parsed_parts, use at your own risk!
        parts = [*replacements.pop('parsed_parts')]
        if parts:
          if isroot(parts[0]): root = parts[0]; names = parts[1:]
          else: root = parts[0][:0]; names = parts
        else: root = None; names = []
      if replacements: final_check_anchor = final_check_names = True
      if 'parts' in replacements: # this is the default PurePath._from_parts behavior, use `names` to be more strict
        parts = [*replacements.pop('parts')]
        if parts:
          sep = b'/' if isinstance(parts[0], bytes) else '/'
          if isroot(parts[0]):
            drive, root, names = from_fspath(parts[0] + sep.join(_ for _ in parts[1:] if _))
          else:
            drive, root, names = from_fspath(sep.join(_ for _ in parts if _))
        else: root = None; names = []
      if 'parent' in replacements:
        if not names: raise make_emptyname_error()
        drv, root, nn = parse(replacements.pop('parent'))
        if drv: drive = drv
        names = [*nn, names[-1]]
      if 'anchor' in replacements:
        drive = None
        root = replacements.pop('anchor')
        #if not isvalidroot(root): raise ValueError(f'Invalid anchor {root!r}')
      if 'drive' in replacements:
        drive = replacements.pop('drive')
        #if drive not in ('', b''): raise ValueError(f'Invalid drive {drive!r}')
      if 'root' in replacements:
        root = replacements.pop('root')
        #if not isvalidroot(root): raise ValueError(f'Invalid root {root!r}')
      if 'names' in replacements:
        names = [*replacements.pop('names')]
        for _ in names: check_name(_)
        final_check_names = False
      if 'name' in replacements:
        if not names: raise make_emptyname_error()
        names[-1] = check_name(replacements.pop('name'))
      if 'stem' in replacements:
        if not names: raise make_emptyname_error()
        stem = check_name(replacements.pop('stem'))
        _, suffix = name_splitext(names[-1])
        names[-1] = stem + suffix
        #j = b'' if isinstance(stem, bytes) else ''
        #names[-1] = stem + j.join(name_splitsuffixes(names[-1])[-1:])
      if 'suffixes' in replacements:
        if not names: raise make_emptyname_error()
        suffixes = (*check_suffixes(replacements.pop('suffixes')),)
        if suffixes:
          j = suffixes[0][:0]
          names[-1] = j.join(_ for i in (name_splitsuffixes(names[-1])[:1], suffixes) for _ in i)
        else:
          names[-1] = name_splitsuffixes(names[-1])[0]
      if 'suffix' in replacements:
        if not names: raise make_emptyname_error()
        suffix = replacements.pop('suffix')
        stem, _ = name_splitext(names[-1])
        if suffix: names[-1] = stem + check_suffix(suffix)
        else: names[-1] = stem
      if replacements:
        raise TypeError(f'PurePosixPath2() unhandled keyword parameters: {", ".join(str(_) for _ in replacements)}')

    if root is None: root = names[0][:0] if names else (drive[:0] if drive is not None else '')
    if final_check_anchor:
      if not isvaliddrive(drive): raise ValueError(f'invalid drive {drive!r}')
      if not isvalidroot(root): raise ValueError(f'invalid root {root!r}')
    if final_check_names:
      for _ in names: check_name(_)
    if names:
      _, *suffixes = name_splitsuffixes(names[-1])
      stem, suffix = name_splitext(names[-1])
    else:
      stem = suffix = root[:0]; suffixes = ()
    if root: names.insert(0, root)
    po = tuple.__new__(cls, (tuple(names), root, stem, suffix, tuple(suffixes)))
    po.__fspath__()  # check part types
    return po

  @property
  def drive(self): return self.root[:0]
  @property
  def root(self): return tuple.__getitem__(self, 1)
  @property
  def anchor(self): return self.root
  @property
  def parents(self):  # pathlib.PurePath returns <PurePath.parents> object
    parts = self.parts
    ani = 0 if self.anchor else 1
    return (*(PurePosixPath2(parsed_parts=parts[:i]) for i in range(1 - ani, len(parts))),)[::-1]
  @property
  def parent(self):
    pts = self.parts
    i = None if self.anchor and len(pts) == 1 else -1
    return PurePosixPath2(parsed_parts=pts[:i])
  @property
  def parts(self): return tuple.__getitem__(self, 0)
  @property
  def name(self): return self.names[-1] if self.names else self.root[:0]
  @property
  def suffix(self): return tuple.__getitem__(self, 3)
  @property
  def suffixes(self): return tuple.__getitem__(self, 4)
  @property
  def stem(self): return tuple.__getitem__(self, 2)
  @property
  def _parts(self): return [*self.parts]  # in PurePosixPath, it is a cached property, but here PurePosixPath2 is frozen/stateless
  @property
  def _cparts(self): return [*self.parts]  # in PurePosixPath, it is a cached property, but here PurePosixPath2 is frozen/stateless
  def __repr__(self): return f'{self.__class__.__name__}({self.__fspath__()!r})'
  def __fspath__(self): return self.anchor + self.sep.join(self.names) or self.curdir
  def __hash__(self): return self.parts.__hash__()  # pathlib.PurePath behavior
  #def __eq__(self): use default behavior (not exactly like pathlib.PurePath behavior)
  #def __ge__(self):
  #def __gt__(self):
  #def __le__(self):
  #def __lt__(self):
  #def __ne__(self):
  def __truediv__(self, other): return PurePosixPath2(self, other)
  def __rtruediv__(self, other): return PurePosixPath2(other, self)
  def as_posix(self): return self.__fspath__()
  def as_uri(self):
    p = self.__fspath__()
    if p[:1] not in ('/', b'/'):
      raise ValueError("relative path can't be expressed as a file URI")
    if isinstance(p, bytes): return b'file://' + p
    return 'file://' + p
  def is_absolute(self): return True if self.root else False
  def is_relative_to(self, other): return self.relative_to(other, _bool=True)
  def is_reserved(self): return False
  def joinpath(self, *other): return PurePosixPath2(self, *other)
  #XXX def match
  def relative_to(self, other, *, _bool=False):
    def checktypes(a, b):
      ta, tb = type(a), type(b)
      if ta != tb: raise TypeError(f'cannot compare {ta.__name__} with {tb.__name__}')
    other = PurePosixPath2(other)
    srt, ort = self.anchor, other.anchor
    checktypes(srt, ort)
    if srt == ort:
      i = 1 if srt else 0
      p1, p2 = self.parts, other.parts
      ip1, ip2 = iter(p1[i:]), iter(p2[i:])
      for n1, n2 in zip(ip1, ip2):
        if n1 != n2: break  # names differs, so other is not a subpath of self
        else: i += 1
      else:
        for _ in ip2: break  # end of self reached, but other still has names, so other is not a subpath of self
        else: return True if _bool else PurePosixPath2(root=srt[:0], parsed_parts=p1[i:])  # root=… is to keep fspath type when parsed_parts is empty
    if _bool: return False
    raise ValueError(f'{self.__fspath__()!r} is not in the subpath of {other.__fspath__()!r} OR one path is relative and the other is absolute.')  # yes, this is the true PurePath error behavior
  def with_name(self, name): return PurePosixPath2(self, name=name)
  def with_stem(self, stem): return PurePosixPath2(self, stem=stem)
  def with_suffix(self, suffix): return PurePosixPath2(self, suffix=suffix)

  # non PurePath API
  @property
  def names(self): return self.parts[1:] if self.anchor else self.parts
  @property
  def sep(self): return b'/' if isinstance(self.root, bytes) else '/'
  @property
  def altsep(self): return None
  @property
  def curdir(self): return b'.' if isinstance(self.root, bytes) else '.'
  @property
  def pardir(self): return b'..' if isinstance(self.root, bytes) else '..'
  @property
  def extsep(self): return b'.' if isinstance(self.root, bytes) else '.'
  def __add__(self, other):
    if hasattr(other, '__fspath__'): other = other.__fspath__()
    return PurePosixPath2(self.__fspath__() + other)
  def __floordiv__(self, other): return PurePosixPath2(anchor=self.anchor, names=[*self.names, other])
  def __rfloordiv__(self, other): raise ValueError('PurePosixPath2() cannot append name from tail')
  def _replace(self, **replacements): return PurePosixPath2(self, **replacements)
