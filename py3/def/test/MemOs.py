def MemOs_stat_to_str(s, props=None):
  if props is None: props = ("mode","uid","gid","size","mtime")
  s = {k:getattr(s, "st_"+k) for k in props}
  s = {k:(oct(v) if k in ("mode",) else v) for k,v in s.items()}
  s = {k:(int(v) if k in ("mtime","atime","ctime") else v) for k,v in s.items()}
  return s
def MemOs_soft_lstat(p, default=None, as_str=True, props=None):
  try: s = os.lstat(p)
  except FileNotFoundError: return default
  else: return fs_sync_stat_to_str(s, props=props) if as_str else s
def MemOs_writefile(memos, path, data):
  fd = memos.open(path, memos.O_WRONLY | memos.O_CREAT | memos.O_TRUNC)
  memos.write(fd, data)
  memos.close(fd)
def MemOs_tester(fn):
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

@MemOs_tester
def test_MemOs_mkdir():
  memos = MemOs()
  assert_raise(FileNotFoundError, lambda: memos.mkdir("d/a"))  # testing traversal FileNotFoundError
  memos.mkdir("d")  # testing create dir in cwd
  memos.mkdir("d/a")  # testing create dir in cwd sub folder
  assert_raise(FileExistsError, lambda: memos.mkdir("d"))  # testing FileExistsError
  MemOs_writefile(memos, "f", b"")
  assert_raise(NotADirectoryError, lambda: memos.mkdir("f/d"))  # testing traversal NotADirectoryError
  memos.umask(0o022)
  memos.mkdir("for_mode", 0o222)  # testing umask
  assert_equal(memos.stat("for_mode").st_mode & 0o777, 0o200)
  # XXX test create dir in root from elsewhere

# XXX test other methods*
