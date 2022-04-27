def splitlines__assert(array):
  expected = (io.StringIO if isinstance(array, str) else io.BytesIO)(array).readlines()
  returned = splitlines(array)
  assert_equal(returned, expected)

def test_splitlines__str():
  splitlines__assert("")
  splitlines__assert("0")
  splitlines__assert("\n")
  splitlines__assert("0\n")
  splitlines__assert("0\n1\n")
  splitlines__assert("0\n1\n2")

def test_splitlines__crlf():
  splitlines__assert(b"")
  splitlines__assert(b"0")
  splitlines__assert(b"\r\n")
  splitlines__assert(b"0\r\n")
  splitlines__assert(b"0\r\n1\r\n")
  splitlines__assert(b"0\r\n1\r\n2")

def test_splitlines__lf():
  splitlines__assert(b"")
  splitlines__assert(b"0")
  splitlines__assert(b"\n")
  splitlines__assert(b"0\n")
  splitlines__assert(b"0\n1\n")
  splitlines__assert(b"0\n1\n2")

def test_splitlines__custom_array():
  assert_equal(splitlines([_ for _ in b""], [0x0D, 0x0A]), [])
  assert_equal(splitlines([_ for _ in b"0"], [0x0D, 0x0A]), [[0x30]])
  assert_equal(splitlines([_ for _ in b"\r\n"], [0x0D, 0x0A]), [[0x0D, 0x0A]])
  assert_equal(splitlines([_ for _ in b"0\r\n"], [0x0D, 0x0A]), [[0x30, 0x0D, 0x0A]])
  assert_equal(splitlines([_ for _ in b"0\r\n1\r\n"], [0x0D, 0x0A]), [[0x30, 0x0D, 0x0A], [0x31, 0x0D, 0x0A]])
  assert_equal(splitlines([_ for _ in b"0\r\n1\r\n2"], [0x0D, 0x0A]), [[0x30, 0x0D, 0x0A], [0x31, 0x0D, 0x0A], [0x32]])
