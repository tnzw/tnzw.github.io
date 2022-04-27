def test_ntpath_checkbasename():
  assert_raise(ValueError, lambda: ntpath_checkbasename("con"))
  assert_raise(ValueError, lambda: ntpath_checkbasename("prn."))
  assert_raise(ValueError, lambda: ntpath_checkbasename("aux.txt"))
  assert_raise(ValueError, lambda: ntpath_checkbasename("lpt1.tar.gz"))
  assert_raise(ValueError, lambda: ntpath_checkbasename("\x00.tar.gz"))
  assert_raise(ValueError, lambda: ntpath_checkbasename("\x19.tar.gz"))
  assert_raise(ValueError, lambda: ntpath_checkbasename("\x20.tar.gz"))
  assert_raise(ValueError, lambda: ntpath_checkbasename(" .tar.gz"))
  assert_raise(ValueError, lambda: ntpath_checkbasename("a .tar.gz "))
  assert_raise(ValueError, lambda: ntpath_checkbasename("a .tar.gz."))
  ntpath_checkbasename("a .tar.gz")
  ntpath_checkbasename(".tar.gz")
  ntpath_checkbasename(".con.txt")
  ntpath_checkbasename(".con")
