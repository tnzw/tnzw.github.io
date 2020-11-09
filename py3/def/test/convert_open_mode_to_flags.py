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
  with open("r", "w") as f: f.write("réad")
  fd = os.open("r", convert_open_mode_to_flags("r"))
  f = open("r", "r")
  try:
    assert_equal(f.read(), "réad")
    assert_equal(os.read(fd, 1024), b"r\xe9ad")
  finally:
    f.close()
    os.close(fd)

@convert_open_mode_to_flags_tester
def test_convert_open_mode_to_flags_rb():
  with open("rb", "w") as f: f.write("réad")
  fd = os.open("rb", convert_open_mode_to_flags("rb"))
  f = open("rb", "rb")
  try:
    assert_equal(f.read(), b"r\xe9ad")
    assert_equal(os.read(fd, 1024), b"r\xe9ad")
  finally:
    f.close()
    os.close(fd)

@convert_open_mode_to_flags_tester
def test_convert_open_mode_to_flags_w():
  fd = os.open("w", convert_open_mode_to_flags("w"))
  f = open("wf", "w")
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
  assert_equal(open("wf", "r").read(), "writtér1")
  assert_equal(open("w", "r").read(), "writtér1")
  fd = os.open("w", convert_open_mode_to_flags("w"))
  f = open("wf", "w")
  f.close()
  os.close(fd)
  assert_equal(open("wf", "r").read(), "")
  assert_equal(open("w", "r").read(), "")

@convert_open_mode_to_flags_tester
def test_convert_open_mode_to_flags_wb():
  fd = os.open("wb", convert_open_mode_to_flags("wb"))
  f = open("wbf", "wb")
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
  fd = os.open("wb", convert_open_mode_to_flags("w"))
  f = open("wbf", "w")
  f.close()
  os.close(fd)
  assert_equal(open("wbf", "r").read(), "")
  assert_equal(open("wb", "r").read(), "")

@convert_open_mode_to_flags_tester
def test_convert_open_mode_to_flags_x():
  fd = os.open("x", convert_open_mode_to_flags("x"))
  f = open("xf", "x")
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
  assert_raise(FileExistsError, lambda: open("xf", "x"))
  assert_raise(FileExistsError, lambda: os.open("x", convert_open_mode_to_flags("x")))

@convert_open_mode_to_flags_tester
def test_convert_open_mode_to_flags_a():
  fd = os.open("a", convert_open_mode_to_flags("a"))
  f = open("af", "a")
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
  fd = os.open("a", convert_open_mode_to_flags("a"))
  f = open("af", "a")
  f.close()
  os.close(fd)
  assert_equal(open("af", "r").read(), "writtén1writtér")
  assert_equal(open("a", "r").read(), "writtén1writtér")


@convert_open_mode_to_flags_tester
def test_convert_open_mode_to_flags_ru():
  assert_raise(FileNotFoundError, lambda: open("ruf", "r+"))
  assert_raise(FileNotFoundError, lambda: os.open("ru", convert_open_mode_to_flags("r+")))
  with open("ru", "w") as f: f.write("rdwr23")
  with open("ruf", "w") as f: f.write("rdwr23")
  fd = os.open("ru", convert_open_mode_to_flags("r+"))
  f = open("ruf", "r+")
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

@convert_open_mode_to_flags_tester
def test_convert_open_mode_to_flags_wu():
  fd = os.open("wu", convert_open_mode_to_flags("w+"))
  f = open("wuf", "w+")
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

@convert_open_mode_to_flags_tester
def test_convert_open_mode_to_flags_xu():
  fd = os.open("xu", convert_open_mode_to_flags("x+"))
  f = open("xuf", "x+")
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
  assert_raise(FileExistsError, lambda: open("xuf", "x+"))
  assert_raise(FileExistsError, lambda: os.open("xu", convert_open_mode_to_flags("x+")))

@convert_open_mode_to_flags_tester
def test_convert_open_mode_to_flags_au():
  fd = os.open("au", convert_open_mode_to_flags("a+"))
  f = open("auf", "a+")
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
  fd = os.open("au", convert_open_mode_to_flags("a+"))
  f = open("auf", "a+")
  f.close()
  os.close(fd)
  assert_equal(open("auf", "r").read(), "writtén1writtér")
  assert_equal(open("au", "r").read(), "writtén1writtér")
