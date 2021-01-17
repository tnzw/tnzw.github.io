def test_pathhelper_ntpath_splitall():
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
    tpath = pathhelper(path, os_module=ntos)
    assert_equal(tpath.splitall(), expected, info=repr(path))

def test_pathhelper_ntpath_pathname():
  def ntos(): pass
  ntos.path = ntpath
  ntos.fspath = os.fspath
  ntos.fsencode = os.fsencode
  ntos.fsdecode = os.fsdecode

  for path in (
    "D:",
    "D:\\",
    "D:\\b",
    "D:\\b\\",
    "",
    "\\",
    "\\b",
    "\\b\\",
    "b",
    "b\\",
  ):
    tpath = pathhelper(path, os_module=ntos)
    assert_equal(tpath.pathname, path)

def test_pathhelper_ntpath_append():
  def ntos(): pass
  ntos.path = ntpath
  ntos.fspath = os.fspath
  ntos.fsencode = os.fsencode
  ntos.fsdecode = os.fsdecode

  for path, append in (
    ("D:",      "C:\\"),
    ("D:\\",    "C:\\"),
    ("D:\\b",   "C:\\"),
    ("D:\\b\\", "C:\\"),
    ("",        "C:\\"),
    ("\\",      "C:\\"),
    ("\\b",     "C:\\"),
    ("\\b\\",   "C:\\"),
    ("b",       "C:\\"),
    ("b\\",     "C:\\"),

    ("D:",      "C:\\a"),
    ("D:\\",    "C:\\a"),
    ("D:\\b",   "C:\\a"),
    ("D:\\b\\", "C:\\a"),
    ("",        "C:\\a"),
    ("\\",      "C:\\a"),
    ("\\b",     "C:\\a"),
    ("\\b\\",   "C:\\a"),
    ("b",       "C:\\a"),
    ("b\\",     "C:\\a"),

    ("D:",      "\\a"),
    ("D:\\",    "\\a"),
    ("D:\\b",   "\\a"),
    ("D:\\b\\", "\\a"),
    ("",        "\\a"),
    ("\\",      "\\a"),
    ("\\b",     "\\a"),
    ("\\b\\",   "\\a"),
    ("b",       "\\a"),
    ("b\\",     "\\a"),
  ):
    tpath = pathhelper(path, os_module=ntos)
    assert_equal(tpath.append(append).pathname, path + append, info=(path, append))
    assert_equal((tpath + append).pathname, path + append, info=(path, append))
    assert_equal((append + tpath).pathname, append + path, info=(path, append))

def test_pathhelper_ntpath_extend(ntos=None):
  def ntos(): pass
  ntos.path = ntpath
  ntos.fspath = os.fspath
  ntos.fsencode = os.fsencode
  ntos.fsdecode = os.fsdecode

  for path, extend, expected in (
    # "C:\\"* are kind of relative paths as they don't start with a separator
    ("D:",      "C:\\", "D:\\C:\\"),  # not "D:C:\\" as isabs("D:") -> False
    ("D:\\",    "C:\\", "D:\\C:\\"),
    ("D:\\b",   "C:\\", "D:\\b\\C:\\"),
    ("D:\\b\\", "C:\\", "D:\\b\\C:\\"),
    ("",        "C:\\", "C:\\"),
    ("\\",      "C:\\", "\\C:\\"),
    ("\\b",     "C:\\", "\\b\\C:\\"),
    ("\\b\\",   "C:\\", "\\b\\C:\\"),
    ("b",       "C:\\", "b\\C:\\"),
    ("b\\",     "C:\\", "b\\C:\\"),

    ("D:",      "C:\\a", "D:\\C:\\a"),  # not "D:C:\\a" as isabs("D:") -> False
    ("D:\\",    "C:\\a", "D:\\C:\\a"),
    ("D:\\b",   "C:\\a", "D:\\b\\C:\\a"),
    ("D:\\b\\", "C:\\a", "D:\\b\\C:\\a"),
    ("",        "C:\\a", "C:\\a"),
    ("\\",      "C:\\a", "\\C:\\a"),
    ("\\b",     "C:\\a", "\\b\\C:\\a"),
    ("\\b\\",   "C:\\a", "\\b\\C:\\a"),
    ("b",       "C:\\a", "b\\C:\\a"),
    ("b\\",     "C:\\a", "b\\C:\\a"),

    ("D:",      "\\a", "D:\\a"),
    ("D:\\",    "\\a", "D:\\a"),
    ("D:\\b",   "\\a", "D:\\b\\a"),
    ("D:\\b\\", "\\a", "D:\\b\\a"),
    ("",        "\\a", "\\a"),
    ("\\",      "\\a", "\\a"),
    ("\\b",     "\\a", "\\b\\a"),
    ("\\b\\",   "\\a", "\\b\\a"),
    ("b",       "\\a", "b\\a"),
    ("b\\",     "\\a", "b\\a"),

    ("D:",      "a", "D:\\a"),  # not "D:a" as isabs("D:") -> False
    ("D:\\",    "a", "D:\\a"),
    ("D:\\b",   "a", "D:\\b\\a"),
    ("D:\\b\\", "a", "D:\\b\\a"),
    ("",        "a", "a"),
    ("\\",      "a", "\\a"),
    ("\\b",     "a", "\\b\\a"),
    ("\\b\\",   "a", "\\b\\a"),
    ("b",       "a", "b\\a"),
    ("b\\",     "a", "b\\a"),
  ):
    tpath = pathhelper(path, os_module=ntos)
    assert_equal(tpath.extend(extend).pathname, expected, info=(path, extend))

def test_pathhelper_posixpath_extend():
  # MUST HAVE SAME RESULT AS WITH ntpath !
  def posixos(): pass
  posixos.path = posixpath
  posixos.fspath = os.fspath
  posixos.fsencode = os.fsencode
  posixos.fsdecode = os.fsdecode

  for path, extend, expected in (
    ("D:",    "C:/", "D:/C:/"),
    ("D:/",   "C:/", "D:/C:/"),
    ("D:/b",  "C:/", "D:/b/C:/"),
    ("D:/b/", "C:/", "D:/b/C:/"),
    ("",      "C:/", "C:/"),
    ("/",     "C:/", "/C:/"),
    ("/b",    "C:/", "/b/C:/"),
    ("/b/",   "C:/", "/b/C:/"),
    ("b",     "C:/", "b/C:/"),
    ("b/",    "C:/", "b/C:/"),

    ("D:",    "C:/a", "D:/C:/a"),
    ("D:/",   "C:/a", "D:/C:/a"),
    ("D:/b",  "C:/a", "D:/b/C:/a"),
    ("D:/b/", "C:/a", "D:/b/C:/a"),
    ("",      "C:/a", "C:/a"),
    ("/",     "C:/a", "/C:/a"),
    ("/b",    "C:/a", "/b/C:/a"),
    ("/b/",   "C:/a", "/b/C:/a"),
    ("b",     "C:/a", "b/C:/a"),
    ("b/",    "C:/a", "b/C:/a"),

    ("D:",    "/a", "D:/a"),
    ("D:/",   "/a", "D:/a"),
    ("D:/b",  "/a", "D:/b/a"),
    ("D:/b/", "/a", "D:/b/a"),
    ("",      "/a", "/a"),
    ("/",     "/a", "/a"),
    ("/b",    "/a", "/b/a"),
    ("/b/",   "/a", "/b/a"),
    ("b",     "/a", "b/a"),
    ("b/",    "/a", "b/a"),

    ("D:",    "a", "D:/a"),
    ("D:/",   "a", "D:/a"),
    ("D:/b",  "a", "D:/b/a"),
    ("D:/b/", "a", "D:/b/a"),
    ("",      "a", "a"),
    ("/",     "a", "/a"),
    ("/b",    "a", "/b/a"),
    ("/b/",   "a", "/b/a"),
    ("b",     "a", "b/a"),
    ("b/",    "a", "b/a"),
  ):
    tpath = pathhelper(path, os_module=posixos)
    assert_equal(tpath.extend(extend).pathname, expected, info=(path, extend))
