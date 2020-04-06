def test_md5_as4uint32_sumbytes_empty():
  assert md5_as4uint32_sumbytes(b"") == (3649838548, 78774415, 2550759657, 2118318316), md5_as4uint32_sumbytes(b"")
def test_md5_as4uint32_sumbytes_empty_list():
  assert md5_as4uint32_sumbytes([]) == (3649838548, 78774415, 2550759657, 2118318316), md5_as4uint32_sumbytes([])
def test_md5_as4uint32_sumbytes_00():
  assert md5_as4uint32_sumbytes(b"\x00") == (2911221907, 2308967934, 2419390157, 1906300239), md5_as4uint32_sumbytes(b"\x00")
def test_md5_as4uint32_sumbytes_00_list():
  assert md5_as4uint32_sumbytes([0]) == (2911221907, 2308967934, 2419390157, 1906300239), md5_as4uint32_sumbytes([0])
def test_md5_as4uint32_sumbytes_0001_list():
  assert md5_as4uint32_sumbytes([0,1]) == (3430355012, 1297438622, 4223497940, 42044299), md5_as4uint32_sumbytes([0,1])
def test_md5_as4uint32_sumbytes_0001_tuple():
  assert md5_as4uint32_sumbytes((0,1)) == (3430355012, 1297438622, 4223497940, 42044299), md5_as4uint32_sumbytes((0,1))
