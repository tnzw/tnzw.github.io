def test_find2():
  assert_raise(ValueError, lambda: find2('a/b', ()))
  assert_equal(find2('a/b/c', '/'), 1)
  assert_equal(find2('a\\b/c', ('/', '\\')), 1)
  assert_equal(find2('a\nb\nc', ('/', '\\')), -1)
  assert_equal(find2(['a', '\\', 'b', '/', 'c'], (['/'], ['\\'])), 1)
  assert_equal(find2(('a', '\\', 'b', '/', 'c'), (('/',), ('\\',))), 1)
