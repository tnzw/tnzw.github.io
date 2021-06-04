### BEGIN SHA256 ###
def test_openssl_aes256cbc_encrypt_1_constantsalt():
  assert_equal(openssl_aes256cbc_encrypt(b"message", b"secret", b"\x00"*8), b'Salted__\x00\x00\x00\x00\x00\x00\x00\x00=\xb05\x7f\xe2\x80\x11q|\nP\xa2\x17\x83\x9c\xa7')
def test_openssl_aes256cbc_encrypt_2_constantsalt():
  assert_equal(openssl_aes256cbc_encrypt(b"The quick brown fox jumps over the lazy dog", b"password", b"\x01"*8), b'Salted__\x01\x01\x01\x01\x01\x01\x01\x01\r\x80\xf8\x15l\xa9+n\xab\xae\xe0\x9a\xb2I 7WR\xb0\x98\xcc\xfc\xae>\xe0}\x16vmo\xce\x90A_\x83\xbe\xea\xeaP\xdcl\x8e\xaf\x8b\xa2\x17>\x86')
def test_openssl_aes256cbc_encrypt_3_nosalt():
  # tested with openssl 1.1.1f:
  # $ echo -n 'The quick brown fox jumps over the lazy dog' | openssl aes-256-cbc -e -nosalt -pass pass:password | hexdump -C
  # XXX stderr:
  # *** WARNING : deprecated key derivation used.
  # Using -iter or -pbkdf2 would be better.
  assert_equal(openssl_aes256cbc_encrypt(b"The quick brown fox jumps over the lazy dog", b"password", b""), b'\x06\x83\x03\x8a\xa1\x1f\x8b\x76\xa8\x89\x5c\x67\x24\x6e\xb5\x40\x46\x26\xac\x33\xa0\x09\x18\xcd\xa2\xf9\x64\x1c\xd7\x05\x64\xdc\x8d\x4b\xb5\x44\xc3\x4a\x2f\xea\x77\x47\xc1\xa5\xfe\x7c\x6b\xe6')
def test_openssl_aes256cbc_encrypt_4_nosalt_str():
  assert_equal(openssl_aes256cbc_encrypt("The quick brown fox jumps over the lazy dog", "password", b""), b'\x06\x83\x03\x8a\xa1\x1f\x8b\x76\xa8\x89\x5c\x67\x24\x6e\xb5\x40\x46\x26\xac\x33\xa0\x09\x18\xcd\xa2\xf9\x64\x1c\xd7\x05\x64\xdc\x8d\x4b\xb5\x44\xc3\x4a\x2f\xea\x77\x47\xc1\xa5\xfe\x7c\x6b\xe6')
def test_openssl_aes256cbc_encrypt_5_nosalt_bytelist():
  assert_equal(openssl_aes256cbc_encrypt(list(b"The quick brown fox jumps over the lazy dog"), list(b"password"), []), b'\x06\x83\x03\x8a\xa1\x1f\x8b\x76\xa8\x89\x5c\x67\x24\x6e\xb5\x40\x46\x26\xac\x33\xa0\x09\x18\xcd\xa2\xf9\x64\x1c\xd7\x05\x64\xdc\x8d\x4b\xb5\x44\xc3\x4a\x2f\xea\x77\x47\xc1\xa5\xfe\x7c\x6b\xe6')
def test_openssl_aes256cbc_encrypt_6_nosalt_iter():
  def iter(it):
    for _ in it: yield _
  assert_equal(openssl_aes256cbc_encrypt(iter(b"The quick brown fox jumps over the lazy dog"), b"password", b""), b'\x06\x83\x03\x8a\xa1\x1f\x8b\x76\xa8\x89\x5c\x67\x24\x6e\xb5\x40\x46\x26\xac\x33\xa0\x09\x18\xcd\xa2\xf9\x64\x1c\xd7\x05\x64\xdc\x8d\x4b\xb5\x44\xc3\x4a\x2f\xea\x77\x47\xc1\xa5\xfe\x7c\x6b\xe6')
def test_openssl_aes256cbc_encrypt_7_len16():
  assert_equal(openssl_aes256cbc_encrypt(b"1234567890123456", b"password", salt=b""), b'0\xc1\xa4\xa6S\x90.\xea\xb3\xb1\xe4\x85\xab"\xda\xc9\xb4jo\xe4\xab\x9f\x14\xffm~\x95q\x9f\x99\x04F')
### END SHA256 ###

### BEGIN MD5 ###
#def test_openssl_aes256cbc_encrypt_1_constantsalt():
#  assert_equal(openssl_aes256cbc_encrypt(b"message", b"secret", b"\x00"*8), b'Salted__\x00\x00\x00\x00\x00\x00\x00\x00Rn.Q\x06K\xcb\xc5\xa5\x96\xc3_\x07t\x86\xbe')
#def test_openssl_aes256cbc_encrypt_2_constantsalt():
#  assert_equal(openssl_aes256cbc_encrypt(b"The quick brown fox jumps over the lazy dog", b"password", b"\x01"*8), b'Salted__\x01\x01\x01\x01\x01\x01\x01\x01\xfez\x81\xf0As:\xab\xe0\x93\x91\xb3\xa5\x07W\x90\xc8\xbc\xae\xaf\xa9G\xb0s\xafi\xc1\xc7\xd7\x13\xb8\x8f\x9as9\xf5is\x88\x1c\xe1 \x1fW\xebC\x13\xf5')
#def test_openssl_aes256cbc_encrypt_3_nosalt():
#  # tested with openssl 1.0.1:
#  # $ echo -n 'The quick brown fox jumps over the lazy dog' | openssl aes-256-cbc -e -nosalt -pass pass:password | hexdump -C
#  assert_equal(openssl_aes256cbc_encrypt(b"The quick brown fox jumps over the lazy dog", b"password", b""), b'\xb6G\x02\r_\xe0\xae:\xaa\x14r\x8b\xc0K\xb3t\xa9h\x916\xe0\xa5\x8dP\xcb\xc8\xae\x84\xd5AD\x03\x11/\x06JBg\x9c|R\xcd\x8a\xa4\x8bw\xd7\x8d')
#def test_openssl_aes256cbc_encrypt_4_nosalt_str():
#  assert_equal(openssl_aes256cbc_encrypt("The quick brown fox jumps over the lazy dog", "password", b""), b'\xb6G\x02\r_\xe0\xae:\xaa\x14r\x8b\xc0K\xb3t\xa9h\x916\xe0\xa5\x8dP\xcb\xc8\xae\x84\xd5AD\x03\x11/\x06JBg\x9c|R\xcd\x8a\xa4\x8bw\xd7\x8d')
#def test_openssl_aes256cbc_encrypt_5_nosalt_bytelist():
#  assert_equal(openssl_aes256cbc_encrypt(list(b"The quick brown fox jumps over the lazy dog"), list(b"password"), []), b'\xb6G\x02\r_\xe0\xae:\xaa\x14r\x8b\xc0K\xb3t\xa9h\x916\xe0\xa5\x8dP\xcb\xc8\xae\x84\xd5AD\x03\x11/\x06JBg\x9c|R\xcd\x8a\xa4\x8bw\xd7\x8d')
#def test_openssl_aes256cbc_encrypt_6_nosalt_iter():
#  def iter(it):
#    for _ in it: yield _
#  assert_equal(openssl_aes256cbc_encrypt(iter(b"The quick brown fox jumps over the lazy dog"), b"password", b""), b'\xb6G\x02\r_\xe0\xae:\xaa\x14r\x8b\xc0K\xb3t\xa9h\x916\xe0\xa5\x8dP\xcb\xc8\xae\x84\xd5AD\x03\x11/\x06JBg\x9c|R\xcd\x8a\xa4\x8bw\xd7\x8d')
### END MD5 ###
