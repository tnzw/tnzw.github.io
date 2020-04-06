def test_binaryprefix_parseint_1():
  assert binaryprefix_parseint("1000k") == 1000000
def test_binaryprefix_parseint_2():
  assert binaryprefix_parseint("1000Ki") == 1024000
