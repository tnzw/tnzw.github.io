def test_OpensslAes256CbcEncoder__1_stressed_random_stream():
  d = OpensslAes256CbcDecoder(b"password", cast=None)
  e = OpensslAes256CbcEncoder(b"password", salt=os.urandom(8), cast=None)
  # Test encode and decode stream, one byte at once + close
  #expected = b"mega big huge message of death of the universe"
  expected = os.urandom(os.urandom(1)[0])
  def yield_from_callable(fn): yield from fn()
  res = bytes(
    iter_chain(
      (db
       for eb in expected
       for db in d.decode(e.encode((eb,), stream=True), stream=True)),
      yield_from_callable(lambda: (db for db in d.decode(e.encode())))
    )
  )
  assert_equal(res, expected)
