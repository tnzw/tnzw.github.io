def test_io_readuntil__1(): assert_equal(io_readuntil(io.BytesIO(b"cabcd"), b"a"), b"ca")
def test_io_readuntil__2(): assert_equal(io_readuntil(io.BytesIO(b"cabcd"), b"cd"), b"cabcd")
def test_io_readuntil__3(): assert_equal(io_readuntil(io.BytesIO(b"abcdab"), b"abcd"), b"abcd")
def test_io_readuntil__separator_not_found_1():
  err = assert_raise(io_IncompleteReadError, lambda: io_readuntil(io.BytesIO(b"cabcd"), b"e"))
  assert_equal(err.partial, b"cabcd")
def test_io_readuntil__separator_not_found_2():
  err = assert_raise(io_IncompleteReadError, lambda: io_readuntil(io.BytesIO(b"cabcd"), b"ba"))
  assert_equal(err.partial, b"cabcd")
def test_io_readuntil__separators__1(): assert_equal(io_readuntil.separators(io.BytesIO(b"cabcd"), b"a"), b"ca")
def test_io_readuntil__separators__2(): assert_equal(io_readuntil.separators(io.BytesIO(b"cabcd"), b"a", b"b"), b"ca")
def test_io_readuntil__separators__3(): assert_equal(io_readuntil.separators(io.BytesIO(b"cabcd"), b"a", b"b", b"c"), b"c")
def test_io_readuntil__separators__sep_in_sep(): assert_equal(io_readuntil.separators(io.BytesIO(b"cabcd"), b"abc", b"b"), b"cab")
def test_io_readuntil__separators__sep_order(): assert_equal(io_readuntil.separators(io.BytesIO(b"nhbn"), b"nhbn", b"hbn", b"nhbhn"), b"nhbn")

def test_io_readuntil__separators__boundary():
  r = io.BytesIO(b"""\
GET / HTTP/1.1
Header: Value

-----------myboundary
Header: Value

MY DATA
-----------myboundary
Header: Value

MY DATA 2
-----------myboundary--
""".replace(b"\n", b"\r\n"))
  boundary = b"---------myboundary"
  start_boundary = b"--" + boundary + b"\r\n"
  sep_boundary = b"\r\n--" + boundary + b"\r\n"
  end_boundary = b"\r\n--" + boundary + b"--\r\n"
  data = io_readuntil(r, b"\r\n\r\n")  # read until end of headers
  assert data.endswith(b"\r\n\r\n"), data
  data = io_readuntil(r, start_boundary)  # find first boundary
  assert data.endswith(start_boundary), data
  data = io_readuntil.separators(r, sep_boundary, end_boundary)  # find next/ending boundary
  assert data.endswith(sep_boundary), data
  data = io_readuntil.separators(r, sep_boundary, end_boundary)  # find next/ending boundary
  assert data.endswith(end_boundary), data
  data = r.read(1)
  assert not data  # check if `r` is consumed conpletely

def test_io_readuntil__separators_iter__boundary():
  r = io.BytesIO(b"""\
GET / HTTP/1.1
Header: Value

-----------myboundary
Header: Value

MY DATA
-----------myboundary
Header: Value

MY DATA 2
-----------myboundary--
""".replace(b"\n", b"\r\n"))
  boundary = b"---------myboundary"
  start_boundary = b"--" + boundary + b"\r\n"
  sep_boundary = b"\r\n--" + boundary + b"\r\n"
  end_boundary = b"\r\n--" + boundary + b"--\r\n"
  data = list(io_readuntil.iter(r, b"\r\n\r\n"))  # read until end of headers
  assert data[-1] == b"\r\n\r\n", data
  data = list(io_readuntil.iter(r, start_boundary))  # find first boundary
  assert data[-1] == start_boundary, data
  data = list(io_readuntil.separators.iter(r, sep_boundary, end_boundary))  # find next/ending boundary
  assert data[-1] == sep_boundary, data
  data = list(io_readuntil.separators.iter(r, sep_boundary, end_boundary))  # find next/ending boundary
  assert data[-1] == end_boundary, data
  data = r.read(1)
  assert not data  # check if `r` is consumed conpletely

def test_io_readuntil__iter_yieldempty():
  r = io.BytesIO(b"HnnhbnHnnDnhbnHnnDnhbhn")
  data = list(io_readuntil.iter(r, b"beurk", errors="yieldempty"))
  assert_equal(b"".join(data), b"HnnhbnHnnDnhbnHnnDnhbhn")
  assert_equal(data[-1], b"")

  r = io.BytesIO(b"H")
  data = list(io_readuntil.iter(r, b"beurk", errors="yieldempty"))
  assert_equal(b"".join(data), b"H")
  assert_equal(data[-1], b"")
