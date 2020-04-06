def test_uint8_reversebits_1(): assert_equal(uint8_reversebits(0xF0), 0x0F)
def test_uint8_reversebits_2(): assert_equal(uint8_reversebits(0xAB), 0xD5)
def test_uint8_reversebits_3(): assert_equal(uint8_reversebits(0x81), 0x81)
def test_uint8_reversebits_4(): assert_equal(uint8_reversebits(0x20), 0x04)
