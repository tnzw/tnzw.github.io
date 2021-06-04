def test_PipeIO():
  p = PipeIO()
  assert_equal(p.write(b"abc"), 3)
  assert_equal(p.write(b"d\nef"), 4)
  assert_equal(p.readline(), b"abcd\n")
  assert_equal(p.readline(), b"ef")
  assert_equal(p.readline(), b"")  # as if EOF
  assert_equal(p.write(b"ghi"), 3)
  assert_equal(p.write(b"j\nkl"), 4)
  assert_equal(p.readline(), b"ghij\n")
  assert_equal(p.readline(), b"kl")
  assert_equal(p.readline(), b"")  # as if EOF
  assert_equal(p.write(b"abc"), 3)
  assert_equal(p.lwrite(b"def"), 3)
  assert_equal(p.peek(), b"defabc")
  assert_equal(p.read(), b"defabc")
  assert_equal(p.read(), b"")  # as if EOF
