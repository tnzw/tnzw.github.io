def test_bytes_format__lossless_encoding():
  encoding = ("UTF-8", "surrogateescape")
  bb = os.urandom(10000)
  assert_equal(bb, bb.decode(*encoding).encode(*encoding))
