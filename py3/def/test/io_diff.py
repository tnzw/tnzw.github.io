def test_io_diff_1_nodiff():
  src = io.BytesIO(b"abcdefg")
  dst = io.BytesIO(b"abcdefg")
  assert io_diff(src, dst)
def test_io_diff_2_diff1():
  src = io.BytesIO(b"abcdefg")
  dst = io.BytesIO(b"abcdefgh")
  assert not io_diff(src, dst)
def test_io_diff_3_diff2():
  src = io.BytesIO(b"abcdefgh")
  dst = io.BytesIO(b"abcdefg")
  assert not io_diff(src, dst)
def test_io_diff_4_dsts_nodiff():
  src  = io.BytesIO(b"abcdefg")
  dst1 = io.BytesIO(b"abcdefg")
  dst2 = io.BytesIO(b"abcdefg")
  dst3 = io.BytesIO(b"abcdefg")
  assert io_diff(src, dst1, dst2, dst3)
def test_io_diff_5_dsts_length_nodiff():
  src  = io.BytesIO(b"abcdefgh")
  dst1 = io.BytesIO(b"abcdefgi")
  dst2 = io.BytesIO(b"abcdefgj")
  dst3 = io.BytesIO(b"abcdefgk")
  assert io_diff(src, dst1, dst2, dst3, length=7)
def test_io_diff_5_dsts_length_diff():
  src  = io.BytesIO(b"abcdefghl")
  dst1 = io.BytesIO(b"abcdefgil")
  dst2 = io.BytesIO(b"abcdefgjl")
  dst3 = io.BytesIO(b"abcdefgkl")
  assert not io_diff(src, dst1, dst2, dst3, length=9)
def test_io_diff_5_dsts_neglength():
  src  = io.BytesIO(b"abcdefghl")
  dst1 = io.BytesIO(b"abcdefgil")
  dst2 = io.BytesIO(b"abcdefgjl")
  dst3 = io.BytesIO(b"abcdefgkl")
  assert not io_diff(src, dst1, dst2, dst3, length=-1)
