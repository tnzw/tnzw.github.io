def fs_copyfile_stat_to_str(s, props=None):
  if props is None: props = ("mode","uid","gid","size","mtime")
  s = {k:getattr(s, "st_"+k) for k in props}
  s = {k:(oct(v) if k in ("mode",) else v) for k,v in s.items()}
  s = {k:(int(v) if k in ("mtime","atime","ctime") else v) for k,v in s.items()}
  return s
def fs_copyfile_soft_lstat(p, default=None, as_str=True, props=None):
  try: s = os.lstat(p)
  except FileNotFoundError: return default
  else: return fs_copyfile_stat_to_str(s, props=props) if as_str else s
def fs_copyfile_readfile(p, maxlength=1024):
  with open(p, "rb") as f: d = f.read(maxlength)
  if len(d) >= maxlength: assert_equal('data length', len(d))
  return d
def fs_copyfile_tester(fn):
  def test(*a,**k):
    tmpdir = tempfile.mkdtemp()
    pwd = os.getcwd()
    try:
      os.chdir(tmpdir)
      return fn(*a,**k)
    finally:
      os.chdir(pwd)
      shutil.rmtree(tmpdir)
  return test

@fs_copyfile_tester
def test_fs_copyfile_1(**K):
  lstat = fs_copyfile_soft_lstat
  tar_xf(io.BytesIO(tar_a_bc_data), directory=".")  # XXX change owners to test them, change modes to test them
  assert_equal(fs_copyfile("a", "aa", **K), (13, 13))
  assert_equal(fs_copyfile_readfile("a"), fs_copyfile_readfile("aa"))
  if K.get("preserve_mode") and K.get("preserve_timestamps"):
    assert_equal(lstat("a"), lstat("aa"))
  else:
    assert_notequal(lstat("a"), lstat("aa"))

def test_fs_copyfile_2_with_attributes(**K):
  K.setdefault("preserve_mode", True)
  #K.setdefault("preserve_ownership", True)
  K.setdefault("preserve_timestamps", True)
  return test_fs_copyfile_1(**K)

@fs_copyfile_tester
def test_fs_copyfile_3_excl(**K):
  K.setdefault("flags", fs_copyfile.EXCL)
  lstat = fs_copyfile_soft_lstat
  tar_xf(io.BytesIO(tar_a_bc_data), directory=".")  # XXX change owners to test them, change modes to test them
  assert_equal(fs_copyfile("a", "aa", **K), (13, 13))
  assert_equal(fs_copyfile_readfile("a"), fs_copyfile_readfile("aa"))
  assert_raise(FileExistsError, lambda: fs_copyfile("b/c", "aa", **K))
