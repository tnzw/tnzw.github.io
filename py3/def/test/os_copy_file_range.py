def os_copy_file_range_tester(fn):
  def test(*a,**k):
    tmpdir = tempfile.mkdtemp()
    pwd = os.getcwd()
    #fds = []
    #def os_open(path, flags, os_module=None):
    #  if os_module is None: os_module = os
    #  fd = os_module.open(path, flags)
    #  fds.append((os_module, fd))
    #  return fd
    try:
      os.chdir(tmpdir)
      #memos = MemOs()
      #memos.fread = lambda path: fs_readfile(path, os_module=memos)
      #memos.fwrite = lambda path, data: fs_writefile(path, data, os_module=memos)
      #a = (memos,) + a
      return fn(*a,**k)
    finally:
      #for o, fd in fds: o.close(fd)
      os.chdir(pwd)
      shutil.rmtree(tmpdir)
  return test
class os_copy_file_range_special_open(tuple):
  modes = {
    "rb": ("O_RDONLY",),
    "wb": ("O_WRONLY", "O_CREAT", "O_TRUNC"),
    "rb+": ("O_RDWR",),
  }
  def __new__(cls, path, mode="rb"):
    flags = 0
    for _ in cls.modes[mode] + ("O_BINARY",): flags |= getattr(os, _, 0)
    return tuple.__new__(cls, (os.open(path, flags),))
  @property
  def fileno(self): return tuple.__getitem__(self, 0)
  def __del__(self): os.close(self.fileno)
  def __enter__(self): return self.fileno
  def __exit__(self, *a): return

@os_copy_file_range_tester
def test_os_copy_file_range_10_0_0(copy_file_range=None):
  _open = os_copy_file_range_special_open
  if copy_file_range is None: copy_file_range = os_copy_file_range
  with open("1", "wb") as f: f.write(b"0123456789azertyuiop")
  with _open("1", "rb") as fd1:
    with _open("2", "wb") as fd2:
      copy_file_range(fd1, fd2, 10, 0, 0)
  with open("1", "rb") as f1:
    with open("2", "rb") as f2:
      d1 = f1.read()
      d2 = f2.read()
      assert_equal(d1[:10], d2)
def test_os_copy_file_range_10_0_0_real_os():
  if not hasattr(os, "copy_file_range"):
    return print("/!\\ os has no attribute copy_file_range")
  try:
    return test_os_copy_file_range_10_0_0(copy_file_range=os.copy_file_range)
  except OSError as e:
    if e.errno != errno.ENOSYS: raise
    print(e)

@os_copy_file_range_tester
def test_os_copy_file_range_10(copy_file_range=None):
  _open = os_copy_file_range_special_open
  if copy_file_range is None: copy_file_range = os_copy_file_range
  with open("1", "wb") as f: f.write(b"0123456789azertyuiop")
  with _open("1", "rb") as fd1:
    with _open("2", "wb") as fd2:
      os.write(fd2, b"lol")
      copy_file_range(fd1, fd2, 10)
  with open("1", "rb") as f1:
    with open("2", "rb") as f2:
      d1 = f1.read()
      d2 = f2.read()
      assert_equal(b"lol", d2[:3])
      assert_equal(d1[:10], d2[3:13])
def test_os_copy_file_range_10_real_os():
  if not hasattr(os, "copy_file_range"):
    return print("/!\\ os has no attribute copy_file_range")
  try:
    return test_os_copy_file_range_10(copy_file_range=os.copy_file_range)
  except OSError as e:
    if e.errno != errno.ENOSYS: raise
    print(e)
