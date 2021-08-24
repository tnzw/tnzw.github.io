def test_Base64Encoder__1_full_blocks():
  std = Base64Encoder()
  assert_equal(std.encode(b"abcdefghi"), b"YWJjZGVmZ2hp")
  assert_equal(std.encode(b"\x00\x10\x83\x10\x51\x87\x20\x92\x8b"), b"ABCDEFGHIJKL")

def test_Base64Encoder__2_unterminated_blocks():
  std = Base64Encoder()
  assert_equal(std.encode(b"abcdefgh"), b"YWJjZGVmZ2g=")
  assert_equal(std.encode(b"\x00\x10\x83\x10\x51\x87\x20"), b"ABCDEFGHIA==")

def test_Base64Encoder__6_encode_stress():
  decoded = os.urandom(os.urandom(1)[0])
  expected = base64.b64encode(decoded)
  encoded = b""
  std = Base64Encoder()
  for dec in decoded: encoded += std.encode(bytes((dec,)), stream=True)
  encoded += std.encode()
  assert_equal(encoded, expected)

def test_Base64Encoder__7_url_scheme_encode_stress():
  decoded = os.urandom(os.urandom(1)[0])
  expected = base64.b64encode(decoded).replace(b"+", b"-").replace(b"/", b"_")
  encoded = b""
  std = Base64Encoder(scheme="url")
  for dec in decoded: encoded += std.encode(bytes((dec,)), stream=True)
  encoded += std.encode()
  assert_equal(encoded, expected)
