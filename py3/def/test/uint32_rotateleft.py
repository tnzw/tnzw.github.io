def test_uint32_rotateleft_1():
  assert uint32_rotateleft(0x11111111,   1) == 0x22222222
def test_uint32_rotateleft_2():
  assert uint32_rotateleft(0x11111111,  33) == 0x22222222
def test_uint32_rotateleft_3():
  assert uint32_rotateleft(0x11111111,  -1) == 0x88888888
def test_uint32_rotateleft_4():
  assert uint32_rotateleft(0x11111111, -33) == 0x88888888
def test_uint32_rotateleft_5():
  assert uint32_rotateleft(0x11111111,   2) == 0x44444444
def test_uint32_rotateleft_6():
  assert uint32_rotateleft(0x11111111,  -2) == 0x44444444
