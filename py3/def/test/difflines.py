def test_difflines():
  assert_equal(difflines("oneline", "oneline"), " oneline")
  assert_equal(difflines("oneline\n", "oneline\n"), " oneline\n ")
  assert_equal(difflines("oneline", ""), "-oneline\n+")
  assert_equal(difflines("", "oneline"), "-\n+oneline")
  #assert_equal(difflines("", "oneline", ignore_ending_emptyline=True), "+oneline\n")
  #assert_equal(difflines("oneline", "", ignore_ending_emptyline=True), "-oneline\n")
