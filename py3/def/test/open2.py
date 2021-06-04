def open2__tester(fn):
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

@open2__tester
def test_open2__rb():
  mos = MemOs()
  for _ in ("O_CREAT", "O_APPEND", "O_TRUNC", "O_BINARY", "O_NOINHERIT", "O_CLOEXEC"): setattr(mos, _, getattr(os, _, 0))
  mock_os = os
  def opener_mock(*a, **k):
    opener_mock.a = a
    opener_mock.k = k
    return mock_os.open(*a, **k)

  with open("lol", "wb") as f: f.write(b"hello\r\nworld")
  fd = mos.open("lol", mos.O_WRONLY | mos.O_CREAT | mos.O_TRUNC | getattr(mos, "O_BINARY", 0))
  mos.write(fd, b"hello\r\nworld")
  mos.close(fd)

  with open(file="lol", mode="rb", opener=opener_mock) as rb1:
    assert_equal(rb1.read(), b"hello\r\nworld")
  # repr(rb1) → <_io.BufferedReader name='lol'>
  # dir(rb1) → ['__class__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__ne__', '__new__', '__next__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '_checkClosed', '_checkReadable', '_checkSeekable', '_checkWritable', '_dealloc_warn', '_finalizing', 'close', 'closed', 'detach', 'fileno', 'flush', 'isatty', 'mode', 'name', 'peek', 'raw', 'read', 'read1', 'readable', 'readinto', 'readinto1', 'readline', 'readlines', 'seek', 'seekable', 'tell', 'truncate', 'writable', 'write', 'writelines']
  # repr(rb1.raw) → <_io.FileIO name='lol' mode='rb' closefd=True>
  # dir(rb1.raw) → ['__class__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__ne__', '__new__', '__next__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '_blksize', '_checkClosed', '_checkReadable', '_checkSeekable', '_checkWritable', '_dealloc_warn', '_finalizing', 'close', 'closed', 'closefd', 'fileno', 'flush', 'isatty', 'mode', 'name', 'read', 'readable', 'readall', 'readinto', 'readline', 'readlines', 'seek', 'seekable', 'tell', 'truncate', 'writable', 'write', 'writelines']

  a, k = opener_mock.a, opener_mock.k
  mock_os = mos
  with open2(file="lol", mode="rb", opener=opener_mock, os_module=mos) as rb2:
    assert_equal((a, k), (opener_mock.a, opener_mock.k))
    assert_equal(rb2.read(), b"hello\r\nworld")

@open2__tester
def test_open2__wb():
  mos = MemOs()
  for _ in ("O_CREAT", "O_APPEND", "O_TRUNC", "O_BINARY", "O_NOINHERIT", "O_CLOEXEC"): setattr(mos, _, getattr(os, _, 0))
  mock_os = os
  def opener_mock(*a, **k):
    opener_mock.a = a
    opener_mock.k = k
    return mock_os.open(*a, **k)

  with open(file="lol", mode="wb", opener=opener_mock) as wb1:
    wb1.write(b"hello\r\nworld")
  # repr(wb1) → <_io.BufferedWriter name='lol'>

  a, k = opener_mock.a, opener_mock.k
  mock_os = mos
  with open2(file="lol", mode="wb", opener=opener_mock, os_module=mos) as wb2:
    assert_equal((a, k), (opener_mock.a, opener_mock.k))
    wb2.write(b"hello\r\nworld")

@open2__tester
def test_open2__r():
  mos = MemOs()
  for _ in ("O_CREAT", "O_APPEND", "O_TRUNC", "O_BINARY", "O_NOINHERIT", "O_CLOEXEC"): setattr(mos, _, getattr(os, _, 0))
  mock_os = os
  def opener_mock(*a, **k):
    opener_mock.a = a
    opener_mock.k = k
    return mock_os.open(*a, **k)

  with open("lol", "wb") as f: f.write(b"hello" + os.linesep.encode() + b"world")
  fd = mos.open("lol", mos.O_WRONLY | mos.O_CREAT | mos.O_TRUNC | getattr(mos, "O_BINARY", 0))
  mos.write(fd, b"hello" + mos.linesep.encode() + b"world")
  mos.close(fd)

  with open(file="lol", mode="r", opener=opener_mock) as rb1:
    assert_equal(rb1.read(), f"hello\nworld")
  # repr(rb1) → # <_io.TextIOWrapper name='lol' mode='r' encoding='cp1252' (windows) or 'UTF-8' (linux)>

  a, k = opener_mock.a, opener_mock.k
  mock_os = mos
  with open2(file="lol", mode="r", opener=opener_mock, os_module=mos) as rb2:
    assert_equal((a, k), (opener_mock.a, opener_mock.k))
    assert_equal(rb2.read(), f"hello\nworld")

@open2__tester
def test_open2__w():
  mos = MemOs()
  for _ in ("O_CREAT", "O_APPEND", "O_TRUNC", "O_BINARY", "O_NOINHERIT", "O_CLOEXEC"): setattr(mos, _, getattr(os, _, 0))
  mock_os = os
  def opener_mock(*a, **k):
    opener_mock.a = a
    opener_mock.k = k
    return mock_os.open(*a, **k)

  with open(file="lol", mode="w", opener=opener_mock) as wb1:
    wb1.write("hello\nworld")

  a, k = opener_mock.a, opener_mock.k
  mock_os = mos
  with open2(file="lol", mode="w", opener=opener_mock, os_module=mos) as wb2:
    assert_equal((a, k), (opener_mock.a, opener_mock.k))
    wb2.write("hello\nworld")

@open2__tester
def test_open2__wp():
  mos = MemOs()
  for _ in ("O_CREAT", "O_APPEND", "O_TRUNC", "O_BINARY", "O_NOINHERIT", "O_CLOEXEC"): setattr(mos, _, getattr(os, _, 0))
  mock_os = os
  def opener_mock(*a, **k):
    opener_mock.a = a
    opener_mock.k = k
    return mock_os.open(*a, **k)

  with open(file="lol", mode="w+", opener=opener_mock) as wp1:
    # repr(wp1) → <_io.TextIOWrapper name='lol' mode='w+' encoding='cp1252'>
    # repr(wp1.buffer) → <_io.BufferedRandom name='lol'>
    # repr(wp1.buffer.raw) → <_io.FileIO name='lol' mode='rb+' closefd=True>
    wp1.write("hello\nworld")
    wp1.seek(0)
    assert_equal(wp1.read(), "hello\nworld")

  a, k = opener_mock.a, opener_mock.k
  mock_os = mos
  with open2(file="lol", mode="w+", opener=opener_mock, os_module=mos) as wp2:
    assert_equal((a, k), (opener_mock.a, opener_mock.k))
    wp2.write("hello\nworld")
    wp2.seek(0)
    assert_equal(wp2.read(), "hello\nworld")
