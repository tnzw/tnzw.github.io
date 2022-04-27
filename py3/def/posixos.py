# posixos.py Version 1.1.1
# Copyright (c) 2021-2022 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def posixos():
  class posixos(object):
    """\
A way to have the same `os` behavior as in a posix environment (like linux on windows)

letter_drive_names => ("cygdrive",):
  Drives are place in /cygdrive/{letter.lower()} (eg /cygdrive/e for E:\\ on windows)
  You can set letter_drive_names to () to have drives on root (eg /e for E:\\ on windows)
  Set to None, you cannot access drives.
  => None:  <no drive access>
  => (): /{letter.lower()}
  => ("mnt",): /mnt/{letter.lower()}
  => ("mnt", "drive"): /mnt/drive/{letter.lower()}

/!\\ On current implementation
  on windows: /cygdrive/e/../here -> E:\\..\\here.
      and so  /cygdrive/e/../here === /cygdrive/e/here
      leading to misbehavior like in "relpath" or "chdir"...
"""
    name = "posix"
    def __init__(self, os_module=None, letter_drive_names=("cygdrive",), name="posix"):
      self._os = os_module
      self._letter_drive_names = letter_drive_names
      self.name = str(name)

    @property
    def os(self): return os if self._os is None else self._os

    # https://docs.python.org/3/library/os.html
    @property
    def curdir(self): return "."
    @property
    def pardir(self): return ".."
    @property
    def sep(self): return "/"
    @property
    def altsep(self): return None
    @property
    def extsep(self): return "."
    @property
    def pathsep(self): return ":"
    @property
    def linesep(self): return "\n"

    class path(object):
      # https://docs.python.org/3/library/os.path.html
      def __init__(self, os_module): self._os = os_module
      for _ in ("curdir", "pardir", "sep", "altsep", "extsep", "pathsep"):
        exec(f"@property\ndef {_}(self): return self._os.{_}", {}, locals())
      del _
      # The goal is to have a FULL posix like `os` on windows
      # original behavior on linux is :
      #   >>> ntpath.isdir("tmp")
      #   True
      #   >>> ntpath.isdir(".\\tmp")
      #   False  <- we want True
      # original behavior on window is :
      #   >>> posixpath.isdir("tmp")
      #   True
      #   >>> posixpath.isdir(".\\tmp")
      #   True  <- we want False
      for _ in ("basename", "commonpath", "commonprefix", "dirname", "isabs", "join",
                "normcase", "normpath", "relpath", "split", "splitdrive", "splitext",
                "supports_unicode_filenames"):
        exec(f"@property\ndef {_}(self): return posixpath.{_}", globals(), locals())
      del _
      def abspath(self, path):
        path = self._os.fspath(path)
        if isinstance(path, str): return self.normpath(self.join(self._os.getcwd(), path))
        return self.normpath(self.join(self._os.getcwdb(), path))
      def exists(self, path):
        try: s = self._os.stat(path, _posixos_path_errors="none")
        except FileNotFoundError: return False
        if s: return True
        return False
      def lexists(self, path):
        try: s = self._os.lstat(path, _posixos_path_errors="none")
        except FileNotFoundError: return False
        if s: return True
        return False
      def isfile(self, path):
        try: s = self._os.stat(path, _posixos_path_errors="none")
        except FileNotFoundError: return False
        if s: return stat.S_ISREG(s.st_mode)
        return False
      def isdir(self, path):
        try: s = self._os.stat(path, _posixos_path_errors="none")
        except FileNotFoundError: return False
        if s: return stat.S_ISDIR(s.st_mode)
        return False
      def islink(self, path):
        try: s = self._os.lstat(path, _posixos_path_errors="none")
        except FileNotFoundError: return False
        if s: return stat.S_ISLNK(s.st_mode)
        return False
      def getatime(self, path): return self._os.stat(path).st_atime
      def getctime(self, path): return self._os.stat(path).st_ctime  # XXX get mtime on windows instead?
      def getmtime(self, path): return self._os.stat(path).st_mtime
      def getsize(self, path): return self._os.stat(path).st_size
      def expanduser(self, path):
        path = self._os.fspath(path)
        if self.isabs(path): return path
        tpath = self._os._translate_path(path, cast="tuplepath")
        if tpath.names:
          tpath = tpath.replace(path=self._os.os.path.expanduser(tpath.names[0]), os_module=self._os.os).extend(tpath[1:])
          return self._os._translate_path(tpath, reverse=True)
        return path
      def realpath(self, path):
        tpath = self._os._translate_path(path)
        newtpath = self._os.os.path.realpath(tpath)
        return self._os._translate_path(newtpath, reverse=True)
      # ("expandvars",
      #  "ismount",
      #  "samefile", "sameopenfile", "samestat")

    def fspath(self, s): return self.os.fspath(s)
    # https://docs.python.org/3/library/sys.html#sys.getfilesystemencoding
    _filesystemencoding = "utf-8"  # actualy should be the locale encoding
    _filesystemencodeerrors = "surrogateescape"  # "surrogatepass" on windows
    def fsencode(self, filename):
      filename = self.fspath(filename)
      if isinstance(filename, str): return filename.encode(self._filesystemencoding, self._filesystemencodeerrors)
      return filename
    def fsdecode(self, filename):
      filename = self.fspath(filename)
      if isinstance(filename, bytes): return filename.decode(self._filesystemencoding, self._filesystemencodeerrors)
      return filename

    def _translate_path(self, path, reverse=False, *, cast=None):  #, errors="strict", default=None):
      if self.os.curdir != "." or self.os.pardir != "..": raise NotImplementedError("unhandled path mechanism")
      if reverse:  # fomr X to posix
        tpath = tuplepath(path, os_module=self.os)
        if self._letter_drive_names not in (None, False) and tpath.fsencode().drivename.lower() in (_.encode() + b":" for _ in "abcdefghijklmnopqrstuvwxyz"):
          #tpath = tpath.replace(names=("mnt", tpath.drivename[:1].lower()) + tpath.names, os_module=self)
          #tpath = tpath.replace(names=(tpath.drivename[:1].lower(),) + tpath.names, os_module=self)
          tpath = tpath.replace(names=self._letter_drive_names + (tpath.drivename[:1].lower(),) + tpath.names, os_module=self)
          tpath = tpath.replace(root=tpath.sep)
        else:
          tpath = tpath.replace(os_module=self)
        if cast == "tuplepath": return tpath
        return tpath.pathname
      else:  # from posix to X
        tpath = tuplepath(path, os_module=self).replace(os_module=self.os)
        seps = list(_ for _  in (tpath.sep, tpath.altsep) if _)
        for name in tpath.names:
          for sep in seps:
            if sep in name:
              raise ValueError("invalid path")
              #if errors == "strict": raise ValueError("invalid path")
              #elif errors == "default": return default
              #elif errors == "ignore": pass
              #else: raise LookupError(f"unknown error handler name {errors!r}")
        if self._letter_drive_names not in (None, False) and tuplepath("A:\\", os_module=self.os).drivename == "A:":
          etpath = tpath.fsencode()
          l = len(self._letter_drive_names)
          #if etpath[:1] == b"/mnt" and etpath[1:2].pathname in (_.encode() for _ in "abcdefghijklmnopqrstuvwxyz"):
          #if etpath.names and etpath.names[0] in (_.encode() for _ in "abcdefghijklmnopqrstuvwxyz"):
          if etpath[:l] == tuplepath(root="/", names=self._letter_drive_names, os_module=self.os).fsencode() and b"".join(etpath.names[l:l+1]) in (_.encode() for _ in "abcdefghijklmnopqrstuvwxyz"):
            #rootname = tpath.names[1].upper()
            #rootname = tpath.names[0].upper()
            rootname = tpath.names[l].upper()
            rootname += b":\\" if isinstance(rootname, bytes) else ":\\"
            #tpath = tpath.replace(root=rootname, names=tpath.names[2:])
            #tpath = tpath.replace(root=rootname, names=tpath.names[1:])
            tpath = tpath.replace(root=rootname, names=tpath.names[l+1:])
        if cast == "tuplepath": return tpath
        return tpath.pathname

    def _call_pathorfd(self, *a, _posixos_path_errors="strict", **opt):
      method, path = a[:2]
      try:
        if not isinstance(path, int): path = self._translate_path(path)
      except ValueError:
        if _posixos_path_errors == "strict": raise
        elif _posixos_path_errors == "none": return None
        else: raise LookupError(f"unknown error handler name {_posixos_path_errors!r}")
      return getattr(self.os, method)(path, *a[2:], **opt)
    def _call_path2(self, *a, _posixos_path_errors="strict", **opt):
      method, src, dst = a[:3]
      try:
        src = self._translate_path(src)
        dst = self._translate_path(dst)
      except ValueError:
        if _posixos_path_errors == "strict": raise
        elif _posixos_path_errors == "none": return None
        else: raise LookupError(f"unknown error handler name {_posixos_path_errors!r}")
      return getattr(self.os, method)(src, dst, *a[3:], **opt)

    # XXX stats, ctime is creation time on windows, get mtime instead?
    def stat(self, *a, **opt): return self._call_pathorfd("stat", *a, **opt)
    def lstat(self, *a, **opt): return self._call_pathorfd("lstat", *a, **opt)
    def fstat(self, *a, **opt): return self.os.fstat(*a, **opt)
    def chdir(self, *a, **opt): return self._call_pathorfd("chdir", *a, **opt)
    def chown(self, *a, **opt): return self._call_pathorfd("chown", *a, **opt)
    def utime(self, *a, **opt): return self._call_pathorfd("utime", *a, **opt)
    def mkdir(self, *a, **opt): return self._call_pathorfd("mkdir", *a, **opt)
    def rmdir(self, *a, **opt): return self._call_pathorfd("rmdir", *a, **opt)
    def readlink(self, *a, **opt): return self._translate_path(self._call_pathorfd("readlink", *a, **opt), reverse=True)
    def link(self, *a, **opt): return self._call_path2("link", *a, **opt)
    def symlink(self, *a, **opt): return self._call_path2("symlink", *a, **opt)
    def unlink(self, *a, **opt): return self._call_pathorfd("unlink", *a, **opt)
    remove = unlink
    def lseek(self, fd, pos, how):
      if   how == self.SEEK_CUR: how = self.os.SEEK_CUR
      elif how == self.SEEK_SET: how = self.os.SEEK_SET
      elif how == self.SEEK_END: how = self.os.SEEK_END
      return self.os.lseek(fd, pos, how)
    SEEK_CUR = 1
    SEEK_END = 2
    SEEK_SET = 0
    def read(self, *a, **opt): return self.os.read(*a, **opt)
    def write(self, *a, **opt): return self.os.write(*a, **opt)
    def fsync(self, *a, **opt): return self.os.fsync(*a, **opt)
    def ftruncate(self, *a, **opt): return self.os.ftruncate(*a, **opt)
    def truncate(self, *a, **opt): return self._call_pathorfd("truncate", *a, **opt)
    def close(self, *a, **opt): return self.os.close(*a, **opt)
    def isatty(self, *a, **opt): return self.os.isatty(*a, **opt)

    def getcwd(self): return self._translate_path(self.os.getcwd(), reverse=True)
    def getcwdb(self): return self._translate_path(self.os.getcwdb(), reverse=True)

    def _convert_open_flags(self, flags, os, *soft):
      if os.O_RDONLY != 0: raise NotImplementedError("cannot handle O_RDONLY != 0")
      new_flags = getattr(os, "O_BINARY", 0)
      for attr in "ACCMODE APPEND ASYNC CLOEXEC CREAT DIRECT DIRECTORY DSYNC EXCL LARGEFILE NDELAY NOATIME NOCTTY NOFOLLOW NONBLOCK PATH RDONLY RDWR RSYNC SYNC TMPFILE TRUNC WRONLY".split():
        selflag = getattr(self, "O_" + attr)
        new_flags |= getattr(os, "O_" + attr, *soft) if (flags & selflag) == selflag else 0
      return new_flags

    O_ACCMODE = 3
    O_APPEND = 1024
    O_ASYNC = 8192
    O_CLOEXEC = 524288
    O_CREAT = 64
    O_DIRECT = 16384
    O_DIRECTORY = 65536
    O_DSYNC = 4096
    O_EXCL = 128
    O_LARGEFILE = 0
    O_NDELAY = 2048
    O_NOATIME = 262144
    O_NOCTTY = 256
    O_NOFOLLOW = 131072
    O_NONBLOCK = 2048
    O_PATH = 2097152
    O_RDONLY = 0
    O_RDWR = 2
    O_RSYNC = 1052672
    O_SYNC = 1052672
    O_TMPFILE = 4259840
    O_TRUNC = 512
    O_WRONLY = 1

    def open(self, path, flags, *a, **opt):
      flags = self._convert_open_flags(flags, self.os, 0)
      return self.os.open(path, flags, *a, **opt)

    def listdir(self, path="."): return list(_.name for _ in self.scandir(path))

    def _ispathindrivefolder(self, path):
      if self._letter_drive_names not in (None, False) and tuplepath("A:\\", os_module=self.os).drivename == "A:":
        if tuplepath(path, os_module=self).fsencode() == tuplepath(root="/", names=self._letter_drive_names, os_module=self.os).fsencode():
          return True
      return False

    def scandir(self, path="."):
      if isinstance(path, int):
        scan = self.os.scandir(path)
        return ScandirIterator(scan, (DirEntry(name=_.name, dir_fd=path, os_module=self) for _ in scan))
      if self._ispathindrivefolder(path):
        #return XXX list all drives!?
        return ScandirIterator(None, iter(()))
      path = self._translate_path(path)
      scan = self.os.scandir(path)
      def __iter__():
        for _ in scan:
          full = self.path.join(path, _.name)
          yield DirEntry(path=full, name=_.name, os_module=self)
      return ScandirIterator(scan, __iter__())

    def replace(self, src, dst, *, src_dir_fd=None, dst_dir_fd=None):
      # windows cannot replace an empty dir with another dir, linux can.
      # linux can't replace an empty dir with a file
      src = self._translate_path(src)
      dst = self._translate_path(dst)
      try:
        return self.os.replace(src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)
      except FileExistsError:
        reraise = False
        try: self.os.rmdir(dst, dir_fd=dst_dir_fd)
        except OSError: reraise = True
        if reraise: raise
      return self.os.replace(src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)

    rename = replace  # same behavior on linux

    def strerror(self, code): return os_strerror(code)
    def fdopen(self, *a, **k): return open2(*a, os_module=self, **k)
    @property
    def supports_follow_symlinks(self): return self.os.supports_follow_symlinks

    # XXX do other methods

    # environ
    # environb
    # supports_bytes_environ

    # walk

  posixos = posixos()
  posixos.path = posixos.path(posixos)
  return posixos
posixos = posixos()
posixos._required_globals = ["os", "posixpath", "DirEntry", "ScandirIterator", "open2", "os_strerror", "tuplepath"]
