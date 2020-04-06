def test_OPENSSL_EVP_BytesToKey_1():
  key, iv = [0]*32, [0]*16
  assert OPENSSL_EVP_BytesToKey(md5_sumbytes, 16, None, None, 1, key, 32, iv, 16) == 32
  assert key == [ 212, 29, 140, 217, 143, 0, 178, 4, 233, 128, 9, 152, 236, 248, 66, 126, 89, 173, 178, 78, 243, 205, 190, 2, 151, 240, 91, 57, 88, 39, 69, 63 ], key
  assert iv == [ 139, 129, 84, 240, 59, 117, 245, 138, 108, 112, 34, 53, 191, 100, 54, 41 ], iv

def test_OPENSSL_EVP_BytesToKey_2():
  key, iv = [0]*32, [0]*16
  assert OPENSSL_EVP_BytesToKey(md5_sumbytes, 16, [1,2,3,4,5,6,7,8], [0], 1, key, 32, iv, 16) == 32
  assert key == [ 166, 231, 211, 180, 111, 223, 175, 11, 222, 42, 31, 131, 42, 0, 210, 222, 226, 40, 14, 214, 80, 249, 0, 209, 7, 51, 232, 76, 239, 121, 15, 115 ]
  assert iv == [ 146, 181, 196, 14, 174, 207, 153, 194, 86, 111, 114, 190, 67, 89, 247, 152 ]