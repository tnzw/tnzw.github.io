def test_url_path_dirname_01_R__a_b_c():
  assert_equal(url_path_dirname( "R:/a/b/c"),  "R:/a/b")
  assert_equal(url_path_dirname(b"R:/a/b/c"), b"R:/a/b")
def test_url_path_dirname_02_R__a_b_():
  assert_equal(url_path_dirname( "R:/a/b/"),  "R:/a/b")
  assert_equal(url_path_dirname(b"R:/a/b/"), b"R:/a/b")
def test_url_path_dirname_03_R__a_b():
  assert_equal(url_path_dirname( "R:/a/b"),  "R:/a")
  assert_equal(url_path_dirname(b"R:/a/b"), b"R:/a")
def test_url_path_dirname_04_R__a_():
  assert_equal(url_path_dirname( "R:/a/"),  "R:/a")
  assert_equal(url_path_dirname(b"R:/a/"), b"R:/a")
def test_url_path_dirname_05_R__a():
  assert_equal(url_path_dirname( "R:/a"),  "R:")
  assert_equal(url_path_dirname(b"R:/a"), b"R:")
def test_url_path_dirname_06_R__():
  assert_equal(url_path_dirname( "R:/"),  "R:")
  assert_equal(url_path_dirname(b"R:/"), b"R:")
def test_url_path_dirname_07_R_():
  assert_equal(url_path_dirname( "R:"),  "")
  assert_equal(url_path_dirname(b"R:"), b"")
def test_url_path_dirname_08_R():
  assert_equal(url_path_dirname( "R"),  "")
  assert_equal(url_path_dirname(b"R"), b"")
def test_url_path_dirname_09__a_b_c():
  assert_equal(url_path_dirname( "/a/b/c"),  "/a/b")
  assert_equal(url_path_dirname(b"/a/b/c"), b"/a/b")
def test_url_path_dirname_10__a_b_():
  assert_equal(url_path_dirname( "/a/b/"),  "/a/b")
  assert_equal(url_path_dirname(b"/a/b/"), b"/a/b")
def test_url_path_dirname_11__a_b():
  assert_equal(url_path_dirname( "/a/b"),  "/a")
  assert_equal(url_path_dirname(b"/a/b"), b"/a")
def test_url_path_dirname_12__a_():
  assert_equal(url_path_dirname( "/a/"),  "/a")
  assert_equal(url_path_dirname(b"/a/"), b"/a")
def test_url_path_dirname_13__a():
  assert_equal(url_path_dirname( "/a"),  "/")
  assert_equal(url_path_dirname(b"/a"), b"/")
def test_url_path_dirname_14__():
  assert_equal(url_path_dirname( "/"),  "/")
  assert_equal(url_path_dirname(b"/"), b"/")
def test_url_path_dirname_15_a_b_c():
  assert_equal(url_path_dirname( "a/b/c"),  "a/b")
  assert_equal(url_path_dirname(b"a/b/c"), b"a/b")
def test_url_path_dirname_16_a_b_():
  assert_equal(url_path_dirname( "a/b/"),  "a/b")
  assert_equal(url_path_dirname(b"a/b/"), b"a/b")
def test_url_path_dirname_17_a_b():
  assert_equal(url_path_dirname( "a/b"),  "a")
  assert_equal(url_path_dirname(b"a/b"), b"a")
def test_url_path_dirname_18_a_():
  assert_equal(url_path_dirname( "a/"),  "a")
  assert_equal(url_path_dirname(b"a/"), b"a")
def test_url_path_dirname_19_a():
  assert_equal(url_path_dirname( "a"),  "")
  assert_equal(url_path_dirname(b"a"), b"")
def test_url_path_dirname_20_UP_a_UP():
  assert_equal(url_path_dirname( "../a/.."),  "../a")
  assert_equal(url_path_dirname(b"../a/.."), b"../a")
def test_url_path_dirname_21_UP_a_():
  assert_equal(url_path_dirname( "../a/"),  "../a")
  assert_equal(url_path_dirname(b"../a/"), b"../a")
def test_url_path_dirname_22_UP_a():
  assert_equal(url_path_dirname( "../a"),  "..")
  assert_equal(url_path_dirname(b"../a"), b"..")
def test_url_path_dirname_23_UP_():
  assert_equal(url_path_dirname( "../"),  "..")
  assert_equal(url_path_dirname(b"../"), b"..")
def test_url_path_dirname_24_UP():
  assert_equal(url_path_dirname( ".."),  "")
  assert_equal(url_path_dirname(b".."), b"")
def test_url_path_dirname_25_():
  assert_equal(url_path_dirname( ""),  "")
  assert_equal(url_path_dirname(b""), b"")
