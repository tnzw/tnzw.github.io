# PureWindowsPath2.py Version 1.0.0
# Copyright (c) 2022 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class PureWindowsPath2(tuple):
  '''\
PureWindowsPath2(*pathsegments, **replacements)

Handles windows paths like pathlib.PureWindowsPath does but with an extended api.

- PureWindowsPath2.names                   → gets parts without anchor
- PureWindowsPath2('hello') // 'world'     → PureWindowsPath2('hello\\world')
- PureWindowsPath2('hello') // 'my\\world' → raises ValueError
- PureWindowsPath2('hello') + 'world'      → PureWindowsPath2('helloworld')
- PureWindowsPath2('hello\\').extra        → '\\'  XXX NIY

In addition to PurePath(), PureWindowsPath2() handles bytes path.

You can convert from any PurePath-like by doing:

    >>> pp = PurePath(…)
    >>> PureWindowsPath2(pp, anchor='C:\\' if pp.is_absolute() else '')
'''
  # https://docs.python.org/3/library/pathlib.html
  # https://docs.python.org/3/reference/datamodel.html

  # (parts, anchor, drive, root, stem, suffix, suffixes, extra)
  #   parts contains anchor if anchor is not empty
  #   eg 'C:\\hello\\world' -> ('C:\\', 'hello', 'world')
  #      '\\hello\\world' -> ('\\', 'hello', 'world')
  #      'hello\\world' -> ('hello', 'world')

  __slots__ = ()
  def __new__(cls, *pathsegments, **replacements):

    def find2(str, tuple, start=0):
      index = -1
      for t in tuple:
        i = str.find(t, start)
        if i != -1:
          if index == -1 or i < index: index = i
      return index

    letters  =  'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    lettersb = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    ###################
    # PATH ALGORITHMS #
    ###################

    ## ntpath.splitdrive('1:\\a') → ('1:', '\\a')
    ## ntpath.splitdrive('A:\\a') → ('A:', '\\a')
    #def _isletterlikedrive(drive, _colon): return drive[1:] == _colon
    #def _hasletterlikedrive(path, _colon): return path[1:2] == _colon
    # PureWindowsPath('1:\\a').drive → ''
    # PureWindowsPath('A:\\a').drive → 'A:'
    def _isletterdrive(drive, _letters, _colon): return drive[:1] in _letters and drive[1:] == _colon
    def _hasletterdrive(path, _letters, _colon): return path[:1] in _letters and path[1:2] == _colon
    def _splitletterdrive(path, _letters, _colon): return (path[:2], path[2:]) if _hasletterdrive(path, _letters, _colon) else (path[:0], path)
    def _isuncdrive(drive, _sep, _altsep):
      if drive[:1] in (_sep, _altsep) and drive[1:2] in (_sep, _altsep) and drive[2:3] not in (_sep, _altsep):
        index = find2(drive, (_sep, _altsep), 2)
        if index == -1: return False
        index2 = find2(drive, (_sep, _altsep), index + 1)
        if index2 == index + 1: return False
        if index2 == -1: return True
      return False
    #def _hasuncdrive(path, _sep, _altsep):
    #  if path[:1] in (_sep, _altsep) and path[1:2] in (_sep, _altsep) and path[2:3] not in (_sep, _altsep):
    #    index = find2(path, (_sep, _altsep), 2)
    #    if index == -1: return False
    #    if path[index + 1:index + 2] not in (_sep, _altsep): return True
    #  return False
    def _splituncdrive(path, _sep, _altsep, _empty):
      if path[:1] in (_sep, _altsep) and path[1:2] in (_sep, _altsep) and path[2:3] not in (_sep, _altsep):
        index = find2(path, (_sep, _altsep), 2)
        if index == -1: return (path[:0], path)
        # algo differs from _isuncdrive() to allow to reproduce pathlib.PureWindowsPath('//./') inconsistency
        if not path[index + 1:index + 2]: return (path[:index + 1], path[:0])
        if path[index + 1:index + 2] in (_sep, _altsep): return (path[:0], path)
        index2 = find2(path, (_sep, _altsep), index + 1)
        # what algo "should" be :
        #if path[index + 1:index + 2] in (_empty, _sep, _altsep): return (path[:0], path)
        #index2 = find2(path, (_sep, _altsep), index + 2)
        if index2 == -1: return (path, path[:0])
        return (path[:index2], path[index2:])
      return (path[:0], path)

    #def _isdrive(drive, _sep, _altsep, _letters, _colon):
    #  return True if _isletterdrive(drive, _letters, _colon) or _isuncdrive(drive, _sep, _altsep) else False
    #def _hasdrive(drive, _sep, _altsep, _letters, _colon):
    #  return True if _hasletterdrive(drive, _letters, _colon) or _hasuncdrive(drive, _sep, _altsep) else False
    def _splitdrive(path, _sep, _altsep, _empty, _letters, _colon):
      drive, path = _splitletterdrive(path, _letters, _colon)
      if drive: return drive, path
      return _splituncdrive(path, _sep, _altsep, _empty)
    def _isvalidroot(path, _sep, _altsep, _empty): return root in (_sep, _altsep, _empty)
    #def _isroot(path, _sep, _altsep): return root in (_sep, _altsep)

    ##############
    # PATH TOOLS #
    ##############

    def isanchor(anchor):
      if isinstance(anchor, bytes): _sep = b'\\'; _altsep = b'/'; _empty = b''; _letters = lettersb; _colon = b':'
      else:                         _sep =  '\\'; _altsep =  '/'; _empty =  ''; _letters = letters;  _colon =  ':'
      drive, root = _splitdrive(anchor, _sep, _altsep, _empty, _letters, _colon)
      return _isvalidroot(root, _sep, _altsep, _empty)
    def isvaliddrive(drive):
      if drive in ('', b''): return True
      if isinstance(drive, bytes): return _isletterdrive(drive, lettersb, b':') or _isuncdrive(drive, b'\\', b'/')
      else:                        return _isletterdrive(drive, letters ,  ':') or _isuncdrive(drive,  '\\',  '/')
    def splitdrive(path):
      if isinstance(path, bytes): return _splitdrive(path, b'\\', b'/', b'', lettersb, b':')
      else:                       return _splitdrive(path,  '\\',  '/',  '', letters ,  ':')
    def isvalidroot(root):
      return root in ('', b'', '\\', b'\\', '/', b'/')

    #def splitext(path):  # returns (path_without_suffix, suffix)
    #  # splitext('\\..a') → ('\\.', '.a') is legit
    #  if isinstance(path, bytes): _sep = b'\\'; _altsep = b'/'; _dot = b'.'; _ddot = b'..'; _empty = b''
    #  else:                       _sep =  '\\'; _altsep =  '/'; _dot =  '.'; _ddot =  '..'; _empty =  ''
    #  if path[-1:] == _dot: return (path, path[:0])  # splitext('\\a.b.') → ('\\a.b.', '')
    #  if path[-2:] == _ddot and path[-3:-2] in (_empty, _sep, _altsep): return (path, path[:0])  # splitext('\\..') → ('\\..', '')
    #  i = len(path)
    #  while i > 0 and path[i-1:i] != _dot: i -= 1
    #  if i > 0 and path[i-1:i] == _dot: i -= 1
    #  if i == 0 or path[i-1:i] in (_sep, _altsep): return (path, path[:0])
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
      if isinstance(name, bytes): _sep = b'\\'; _altsep = b'/'; _dot = b'.'; _letters = lettersb; _colon = b':'
      else:                       _sep =  '\\'; _altsep =  '/'; _dot =  '.'; _letters = letters ; _colon =  ':'
      # '\0' and special chars '\\/:*?"<>|' are allowed in Pure{Posix,Windows}Path
      # XXX add a parameter to disallow special chars? or add a method pwp.has_reserved_char()?
      # None raises ValueError: Invalid name None
      if name and _sep not in name and _altsep not in name and name != _dot and not _hasletterdrive(name, _letters, _colon): return name
      raise ValueError(f'Invalid name {name!r}')
    def check_suffix(s):  # PurePath().with_suffix() behavior
      if isinstance(s, bytes): _sep = b'\\'; _altsep = b'/'; _dot = b'.'
      else:                    _sep =  '\\'; _altsep =  '/'; _dot =  '.'
      if s and s[:1] == _dot and s[1:] and _sep not in s[1:] and _altsep not in s[1:]: return s
      raise ValueError(f'Invalid suffix {s!r}')
    def check_suffixes(ss):
      si = iter(ss)
      for s in si:
        if isinstance(ss, bytes): _sep = b'\\'; _altsep = b'/'; _dot = b'.'
        else:                     _sep =  '\\'; _altsep =  '/'; _dot =  '.'
        for si in ((s,), si):
          for s in si:
            if s and s[:1] == _dot and _sep not in s[1:] and _altsep not in s[1:] and _dot not in s[1:]: yield s
            else: raise ValueError(f'Invalid suffix {s!r}')
        break

    def extract_purepath_parts(purepath, ex):
      try: drv = purepath.drive; rt = purepath.root; pts = purepath.parts
      except AttributeError: return False
      ex[:] = drv, rt, [*(pts[1:] if drv or rt else pts)]
      return True

    def from_fspath(fspath):
      if isinstance(fspath, bytes): drive = root = _empty = b''; _sep = b'\\'; _altsep = b'/'; _dot = b'.'; _letters = lettersb; _colon = b':'
      else:                         drive = root = _empty =  ''; _sep =  '\\'; _altsep =  '/'; _dot =  '.'; _letters = letters ; _colon =  ':'
      names = []
      if len(fspath):
        # parse drive
        drive, fspath = _splitdrive(fspath, _sep, _altsep, _empty, _letters, _colon)
        # parse root
        if fspath[:1] in (_sep, _altsep): l = 1; root = fspath[:l]
        else: l = 0
        # parse names
        i = find2(fspath, (_sep, _altsep), l)
        while i >= 0:
          name = fspath[l:i]
          if name and name != _dot: names.append(name)  # normalises original path
          l = i + 1
          i = find2(fspath, (_sep, _altsep), l)
        name = fspath[l:]
        if name and name != _dot: names.append(name)  # normalises original path
      return drive, root, names

    def parse(pathsegment):
      ex = []
      if type(pathsegment) == PureWindowsPath2:
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
          drive, root = splitdrive(parts[0])
          if isvalidroot(root): names = parts[1:]
          else: drive = None; root = parts[0][:0]; names = parts
        else: drive = root = None; names = []
      if replacements: final_check_anchor = final_check_names = True
      if 'parts' in replacements: # this is the default PurePath._from_parts behavior, use `names` to be more strict
        parts = [*replacements.pop('parts')]
        if parts:
          sep = b'\\' if isinstance(parts[0], bytes) else '\\'
          if isanchor(parts[0]):
            drive, root, names = from_fspath(parts[0] + sep.join(_ for _ in parts[1:] if _))
          else:
            drive, root, names = from_fspath(sep.join(_ for _ in parts if _))
        else: drive = root = None; names = []
      if 'parent' in replacements:
        if not names: raise make_emptyname_error()
        drv, root, nn = parse(replacements.pop('parent'))
        if drv: drive = drv
        names = [*nn, names[-1]]
      if 'anchor' in replacements:
        drive, root = splitdrive(replacements.pop('anchor'))
        #if not isanchor(drive + root): raise ValueError(f'Invalid anchor {anchor!r}')
      if 'drive' in replacements:
        drive = replacements.pop('drive')
        #if not isvaliddrive(drive): raise ValueError(f'Invalid drive {drive!r}')
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
        raise TypeError(f'PureWindowsPath2() unhandled keyword parameters: {", ".join(str(_) for _ in replacements)}')

    if root is None: root = names[0][:0] if names else (drive[:0] if drive is not None else '')
    if drive is None: drive = root[:0]
    if isinstance(root, bytes): _sep = b'\\'; _altsep = b'/'
    else:                       _sep =  '\\'; _altsep =  '/'
    drive = drive.replace(_altsep, _sep)
    root = root.replace(_altsep, _sep)
    if drive.startswith(_sep): root = _sep  # force root if drive is UNC drive
    anchor = drive + root
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
    if anchor: names.insert(0, anchor)
    po = tuple.__new__(cls, (tuple(names), anchor, drive, root, stem, suffix, tuple(suffixes)))
    po.__fspath__()  # check part types
    return po

  @property
  def drive(self): return tuple.__getitem__(self, 2)
  @property
  def root(self): return tuple.__getitem__(self, 3)
  @property
  def anchor(self): return tuple.__getitem__(self, 1)
  @property
  def parents(self):  # pathlib.PurePath returns <PurePath.parents> object
    parts = self.parts
    ani = 0 if self.anchor else 1
    return (*(PureWindowsPath2(parsed_parts=parts[:i]) for i in range(1 - ani, len(parts))),)[::-1]
  @property
  def parent(self):
    pts = self.parts
    i = None if self.anchor and len(pts) == 1 else -1
    return PureWindowsPath2(parsed_parts=pts[:i])
  @property
  def parts(self): return tuple.__getitem__(self, 0)
  @property
  def name(self): return self.names[-1] if self.names else self.root[:0]
  @property
  def suffix(self): return tuple.__getitem__(self, 5)
  @property
  def suffixes(self): return tuple.__getitem__(self, 6)
  @property
  def stem(self): return tuple.__getitem__(self, 4)
  @property
  def _parts(self): return [*self.parts]  # in PureWindowsPath, it is a cached property, but here PureWindowsPath2 is frozen/stateless
  @property
  def _cparts(self): return [*(_.lower() for _ in self.parts)]  # in PureWindowsPath, it is a cached property, but here PureWindowsPath2 is frozen/stateless
  def __repr__(self): return f'{self.__class__.__name__}({self.as_posix()!r})'
  def __fspath__(self): return self.anchor + self.sep.join(self.names) or self.curdir
  def __hash__(self): return (*self._cparts,).__hash__()  # pathlib.PureWindowsPath behavior
  #def __eq__(self): use default behavior (not exactly like pathlib.PurePath behavior)
  #def __ge__(self):
  #def __gt__(self):
  #def __le__(self):
  #def __lt__(self):
  #def __ne__(self):
  def __truediv__(self, other): return PureWindowsPath2(self, other)
  def __rtruediv__(self, other): return PureWindowsPath2(other, self)
  def as_posix(self): p = self.__fspath__(); return p.replace(b'\\', b'/') if isinstance(p, bytes) else p.replace('\\', '/')  # yes… this is original behavior…
  def as_uri(self):
    p = self.__fspath__()
    if isinstance(p, bytes): _sep = b'/'; _file = b'file:'; p = p.replace(b'\\', b'/')
    else:                    _sep =  '/'; _file =  'file:'; p = p.replace( '\\',  '/')
    if self.is_absolute():  # is_absolute() is True if drive is not empty
      if p.startswith(_sep): return _file + p  # if drive is UNC
      return _file + _sep * 3 + p  # if drive is letter
    raise ValueError("relative path can't be expressed as a file URI")
  def is_absolute(self): return True if self.drive and self.root else False  # if no drive, then not absolute
  def is_relative_to(self, other): return self.relative_to(other, _bool=True)
  def is_reserved(self):
    name = self.name.lower()
    l = len(name)
    # https://help.interfaceware.com/v6/windows-reserved-file-names
    # by doing brut force on 0 to 4 characters, PureWindowsPath also concider reserved :
    #   '(?i)((CON|PRN|AUX|NUL)[ .:]?|(COM|LPT)[1-9\xb2\xb3\xb9])' (NB: '(?i)(COM|LPT)0' is not reserved)
    def enc(s): return bytes(ord(c) for c in s)
    reserved1i = iter(('con', 'prn', 'aux', 'nul'))
    reserved2i = iter(('com', 'lpt'))
    spec = ' .:'
    digits = '123456789\xb2\xb3\xb9'  # XXX '\xb2' should be converted as b'\xb2' or b'\xc2\xb2'?
    if l == 3:
      if isinstance(name, bytes): reserved1i = (enc(_) for _ in reserved1i)
      if name in reserved1i: return True
    elif l == 4:
      if isinstance(name, bytes):
        reserved1i = (enc(_) for _ in reserved1i)
        reserved2i = (enc(_) for _ in reserved2i)
        spec = enc(spec)
        digits = enc(digits)
      for _ in reserved1i:
        if name[:3] == _ and name[-1:] in spec: return True
      for _ in reserved2i:
        if name[:3] == _ and name[-1:] in digits: return True
    return False
  def joinpath(self, *other): return PureWindowsPath2(self, *other)
  #XXX def match
  def relative_to(self, other, *, _bool=False):
    def checktypes(a, b):
      ta, tb = type(a), type(b)
      if ta != tb: raise TypeError(f'cannot compare {ta.__name__} with {tb.__name__}')
    other = PureWindowsPath2(other)
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
        else: return True if _bool else PureWindowsPath2(root=srt[:0], parsed_parts=p1[i:])  # root=… is to keep fspath type when parsed_parts is empty
    if _bool: return False
    raise ValueError(f'{self.__fspath__()!r} is not in the subpath of {other.__fspath__()!r} OR one path is relative and the other is absolute.')  # yes, this is the true PurePath error behavior
  def with_name(self, name): return PureWindowsPath2(self, name=name)
  def with_stem(self, stem): return PureWindowsPath2(self, stem=stem)
  def with_suffix(self, suffix): return PureWindowsPath2(self, suffix=suffix)

  # non PurePath API
  @property
  def names(self): return self.parts[1:] if self.anchor else self.parts
  @property
  def sep(self): return b'\\' if isinstance(self.root, bytes) else '\\'
  @property
  def altsep(self): return b'/' if isinstance(self.root, bytes) else '/'
  @property
  def curdir(self): return b'.' if isinstance(self.root, bytes) else '.'
  @property
  def pardir(self): return b'..' if isinstance(self.root, bytes) else '..'
  @property
  def extsep(self): return b'.' if isinstance(self.root, bytes) else '.'
  def __add__(self, other):
    if hasattr(other, '__fspath__'): other = other.__fspath__()
    return PureWindowsPath2(self.__fspath__() + other)
  def __floordiv__(self, other): return PureWindowsPath2(anchor=self.anchor, names=[*self.names, other])
  def __rfloordiv__(self, other): raise ValueError('PureWindowsPath2() cannot append name from tail')
  def _replace(self, **replacements): return PureWindowsPath2(self, **replacements)
