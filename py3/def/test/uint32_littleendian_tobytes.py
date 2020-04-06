def test_uint32_littleendian_tobytes_1():
  assert uint32_littleendian_tobytes(0x12345678) == b"\x78\x56\x34\x12"
