def test_uint32_bigendian_frombytes_1():
  assert uint32_bigendian_frombytes(b"\x12\x34\x56\x78") == 0x12345678, "0x%08x" % (uint32_bigendian_frombytes(b"\x12\x34\x56\x78"),)
def test_uint32_bigendian_frombytes_2():
  assert uint32_bigendian_frombytes([0x12,0x34,0x56,0x78]) == 0x12345678, "0x%08x" % (uint32_bigendian_frombytes([0x12,0x34,0x56,0x78]),)
def test_uint32_bigendian_frombytes_3():
  assert uint32_bigendian_frombytes((0x12,0x34,0x56,0x78)) == 0x12345678, "0x%08x" % (uint32_bigendian_frombytes((0x12,0x34,0x56,0x78)),)
