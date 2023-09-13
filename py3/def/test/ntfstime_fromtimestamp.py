def test_ntfstime_fromtimestamp():
  assert_equal(ntfstime_fromtimestamp( 0.1), 116444736001000000)
  assert_equal(ntfstime_fromtimestamp( 0  ), 116444736000000000)
  assert_equal(ntfstime_fromtimestamp(-1  ), 116444735990000000)
  assert_equal(ntfstime_fromtimestamp(-0.1), 116444735999000000)
  assert_equal(ntfstime_fromtimestamp(-11644473600  ),         0)
  assert_equal(ntfstime_fromtimestamp(-11644473600.5),  -5000000)
  assert_equal(ntfstime_fromtimestamp(-11644473601  ), -10000000)
  # these two tests below are to test the limits of 64 bit floats
  assert_equal(ntfstime_fromtimestamp(1681291380.54316855      ), 133257649805431685)  # may fail on dumb implementation of ntfstime_fromtimestamp()
  assert_equal(ntfstime_fromtimestamp(1681291380.54316855, True), 133257649805431686)  # may fail on dumb implementation of ntfstime_fromtimestamp()
