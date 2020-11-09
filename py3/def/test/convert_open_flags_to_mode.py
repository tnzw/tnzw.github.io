def convert_open_flags_to_mode_tester(fn):
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

@convert_open_flags_to_mode_tester
def test_convert_open_flags_to_mode_RDONLY():
  flags = os.O_RDONLY
  with open("r", "w") as f: f.write("réad")
  fd = os.open("r", flags)
  f = open("r", convert_open_flags_to_mode(flags))
  try:
    assert_equal(f.read(), "réad")
    assert_equal(os.read(fd, 1024), b"r\xe9ad")
  finally:
    f.close()
    os.close(fd)

@convert_open_flags_to_mode_tester
def test_convert_open_flags_to_mode_RDONLY_BINARY():
  flags = os.O_RDONLY | os.O_BINARY
  with open("rb", "w") as f: f.write("réad")
  fd = os.open("rb", flags)
  f = open("rb", convert_open_flags_to_mode(flags))
  try:
    assert_equal(f.read(), b"r\xe9ad")
    assert_equal(os.read(fd, 1024), b"r\xe9ad")
  finally:
    f.close()
    os.close(fd)

def test_convert_open_flags_to_mode_WRONLY():
  assert_raise(ValueError, lambda: convert_open_flags_to_mode(os.O_WRONLY))
def test_convert_open_flags_to_mode_WRONLY_CREAT():
  assert_raise(ValueError, lambda: convert_open_flags_to_mode(os.O_WRONLY|os.O_CREAT))

@convert_open_flags_to_mode_tester
def test_convert_open_flags_to_mode_WRONLY_CREAT_TRUNC():
  flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
  fd = os.open("w", flags)
  f = open("wf", convert_open_flags_to_mode(flags))
  try:
    assert_equal(f.write("writtén1"), 8)
    assert_equal(os.write(fd, b"writt\xe9n1"), 8)
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_raise(io.UnsupportedOperation, lambda: f.read(9))
    assert_raise(OSError, lambda: os.read(fd, 9))
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.write("writtér"), 7)
    assert_equal(os.write(fd, b"writt\xe9r"), 7)
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
  finally:
    f.close()
    os.close(fd)
  assert_equal(open("wf", "r").read(), "writtér1")
  assert_equal(open("w", "r").read(), "writtér1")
  fd = os.open("w", flags)
  f = open("wf", convert_open_flags_to_mode(flags))
  f.close()
  os.close(fd)
  assert_equal(open("wf", "r").read(), "")
  assert_equal(open("w", "r").read(), "")

@convert_open_flags_to_mode_tester
def test_convert_open_flags_to_mode_WRONLY_CREAT_TRUNC_BINARY():
  flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_BINARY
  fd = os.open("wb", flags)
  f = open("wbf", convert_open_flags_to_mode(flags))
  try:
    assert_equal(f.write(b"writt\xe9n1"), 8)
    assert_equal(os.write(fd, b"writt\xe9n1"), 8)
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_raise(io.UnsupportedOperation, lambda: f.read(9))
    assert_raise(OSError, lambda: os.read(fd, 9))
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.write(b"writt\xe9r"), 7)
    assert_equal(os.write(fd, b"writt\xe9r"), 7)
  finally:
    f.close()
    os.close(fd)
  assert_equal(open("wbf", "rb").read(), b"writt\xe9r1")
  assert_equal(open("wb", "rb").read(), b"writt\xe9r1")
  fd = os.open("wb", flags)
  f = open("wbf", convert_open_flags_to_mode(flags))
  f.close()
  os.close(fd)
  assert_equal(open("wbf", "r").read(), "")
  assert_equal(open("wb", "r").read(), "")

@convert_open_flags_to_mode_tester
def test_convert_open_flags_to_mode_WRONLY_CREAT_EXCL(additional_flags=0):
  flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | additional_flags
  fd = os.open("x", flags)
  f = open("xf", convert_open_flags_to_mode(flags))
  try:
    assert_equal(f.write("excl1"), 5)
    assert_equal(os.write(fd, b"excl1"), 5)
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_raise(io.UnsupportedOperation, lambda: f.read(6))
    assert_raise(OSError, lambda: os.read(fd, 6))
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.write("exsl"), 4)
    assert_equal(os.write(fd, b"exsl"), 4)
  finally:
    f.close()
    os.close(fd)
  assert_equal(open("xf", "r").read(), "exsl1")
  assert_equal(open("x", "r").read(), "exsl1")
  assert_raise(FileExistsError, lambda: open("xf", convert_open_flags_to_mode(flags)))
  assert_raise(FileExistsError, lambda: os.open("x", flags))

def test_convert_open_flags_to_mode_WRONLY_CREAT_EXCL_TRUNC():
  return test_convert_open_flags_to_mode_WRONLY_CREAT_EXCL(os.O_TRUNC)

@convert_open_flags_to_mode_tester
def test_convert_open_flags_to_mode_WRONLY_CREAT_APPEND():
  flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND
  fd = os.open("a", flags)
  f = open("af", convert_open_flags_to_mode(flags))
  try:
    assert_equal(f.write("writtén1"), 8)
    assert_equal(os.write(fd, b"writt\xe9n1"), 8)
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_raise(io.UnsupportedOperation, lambda: f.read(9))
    assert_raise(OSError, lambda: os.read(fd, 9))
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.write("writtér"), 7)
    assert_equal(os.write(fd, b"writt\xe9r"), 7)
  finally:
    f.close()
    os.close(fd)
  assert_equal(open("af", "r").read(), "writtén1writtér")
  assert_equal(open("a", "r").read(), "writtén1writtér")
  fd = os.open("a", flags)
  f = open("af", convert_open_flags_to_mode(flags))
  f.close()
  os.close(fd)
  assert_equal(open("af", "r").read(), "writtén1writtér")
  assert_equal(open("a", "r").read(), "writtén1writtér")

def test_convert_open_flags_to_mode_WRONLY_CREAT_APPEND_TRUNC():
  assert_raise(ValueError, lambda: convert_open_flags_to_mode(os.O_WRONLY|os.O_CREAT|os.O_APPEND|os.O_TRUNC))
def test_convert_open_flags_to_mode_WRONLY_CREAT_APPEND_EXCL():
  assert_raise(ValueError, lambda: convert_open_flags_to_mode(os.O_WRONLY|os.O_CREAT|os.O_APPEND|os.O_EXCL))

@convert_open_flags_to_mode_tester
def test_convert_open_flags_to_mode_RDWR():
  flags = os.O_RDWR
  assert_raise(FileNotFoundError, lambda: open("ruf", convert_open_flags_to_mode(flags)))
  assert_raise(FileNotFoundError, lambda: os.open("ru", flags))
  with open("ru", "w") as f: f.write("rdwr23")
  with open("ruf", "w") as f: f.write("rdwr23")
  fd = os.open("ru", flags)
  f = open("ruf", convert_open_flags_to_mode(flags))
  try:
    assert_equal(f.write("rdwr1"), 5)
    assert_equal(os.write(fd, b"rdwr1"), 5)
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.read(7), "rdwr13")
    assert_equal(os.read(fd, 7), b"rdwr13")
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.write("rdwn"), 4)
    assert_equal(os.write(fd, b"rdwn"), 4)
  finally:
    f.close()
    os.close(fd)
  assert_equal(open("ruf", "r").read(), "rdwn13")
  assert_equal(open("ru", "r").read(), "rdwn13")

def test_convert_open_flags_to_mode_RDWR_CREAT():
  assert_raise(ValueError, lambda: convert_open_flags_to_mode(os.O_RDWR|os.O_CREAT))

@convert_open_flags_to_mode_tester
def test_convert_open_flags_to_mode_RDWR_CREAT_TRUNC():
  flags = os.O_RDWR | os.O_CREAT | os.O_TRUNC
  fd = os.open("wu", flags)
  f = open("wuf", convert_open_flags_to_mode(flags))
  try:
    assert_equal(f.write("rdwr1"), 5)
    assert_equal(os.write(fd, b"rdwr1"), 5)
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.read(6), "rdwr1")
    assert_equal(os.read(fd, 6), b"rdwr1")
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.write("rdwn"), 4)
    assert_equal(os.write(fd, b"rdwn"), 4)
  finally:
    f.close()
    os.close(fd)
  assert_equal(open("wuf", "r").read(), "rdwn1")
  assert_equal(open("wu", "r").read(), "rdwn1")

@convert_open_flags_to_mode_tester
def test_convert_open_flags_to_mode_RDWR_CREAT_EXCL(additional_flags=0):
  flags = os.O_RDWR | os.O_CREAT | os.O_EXCL | additional_flags
  fd = os.open("xu", flags)
  f = open("xuf", convert_open_flags_to_mode(flags))
  try:
    assert_equal(f.write("rdwr1"), 5)
    assert_equal(os.write(fd, b"rdwr1"), 5)
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.read(6), "rdwr1")
    assert_equal(os.read(fd, 6), b"rdwr1")
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.write("rdwn"), 4)
    assert_equal(os.write(fd, b"rdwn"), 4)
  finally:
    f.close()
    os.close(fd)
  assert_equal(open("xuf", "r").read(), "rdwn1")
  assert_equal(open("xu", "r").read(), "rdwn1")
  assert_raise(FileExistsError, lambda: open("xuf", convert_open_flags_to_mode(flags)))
  assert_raise(FileExistsError, lambda: os.open("xu", flags))

def test_convert_open_flags_to_mode_RDWR_CREAT_EXCL_TRUNC():
  return test_convert_open_flags_to_mode_RDWR_CREAT_EXCL(os.O_TRUNC)

@convert_open_flags_to_mode_tester
def test_convert_open_flags_to_mode_RDWR_CREAT_APPEND():
  flags = os.O_RDWR | os.O_CREAT | os.O_APPEND
  fd = os.open("au", flags)
  f = open("auf", convert_open_flags_to_mode(flags))
  try:
    assert_equal(f.write("writtén1"), 8)
    assert_equal(os.write(fd, b"writt\xe9n1"), 8)
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.read(9), "writtén1")
    assert_equal(os.read(fd, 9), b"writt\xe9n1")
    f.seek(0, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    assert_equal(f.write("writtér"), 7)
    assert_equal(os.write(fd, b"writt\xe9r"), 7)
  finally:
    f.close()
    os.close(fd)
  assert_equal(open("auf", "r").read(), "writtén1writtér")
  assert_equal(open("au", "r").read(), "writtén1writtér")
  fd = os.open("au", flags)
  f = open("auf", convert_open_flags_to_mode(flags))
  f.close()
  os.close(fd)
  assert_equal(open("auf", "r").read(), "writtén1writtér")
  assert_equal(open("au", "r").read(), "writtén1writtér")
