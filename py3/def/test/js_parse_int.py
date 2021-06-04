def test_js_parse_int():
  def assert_is_nan(v):
    if not math.isnan(v): assert_is(v, math.nan)

  assert_equal(js_parse_int('0xF', 16)   , 15)
  assert_equal(js_parse_int('F', 16)     , 15)
  assert_equal(js_parse_int('17', 8)     , 15)
  assert_equal(js_parse_int('015', 10)   , 15)
  assert_equal(js_parse_int(15.99, 10)   , 15)
  assert_equal(js_parse_int('15,123', 10), 15)
  assert_equal(js_parse_int('FXX123', 16), 15)
  assert_equal(js_parse_int('1111', 2)   , 15)
  assert_equal(js_parse_int('15 * 3', 10), 15)
  assert_equal(js_parse_int('15e2', 10)  , 15)
  assert_equal(js_parse_int('15px', 10)  , 15)
  assert_equal(js_parse_int('12', 13)    , 15)

  assert_is_nan(js_parse_int('Hello', 8))
  assert_is_nan(js_parse_int('546', 2))

  assert_equal(js_parse_int('-F', 16)   , -15)
  assert_equal(js_parse_int('-0F', 16)  , -15)
  assert_equal(js_parse_int('-0XF', 16) , -15)
  assert_equal(js_parse_int(-15.1, 10)  , -15)
  assert_equal(js_parse_int('-17', 8)   , -15)
  assert_equal(js_parse_int('-15', 10)  , -15)
  assert_equal(js_parse_int('-1111', 2) , -15)
  assert_equal(js_parse_int('-15e1', 10), -15)
  assert_equal(js_parse_int('-12', 13)  , -15)

  assert_equal(js_parse_int('0e0', 16), 224)
