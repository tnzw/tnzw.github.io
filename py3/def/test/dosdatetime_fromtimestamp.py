def test_dosdatetime_fromtimestamp():
  localtime_offset = -(time.altzone if getattr(time, 'daylight', 0) else time.timezone)  # localtime_offset = +7200 on GMT+2 systems
  # so 1681298580 is 2023-04-12 11:23:00 GMT+0 or 2023-04-12 13:23:00 GMT+2
  assert_equal(struct.pack('<L', dosdatetime_fromtimestamp(1681298580.5431685 - localtime_offset      )), b"\xE0\x5A\x8C\x56");  # expected dosdatetime is 2023-04-12 11:23:00 (naive)
  assert_equal(struct.pack('<L', dosdatetime_fromtimestamp(1681298580.5431685 - localtime_offset, True)), b"\xE1\x5A\x8C\x56");  # expected dosdatetime is 2023-04-12 11:23:02 (naive)
  assert_equal(struct.pack('<L', dosdatetime_fromtimestamp(1681298582         - localtime_offset      )), b"\xE1\x5A\x8C\x56");  # expected dosdatetime is 2023-04-12 11:23:02 (naive)
  assert_equal(struct.pack('<L', dosdatetime_fromtimestamp(1681298582         - localtime_offset, True)), b"\xE1\x5A\x8C\x56");  # expected dosdatetime is 2023-04-12 11:23:02 (naive)
  # 1684029811 is 2023-05-14 02:03:31 GMT+0 or 2023-05-14 04:03:31 GMT+2
  assert_equal(struct.pack('<L', dosdatetime_fromtimestamp(1684029811.6733015 - localtime_offset      )), b"\x6F\x10\xAE\x56");  # expected dosdatetime is 2023-04-12 02:03:30 (naive)
  assert_equal(struct.pack('<L', dosdatetime_fromtimestamp(1684029811.6733015 - localtime_offset, True)), b"\x70\x10\xAE\x56");  # expected dosdatetime is 2023-04-12 02:03:32 (naive)
