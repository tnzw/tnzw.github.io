def test_iter_blocks_1():
  expected_blocks = [[1,2],[3,4],[5]]
  for block in iter_blocks([1,2,3,4,5],2):
    expected_block = expected_blocks.pop(0)
    assert expected_block == block, "expected_block {!r} != block {!r}".format(expected_block, block)
