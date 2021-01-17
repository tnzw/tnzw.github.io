def os_walk_stat_to_str(s, props=None):
  if props is None: props = ("mode","uid","gid","size","mtime")
  s = {k:getattr(s, "st_"+k) for k in props}
  s = {k:(oct(v) if k in ("mode",) else v) for k,v in s.items()}
  s = {k:(int(v) if k in ("mtime","atime","ctime") else v) for k,v in s.items()}
  return s
def os_walk_soft_lstat(p, default=None, as_str=True, props=None):
  try: s = os.lstat(p)
  except FileNotFoundError: return default
  else: return fs_sync_stat_to_str(s, props=props) if as_str else s
def os_walk_tester(fn):
  def test(*a,**k):
    pwd = os.getcwd()
    tmpdir = tempfile.mkdtemp()
    try:
      os.chdir(tmpdir)
      for _ in ("src", "dst", "bak"): os.mkdir(_)
      return fn(*a,**k)
    finally:
      os.chdir(pwd)
      shutil.rmtree(tmpdir)
  return test

@os_walk_tester
def test_os_walk_strpath():
  tar_xf(io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data))
  orig_os_walk = [_ for _ in os.walk(".")]
  cust_os_walk = [_ for _ in os_walk(".")]
  assert_equal(repr(orig_os_walk), repr(cust_os_walk))
@os_walk_tester
def test_os_walk_bytespath():
  tar_xf(io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data))
  orig_os_walk = [_ for _ in os.walk(b".")]
  cust_os_walk = [_ for _ in os_walk(b".")]
  assert_equal(repr(orig_os_walk), repr(cust_os_walk))
@os_walk_tester
def test_os_walk_bytespath_downtop():
  tar_xf(io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data))
  orig_os_walk = [_ for _ in os.walk(b".", topdown=False)]
  cust_os_walk = [_ for _ in os_walk(b".", topdown=False)]
  assert_equal(repr(orig_os_walk), repr(cust_os_walk))
