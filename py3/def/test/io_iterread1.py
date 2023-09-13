def test_io_iterread1_1_with_size():
  r = io.BytesIO(b"abcdefg")
  r.read = None
  expected_results = [b"ab",b"cd",b"ef",b"g"]
  for _ in io_iterread1(r, 2):
    assert_equal(_, expected_results.pop(0))
  assert_equal([], expected_results)
def test_io_iterread1_2_with_length():
  r = io.BytesIO(b"abcdefg")
  r.read = None
  expected_results = [b"abcde"]
  for _ in io_iterread1(r, -1, 5):
    assert_equal(_, expected_results.pop(0))
  assert_equal([], expected_results)
def test_io_iterread1_3_with_length_and_size():
  r = io.BytesIO(b"abcdefg")
  r.read = None
  expected_results = [b"abc",b"de"]
  for _ in io_iterread1(r, 3, 5):
    assert_equal(_, expected_results.pop(0))
  assert_equal([], expected_results)
def test_io_iterread1_4_fallback():
  r = io.BytesIO(b"abcdefg")
  r.read1 = None
  expected_results = [b"abc",b"de"]
  for _ in io_iterread1(r, 3, 5):
    assert_equal(_, expected_results.pop(0))
  assert_equal([], expected_results)
def test_io_iterread1_5_no_fallback():
  r = io.BytesIO(b"abcdefg")
  r.read1 = 1
  try:
    for _ in io_iterread1(r, 3, 5, fallback=False):
      assert 0
  except TypeError as e:
    assert_equal(str(e), "'int' object is not callable")
