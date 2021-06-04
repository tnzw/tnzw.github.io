def test_uri_component_encode__long_symbol():
  assert_equal(uri_component_encode("\U0001F3AE"), b"%F0%9F%8E%AE")
