import sqlite3
def Sqlite3Os_stat_to_str(s, props=None):
  if props is None: props = ("mode","uid","gid","size","mtime")
  s = {k:getattr(s, "st_"+k) for k in props}
  s = {k:(oct(v) if k in ("mode",) else v) for k,v in s.items()}
  s = {k:(int(v) if k in ("mtime","atime","ctime") else v) for k,v in s.items()}
  return s
def Sqlite3Os_soft_lstat(p, default=None, as_str=True, props=None):
  try: s = os.lstat(p)
  except FileNotFoundError: return default
  else: return fs_sync_stat_to_str(s, props=props) if as_str else s
def Sqlite3Os_writefile(sqlos, path, data):
  fd = sqlos.open(path, sqlos.O_WRONLY | sqlos.O_CREAT | sqlos.O_TRUNC)
  sqlos.write(fd, data)
  sqlos.close(fd)
def Sqlite3Os_tester(fn):
  def test(*a,**k):
    tmpdir = tempfile.mkdtemp()
    pwd = os.getcwd()
    try:
      os.chdir(tmpdir)
      for _ in ("src", "dst", "bak"): os.mkdir(_)
      return fn(*a,**k)
    finally:
      os.chdir(pwd)
      shutil.rmtree(tmpdir)
  return test

@Sqlite3Os_tester
def test_Sqlite3Os_mkdir():
  sqlos = Sqlite3Os(":memory:")
  assert_raise(FileNotFoundError, lambda: sqlos.mkdir("d/a"))  # testing traversal FileNotFoundError
  sqlos.mkdir("d")  # testing create dir in cwd
  #print("-----------------------\n", sqlos.sql.dump(), "------------------------------\n")
  sqlos.mkdir("d/a")  # testing create dir in cwd sub folder
  assert_raise(FileExistsError, lambda: sqlos.mkdir("d"))  # testing FileExistsError
  Sqlite3Os_writefile(sqlos, "f", b"")
  assert_raise(NotADirectoryError, lambda: sqlos.mkdir("f/d"))  # testing traversal NotADirectoryError
  sqlos.umask(0o022)
  sqlos.mkdir("for_mode", 0o222)  # testing umask
  assert_equal(sqlos.stat("for_mode").st_mode & 0o777, 0o200)
  sqlos.chdir("d/a")
  assert_raise(FileNotFoundError, lambda: sqlos.mkdir("/e/f"))  # testing root traversal FileNotFoundError
  assert_raise(FileExistsError, lambda: sqlos.mkdir("/d"))  # testing root FileExistsError
  sqlos.mkdir("/e")  # testing create dir in root
  sqlos.mkdir("/e/f")  # testing create dir in root sub folder

@Sqlite3Os_tester
def test_Sqlite3Os_read():
  sqlos = Sqlite3Os(":memory:")
  r = sqlos.open("r", sqlos.O_WRONLY | sqlos.O_CREAT | sqlos.O_TRUNC)
  sqlos.write(r, b"first line\nsecond line\nthird line")
  sqlos.close(r)
  r = sqlos.open("r", sqlos.O_RDONLY)
  assert_equal(sqlos.read(r, 3), b"fir")
  assert_equal(sqlos.read(r, 3), b"st ")
  assert_equal(sqlos.read(r, 3), b"lin")
  sqlos.close(r)

@Sqlite3Os_tester
def test_Sqlite3Os_write():
  sqlos = Sqlite3Os(":memory:")
  w = sqlos.open("w", sqlos.O_WRONLY | sqlos.O_CREAT | sqlos.O_TRUNC)
  sqlos.write(w, b"first line\n")
  sqlos.write(w, b"second line\n")
  sqlos.write(w, b"third line")
  sqlos.close(w)
  w = sqlos.open("w", sqlos.O_RDONLY)
  read = b"".join(_ for _ in os_iterread(w, os_module=sqlos))
  sqlos.close(w)
  assert_equal(read, b"first line\nsecond line\nthird line")

# XXX test other methods*
