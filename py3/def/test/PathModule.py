def test_PathModule():

  def mega_mega_iter_test_string(max_comp):
    chars = ("a", ".a", "..a", "a.", ".a.", "..a.", "a.b", ".a.b", "..a.b", "/", ".", "..", ":", "?")
    yield ""
    if max_comp > 0:
      for c in chars:
        for s in iter_test_string(max_comp - 1):
          yield c + s

  def mega_iter_test_string():
    for drive in ("", "W", "D:"):
      for root in ("", "/", "\\", "//", "\\\\", "///", "\\\\\\"):
        for sep in ("/", "\\"):
          for c1 in ("", sep, ".", "..", "?", ":"):
            for c2 in ("", sep):
              for c3 in ("", sep, "a", "E:", ".", ".."):
                for c4 in ("", sep):
                  for c5 in ("", "a", ".a", "..a", "a.", ".a.", "..a.", "a.b", ".a.b", "..a.b", ".", ".."):
                    for c6 in ("", sep, sep * 2):
                      yield drive + root + c1 + c2 + c3 + c4 + c5 + c6
                      yield os.fsencode(drive + root + c1 + c2 + c3 + c4 + c5 + c6)

  def iter_test_string():
    return iter((
      "",
      "a", "a/", "a//", "a/b", "a//b", "a/b/", "a/b//", "a//b/", "a//b//",
      ".", "./", ".//", "./b", ".//b", "./b/", "./b//", ".//b/", ".//b//",
      "a", "a/", "a//", "a/.", "a//.", "a/./", "a/.//", "a//./", "a//.//",
      ".", "./", ".//", "./.", ".//.", "././", "././/", ".//./", ".//.//",
      "..", "../", "..//", "../b", "..//b", "../b/", "../b//", "..//b/", "..//b//",
      "a", "a/", "a//", "a/..", "a//..", "a/../", "a/..//", "a//../", "a//..//",
      "..", "../", "..//", "../..", "..//..", "../../", "../..//", "..//../", "..//..//",

      "/", "//",
      "/a", "//a", "/a/", "/a//", "//a/", "/a/b", "/a//b", "/a/b/", "/a/b//", "/a//b/", "/a//b//",
    ))


  assert_equal(PathModule.make_nt_style().splitdrive("C://"), ntpath.splitdrive("C://"))
  assert_equal(PathModule.make_nt_style().splitdrive(".://"), ntpath.splitdrive(".://"))
  assert_equal(PathModule.make_nt_style().splitdrive("C:D//"), ntpath.splitdrive("C:D//"))
  assert_equal(PathModule.make_nt_style().splitdrive("//host/computer"), ntpath.splitdrive("//host/computer"))
  assert_equal(PathModule.make_nt_style().splitdrive("//host/computer/dir"), ntpath.splitdrive("//host/computer/dir"))
  assert_equal(PathModule.make_nt_style(altsep="//").splitdrive("////host//computer//dir"), ("////host//computer", "//dir"))
  assert_equal(PathModule.make_nt_style(allow_unc_path=False).splitdrive("//host/computer/dir"), ("", "//host/computer/dir"))

  assert_equal(PathModule.make_nt_style().split("C://dir"), ntpath.split("C://dir"))
  assert_equal(PathModule.make_nt_style().split("//host/computer/dir"), ntpath.split("//host/computer/dir"))
  assert_equal(PathModule.make_nt_style().split("//host/computer//dir"), ntpath.split("//host/computer//dir"))
  assert_equal(PathModule.make_posix_style().split("//host/computer//dir"), posixpath.split("//host/computer//dir"))
  assert_equal(PathModule.make_url_style().split("//host/computer//dir"), ("//host/computer/", "dir"))

  assert_equal(PathModule.make_posix_style().basename("myfile.py"), "myfile.py")
  assert_equal(PathModule.make_posix_style().basename("/myfile.py"), "myfile.py")
  assert_equal(PathModule.make_nt_style().basename("C:"), "")

  assert_equal(PathModule.make_posix_style().splitext("myfile.py"), ("myfile", ".py"))
  assert_equal(PathModule.make_posix_style().splitext("/myfile.py"), ("/myfile", ".py"))

  assert_equal(PathModule.make_posix_style().normpath("/lol"), posixpath.normpath("/lol"))
  assert_equal(PathModule.make_posix_style().normpath("//lol"), posixpath.normpath("//lol"))
  assert_equal(PathModule.make_posix_style().normpath("///lol"), posixpath.normpath("/lol"))
  assert_equal(PathModule.make_url_style().normpath("///lol"), "///lol")
  assert_equal(PathModule.make_nt_style().normpath("//?/lol/.././.."), ntpath.normpath("//?/lol/.././.."))
  assert_equal(PathModule.make_nt_style().normpath("\\\\?\\lol\\..\\.\\.."), ntpath.normpath("\\\\?\\lol\\..\\.\\.."))
  assert_equal(PathModule.make_nt_style().normpath("\\\\??\\lol\\..\\.\\.."), ntpath.normpath("\\\\??\\lol\\..\\.\\.."))

  assert_equal(PathModule.make_nt_style().isabs("C:"), ntpath.isabs("C:"))
  assert_equal(PathModule.make_nt_style().isabs("C:/"), ntpath.isabs("C:/"))
  assert_equal(PathModule.make_nt_style().isabs("//host/computer"), ntpath.isabs("//host/computer"))
  assert_equal(PathModule.make_nt_style().isabs("//host/computer/dir"), ntpath.isabs("//host/computer/dir"))
  assert_equal(PathModule.make_nt_style().isabs("/"), ntpath.isabs("/"))
  assert_equal(PathModule.make_nt_style().isabs("."), ntpath.isabs("."))

  #iter_test_string = mega_iter_test_string
  #for s in iter_test_string(): assert_equal(PathModule.make_posix_style().split(s), posixpath.split(s), info=f"split({s!r})")
  #for s in iter_test_string(): assert_equal(PathModule.make_nt_style().split(s), ntpath.split(s), info=f"split({s!r})")

