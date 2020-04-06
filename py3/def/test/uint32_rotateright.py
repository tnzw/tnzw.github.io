def test_uint32_rotateright_1():
  assert uint32_rotateright(0x11111111,   1) == 0x88888888
def test_uint32_rotateright_2():
  assert uint32_rotateright(0x11111111,  33) == 0x88888888
def test_uint32_rotateright_3():
  assert uint32_rotateright(0x11111111,  -1) == 0x22222222
def test_uint32_rotateright_4():
  assert uint32_rotateright(0x11111111, -33) == 0x22222222
def test_uint32_rotateright_5():
  assert uint32_rotateright(0x11111111,   2) == 0x44444444
def test_uint32_rotateright_6():
  assert uint32_rotateright(0x11111111,  -2) == 0x44444444
