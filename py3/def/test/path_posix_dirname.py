def test_path_posix_dirname_01_R__a_b_c():
  assert_equal(path_posix_dirname( "R:/a/b/c"),  "R:/a/b")
  assert_equal(path_posix_dirname(b"R:/a/b/c"), b"R:/a/b")
def test_path_posix_dirname_02_R__a_b_():
  assert_equal(path_posix_dirname( "R:/a/b/"),  "R:/a")
  assert_equal(path_posix_dirname(b"R:/a/b/"), b"R:/a")
def test_path_posix_dirname_03_R__a_b():
  assert_equal(path_posix_dirname( "R:/a/b"),  "R:/a")
  assert_equal(path_posix_dirname(b"R:/a/b"), b"R:/a")
def test_path_posix_dirname_04_R__a_():
  assert_equal(path_posix_dirname( "R:/a/"),  "R:")
  assert_equal(path_posix_dirname(b"R:/a/"), b"R:")
def test_path_posix_dirname_05_R__a():
  assert_equal(path_posix_dirname( "R:/a"),  "R:")
  assert_equal(path_posix_dirname(b"R:/a"), b"R:")
def test_path_posix_dirname_06_R__():
  assert_equal(path_posix_dirname( "R:/"),  ".")
  assert_equal(path_posix_dirname(b"R:/"), b".")
def test_path_posix_dirname_07_R_():
  assert_equal(path_posix_dirname( "R:"),  ".")
  assert_equal(path_posix_dirname(b"R:"), b".")
def test_path_posix_dirname_08_R():
  assert_equal(path_posix_dirname( "R"),  ".")
  assert_equal(path_posix_dirname(b"R"), b".")
def test_path_posix_dirname_09__a_b_c():
  assert_equal(path_posix_dirname( "/a/b/c"),  "/a/b")
  assert_equal(path_posix_dirname(b"/a/b/c"), b"/a/b")
def test_path_posix_dirname_10__a_b_():
  assert_equal(path_posix_dirname( "/a/b/"),  "/a")
  assert_equal(path_posix_dirname(b"/a/b/"), b"/a")
def test_path_posix_dirname_11__a_b():
  assert_equal(path_posix_dirname( "/a/b"),  "/a")
  assert_equal(path_posix_dirname(b"/a/b"), b"/a")
def test_path_posix_dirname_12__a_():
  assert_equal(path_posix_dirname( "/a/"),  "/")
  assert_equal(path_posix_dirname(b"/a/"), b"/")
def test_path_posix_dirname_13__a():
  assert_equal(path_posix_dirname( "/a"),  "/")
  assert_equal(path_posix_dirname(b"/a"), b"/")
def test_path_posix_dirname_14__():
  assert_equal(path_posix_dirname( "/"),  "/")
  assert_equal(path_posix_dirname(b"/"), b"/")
def test_path_posix_dirname_15_a_b_c():
  assert_equal(path_posix_dirname( "a/b/c"),  "a/b")
  assert_equal(path_posix_dirname(b"a/b/c"), b"a/b")
def test_path_posix_dirname_16_a_b_():
  assert_equal(path_posix_dirname( "a/b/"),  "a")
  assert_equal(path_posix_dirname(b"a/b/"), b"a")
def test_path_posix_dirname_17_a_b():
  assert_equal(path_posix_dirname( "a/b"),  "a")
  assert_equal(path_posix_dirname(b"a/b"), b"a")
def test_path_posix_dirname_18_a_():
  assert_equal(path_posix_dirname( "a/"),  ".")
  assert_equal(path_posix_dirname(b"a/"), b".")
def test_path_posix_dirname_19_a():
  assert_equal(path_posix_dirname( "a"),  ".")
  assert_equal(path_posix_dirname(b"a"), b".")
def test_path_posix_dirname_20_UP_a_UP():
  assert_equal(path_posix_dirname( "../a/.."),  "../a")
  assert_equal(path_posix_dirname(b"../a/.."), b"../a")
def test_path_posix_dirname_21_UP_a_():
  assert_equal(path_posix_dirname( "../a/"),  "..")
  assert_equal(path_posix_dirname(b"../a/"), b"..")
def test_path_posix_dirname_22_UP_a():
  assert_equal(path_posix_dirname( "../a"),  "..")
  assert_equal(path_posix_dirname(b"../a"), b"..")
def test_path_posix_dirname_23_UP_():
  assert_equal(path_posix_dirname( "../"),  ".")
  assert_equal(path_posix_dirname(b"../"), b".")
def test_path_posix_dirname_24_UP():
  assert_equal(path_posix_dirname( ".."),  ".")
  assert_equal(path_posix_dirname(b".."), b".")
def test_path_posix_dirname_25_():
  assert_equal(path_posix_dirname( ""),  ".")
  assert_equal(path_posix_dirname(b""), b".")
