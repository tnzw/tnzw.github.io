def AltOs_stat_to_str(s, props=None):
  if props is None: props = ("mode","uid","gid","size","mtime")
  s = {k:getattr(s, "st_"+k) for k in props}
  s = {k:(oct(v) if k in ("mode",) else v) for k,v in s.items()}
  s = {k:(int(v) if k in ("mtime","atime","ctime") else v) for k,v in s.items()}
  return s
def AltOs_soft_lstat(p, default=None, as_str=True, props=None):
  try: s = os.lstat(p)
  except FileNotFoundError: return default
  else: return fs_sync_stat_to_str(s, props=props) if as_str else s
def AltOs_writefile(altos, path, data):
  fd = altos.open(path, altos.O_WRONLY | altos.O_CREAT | altos.O_TRUNC)
  altos.write(fd, data)
  altos.close(fd)
def AltOs_tester(fn):
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
class AltOs_mock(object):
  def __init__(self, *a, **kw):
    self.os = AltOs(*a, **kw)
    self.mocks = {}
  def mock_clear(self): self.mocks.clear()
  def mock_get(self, name): return self.mocks[name] if name in self.mocks else 0
  def __getattr__(self, name):
    self.mocks[name] = self.mocks.get(name, 0) + 1
    return getattr(self.os, name)

@AltOs_tester
def test_AltOs__mkdir():
  altos = AltOs_mock()
  altos.mkdir("src/new_dir")
  assert_equal(altos.mock_get("mkdir"), 1)

@AltOs_tester
def test_AltOs__stat():
  altos = AltOs_mock()
  altos.stat("src")

@AltOs_tester
def test_AltOs__mount():
  altos = AltOs_mock()
  altos.mount("dst", altos)
  altos.stat("dst/src")
  assert_raise(FileNotFoundError, lambda: altos.stat("src/lol"))
  assert_raise(FileNotFoundError, lambda: altos.stat("dst/src/lol"))
  altos.mkdir("src/lol")
  altos.stat("src/lol")
  altos.stat("dst/src/lol")

@AltOs_tester
def test_AltOs__chroot_getcwd_1():
  altos = AltOs_mock()
  altos.mkdir("src/private")
  altos.mkdir("src/perso")
  altos.chroot("src/private")
  assert_equal(altos.getcwd(), f"{altos.sep}")
@AltOs_tester
def test_AltOs__chroot_getcwd_2():
  altos = AltOs_mock()
  altos.mkdir("src/private")
  altos.mkdir("src/perso")
  altos.chdir("src")
  altos.chroot("private")
  assert_equal(altos.getcwd(), f"{altos.sep}")
@AltOs_tester
def test_AltOs__chroot_getcwd_3():
  altos = AltOs_mock()
  altos.mkdir("src/private")
  altos.mkdir("src/perso")
  altos.chdir("src/perso")
  altos.chroot(".")
  assert_equal(altos.getcwd(), f"{altos.sep}")
@AltOs_tester
def test_AltOs__chroot_getcwd_4():
  altos = AltOs_mock()
  altos.mkdir("src/private")
  altos.mkdir("src/perso")
  altos.chdir("src/perso")
  altos.chroot("..")
  assert_equal(altos.getcwd(), f"{altos.sep}perso")
@AltOs_tester
def test_AltOs__chroot_getcwd_5():
  altos = AltOs_mock()
  altos.mkdir("src/private")
  altos.mkdir("src/perso")
  altos.chdir("src/perso")
  altos.chroot("../private")
  assert_equal(altos.getcwd(), altos.sep)

@AltOs_tester
def test_AltOs__path_translation():
  altos = AltOs(path=PathModule(sep=";", altsep=",", extsep="!", curdir="?", pardir="^"))
  altos.mkdir("src;private")
  altos.mkdir("src;private;lol")
  assert_equal(altos.listdir("src;private"), ["lol"])
  assert_equal(altos.listdir("src;private;^"), ["private"])

# XXX test other methods*
#     mount + chdir
#     mount + chroot
