# slashpath.py Version 1.0.1
# Copyright (c) 2020-2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class slashpath(object):
  # https://docs.python.org/3/library/os.path.html
  # we only keep methods that does not call system (I didn't check the source code uh)
  @staticmethod
  def _backslashed(bstr):
    if os.name == "nt":
      if isinstance(bstr, bytes): return bstr.replace(b"\\", b"/")
      if isinstance(bstr, str): return bstr.replace("\\", "/")
    return bstr
  @property
  def curdir(self): return "."
  @property
  def curdirb(self): return b"."
  @property
  def pardir(self): return ".."
  @property
  def pardirb(self): return b".."
  @property
  def sep(self): return "/"
  @property
  def sepb(self): return b"/"
  @property
  def altsep(self): return "\\" if os.name == "nt" else None
  @property
  def altsepb(self): return b"\\" if os.name == "nt" else None
  @property
  def extsep(self): return "."
  @property
  def extsepb(self): return b"."
  def abspath     (self, *a, **k): return self._backslashed(os.path.abspath     (*a, **k))
  def basename    (self, *a, **k): return self._backslashed(os.path.basename    (*a, **k))
  def commonpath  (self, *a, **k): return self._backslashed(os.path.commonpath  (*a, **k))
  def commonprefix(self, *a, **k): return self._backslashed(os.path.commonprefix(*a, **k))
  def dirname     (self, *a, **k): return self._backslashed(os.path.dirname     (*a, **k))
  def expanduser  (self, *a, **k): return self._backslashed(os.path.expanduser  (*a, **k))
  def expandvars  (self, *a, **k): return self._backslashed(os.path.expandvars  (*a, **k))
  def isabs       (self, *a, **k): return self._backslashed(os.path.isabs       (*a, **k))
  def join        (self, *a, **k): return self._backslashed(os.path.join        (*a, **k))
  def normcase    (self, *a, **k): return self._backslashed(os.path.normcase    (*a, **k))
  def normpath    (self, *a, **k): return self._backslashed(os.path.normpath    (*a, **k))
  def split       (self, *a, **k): return self._backslashed(os.path.split       (*a, **k))
  def splitdrive  (self, *a, **k): return self._backslashed(os.path.splitdrive  (*a, **k))
  def splitext    (self, *a, **k): return self._backslashed(os.path.splitext    (*a, **k))
  @property
  def supports_unicode_filenames(self): return os.path.supports_unicode_filenames
slashpath = slashpath()
slashpath._required_globals = ["os"]
