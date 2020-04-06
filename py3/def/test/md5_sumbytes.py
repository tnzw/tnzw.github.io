def test_md5_sumbytes_empty():
  assert md5_sumbytes(b"") == b"\xd4\x1d\x8c\xd9\x8f\x00\xb2\x04\xe9\x80\x09\x98\xec\xf8\x42\x7e", md5_sumbytes(b"")
def test_md5_sumbytes_quickbrownfox():
  assert md5_sumbytes(b"The quick brown fox jumps over the lazy dog") == b"\x9e\x10\x7d\x9d\x37\x2b\xb6\x82\x6b\xd8\x1d\x35\x42\xa4\x19\xd6", md5_sumbytes(b"The quick brown fox jumps over the lazy dog")
def test_md5_sumbytes_quickbrownfoxdot():
  assert md5_sumbytes(b"The quick brown fox jumps over the lazy dog.") == b"\xe4\xd9\x09\xc2\x90\xd0\xfb\x1c\xa0\x68\xff\xad\xdf\x22\xcb\xd0", md5_sumbytes(b"The quick brown fox jumps over the lazy dog.")
