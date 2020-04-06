def test_uint32_bigendian_tobytes_1():
  assert uint32_bigendian_tobytes(0x12345678) == b"\x12\x34\x56\x78"
