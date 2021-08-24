# PathModule.py Version 1.0.1
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class PathModule(object):

  def __init__(self, *, fsencoding="utf-8", fsencodeerrors="surrogateescape", splitdrive=None, special_prefixes=None, extra_root_prefixes=None, case_sensitive=True, allow_unc_path=None, allow_letter_drive=None, allow_initial_slashes=None, allow_empty_names=None, os_module=None, **opt):
    self._os = os_module
    for arg in ("sep", "altsep", "extsep", "pathsep", "curdir", "pardir", "fsencoding", "fsencodeerrors"):
      if arg in opt:
        setattr(self, "_" + arg, opt.pop(arg))
    if opt: raise TypeError(f"PathModule() got an unexpected keyword argument {opt.popitem()[0]!r}")
    self._splitdrive = splitdrive
    self._case_sensitive = True if case_sensitive else False
    self._allow_empty_names = True if allow_empty_names else False
    #self._keep_multi_slashes = keep_multi_slashes
    #self._defaults_curdir = defaults_curdir
    #if splitdrive: self._splitdrive = splitdrive
    #elif os_module is None: self._splitdrive = "posix"
    #elif os_module.name == "nt": self._splitdrive = "nt"
    #else: self._splitdrive = "posix"
    if special_prefixes: self._special_prefixes = special_prefixes
    elif os_module is None: self._special_prefixes = ()
    elif os_module.name == "posix": self._special_prefixes = self.get_posix_special_prefixes(sep=self.sep)
    elif os_module.name == "nt": self._special_prefixes = self.get_nt_special_prefixes(sep=self.sep)
    else: self._special_prefixes = ()
    if extra_root_prefixes: self._extra_root_prefixes = extra_root_prefixes
    elif os_module is None: self._extra_root_prefixes = ()
    elif os_module.name == "posix": self._extra_root_prefixes = self.get_posix_extra_root_prefixes(sep=self.sep)
    elif os_module.name == "nt": self._extra_root_prefixes = self.get_nt_extra_root_prefixes(sep=self.sep)
    else: self._extra_root_prefixes = ()
    if allow_unc_path: self._allow_unc_path = True if allow_unc_path else False
    elif os_module is None: self._allow_unc_path = False
    elif os_module.name == "nt": self._allow_unc_path = True
    else: self._allow_unc_path = False
    if allow_letter_drive: self._allow_letter_drive = True if allow_letter_drive else False
    elif os_module is None: self._allow_letter_drive = False
    elif os_module.name == "nt": self._allow_letter_drive = True
    else: self._allow_letter_drive = False
    if allow_initial_slashes: self._allow_initial_slashes = True if allow_initial_slashes else False
    elif os_module is None: self._allow_initial_slashes = False
    elif os_module.name == "posix": self._allow_initial_slashes = True
    else: self._allow_initial_slashes = False


  @classmethod
  def make_nt_style(cls, **opt):
    d = dict(sep="\\", altsep="/", extsep=".", pathsep=";", curdir=".", pardir="..", fsencoding="utf-8", fsencodeerrors="surrogatepass", special_prefixes=cls.get_nt_special_prefixes(), case_sensitive=False, allow_unc_path=True, allow_letter_drive=True)
    d.update(opt)
    return cls(**d)
  @classmethod
  def make_posix_style(cls, **opt):
    d = dict(sep="/", extsep=".", pathsep=":", curdir=".", pardir="..", fsencoding="utf-8", fsencodeerrors="surrogateescape", special_prefixes=cls.get_posix_special_prefixes(), allow_initial_slashes=True)
    d.update(opt)
    return cls(**d)
  @classmethod
  def make_url_style(cls, **opt):
    d = dict(sep="/", extsep=".", curdir=".", pardir="..", fsencoding="utf-8", fsencodeerrors="surrogateescape", allow_empty_names=True)
    d.update(opt)
    return cls(**d)

  @staticmethod
  def get_nt_special_prefixes(sep="\\"):
    sep = os_fspath(sep)
    dot, qm = (".", "?") if isinstance(sep, str) else (b".", b"?")
    return (sep + sep + dot + sep, sep + sep + qm + sep)
  @staticmethod
  def get_posix_special_prefixes(sep="/"): return ()
  @staticmethod
  def get_nt_extra_root_prefixes(sep="\\"): return ()
  @staticmethod
  def get_posix_extra_root_prefixes(sep="/"): return ()

  def _getattr(self, name, *default):
    _os = self._os
    if _os is None: return getattr(self, "_" + name, *default)
    undefined = []
    prop = getattr(self, "_" + name, undefined)
    if prop is undefined: return getattr(_os, name, *default)
    return prop

  def _fsencode(self, filename, reverse=False):
    method, type = ("decode", str) if reverse else ("encode", bytes)
    filename = os_fspath(filename)
    if isinstance(filename, type): return filename
    _os = self._os
    _fsencoding = getattr(self, "_fsencoding", None)
    if _fsencoding or _os is None:
      if not _fsencoding: _fsencoding = "UTF-8"
      _fsencodeerrors = getattr(self, "_fsencodeerrors", None) or ("surrogateescape" if _fsencoding.lower() in ("utf-8", "utf8") else "strict")
      return getattr(filename, method)("UTF-8", _fsencodeerrors)
    return getattr(_os, "fs" + method)(filename)

  def _fsdecode(self, filename): return self._fsencode(filename, reverse=True)

  @property
  def sep(self):     return self._fsdecode(self._getattr("sep"))
  @property
  def altsep(self):
    altsep = self._getattr("altsep", None)
    return None if altsep is None else self._fsdecode(altsep)
  @property
  def extsep(self):  return self._fsdecode(self._getattr("extsep"))
  @property
  def pathsep(self): return self._fsdecode(self._getattr("pathsep"))
  @property
  def curdir(self):  return self._fsdecode(self._getattr("curdir"))
  @property
  def pardir(self):  return self._fsdecode(self._getattr("pardir"))

  @property
  def sepb(self):     return self._fsencode(self._getattr("sep"))
  @property
  def altsepb(self):
    altsep = self._getattr("altsep", None)
    return None if altsep is None else self._fsencode(altsep)
  @property
  def extsepb(self):  return self._fsencode(self._getattr("extsep"))
  @property
  def pathsepb(self): return self._fsencode(self._getattr("pathsep"))
  @property
  def curdirb(self):  return self._fsencode(self._getattr("curdir"))
  @property
  def pardirb(self):  return self._fsencode(self._getattr("pardir"))

  def splitdrive(self, p):
    _splitdrive = self._splitdrive
    if _splitdrive is not None: return _splitdrive(p)
    p = os_fspath(p)
    if isinstance(p, bytes): sep, altsep, colon = self.sepb, self.altsepb, b":"
    else: sep, altsep, colon = self.sep, self.altsep, ":"
    if len(p) >= 2:
      if self._allow_unc_path:
        seps = (sep,) if altsep is None else (sep, altsep)
        def extract_comp(path, count):
          if count <= 0: return ()
          for sep in seps:
            if path.startswith(sep):
              len_sep = len(sep)
              return (("s", len_sep),) + extract_comp(path[len_sep:], count - 1)
          ii = tuple(i for i in (path.find(s) for s in seps) if i != -1)
          if ii:
            i = min(ii)
            return (("c", i),) + extract_comp(path[i:], count - 1)
          return (("c", len(path)),)
        ex = extract_comp(p, 5)
        if "".join(c for c, _ in ex) == "sscsc":
          i = sum(l for _, l in ex)
          return p[:i], p[i:]
      if self._allow_letter_drive:
        if p[1:2] == colon: return p[:2], p[2:]
    return p[:0], p

    #_splitdrive = self._splitdrive
    #if callable(_splitdrive): return _splitdrive(p)
    #_os = self._os
    #_splitdrive = _splitdrive if _splitdrive else (None if _os is None else getattr(_os, "name", None))
    #if _splitdrive == "nt":
    #  p = os_fspath(p)
    #  if len(p) >= 2:
    #    if isinstance(p, bytes): sep, altsep, colon = self.sepb, self.altsepb, b":"
    #    else: sep, altsep, colon = self.sep, self.altsep, ":"
    #    seps = (sep,) if altsep is None else (sep, altsep)
    #    if self._allow_unc_path:
    #      def extract_comp(path, count):
    #        if count <= 0: return ()
    #        for sep in seps:
    #          if path.startswith(sep):
    #            len_sep = len(sep)
    #            return (("s", len_sep),) + extract_comp(path[len_sep:], count - 1)
    #        ii = tuple(i for i in (path.find(s) for s in seps) if i != -1)
    #        if ii:
    #          i = min(ii)
    #          return (("c", i),) + extract_comp(path[i:], count - 1)
    #        return (("c", len(path)),)
    #      ex = extract_comp(p, 5)
    #      if "".join(c for c, _ in ex) == "sscsc":
    #        # is a UNC path
    #        i = sum(l for _, l in ex)
    #        return p[:i], p[i:]
    #    if p[1:2] == colon: return p[:2], p[2:]
    #  return p[:0], p
    #if _splitdrive in ("posix", None):
    #  p = os_fspath(p)
    #  return p[:0], p
    #raise ValueError("unhandled splitdrive")

  def split(self, p):
    p = os_fspath(p)
    sep, altsep = (self.sepb, self.altsepb) if isinstance(p, bytes) else (self.sep, self.altsep)
    seps = (sep,) if altsep is None else (sep, altsep)
    d, p = self.splitdrive(p)
    i = max(p.rfind(s) for s in seps)
    if i == -1: return d, p
    i += 1
    h, t = p[:i], p[i:]
    h2 = h
    if self._allow_empty_names:
      for s in seps:
        if h2.endswith(s): h2 = h2[:-len(s)]; break
    else:
      while True:
        for s in seps:
          if h2.endswith(s): h2 = h2[:-len(s)]; break
        else: break
    h = h2 or h
    return d + h, t

  def normpath(self, path):
    path = os_fspath(path)
    if isinstance(path, bytes): sep, altsep, empty, curdir, pardir, special_prefixes, root_prefixes = self.sepb, self.altsepb, self.sepb[:0], self.curdirb, self.pardirb, tuple(self._fsencode(_) for _ in self._special_prefixes), tuple(self._fsencode(_) for _ in self._extra_root_prefixes)
    else: sep, altsep, empty, curdir, pardir, special_prefixes, root_prefixes = self.sep, self.altsep, self.sep[:0], self.curdir, self.pardir, tuple(self._fsdecode(_) for _ in self._special_prefixes), tuple(self._fsdecode(_) for _ in self._extra_root_prefixes)
    if path.startswith(special_prefixes): return path
    if altsep is not None: path = path.replace(altsep, sep)
    len_sep = len(sep)
    prefix, path = self.splitdrive(path)
    for i, _ in enumerate(root_prefixes):
      if path.startswith(_):
        prefix += _
        path = path[len(_):]
        break
    else:
      if self._allow_initial_slashes:
        if path.startswith(sep*3): prefix += sep; path = path[len_sep*3:]
        elif path.startswith(sep*2): prefix += sep * 2; path = path[len_sep*2:]
        elif path.startswith(sep): prefix += sep; path = path[len_sep:]
      elif path.startswith(sep): prefix += sep; path = path[len_sep:]
    comps = path.split(sep)
    new_comps = []
    allow_empty_names = self._allow_empty_names
    curdir_tuple = (curdir,) if allow_empty_names else (empty, curdir)
    for comp in comps:
      if comp in curdir_tuple:
        if not allow_empty_names: continue
      if (comp != pardir or (not prefix and not new_comps) or
          (new_comps and new_comps[-1] == pardir)):
        new_comps.append(comp)
      elif new_comps: new_comps.pop()
    path = prefix + sep.join(new_comps)
    return path or (empty if allow_empty_names else curdir)

  def isabs(self, s):
    s = os_fspath(s)
    s = self.splitdrive(s)[1]
    if isinstance(s, bytes):
      seps = tuple(_ for _ in (self.sepb, self.altsepb) if _ is not None)
      root_prefixes = tuple(self._fsencode(_) for _ in self._extra_root_prefixes)
    else:
      seps = tuple(_ for _ in (self.sep, self.altsep) if _ is not None)
      root_prefixes = tuple(self._fsdecode(_) for _ in self._extra_root_prefixes)
    for _ in root_prefixes:
      if s.startswith(_): return True
    return s.startswith(seps)

  def join(self, path, *paths):
    lower = (lambda s: s.lower()) if self._case_sensitive else (lambda s: s)
    path = os_fspath(path)
    if isinstance(path, bytes): sep, altsep = self.sepb, self.altsepb
    else: sep, altsep = self.sep, self.altsep
    if not paths: path[:0] + sep  # ensure path type
    seps = (sep,) if altsep is None else (sep, altsep)
    result_drive, result_path = self.splitdrive(path)
    for p in map(os_fspath, paths):
      p_drive, p_path = self.splitdrive(p)
      if self.isabs(p_path):
        if p_drive or not result_drive: result_drive = p_drive
        result_path = p_path
        continue
      elif p_drive and p_drive != result_drive:
        if lower(p_drive) != lower(result_drive):
          result_drive, result_path = p_drive, p_path
          continue
        result_drive = p_drive  # same drive in different case
      if result_path and not result_path.endswith(seps): result_path += sep
      result_path += p_path
    if self._allow_unc_path and not self.isabs(result_path):
      def extract_comp(path, count):
        if count <= 0: return ()
        for sep in seps:
          if path.startswith(sep):
            len_sep = len(sep)
            return (("s", len_sep),) + extract_comp(path[len_sep:], count - 1)
        ii = tuple(i for i in (path.find(s) for s in seps) if i != -1)
        if ii:
          i = min(ii)
          return (("c", i),) + extract_comp(path[i:], count - 1)
        return (("c", len(path)),)
      ex = extract_comp(result_drive, 5)
      if "".join(c for c, _ in ex) == "sscsc": result_path = sep + result_path
    return result_drive + result_path

  def splitext(self, p):
    p = os_fspath(p)
    if isinstance(p, bytes): extsep = self.extsepb
    else: extsep = self.extsep
    b = self.basename(p)
    b = b.lstrip(extsep)
    i = b.rfind(extsep)
    if i == -1: return p, p[:0]
    ext = b[i:]
    return p[:-len(ext)], b[i:]

  def basename(self, p):
    p = os_fspath(p)
    if isinstance(p, bytes): sep, altsep, extsep = self.sepb, self.altsepb, self.extsepb
    else: sep, altsep, extsep = self.sep, self.altsep, self.extsep
    d, p = self.splitdrive(p)
    i = max(p.rfind(s) for s in (sep, altsep) if s is not None)
    if i == -1: return p
    return p[i + 1:]

  # XXX do other methods!

PathModule._required_globals = ["os_fspath"]
