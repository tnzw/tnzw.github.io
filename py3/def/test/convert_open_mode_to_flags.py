def convert_open_mode_to_flags_tester(fn):
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

@convert_open_mode_to_flags_tester
def test_convert_open_mode_to_flags_r():
  assert_raise(ValueError, lambda: convert_open_mode_to_flags("r"))

@convert_open_mode_to_flags_tester
def test_convert_open_mode_to_flags_rb():
  with open("rb", "w") as f: f.write("read")
  fd = os.open("rb", convert_open_mode_to_flags("rb"))
  f = open("rb", "rb")
  try:
    assert_equal(f.read(), b"read")
    assert_equal(os.read(fd, 1024), b"read")
  finally:
    f.close()
    os.close(fd)

@convert_open_mode_to_flags_tester
def test_convert_open_mode_to_flags_w():
  assert_raise(ValueError, lambda: convert_open_mode_to_flags("w"))

@convert_open_mode_to_flags_tester
def test_convert_open_mode_to_flags_wb():
  fd = os.open("wb", convert_open_mode_to_flags("wb"))
  f = open("wbf", "wb")
  try:
    assert_equal(f.write(b"written1"), 8)
    assert_equal(os.write(fd, b"written1"), 8)
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_raise(io.UnsupportedOperation, lambda: f.read(9))
    assert_raise(OSError, lambda: os.read(fd, 9))
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.write(b"writter"), 7)
    assert_equal(os.write(fd, b"writter"), 7)
  finally:
    f.close()
    os.close(fd)
  assert_equal(open("wbf", "r").read(), "writter1")
  assert_equal(open("wb", "r").read(), "writter1")
  fd = os.open("wb", convert_open_mode_to_flags("wb"))
  f = open("wbf", "wb")
  f.close()
  os.close(fd)
  assert_equal(open("wbf", "r").read(), "")
  assert_equal(open("wb", "r").read(), "")

@convert_open_mode_to_flags_tester
def test_convert_open_mode_to_flags_xb():
  fd = os.open("x", convert_open_mode_to_flags("xb"))
  f = open("xf", "xb")
  try:
    assert_equal(f.write(b"excl1"), 5)
    assert_equal(os.write(fd, b"excl1"), 5)
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_raise(io.UnsupportedOperation, lambda: f.read(6))
    assert_raise(OSError, lambda: os.read(fd, 6))
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.write(b"exsl"), 4)
    assert_equal(os.write(fd, b"exsl"), 4)
  finally:
    f.close()
    os.close(fd)
  assert_equal(open("xf", "r").read(), "exsl1")
  assert_equal(open("x", "r").read(), "exsl1")
  assert_raise(FileExistsError, lambda: open("xf", "xb"))
  assert_raise(FileExistsError, lambda: os.open("x", convert_open_mode_to_flags("xb")))

@convert_open_mode_to_flags_tester
def test_convert_open_mode_to_flags_ab():
  fd = os.open("a", convert_open_mode_to_flags("ab"))
  f = open("af", "ab")
  try:
    assert_equal(f.write(b"written1"), 8)
    assert_equal(os.write(fd, b"written1"), 8)
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_raise(io.UnsupportedOperation, lambda: f.read(9))
    assert_raise(OSError, lambda: os.read(fd, 9))
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.write(b"writter"), 7)
    assert_equal(os.write(fd, b"writter"), 7)
  finally:
    f.close()
    os.close(fd)
  assert_equal(open("af", "r").read(), "written1writter")
  assert_equal(open("a", "r").read(), "written1writter")
  fd = os.open("a", convert_open_mode_to_flags("ab"))
  f = open("af", "ab")
  f.close()
  os.close(fd)
  assert_equal(open("af", "r").read(), "written1writter")
  assert_equal(open("a", "r").read(), "written1writter")

@convert_open_mode_to_flags_tester
def test_convert_open_mode_to_flags_rub():
  assert_raise(FileNotFoundError, lambda: open("ruf", "r+b"))
  assert_raise(FileNotFoundError, lambda: os.open("ru", convert_open_mode_to_flags("r+b")))
  with open("ru", "w") as f: f.write("rdwr23")
  with open("ruf", "w") as f: f.write("rdwr23")
  fd = os.open("ru", convert_open_mode_to_flags("r+b"))
  f = open("ruf", "r+b")
  try:
    assert_equal(f.write(b"rdwr1"), 5)
    assert_equal(os.write(fd, b"rdwr1"), 5)
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.read(7), b"rdwr13")
    assert_equal(os.read(fd, 7), b"rdwr13")
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.write(b"rdwn"), 4)
    assert_equal(os.write(fd, b"rdwn"), 4)
  finally:
    f.close()
    os.close(fd)
  assert_equal(open("ruf", "r").read(), "rdwn13")
  assert_equal(open("ru", "r").read(), "rdwn13")

@convert_open_mode_to_flags_tester
def test_convert_open_mode_to_flags_wub():
  fd = os.open("wu", convert_open_mode_to_flags("w+b"))
  f = open("wuf", "w+b")
  try:
    assert_equal(f.write(b"rdwr1"), 5)
    assert_equal(os.write(fd, b"rdwr1"), 5)
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.read(6), b"rdwr1")
    assert_equal(os.read(fd, 6), b"rdwr1")
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.write(b"rdwn"), 4)
    assert_equal(os.write(fd, b"rdwn"), 4)
  finally:
    f.close()
    os.close(fd)
  assert_equal(open("wuf", "r").read(), "rdwn1")
  assert_equal(open("wu", "r").read(), "rdwn1")

@convert_open_mode_to_flags_tester
def test_convert_open_mode_to_flags_xub():
  fd = os.open("xu", convert_open_mode_to_flags("x+b"))
  f = open("xuf", "x+b")
  try:
    assert_equal(f.write(b"rdwr1"), 5)
    assert_equal(os.write(fd, b"rdwr1"), 5)
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.read(6), b"rdwr1")
    assert_equal(os.read(fd, 6), b"rdwr1")
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.write(b"rdwn"), 4)
    assert_equal(os.write(fd, b"rdwn"), 4)
  finally:
    f.close()
    os.close(fd)
  assert_equal(open("xuf", "r").read(), "rdwn1")
  assert_equal(open("xu", "r").read(), "rdwn1")
  assert_raise(FileExistsError, lambda: open("xuf", "x+b"))
  assert_raise(FileExistsError, lambda: os.open("xu", convert_open_mode_to_flags("x+b")))

@convert_open_mode_to_flags_tester
def test_convert_open_mode_to_flags_aub():
  fd = os.open("au", convert_open_mode_to_flags("a+b"))
  f = open("auf", "a+b")
  try:
    assert_equal(f.write(b"written1"), 8)
    assert_equal(os.write(fd, b"written1"), 8)
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.read(9), b"written1")
    assert_equal(os.read(fd, 9), b"written1")
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.write(b"writter"), 7)
    assert_equal(os.write(fd, b"writter"), 7)
  finally:
    f.close()
    os.close(fd)
  assert_equal(open("auf", "r").read(), "written1writter")
  assert_equal(open("au", "r").read(), "written1writter")
  fd = os.open("au", convert_open_mode_to_flags("a+b"))
  f = open("auf", "a+b")
  f.close()
  os.close(fd)
  assert_equal(open("auf", "r").read(), "written1writter")
  assert_equal(open("au", "r").read(), "written1writter")
