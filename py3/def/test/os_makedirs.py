def os_makedirs_stat_to_str(s, props=None):
  if props is None: props = ("mode","uid","gid","size","mtime")
  s = {k:getattr(s, "st_"+k) for k in props}
  s = {k:(oct(v) if k in ("mode",) else v) for k,v in s.items()}
  s = {k:(int(v) if k in ("mtime","atime","ctime") else v) for k,v in s.items()}
  return s
def os_makedirs_soft_lstat(p, default=None, as_str=True, props=None):
  try: s = os.lstat(p)
  except FileNotFoundError: return default
  else: return fs_sync_stat_to_str(s, props=props) if as_str else s
def os_makedirs_assert_mode(p, mode):
  m = os.lstat(p).st_mode & 0o777
  assert_equal(m, mode, f"0o{m:o} 0o{mode:o}")
def os_makedirs_tester(fn):
  def test(*a,**k):
    pwd = os.getcwd()
    umask = os.umask(0o022)
    tmpdir = tempfile.mkdtemp()
    try:
      os.chdir(tmpdir)
      for _ in ("src", "dst", "bak"): os.mkdir(_)
      return fn(*a,**k)
    finally:
      os.umask(umask)
      os.chdir(pwd)
      shutil.rmtree(tmpdir)
  return test

@os_makedirs_tester
def test_os_makedirs_relpath1():
  os.makedirs("orig")
  os_makedirs("cust")
  os.path.isdir("orig")
  os.path.isdir("cust")
@os_makedirs_tester
def test_os_makedirs_relpath2():
  os.makedirs("orig/lol")
  os_makedirs("cust/lol")
  os.path.isdir("orig/lol")
  os.path.isdir("cust/lol")
@os_makedirs_tester
def test_os_makedirs_relpath3():
  os.makedirs("orig/lol/hey")
  os_makedirs("cust/lol/hey")
  os.path.isdir("orig/lol/hey")
  os.path.isdir("cust/lol/hey")
@os_makedirs_tester
def test_os_makedirs_relpath3_alreadyexists():
  os.makedirs("orig/lol/hey")
  os_makedirs("cust/lol/hey")
  assert_raise(FileExistsError, lambda: os.makedirs("orig/lol/hey"))
  assert_raise(FileExistsError, lambda: os_makedirs("cust/lol/hey"))
@os_makedirs_tester
def test_os_makedirs_relpath3_mode():
  if os.name == "nt": return  # always 0o777 on windows
  os.makedirs("orig/lol/hey", mode=0o721)
  os_makedirs("cust/lol/hey", mode=0o721)
  os.path.isdir("orig/lol/hey")
  os.path.isdir("cust/lol/hey")
  os_makedirs_assert_mode("orig", 0o755)
  os_makedirs_assert_mode("cust", 0o755)
  os_makedirs_assert_mode("orig/lol", 0o755)
  os_makedirs_assert_mode("cust/lol", 0o755)
  os_makedirs_assert_mode("orig/lol/hey", 0o701)  # 0o701 is 0o721 with umask 0o022
  os_makedirs_assert_mode("cust/lol/hey", 0o701)  # 0o701 is 0o721 with umask 0o022
@os_makedirs_tester
def test_os_makedirs_relpath3_existok():
  os.makedirs("orig/lol/hey", exist_ok=True)
  os_makedirs("cust/lol/hey", exist_ok=True)
  os.makedirs("orig/lol/hey", exist_ok=True)
  os_makedirs("cust/lol/hey", exist_ok=True)
@os_makedirs_tester
def test_os_makedirs_relpath3_existok_onfile():
  os.makedirs("orig/lol")
  os_makedirs("cust/lol")
  with open("orig/lol/hey", "w"): pass
  with open("cust/lol/hey", "w"): pass
  assert_raise(FileExistsError, lambda: os.makedirs("orig/lol/hey", exist_ok=True))
  assert_raise(FileExistsError, lambda: os_makedirs("cust/lol/hey", exist_ok=True))
@os_makedirs_tester
def test_os_makedirs_relpath3_existok_onsymlink():
  if os.name == "nt": return  # cannot put symlink on windows
  os.makedirs("orig/lol")
  os_makedirs("cust/lol")
  os.symlink("orig/lol/ho", "orig/lol/hey")
  os.symlink("cust/lol/ho", "cust/lol/hey")
  assert_raise(FileExistsError, lambda: os.makedirs("orig/lol/hey", exist_ok=True))
  assert_raise(FileExistsError, lambda: os_makedirs("cust/lol/hey", exist_ok=True))
@os_makedirs_tester
def test_os_makedirs_relpath1_parents0():
  os_makedirs("cust", parents=0)
  os.path.isdir("cust")
@os_makedirs_tester
def test_os_makedirs_relpath2_parents0():
  assert_raise(FileNotFoundError, lambda: os_makedirs("cust/lol", parents=0))
@os_makedirs_tester
def test_os_makedirs_relpath2_parents1():
  os_makedirs("cust/lol", parents=1)
  os.path.isdir("cust/lol")
@os_makedirs_tester
def test_os_makedirs_relpath3_parents1():
  assert_raise(FileNotFoundError, lambda: os_makedirs("cust/lol/hey", parents=1))
@os_makedirs_tester
def test_os_makedirs_relpath3_parents2():
  os_makedirs("cust/lol/hey", parents=2)
  os.path.isdir("cust/lol/hey")
@os_makedirs_tester
def test_os_makedirs_relpath4_parents2():
  assert_raise(FileNotFoundError, lambda: os_makedirs("cust/lol/hey/ya", parents=2))
