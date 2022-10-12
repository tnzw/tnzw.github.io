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
def AltOs_readfile(altos, path, max_length, loop_protection=None):
  if loop_protection is None: loop_protection = max_length
  fd = altos.open(path, altos.O_RDONLY)
  data = _ = altos.read(fd, max_length)
  for i in range(loop_protection):
    l = len(_)
    ld = len(data)
    if l <= 0 or ld >= max_length:
      altos.close(fd)
      return data
    _ = altos.read(fd, max_length - ld)
    data += _
  raise RuntimeError('AltOs_readfile() infinite loop')
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
  altos = AltOs(path_module=PathModule(sep=";", altsep=",", extsep="!", curdir="?", pardir="^"))
  altos.mkdir("src;private")
  altos.mkdir("src;private;lol")
  assert_equal(altos.listdir("src;private"), ["lol"])
  assert_equal(altos.listdir("src;private;^"), ["private"])

@AltOs_tester
def test_AltOs__path_maze():
  altos = AltOs_mock()
  altos.mkdir('mnt')
  AltOs_writefile(altos, 'aos.txt', b'is aos')
  print('XXX')
  # XXX PLEASE DO mount mem os on mnt
  AltOs_writefile(altos, 'mnt/mos.txt', b'is mos')
  # XXX PLEASE DO assert_equal(AltOs_readfile(memos, 'mos.txt'), b'is mos')
  assert_equal(AltOs_readfile(altos, 'mnt/../mnt/mos.txt', 4096), b'is mos')
  assert_equal(AltOs_readfile(altos, 'mnt/../aos.txt', 4096), b'is aos')

@AltOs_tester
def test_AltOs__readlink_maze():
  if sys.platform == 'win32': print('skip on windows'); return
  # XXX review this test and make THIS maze
  #   altos (ntpath)
  #   (cwd)
  #   + mnt\
  #   | - to_txt -> ..\txt
  #   - txt  b'is os'
  #   altos.mkdir('mnt'); altos.symlink('..\\txt', 'mnt\\to_txt'); writefile(altos, 'txt', b'is os')
  #
  #   memos
  #   + mnt/  (cwd)
  #   | - to_txt -> ../txt
  #   - txt  b'is memos'
  #   memos.mkdir('mnt'); memos.symlink('../txt',  'mnt/to_txt' ); writefile(memos, 'txt', b'is memos')
  #   memos.chdir('mnt')
  #
  #   altos.mount('mnt', memos)
  #   altos.readlink('mnt\\txt') -> b'../??\\??txt'
  #   readfile(altos, 'mnt\\txt') -> b'is os'  # like linux behavior

  # on linux XXX ↓
  # Exception in thread Thread-11:
  # Traceback (most recent call last):
  #   File "/usr/lib/python3.10/threading.py", line 1016, in _bootstrap_inner
  #     self.run()
  #   File "/usr/lib/python3.10/threading.py", line 1378, in run
  #     self.function(*self.args, **self.kwargs)
  #   File "/mnt/f/tc/py3/pythoncustom.tester.py", line 23363, in sub
  #     fn()
  #   File "/mnt/f/tc/py3/pythoncustom.tester.py", line 16632, in test
  #     return fn(*a,**k)
  #   File "/mnt/f/tc/py3/pythoncustom.tester.py", line 16752, in test_AltOs__readlink_maze
  #     altos.mkdir('mnt')
  #   File "/mnt/f/tc/py3/pythoncustom.tester.py", line 930, in mkdir
  #     return self._call_path("mkdir", path, mode=mode, dir_fd=dir_fd)
  #   File "/mnt/f/tc/py3/pythoncustom.tester.py", line 1064, in _call_path
  #     return getattr(os, method)(subpath.replace(os_module=os).pathname, *a[2:], **k)
  # FileNotFoundError: [Errno 2] No such file or directory: '\\tmp/tmpwcz_0aau/mnt'
  altos = AltOs_mock(path_module=ntpath)
  altos.mkdir('mnt')
  AltOs_writefile(altos, 'aos.txt', b'is aos')
  altos.symlink('mnt\\mos.txt', 'to_mos')
  print('XXX')
  # XXX PLEASE DO mount mem os on mnt with a different path_module
  AltOs_writefile(altos, 'mnt\\mos.txt', b'is mos')
  # XXX PLEASE DO memos.symlink('../aos.txt', 'to_aos')
  # XXX assert_equal(altos.readlink('mnt\\to_aos'), b'../??\\??aos.txt)
  assert_equal(AltOs_readfile(altos, 'mnt\\to_aos', 4096), b'is aos')

@AltOs_tester
def test_AltOs__utime_param_check():
  altos = AltOs_mock()
  assert_raise(ValueError, lambda: altos.utime('.', times=(1, 1), ns=(1, 1)))

# XXX test other methods*
#     mount + chdir
#     mount + chroot
