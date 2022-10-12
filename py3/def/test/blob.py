def test_blob():

  # repr
  assert_equal(repr(blob(([108, 111, 108],))), "blob([arrayview([108, 111, 108], slice(0, None, 1))])")
  assert_equal(repr(blob((b"lol",))), "blob([arrayview(b'lol', slice(0, None, 1))])")
  assert_equal(repr(blob((b"lol",), type="epyt")), "blob([arrayview(b'lol', slice(0, None, 1))], type='epyt')")

  # size
  assert_equal(len(blob((b"lol",))), 3)
  assert_equal(len(blob((b"lol",b"blue"))), 7)
  assert_equal(len(blob((arrayview(b"lol"),b"blue"))), 7)
  assert_equal(len(blob((blob((b"lol",)),b"blue"))), 7)

  # bytes
  assert_equal(bytes(blob((b"lol",b"blue"))), b"lolblue")

  # slice
  assert_equal(bytes(blob((b"lol",b"blue")).slice(1)), b"lolblue"[1:])
  assert_equal(bytes(blob((b"lol",b"blue")).slice(-1)), b"lolblue"[-1:])
  assert_equal(bytes(blob((b"lol",b"blue")).slice(1, 2)), b"lolblue"[1:2])
  assert_equal(bytes(blob((b"lol",b"blue")).slice(1, 4)), b"lolblue"[1:4])
  assert_equal(bytes(blob((b"lol",b"blue")).slice(1, -5)), b"lolblue"[1:-5])
  assert_equal(bytes(blob((b"lol",b"blue")).slice(1, -1)), b"lolblue"[1:-1])
  assert_equal(bytes(blob((b"lol",b"blue")).slice(0, -1)), b"lolblue"[0:-1])
  assert_equal(blob((b"lol",b"blue")).slice(0, -1, type="meow").type, "meow")

  # __getitem__ index
  for i in range(7): assert_equal(blob((b"lol",b"blue"))[i], b"lolblue"[i])

  # __iter__
  for i, c in enumerate(blob((b"lol",b"blue"))): assert_equal(c, b"lolblue"[i])

  # __getitem__ slice
  assert_equal(bytes(blob((b"lol",b"blue"))[1:]), b"lolblue"[1:])
  assert_equal(bytes(blob((b"lol",b"blue"))[-1:]), b"lolblue"[-1:])
  assert_equal(bytes(blob((b"lol",b"blue"))[1:2]), b"lolblue"[1:2])
  assert_equal(bytes(blob((b"lol",b"blue"))[1:4]), b"lolblue"[1:4])
  assert_equal(bytes(blob((b"lol",b"blue"))[1:-5]), b"lolblue"[1:-5])
  assert_equal(bytes(blob((b"lol",b"blue"))[1:-1]), b"lolblue"[1:-1])
  assert_equal(bytes(blob((b"lol",b"blue"))[:-1]), b"lolblue"[:-1])
  assert_equal(blob((b"lol",b"blue"), type="meow")[:-1].type, "")

  # __setitem__
  a1, a2 = bytearray(b"0123456789"), bytearray(b"abcdefghij"); b = blob((a1,a2)); b[0] = 0; assert_equal(bytes(a1), b"\x00123456789"); assert_equal(bytes(a2), b"abcdefghij");
  a1, a2 = bytearray(b"0123456789"), bytearray(b"abcdefghij"); b = blob((a1,a2)); b[10] = 9; assert_equal(bytes(a1), b"0123456789"); assert_equal(bytes(a2), b"\tbcdefghij");
  a1, a2 = bytearray(b"0123456789"), bytearray(b"abcdefghij"); b = blob((a1,a2)); b[8:14] = b"AZERTY"; assert_equal(bytes(a1), b"01234567AZ"); assert_equal(bytes(a2), b"ERTYefghij");
  a1, a2 = bytearray(b"0123456789"), bytearray(b"abcdefghij"); b = blob((a1,a2)); assert_raise(ValueError, lambda: b.__setitem__(slice(8,10), b"AZER")); #assert_equal(bytes(a1), b"01234567AZ"); assert_equal(bytes(a2), b"abcdefghij");
  a1, a2 = bytearray(b"0123456789"), bytearray(b"abcdefghij"); b = blob((a1,a2)); assert_raise(ValueError, lambda: b.__setitem__(slice(8,12), b"AZ")); #assert_equal(bytes(a1), b"01234567AZ"); assert_equal(bytes(a2), b"abcdefghij");

  # __eq__
  assert_equal(blob((b"abc",)), b"abc")
  assert_notequal(blob((b"abc",)), b"ab")
  assert_notequal(blob((b"abc",)), b"abd")
  assert_notequal(blob((b"abc",)), b"abcd")

  # __ge__
  assert blob((b"abc",)) >= b"aba"
  assert blob((b"abc",)) >= b"abc"
  assert not blob((b"abc",)) >= b"abd"
  assert blob((b"abc",)) >= b"ab"
  assert not blob((b"abc",)) >= b"abcd"

  # __gt__
  assert blob((b"abc",)) > b"aba"
  assert not blob((b"abc",)) > b"abc"
  assert not blob((b"abc",)) > b"abd"
  assert blob((b"abc",)) > b"ab"
  assert not blob((b"abc",)) > b"abcd"

  # __le__
  assert not blob((b"abc",)) <= b"aba"
  assert blob((b"abc",)) <= b"abc"
  assert blob((b"abc",)) <= b"abd"
  assert not blob((b"abc",)) <= b"ab"
  assert blob((b"abc",)) <= b"abcd"

  # __lt__
  assert not blob((b"abc",)) < b"aba"
  assert not blob((b"abc",)) < b"abc"
  assert blob((b"abc",)) < b"abd"
  assert not blob((b"abc",)) < b"ab"
  assert blob((b"abc",)) < b"abcd"

  # __add__ and __mul__
  assert_equal(blob((b"abc",)) + b"def", b"abcdef")
  assert_equal(blob((b"abc",)) * 2, b"abcabc")
  b = blob((bytearray(b"abc"),)) * 2
  b[0] = b"d"[0]
  assert_equal(b, b"dbcdbc")

  # count
  assert_equal(blob((b"abc",)).count(b"a"[0]), 1)
  assert_equal(blob((b"abc",)).count(b"b"[0]), 1)
  assert_equal(blob((b"abc",)).count(b"c"[0]), 1)
  assert_equal(blob((b"abc",)).count(b"d"[0]), 0)

  # index
  assert_equal(blob((b"abc",)).index(b"a"[0]), 0)
  assert_equal(blob((b"abc",)).index(b"b"[0]), 1)
  assert_equal(blob((b"abc",)).index(b"c"[0]), 2)
  assert_raise(ValueError, lambda: blob((b"abc",)).index(b"d"[0]))
  assert_raise(ValueError, lambda: blob((b"abc",)).index(b"a"[0], 1))
  assert_raise(ValueError, lambda: blob((b"abc",)).index(b"c"[0], 1, 2))
  assert_equal(blob((b"abc",)).index(b"b"[0], 1, 2), 1)

  # internal mechanism
  assert_equal(len(blob((b"abc",b"def",b"ghi"))._chunks), 3)
  assert_equal(len(blob((b"abc",b"def",b"ghi"))[3:6]._chunks), 1)
  #assert_equal(len(blob((b"abc",b"def",b"ghi")).detached()._chunks), 1)

def test_blob__readonly():
  def assign(o, k, v): o[k] = v

  b = blob((bytearray(b"lol"),), readonly=2)
  assert_equal(b.readonly, True)
  assert_equal(bytes(b), b"lol")
  assert_raise(TypeError, lambda: assign(b, 1, 2))
  assert_raise(TypeError, lambda: assign(b, slice(1, 3), b"34"))
  assert_raise(TypeError, lambda: assign(b[:], slice(1, 3), b"34"))
  assert_raise(TypeError, lambda: assign(b.slice(), slice(1, 3), b"34"))
