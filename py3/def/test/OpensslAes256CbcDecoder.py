def test_OpensslAes256CbcDecoder__1():
  assert_equal(OpensslAes256CbcDecoder(b"secret").transcode(b'Salted__\x00\x00\x00\x00\x00\x00\x00\x00=\xb05\x7f\xe2\x80\x11q|\nP\xa2\x17\x83\x9c\xa7'), b"message")
def test_OpensslAes256CbcDecoder__2_stream_n_copy():
  t = OpensslAes256CbcDecoder(b"password")
  assert_equal(t.transcode(b'Salted__', stream=True), b"")
  assert_equal(t.transcode(b'\x01\x01\x01\x01\x01\x01', stream=True), b"")
  assert_equal(t.transcode(b'\x01\x01', stream=True), b"")
  assert_equal(t.transcode(b'\r\x80\xf8\x15l\xa9+n\xab\xae\xe0\x9a\xb2I 7WR\xb0\x98\xcc\xfc\xae>\xe0}\x16vmo\xce', stream=True), b'The quick brown ')
  t2 = t.copy()
  assert_equal(t.transcode(b'\x90A_\x83\xbe\xea\xeaP\xdcl\x8e\xaf\x8b\xa2\x17>\x86', stream=True), b"fox jumps over t")
  assert_equal(t.transcode(), b"he lazy dog")
  assert_equal(t2.transcode(b'\x90A_\x83\xbe\xea\xeaP\xdcl\x8e\xaf\x8b\xa2\x17>\x86', stream=True), b"fox jumps over t")
  assert_equal(t2.transcode(), b"he lazy dog")
def test_OpensslAes256CbcDecoder__3_1byte_at_once_stream():
  t = OpensslAes256CbcDecoder(b"password")
  message = b'Salted__\x01\x01\x01\x01\x01\x01\x01\x01\r\x80\xf8\x15l\xa9+n\xab\xae\xe0\x9a\xb2I 7WR\xb0\x98\xcc\xfc\xae>\xe0}\x16vmo\xce\x90A_\x83\xbe\xea\xeaP\xdcl\x8e\xaf\x8b\xa2\x17>\x86'
  decoded = b""
  for b in message: decoded += t.transcode((b,), stream=True)
  decoded += t.transcode()
  assert_equal(decoded, b"The quick brown fox jumps over the lazy dog")
def test_OpensslAes256CbcDecoder__4_len16():
  def openssl_aes256cbc_decode(message, password): return OpensslAes256CbcDecoder(password).transcode(message)
  assert_equal(openssl_aes256cbc_decode(b"\x53\x61\x6c\x74\x65\x64\x5f\x5f\x34\x60\xf5\xce\xf2\xd8\xac\x5e\x4a\xbc\x34\x1b\xa7\x4a\xc7\x3f\x2d\xa9\x35\x6f\xb8\x67\xde\x4b\xd4\x45\x76\xfe\xc0\x21\xc8\x5e\x49\xc1\x86\x98\xfb\xf1\x77\x07", b"password"), b"1234567890123456")
