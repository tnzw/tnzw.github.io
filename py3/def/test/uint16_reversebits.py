def test_uint16_reversebits_1(): assert_equal(uint16_reversebits(0xF000), 0x000F)
def test_uint16_reversebits_2(): assert_equal(uint16_reversebits(0xABCD), 0xB3D5)
def test_uint16_reversebits_3(): assert_equal(uint16_reversebits(0x8001), 0x8001)
def test_uint16_reversebits_4(): assert_equal(uint16_reversebits(0x0200), 0x0040)
