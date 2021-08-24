def test_Base64Decoder__1_full_blocks():
  std = Base64Decoder()
  assert_equal(std.decode(b"YWJjZGVmZ2hp"), b"abcdefghi")
  assert_equal(std.decode(b"ABCDEFGHIJKL"), b"\x00\x10\x83\x10\x51\x87\x20\x92\x8b")

def test_Base64Decoder__2_padded_blocks():
  std = Base64Decoder()
  assert_equal(std.decode(b"YWI=Yw==ZGVmZ2hp"), b"abcdefghi")
  assert_equal(std.decode(b"ABC=DE==FGHIJKL="), b"\x00\x10\x0c\x14\x61\xc8\x24\xa2")

def test_Base64Decoder__2_white_spaces():
  std = Base64Decoder()
  assert_equal(std.decode(b"YW JjZG\nVmZ2 hp"), b"abcdefghi")
  assert_equal(std.decode(b"ABCD EFGH\nIJKL"), b"\x00\x10\x83\x10\x51\x87\x20\x92\x8b")

def test_Base64Decoder__3_early_EOF():
  std = Base64Decoder()
  assert_raise(ValueError, lambda: std.decode(b"YWJjZGVmZ2h"))
  assert_raise(ValueError, lambda: std.decode(b"ABCDEFGHIJK"))

def test_Base64Decoder__4_early_EOF_errors_pad():
  std = Base64Decoder(errors="pad")
  assert_equal(std.decode(b"YWJjZGVmZ2h"), b"abcdefgh")
  assert_equal(std.decode(b"ABCDEFGHIJK"), b"\x00\x10\x83\x10\x51\x87\x20\x92")

def test_Base64Decoder__5_invalid_code():
  std = Base64Decoder()
  assert_raise(ValueError, lambda: std.decode(b"YWJ~jZGVmZ2h~p"))
  assert_raise(ValueError, lambda: std.decode(b"ABC~DEFGHIJK~L"))

def test_Base64Decoder__5_invalid_code_errors_ignore():
  std = Base64Decoder(errors="ignore")
  assert_equal(std.decode(b"YWJ~jZGVmZ2h~p"), b"abcdefghi")
  assert_equal(std.decode(b"ABC~DEFGHIJK~L"), b"\x00\x10\x83\x10\x51\x87\x20\x92\x8b")

def test_Base64Decoder__6_decode_stress():
  expected = os.urandom(os.urandom(1)[0])
  encoded = base64.b64encode(expected)
  decoded = b""
  std = Base64Decoder()
  for enc in encoded: decoded += std.decode(bytes((enc,)), stream=True)
  #decoded += std.decode()  # useless here ?
  assert_equal(decoded, expected)

def test_Base64Decoder__7_url_scheme_decode_stress():
  expected = os.urandom(os.urandom(1)[0])
  encoded = base64.b64encode(expected).replace(b"+", b"-").replace(b"/", b"_")
  decoded = b""
  std = Base64Decoder(scheme="url")
  for enc in encoded: decoded += std.decode(bytes((enc,)), stream=True)
  #decoded += std.decode()  # useless here ?
  assert_equal(decoded, expected)
