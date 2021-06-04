def FileIO__tester(fn):
  def test(*a,**k):
    tmpdir = tempfile.mkdtemp()
    pwd = os.getcwd()
    try:
      os.chdir(tmpdir)
      #memos = MemOs()
      #memos.fread = lambda path: fs_readfile(path, os_module=memos)
      #memos.fwrite = lambda path, data: fs_writefile(path, data, os_module=memos)
      #a = (memos,) + a
      return fn(*a,**k)
    finally:
      os.chdir(pwd)
      shutil.rmtree(tmpdir)
  return test

@FileIO__tester
def test_FileIO__del_closes_real_os():
  fd = os.open("test", os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
  fh = io.FileIO("test", "wb", opener=lambda *a: fd)
  del fh  # garbage collect fh
  assert_raise(OSError, lambda: os.close(fd))

@FileIO__tester
def test_FileIO__del_closes():
  fd = os.open("test", os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
  fh = FileIO("test", "wb", opener=lambda *a: fd)
  del fh  # garbage collect fh
  assert_raise(OSError, lambda: os.close(fd))

