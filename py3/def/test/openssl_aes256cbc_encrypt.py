def test_openssl_aes256cbc_encrypt_1_constantsalt():
  assert_equal(openssl_aes256cbc_encrypt(b"message", b"secret", b"\x00"*8), b'Salted__\x00\x00\x00\x00\x00\x00\x00\x00Rn.Q\x06K\xcb\xc5\xa5\x96\xc3_\x07t\x86\xbe')
def test_openssl_aes256cbc_encrypt_2_constantsalt():
  assert_equal(openssl_aes256cbc_encrypt(b"The quick brown fox jumps over the lazy dog", b"password", b"\x01"*8), b'Salted__\x01\x01\x01\x01\x01\x01\x01\x01\xfez\x81\xf0As:\xab\xe0\x93\x91\xb3\xa5\x07W\x90\xc8\xbc\xae\xaf\xa9G\xb0s\xafi\xc1\xc7\xd7\x13\xb8\x8f\x9as9\xf5is\x88\x1c\xe1 \x1fW\xebC\x13\xf5')
def test_openssl_aes256cbc_encrypt_3_nosalt():
  assert_equal(openssl_aes256cbc_encrypt(b"The quick brown fox jumps over the lazy dog", b"password", b""), b'\xb6G\x02\r_\xe0\xae:\xaa\x14r\x8b\xc0K\xb3t\xa9h\x916\xe0\xa5\x8dP\xcb\xc8\xae\x84\xd5AD\x03\x11/\x06JBg\x9c|R\xcd\x8a\xa4\x8bw\xd7\x8d')
def test_openssl_aes256cbc_encrypt_4_nosalt_str():
  assert_equal(openssl_aes256cbc_encrypt("The quick brown fox jumps over the lazy dog", "password", b""), b'\xb6G\x02\r_\xe0\xae:\xaa\x14r\x8b\xc0K\xb3t\xa9h\x916\xe0\xa5\x8dP\xcb\xc8\xae\x84\xd5AD\x03\x11/\x06JBg\x9c|R\xcd\x8a\xa4\x8bw\xd7\x8d')
def test_openssl_aes256cbc_encrypt_5_nosalt_bytelist():
  assert_equal(openssl_aes256cbc_encrypt(list(b"The quick brown fox jumps over the lazy dog"), list(b"password"), []), b'\xb6G\x02\r_\xe0\xae:\xaa\x14r\x8b\xc0K\xb3t\xa9h\x916\xe0\xa5\x8dP\xcb\xc8\xae\x84\xd5AD\x03\x11/\x06JBg\x9c|R\xcd\x8a\xa4\x8bw\xd7\x8d')
def test_openssl_aes256cbc_encrypt_6_nosalt_iter():
  def iter(it):
    for _ in it: yield _
  assert_equal(openssl_aes256cbc_encrypt(iter(b"The quick brown fox jumps over the lazy dog"), b"password", b""), b'\xb6G\x02\r_\xe0\xae:\xaa\x14r\x8b\xc0K\xb3t\xa9h\x916\xe0\xa5\x8dP\xcb\xc8\xae\x84\xd5AD\x03\x11/\x06JBg\x9c|R\xcd\x8a\xa4\x8bw\xd7\x8d')
