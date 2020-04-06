def test_uint32_reversebits_1(): assert_equal(uint32_reversebits(0x00F00000), 0x00000F00)
def test_uint32_reversebits_2(): assert_equal(uint32_reversebits(0xABCDEF01), 0x80F7B3D5)
def test_uint32_reversebits_3(): assert_equal(uint32_reversebits(0x80000001), 0x80000001)
def test_uint32_reversebits_4(): assert_equal(uint32_reversebits(0x00200000), 0x00000400)
