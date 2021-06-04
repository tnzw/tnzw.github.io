def test_tuplepath__ntpath_creation():
  def ntos(): pass
  ntos.path = ntpath
  ntos.fspath = os.fspath
  ntos.fsencode = os.fsencode
  ntos.fsdecode = os.fsdecode

  for path, expected in (
    ("D:",      ("D:",)),
    ("D:\\",    ("D:\\",)),
    ("D:\\b",   ("D:\\", "b")),
    ("D:\\b\\", ("D:\\", "b", "")),
    ("",        ("",)),
    ("\\",      ("\\",)),
    ("\\b",     ("\\", "b")),
    ("\\b\\",   ("\\", "b", "")),
    ("b",       ("", "b")),
    ("b\\",     ("", "b", "")),
  ):
    tpath = tuplepath(path, os_module=ntos)
    assert_equal(tpath.tuple, expected, info=repr(path))

def test_tuplepath__ntpath_serialisation():
  def ntos(): pass
  ntos.path = ntpath
  ntos.fspath = os.fspath
  ntos.fsencode = os.fsencode
  ntos.fsdecode = os.fsdecode

  for path, expected in (
    ("D:",      "D:"),
    ("D:\\",    "D:\\"),
    ("D:\\b",   "D:\\b"),
    ("D:\\b\\", "D:\\b\\"),
    ("",        ""),
    ("\\",      "\\"),
    ("\\b",     "\\b"),
    ("\\b\\",   "\\b\\"),
    ("b",       "b"),
    ("b\\",     "b\\"),
  ):
    tpath = tuplepath(path, os_module=ntos)
    assert_equal(tpath.pathname, expected, info=repr(path))

def test_tuplepath__ntpath_append():
  def ntos(): pass
  ntos.path = ntpath
  ntos.fspath = os.fspath
  ntos.fsencode = os.fsencode
  ntos.fsdecode = os.fsdecode

  for path, append, expected in (
    ("D:",      "C:\\", ("D:", "C:", "")),
    ("D:\\",    "C:\\", ("D:\\", "C:", "")),
    ("D:\\b",   "C:\\", ("D:\\", "bC:", "")),
    ("D:\\b\\", "C:\\", ("D:\\", "b", "C:", "")),
    ("",        "C:\\", ("C:\\",)),
    ("\\",      "C:\\", ("\\", "C:", "")),
    ("\\b",     "C:\\", ("\\", "bC:", "")),
    ("\\b\\",   "C:\\", ("\\", "b", "C:", "")),
    ("b",       "C:\\", ("", "bC:", "")),
    ("b\\",     "C:\\", ("", "b", "C:", "")),

    ("D:",      "C:\\a", ("D:", "C:", "a")),
    ("D:\\",    "C:\\a", ("D:\\", "C:", "a")),
    ("D:\\b",   "C:\\a", ("D:\\", "bC:", "a")),
    ("D:\\b\\", "C:\\a", ("D:\\", "b", "C:", "a")),
    ("",        "C:\\a", ("C:\\", "a")),
    ("\\",      "C:\\a", ("\\", "C:", "a")),
    ("\\b",     "C:\\a", ("\\", "bC:", "a")),
    ("\\b\\",   "C:\\a", ("\\", "b", "C:", "a")),
    ("b",       "C:\\a", ("", "bC:", "a")),
    ("b\\",     "C:\\a", ("", "b", "C:", "a")),

    ("D:",      "\\a", ("D:", "", "a")),
    ("D:\\",    "\\a", ("D:\\", "", "a")),
    ("D:\\b",   "\\a", ("D:\\", "b", "a")),
    ("D:\\b\\", "\\a", ("D:\\", "b", "", "a")),
    ("",        "\\a", ("\\", "a")),
    ("\\",      "\\a", ("\\", "", "a")),
    ("\\b",     "\\a", ("\\", "b", "a")),
    ("\\b\\",   "\\a", ("\\", "b", "", "a")),
    ("b",       "\\a", ("", "b", "a")),
    ("b\\",     "\\a", ("", "b", "", "a")),
  ):
    tpath = tuplepath(path, os_module=ntos)
    assert_equal(tpath.append(append).tuple, expected, info=(path, append))
    assert_equal(tpath.append(append).pathname, path + append, info=(path, append, expected))
    assert_equal((tpath + append).pathname, path + append, info=(path, append, expected))
    assert_equal((append + tpath).pathname, append + path, info=(path, append, expected))

def test_tuplepath__ntpath_extend():
  def ntos(): pass
  ntos.path = ntpath
  ntos.fspath = os.fspath
  ntos.fsencode = os.fsencode
  ntos.fsdecode = os.fsdecode

  for path, extend, expected in (
    # "C:\\"* are kind of relative paths as they don't start with a separator
    ("D:",      "C:\\", ("D:", "C:", "")),
    ("D:\\",    "C:\\", ("D:\\", "C:", "")),
    ("D:\\b",   "C:\\", ("D:\\", "b", "C:", "")),
    ("D:\\b\\", "C:\\", ("D:\\", "b", "C:", "")),
    ("",        "C:\\", ("C:\\",)),
    ("\\",      "C:\\", ("\\", "C:", "")),
    ("\\b",     "C:\\", ("\\", "b", "C:", "")),
    ("\\b\\",   "C:\\", ("\\", "b", "C:", "")),
    ("b",       "C:\\", ("", "b", "C:", "")),
    ("b\\",     "C:\\", ("", "b", "C:", "")),

    ("D:",      "C:\\a", ("D:", "C:", "a")),
    ("D:\\",    "C:\\a", ("D:\\", "C:", "a")),
    ("D:\\b",   "C:\\a", ("D:\\", "b", "C:", "a")),
    ("D:\\b\\", "C:\\a", ("D:\\", "b", "C:", "a")),
    ("",        "C:\\a", ("C:\\", "a")),
    ("\\",      "C:\\a", ("\\", "C:", "a")),
    ("\\b",     "C:\\a", ("\\", "b", "C:", "a")),
    ("\\b\\",   "C:\\a", ("\\", "b", "C:", "a")),
    ("b",       "C:\\a", ("", "b", "C:", "a")),
    ("b\\",     "C:\\a", ("", "b", "C:", "a")),

    ("D:",      "\\a", ("D:", "a")),
    ("D:\\",    "\\a", ("D:\\", "a")),
    ("D:\\b",   "\\a", ("D:\\", "b", "a")),
    ("D:\\b\\", "\\a", ("D:\\", "b", "a")),
    ("",        "\\a", ("\\", "a")),
    ("\\",      "\\a", ("\\", "a")),
    ("\\b",     "\\a", ("\\", "b", "a")),
    ("\\b\\",   "\\a", ("\\", "b", "a")),
    ("b",       "\\a", ("", "b", "a")),
    ("b\\",     "\\a", ("", "b", "a")),

    ("D:",      "a", ("D:", "a")),
    ("D:\\",    "a", ("D:\\", "a")),
    ("D:\\b",   "a", ("D:\\", "b", "a")),
    ("D:\\b\\", "a", ("D:\\", "b", "a")),
    ("",        "a", ("", "a")),
    ("\\",      "a", ("\\", "a")),
    ("\\b",     "a", ("\\", "b", "a")),
    ("\\b\\",   "a", ("\\", "b", "a")),
    ("b",       "a", ("", "b", "a")),
    ("b\\",     "a", ("", "b", "a")),
  ):
    tpath = tuplepath(path, os_module=ntos)
    assert_equal(tpath.extend(extend).tuple, expected, info=(path, extend))

def test_tuplepath__ntpath_extend():
  def posixos(): pass
  posixos.path = posixpath
  posixos.fspath = os.fspath
  posixos.fsencode = os.fsencode
  posixos.fsdecode = os.fsdecode

  for path, extend, expected in (
    ("D:",    "C:/", ("", "D:", "C:", "")),
    ("D:/",   "C:/", ("", "D:", "C:", "")),
    ("D:/b",  "C:/", ("", "D:", "b", "C:", "")),
    ("D:/b/", "C:/", ("", "D:", "b", "C:", "")),
    ("",      "C:/", ("", "C:", "")),
    ("/",     "C:/", ("/", "C:", "")),
    ("/b",    "C:/", ("/", "b", "C:", "")),
    ("/b/",   "C:/", ("/", "b", "C:", "")),
    ("b",     "C:/", ("", "b", "C:", "")),
    ("b/",    "C:/", ("", "b", "C:", "")),

    ("D:",    "C:/a", ("", "D:", "C:", "a")),
    ("D:/",   "C:/a", ("", "D:", "C:", "a")),
    ("D:/b",  "C:/a", ("", "D:", "b", "C:", "a")),
    ("D:/b/", "C:/a", ("", "D:", "b", "C:", "a")),
    ("",      "C:/a", ("", "C:", "a")),
    ("/",     "C:/a", ("/", "C:", "a")),
    ("/b",    "C:/a", ("/", "b", "C:", "a")),
    ("/b/",   "C:/a", ("/", "b", "C:", "a")),
    ("b",     "C:/a", ("", "b", "C:", "a")),
    ("b/",    "C:/a", ("", "b", "C:", "a")),

    ("D:",    "/a", ("", "D:", "a")),
    ("D:/",   "/a", ("", "D:", "a")),
    ("D:/b",  "/a", ("", "D:", "b", "a")),
    ("D:/b/", "/a", ("", "D:", "b", "a")),
    ("",      "/a", ("/", "a")),
    ("/",     "/a", ("/", "a")),
    ("/b",    "/a", ("/", "b", "a")),
    ("/b/",   "/a", ("/", "b", "a")),
    ("b",     "/a", ("", "b", "a")),
    ("b/",    "/a", ("", "b", "a")),

    ("D:",    "a", ("", "D:", "a")),
    ("D:/",   "a", ("", "D:", "a")),
    ("D:/b",  "a", ("", "D:", "b", "a")),
    ("D:/b/", "a", ("", "D:", "b", "a")),
    ("",      "a", ("", "a")),
    ("/",     "a", ("/", "a")),
    ("/b",    "a", ("/", "b", "a")),
    ("/b/",   "a", ("/", "b", "a")),
    ("b",     "a", ("", "b", "a")),
    ("b/",    "a", ("", "b", "a")),
  ):
    tpath = tuplepath(path, os_module=posixos)
    assert_equal(tpath.extend(extend).tuple, expected, info=(path, extend))

def test_tuplepath__append_types():
  assert_equal(tuplepath("one").append(b"two").pathname, "onetwo")
  assert_equal(tuplepath(b"one").append("two").pathname, b"onetwo")

def test_tuplepath__extend_types():
  sep = os.sep
  sepb = sep.encode()
  assert_equal(tuplepath("one").extend(b"two").pathname, f"one{sep}two")
  assert_equal(tuplepath(b"one").extend("two").pathname, b"one"+sepb+b"two")

def test_tuplepath__mixed_type():
  assert_equal(tuplepath(("/", b"element")).pathname, "/element")
  assert_equal(tuplepath((b"/", "element")).pathname, b"/element")
