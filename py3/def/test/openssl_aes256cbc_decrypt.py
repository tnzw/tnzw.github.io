def test_openssl_aes256cbc_decrypt_1():
  assert_equal(openssl_aes256cbc_decrypt(b'Salted__\x00\x00\x00\x00\x00\x00\x00\x00Rn.Q\x06K\xcb\xc5\xa5\x96\xc3_\x07t\x86\xbe', b"secret"), b"message")
def test_openssl_aes256cbc_decrypt_2():
  assert_equal(openssl_aes256cbc_decrypt(b'Salted__\x01\x01\x01\x01\x01\x01\x01\x01\xfez\x81\xf0As:\xab\xe0\x93\x91\xb3\xa5\x07W\x90\xc8\xbc\xae\xaf\xa9G\xb0s\xafi\xc1\xc7\xd7\x13\xb8\x8f\x9as9\xf5is\x88\x1c\xe1 \x1fW\xebC\x13\xf5', b"password"), b"The quick brown fox jumps over the lazy dog")
def test_openssl_aes256cbc_decrypt_3_nosalt():
  assert_equal(openssl_aes256cbc_decrypt(b'\xb6G\x02\r_\xe0\xae:\xaa\x14r\x8b\xc0K\xb3t\xa9h\x916\xe0\xa5\x8dP\xcb\xc8\xae\x84\xd5AD\x03\x11/\x06JBg\x9c|R\xcd\x8a\xa4\x8bw\xd7\x8d', b"password"), b"The quick brown fox jumps over the lazy dog")
def test_openssl_aes256cbc_decrypt_5_nosalt_bytelist():
  assert_equal(openssl_aes256cbc_decrypt(list(b'\xb6G\x02\r_\xe0\xae:\xaa\x14r\x8b\xc0K\xb3t\xa9h\x916\xe0\xa5\x8dP\xcb\xc8\xae\x84\xd5AD\x03\x11/\x06JBg\x9c|R\xcd\x8a\xa4\x8bw\xd7\x8d'), list(b"password")), b"The quick brown fox jumps over the lazy dog")
def test_openssl_aes256cbc_decrypt_6_nosalt_iter():
  def iter(it):
    for _ in it: yield _
  assert_equal(openssl_aes256cbc_decrypt(iter(b'\xb6G\x02\r_\xe0\xae:\xaa\x14r\x8b\xc0K\xb3t\xa9h\x916\xe0\xa5\x8dP\xcb\xc8\xae\x84\xd5AD\x03\x11/\x06JBg\x9c|R\xcd\x8a\xa4\x8bw\xd7\x8d'), b"password"), b"The quick brown fox jumps over the lazy dog")
