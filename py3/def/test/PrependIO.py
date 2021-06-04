def test_PrependIO():
  b = io.BytesIO()
  p = PrependIO(b)
  assert_equal(p.write(b"abc"), 3)
  b.seek(0)
  assert_equal(b.getvalue(), b"abc")
  assert_equal(p.prepend(b"d\nef"), 4)
  assert_equal(p.readline(), b"d\n")
  assert_equal(p.readline(), b"efabc")
  assert_equal(p.readline(), b"")  # as if EOF
  assert_equal(p.prepend(b"ghi"), 3)
  assert_equal(p.write(b"jkl"), 3)
  p.seek(-3, 1)
  assert_equal(p.read(), b"ghijkl")
  assert_equal(p.read(), b"")  # as if EOF
  # internal mechanism (read1)
  p.prepend(b"a")
  p.seek(-p.write(b"b"), 1)
  assert_equal(p.read1(), b"a")
  assert_equal(p.read1(), b"b")
  assert_equal(p.read1(), b"")