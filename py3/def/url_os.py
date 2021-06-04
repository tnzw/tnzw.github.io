# url_os.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def url_os():
  # see /usr/lib/python3.9/posixpath
  def _get_sep(s): return b"/" if isinstance(s, bytes) else "/"
  class urlpath():
    os = None
    sep = "/"
    altsep = None
    curdir = "."
    pardir = ".."
    extsep = "."
    pathsep = "?"  # XXX ok ?
    altpathsep = "#"  # XXX ok ?
    alt2pathsep = "&"  # XXX ok ?
    def normcase(self, s): return self.os.fspath(s)
    def isabs(self, s):
      s = self.os.fspath(s)
      sep = _get_sep(s)
      return s.startswith(sep)
    def join(self, a, *p):
      a = self.os.fspath(a)
      sep, dot = (b"/", b".") if isinstance(a, bytes) else ("/", ".")
      path = a
      nowabs = self.isabs(a)
      for b in map(self.os.fspath, p):
        if self.isabs(b): path, nowabs = b, True
        else: path += sep + b
      if not nowabs and path.startswith(sep): return dot + path
      return path
    def split(self, p):
      p = self.os.fspath(p)
      sep = _get_sep(p)
      i = p.rfind(sep) + 1
      head, tail = p[:i], p[i:]
      if head and head != sep: head = head[:-1]
      return head, tail
    def splitext(self, p):
      p = self.basename(p)
      if isinstance(p, bytes): sep, extsep = b"/", b"."
      else: sep, extsep = "/", "."
      i = p[1:].rfind(extsep)
      if i == -1: return p, p[:0]
      return p[:i+1], p[i+1:]
    def splitdrive(self, p):
      p = self.os.fspath(p)
      return p[:0], p
    def basename(self, p):
      p = self.os.fspath(p)
      sep = _get_sep(p)
      i = p.rfind(sep) + 1
      return p[i:]
    def dirname(self, p):
      p = self.os.fspath(p)
      sep = _get_sep(p)
      i = p.rfind(sep) + 1
      head = p[:i]
      if head and head != sep: head = head[:-1]
      return head
    def normpath(self, path):
      # same as posixpath except that "" component is concidered ok,
      # and "." is concidered empty
      path = self.os.fspath(path)
      if isinstance(path, bytes): sep, empty, dot, dotdot = b"/", b"", b".", b".."
      else: sep, empty, dot, dotdot = "/", "", ".", ".."
      if path == empty: return empty
      isabs = path.startswith(sep)
      comps = (path[1:] if isabs else path).split(sep)
      new_comps = []
      for comp in comps:
        if comp in (dot,): comp = empty
        if (comp != dotdot or (not isabs and not new_comps) or
            (new_comps and new_comps[-1] == dotdot)):
          new_comps.append(comp)
        elif new_comps: new_comps.pop()
      comps = new_comps
      path = sep.join(comps)
      if isabs: path = sep + path
      return path or empty
  class url_os():
    path = urlpath()
    def fspath(self, path): return os_fspath(path)
    def fsencode(self, filename):
      filename = self.fspath(filename)
      if isinstance(filename, str): return filename.encode("UTF-8", "strict")
      return filename
    def fsdecode(self, filename):
      filename = self.fspath(filename)
      if isinstance(filename, bytes): return filename.decode("UTF-8", "strict")
      return filename
  url_os = url_os()
  url_os.path.os = url_os
  return url_os
url_os = url_os()
url_os._required_globals = ["os_fspath"]
