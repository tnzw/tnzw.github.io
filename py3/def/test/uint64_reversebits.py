def test_uint64_reversebits_1(): assert_equal(uint64_reversebits(0x0000F00000000000), 0x00000000000F0000)
def test_uint64_reversebits_2(): assert_equal(uint64_reversebits(0xABCDEF0123456789), 0x91E6A2C480F7B3D5)
def test_uint64_reversebits_3(): assert_equal(uint64_reversebits(0x8000000000000001), 0x8000000000000001)
def test_uint64_reversebits_4(): assert_equal(uint64_reversebits(0x0020000000000000), 0x0000000000000400)
