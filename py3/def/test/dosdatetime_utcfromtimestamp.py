def test_dosdatetime_fromutctimestamp():
  # so 1681298580 is 2023-04-12 11:23:00 GMT+0
  assert_equal(struct.pack('<L', dosdatetime_utcfromtimestamp(1681298580.5431685      )), b"\xE0\x5A\x8C\x56");  # expected dosdatetime is 2023-04-12 11:23:00 (naive)
  assert_equal(struct.pack('<L', dosdatetime_utcfromtimestamp(1681298580.5431685, True)), b"\xE1\x5A\x8C\x56");  # expected dosdatetime is 2023-04-12 11:23:02 (naive)
  assert_equal(struct.pack('<L', dosdatetime_utcfromtimestamp(1681298582              )), b"\xE1\x5A\x8C\x56");  # expected dosdatetime is 2023-04-12 11:23:02 (naive)
  assert_equal(struct.pack('<L', dosdatetime_utcfromtimestamp(1681298582        , True)), b"\xE1\x5A\x8C\x56");  # expected dosdatetime is 2023-04-12 11:23:02 (naive)
  # 1684029811 is 2023-05-14 02:03:31 GMT+0
  assert_equal(struct.pack('<L', dosdatetime_utcfromtimestamp(1684029811.6733015      )), b"\x6F\x10\xAE\x56");  # expected dosdatetime is 2023-04-12 02:03:30 (naive)
  assert_equal(struct.pack('<L', dosdatetime_utcfromtimestamp(1684029811.6733015, True)), b"\x70\x10\xAE\x56");  # expected dosdatetime is 2023-04-12 02:03:32 (naive)
