def test_paddingarray():
  assert_equal(paddingarray('a', 1)[0], 'a')
  assert_raise(IndexError, lambda: paddingarray('a', 1)[1])
  assert_equal(len(paddingarray('a', 10)), 10)
  for _ in paddingarray('a', 10): assert_equal(_, 'a')
  assert_equal(len(paddingarray('a', 10)[2:-2]), 6)
  assert_equal(sum(paddingarray(2, 10)[2:-2]), 12)
  assert_equal(sum(paddingarray(2, 10)[2:-2:2]), 6)
