def os__tester(fn):
  def test(*a, **k):
    tmpdir = tempfile.mkdtemp()
    pwd = os.getcwd()
    try:
      os.chdir(tmpdir)
      os_module = k.pop("os", os)
      return fn(*a, os=os_module, nt_like=k.pop("nt_like", os_module.name == "nt"), **k)
    finally:
      os.chdir(pwd)
      shutil.rmtree(tmpdir)
  return test

def os__data_summary(data):
  cdata = []
  pb = -1
  n = 0
  for b in data:
    if b != pb:
      if n > 0: cdata.append(f"{bytes((pb,))!r} * {n}")
      pb = b
      n = 1
    else:
      n += 1
  if n > 0: cdata.append(f"{bytes((pb,))!r} * {n}")
  return " ".join(cdata)

def os__copy_file_range__check_availability(os, filename="os__copy_file_range__check_availability"):
  # testing if copy_file_range is actualy possible to test
  fs_writefile(filename, b"", os_module=os)
  fd = None
  try:
    fd = os.open(filename, os.O_RDONLY)
    os.copy_file_range(fd, fd, 0, 0, 0)
  except AttributeError as e:
    if not e.args[0].endswith(repr("copy_file_range")): raise
    return str(e)
  except OSError as e:
    if e.errno != errno.ENOSYS: raise
    return str(e)
  finally:
    if fd is not None: os.close(fd)
  return ""

@os__tester
def test_os__open_read_write_close(os, nt_like=False, **k):
  def rb(n): return fs_readfile(n, os_module=os)

  fd = os.open("first", os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_BINARY", 0))
  assert_equal(os.write(fd, b"F"), 1)
  assert_equal(os.write(fd, b"I"), 1)
  assert_equal(os.write(fd, b"R"), 1)
  assert_equal(os.write(fd, b"S"), 1)
  assert_equal(os.write(fd, b"T"), 1)
  assert_equal(os.write(fd, b""), 0)
  assert_equal(os.write(fd, b""), 0)
  os.close(fd)
  assert_raise(OSError, lambda: os.close(fd))

  fd = os.open("first", os.O_RDONLY | getattr(os, "O_BINARY", 0))
  assert_equal(os.read(fd, 1), b"F")
  assert_equal(os.read(fd, 1), b"I")
  assert_equal(os.read(fd, 1), b"R")
  assert_equal(os.read(fd, 1), b"S")
  assert_equal(os.read(fd, 1), b"T")
  assert_equal(os.read(fd, 1), b"")
  assert_equal(os.read(fd, 1), b"")
  os.close(fd)
  assert_raise(OSError, lambda: os.close(fd))
  assert_equal(rb("first"), b"FIRST")

  fd = os.open("first", os.O_WRONLY | getattr(os, "O_BINARY", 0))
  assert_equal(os.write(fd, b"YEP"), 3)  # test isn't good because writing 3 bytes AT MOST
  os.close(fd)

  fd = os.open("first", os.O_RDONLY | getattr(os, "O_BINARY", 0))
  assert_equal(os.read(fd, 1), b"Y")
  assert_equal(os.read(fd, 1), b"E")
  assert_equal(os.read(fd, 1), b"P")
  assert_equal(os.read(fd, 1), b"S")
  assert_equal(os.read(fd, 1), b"T")
  assert_equal(os.read(fd, 1), b"")
  assert_equal(os.read(fd, 1), b"")
  os.close(fd)
  assert_equal(rb("first"), b"YEPST")

  fd = os.open("first", os.O_WRONLY | getattr(os, "O_BINARY", 0))
  assert_equal(os.write(fd, b"S"), 1)
  assert_equal(os.write(fd, b"E"), 1)
  assert_equal(os.write(fd, b"C"), 1)
  assert_equal(os.write(fd, b"O"), 1)
  assert_equal(os.write(fd, b"N"), 1)
  assert_equal(os.write(fd, b"D"), 1)
  os.close(fd)

  fd = os.open("first", os.O_RDONLY | getattr(os, "O_BINARY", 0))
  assert_equal(os.read(fd, 1), b"S")
  assert_equal(os.read(fd, 1), b"E")
  assert_equal(os.read(fd, 1), b"C")
  assert_equal(os.read(fd, 1), b"O")
  assert_equal(os.read(fd, 1), b"N")
  assert_equal(os.read(fd, 1), b"D")
  assert_equal(os.read(fd, 1), b"")
  os.close(fd)
  assert_equal(rb("first"), b"SECOND")

  fd = os.open("first", os.O_RDWR | getattr(os, "O_BINARY", 0))
  assert_equal(os.read(fd, 1), b"S")
  assert_equal(os.write(fd, b"I"), 1)
  assert_equal(os.read(fd, 1), b"C")
  assert_equal(os.write(fd, b"S"), 1)
  assert_equal(os.read(fd, 1), b"N")
  assert_equal(os.read(fd, 1), b"D")
  assert_equal(os.read(fd, 1), b"")
  os.close(fd)
  assert_equal(rb("first"), b"SICSND")

  fd = os.open("first", os.O_WRONLY | os.O_TRUNC | getattr(os, "O_BINARY", 0))
  assert_equal(os.write(fd, b"NOPE"), 4)  # test isn't good because writing 4 bytes AT MOST
  os.close(fd)

  fd = os.open("first", os.O_RDONLY | getattr(os, "O_BINARY", 0))
  assert_equal(os.read(fd, 4), b"NOPE")  # test isn't good because reading 4 bytes AT MOST
  assert_equal(os.read(fd, 1), b"")
  os.close(fd)
  assert_equal(rb("first"), b"NOPE")

  if nt_like:
    assert_raise(OSError, lambda: os.open("first", os.O_RDONLY | os.O_TRUNC | getattr(os, "O_BINARY", 0)))
  else:
    fd = os.open("first", os.O_RDONLY | os.O_TRUNC | getattr(os, "O_BINARY", 0))
    assert_equal(os.read(fd, 1), b"")
    assert_equal(os.read(fd, 1), b"")
    os.close(fd)

  assert_raise(OSError, lambda: os.open("first", os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)))
  assert_raise(OSError, lambda: os.open("first", os.O_RDONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)))
  assert_raise(OSError, lambda: os.open("first", os.O_RDWR | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)))

  fd = os.open("first", os.O_WRONLY | os.O_EXCL | getattr(os, "O_BINARY", 0))
  os.close(fd)

  fd = os.open("first", os.O_RDONLY | os.O_EXCL | getattr(os, "O_BINARY", 0))
  os.close(fd)

  fd = os.open("first", os.O_RDWR | os.O_EXCL | getattr(os, "O_BINARY", 0))
  os.close(fd)

@os__tester
def test_os__copy_file_range(os, **k):
  def rb(n): return fs_readfile(n, os_module=os)
  def wb(n,d): fs_writefile(n, d, os_module=os)
  err = os__copy_file_range__check_availability(os)
  if err: return print("/!\\ " + err)

  wb("first", b'1' * 33000)
  fd = os.open("first", os.O_RDWR | getattr(os, "O_BINARY", 0))
  assert_equal(os.copy_file_range(fd, fd, 33000, 0, 5), 33000)
  os.close(fd)
  assert_equal(os__data_summary(rb("first")), "b'1' * 33005")

  wb("second", b'2' * 34000)
  src = os.open("first", os.O_RDONLY | getattr(os, "O_BINARY", 0))
  dst = os.open("second", os.O_WRONLY | getattr(os, "O_BINARY", 0))
  assert_equal(os.copy_file_range(src, dst, 33000, 0, 0), 33000)
  os.close(src)
  os.close(dst)
  assert_equal(os__data_summary(rb("second")), "b'1' * 33000 b'2' * 1000")

@os__tester
def test_os__copy_file_range__linesep(os, **k):
  def rb(n): return fs_readfile(n, os_module=os)
  def wb(n,d): fs_writefile(n, d, os_module=os)
  err = os__copy_file_range__check_availability(os)
  if err: return print("/!\\ " + err)

  if os.linesep == "\n": print("no need to test O_BINARY ignorance if os.linesep == '\\n'")
  elif os.linesep == "\r\n":
    wb("first", b"FIR\r\nST")
    fd = os.open("first", os.O_RDWR)  # no O_BINARY !
    os.copy_file_range(fd, fd, 7, 0, 7)
    os.close(fd)
    assert_equal(rb("first"), b"FIR\r\nSTFIR\r\nST")

    wb("first", b"FIRST\r\n")
    fd = os.open("first", os.O_RDWR)  # no O_BINARY !
    os.copy_file_range(fd, fd, 6, 0, 6)
    os.close(fd)
    assert_equal(rb("first"), b"FIRST\rFIRST\r")
  else:
    assert_equal(os.linesep, "\r\n")


@os__tester
def test_os__replace(os, **k):
  def wb(n,d): fs_writefile(n, d, os_module=os)

  # with one name relative paths
  wb("first", b"FIRST")
  os.replace("first", "second")
  assert_raise(OSError, lambda: os.replace("third", "second"))
  wb("third", b"THIRD")
  os.replace("third", "second")

@os__tester
def test_os__unlink(os, **k):
  def wb(n,d): fs_writefile(n, d, os_module=os)

  # with one name relative paths
  assert_raise(OSError, lambda: os.unlink("first"))
  wb("first", b"FIRST")
  os.unlink("first")
  assert_raise(OSError, lambda: os.unlink("first"))
  assert_raise(OSError, lambda: os.unlink("second"))

@os__tester
def test_os__listdir(os, **k):
  def wb(n,d): fs_writefile(n, d, os_module=os)

  # with one name relative paths
  assert_equal(os.listdir(), [])
  assert_equal(os.listdir("."), [])
  assert_equal(os.listdir(b"."), [])
  wb("first", b"FIRST")
  assert_equal(os.listdir(), ["first"])
  assert_equal(os.listdir("."), ["first"])
  assert_equal(os.listdir(b"."), [b"first"])
