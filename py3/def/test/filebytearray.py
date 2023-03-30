def filebytearray__tester(fn):
  def test(*a,**k):
    tmpdir = tempfile.mkdtemp()
    pwd = os.getcwd()
    try:
      os.chdir(tmpdir)
      return fn(*a,**k)
    finally:
      os.chdir(pwd)
      shutil.rmtree(tmpdir)
  return test

@filebytearray__tester
def test_filebytearray__getitem__():
  with filebytearray('tmp', 'w+', blksize=3) as fba:
    fba[:] = b'abcdefg'
    assert type(fba[:]) is bytearray, type(fba[:])
    assert type(fba[0]) is int, type(fba[0])  # [int] get
    assert fba[0] == 0x61, fba[0]  # [int] get
    assert fba[-1] == 0x67, fba[-1]  # [int] get
    assert_raise(IndexError, lambda: fba[7])  # [int] out of range
    assert_raise(IndexError, lambda: fba[-8])  # [int] neg index
    assert fba[:] == b'abcdefg', fba[:]  # [slice] get
    assert fba[-10:10] == b'abcdefg', fba[-10:10]  # [slice] out of range

@filebytearray__tester
def test_filebytearray__setitem__():
  def setitem(o, k, v): o[k] = v
  with filebytearray('tmp', 'w+') as fba:
    fba[:] = b'abcdefg'  # [slice] extend
    fba[0] = 0x30  # [int] overwrite
    assert fba == b'0bcdefg', fba[:]
    fba[-1] = 0x36  # [int] overwrite
    assert fba == b'0bcdef6', fba[:]
    assert_raise(IndexError, lambda: setitem(fba, 7, 0x37))  # [int] append
    assert_raise(IndexError, lambda: setitem(fba, -8, 0x29))  # [int] neg index
    assert_raise(IndexError, lambda: setitem(fba, 9, 0x39))  # [int] write sparse data
    assert_raise(ValueError, lambda: setitem(fba, slice(0, 3), b'01'))  # [slice] pop & rewrite
    fba[0:3] = b'012'  # [slice] overwrite
    assert fba == b'012def6', fba[:]
    fba[:] = b'01'  # [slice] truncate
    assert fba == b'01', fba[:]
    fba[1:] = b'123'  # [slice] overwrite & extend
    assert fba == b'0123', fba[:]
    fba[6:9] = b'678'  # [slice] write sparse data
    assert fba == b'0123\x00\x00678', fba[:]
    assert_raise(ValueError, lambda: setitem(fba, slice(6,9,2), b'68X'))  # [extended slice] write sparse data

@filebytearray__tester
def test_filebytearray__pop():
  with filebytearray('tmp', 'w+') as fba:
    fba[:] = b'abcdefg'  # len: 7
    assert_equal(fba.pop(), b'g'[0])  # now len: 6
    assert_equal(fba.pop(5), b'f'[0])  # now len: 5
    assert_raise(ValueError, lambda: fba.pop(3))  # pop inside a file is disabled
    assert_equal(fba.pop(-1), b'e'[0])  # now len: 4
    assert_raise(IndexError, lambda: fba.pop(4))
    assert_raise(IndexError, lambda: fba.pop(-5))
    fba[:] = b''  # now len: 0
    assert_raise(IndexError, lambda: fba.pop())  # still len: 0
    assert_raise(TypeError, lambda: fba.pop(None))

@filebytearray__tester
def test_filebytearray__insert():
  with filebytearray('tmp', 'w+') as fba:
    fba[:] = b'abcdefg'  # len: 7
    fba.insert(7, b'h'[0])
    assert fba == b'abcdefgh'
    assert_raise(ValueError, lambda: fba.insert(3, 32))  # inserti inside a file is disabled
    assert_raise(ValueError, lambda: fba.insert(-1, 32))  # inserti inside a file is disabled

@filebytearray__tester
def test_filebytearray__eq__():
  with filebytearray('tmp', 'w+', blksize=3) as fba:
    fba[:] = b'abcdefg'
    assert fba == fba       , fba[:]
    assert fba == b'abcdefg', fba[:]
    assert fba != b'abcdef' , fba[:]
    assert fba != b'abcdefh', fba[:]
    assert fba != tuple(b'abcdefg')  # like bytearray(b'abcdefg') != tuple(b'abcdefg')
    with filebytearray('tmp2', 'w+', blksize=5) as fba2:
      fba2[:] = b'abcdefg'
      assert fba == fba2

@filebytearray__tester
def test_filebytearray__ge__():
  with filebytearray('tmp', 'w+', blksize=3) as fba:
    fba[:] = b'abcdefg'
    assert fba >= b'aa'
    assert fba >= b'abcdef'
    assert fba >= b'abcdefg'
    assert not (fba >= b'abcdefgh')
    assert not (fba >= b'zz')

@filebytearray__tester
def test_filebytearray__gt__():
  with filebytearray('tmp', 'w+', blksize=3) as fba:
    fba[:] = b'abcdefg'
    assert fba > b'aa'
    assert fba > b'abcdef'
    assert not (fba > b'abcdefg')
    assert not (fba > b'abcdefgh')
    assert not (fba > b'zz')

@filebytearray__tester
def test_filebytearray__le__():
  with filebytearray('tmp', 'w+', blksize=3) as fba:
    fba[:] = b'abcdefg'
    assert not (fba <= b'aa')
    assert not (fba <= b'abcdef')
    assert fba <= b'abcdefg'
    assert fba <= b'abcdefgh'
    assert fba <= b'zz'

@filebytearray__tester
def test_filebytearray__lt__():
  with filebytearray('tmp', 'w+', blksize=3) as fba:
    fba[:] = b'abcdefg'
    assert not (fba < b'aa')
    assert not (fba < b'abcdef')
    assert not (fba < b'abcdefg')
    assert fba < b'abcdefgh'
    assert fba < b'zz'

@filebytearray__tester
def test_filebytearray__islower():
  with filebytearray('tmp', 'w+', blksize=3) as fba:
    fba[:] = b''
    assert not fba.islower()
    fba[:] = b'.'
    assert not fba.islower()
    fba[:] = b'abc.def'
    assert fba.islower()
    fba[:] = b'abc.deF'
    assert not fba.islower()

@filebytearray__tester
def test_filebytearray__isupper():
  with filebytearray('tmp', 'w+', blksize=3) as fba:
    fba[:] = b''
    assert not fba.isupper()
    fba[:] = b'.'
    assert not fba.isupper()
    fba[:] = b'ABC.DEF'
    assert fba.isupper()
    fba[:] = b'ABC.DEf'
    assert not fba.isupper()

@filebytearray__tester
def test_filebytearray__isalnum():
  with filebytearray('tmp', 'w+', blksize=3) as fba:
    fba[:] = b'abcdefg'; assert fba.isalnum()
    fba[:] = b'0123456'; assert fba.isalnum()
    fba[:] = b'abCD456'; assert fba.isalnum()
    fba[:] = b''; assert not fba.isalnum()
    fba[:] = b'abc.def'; assert not fba.isalnum()
    fba[:] = b' 123456'; assert not fba.isalnum()

@filebytearray__tester
def test_filebytearray__isalpha():
  with filebytearray('tmp', 'w+', blksize=3) as fba:
    fba[:] = b'abcdefg'; assert fba.isalpha()
    fba[:] = b'0123456'; assert not fba.isalpha()
    fba[:] = b'abCDefg'; assert fba.isalpha()
    fba[:] = b'abCD456'; assert not fba.isalpha()
    fba[:] = b''; assert not fba.isalpha()
    fba[:] = b'abc.def'; assert not fba.isalpha()
    fba[:] = b' 123456'; assert not fba.isalpha()

@filebytearray__tester
def test_filebytearray__isascii():
  with filebytearray('tmp', 'w+', blksize=3) as fba:
    fba[:] = b'abCD456'; assert fba.isascii()
    fba[:] = b'abCD45\x80'; assert not fba.isascii()
    fba[:] = b'\x00bcdefg'; assert fba.isascii()
    fba[:] = b'\x00bcdef\x80'; assert not fba.isascii()
    fba[:] = b''; assert fba.isascii()

@filebytearray__tester
def test_filebytearray__isdigit():
  with filebytearray('tmp', 'w+', blksize=3) as fba:
    fba[:] = b'abcdefg'; assert not fba.isdigit()
    fba[:] = b'0123456'; assert fba.isdigit()
    fba[:] = b'abCDefg'; assert not fba.isdigit()
    fba[:] = b'abCD456'; assert not fba.isdigit()
    fba[:] = b''; assert not fba.isdigit()
    fba[:] = b'123.456'; assert not fba.isdigit()
    fba[:] = b' 123456'; assert not fba.isdigit()

@filebytearray__tester
def test_filebytearray__isspace():
  with filebytearray('tmp', 'w+', blksize=3) as fba:
    fba[:] = b'abcdefg'; assert not fba.isspace()
    fba[:] = b'\t\n\x0b\x0c\r '; assert fba.isspace()
    fba[:] = b''; assert not fba.isspace()
    fba[:] = b' 123456'; assert not fba.isspace()

@filebytearray__tester
def test_filebytearray__find():  # mainly testing os_find_in_file()
  with filebytearray('tmp', 'w+', blksize=2) as fba:
    fba[:] = b'abcdefg'
    assert_equal(fba.find(b''), 0)
    assert_equal(fba.find(b'', 1), 1)
    assert_equal(fba.find(b'', 10), -1)
    assert_equal(fba.find(b'abc'), 0)
    assert_equal(fba.find(b'def'), 3)
    assert_equal(fba.find(b'def', 2), 3)
    assert_equal(fba.find(b'def', 4), -1)
    assert_equal(fba.find(b'def', 0, -1), 3)
    assert_equal(fba.find(b'def', 0, -2), -1)
    assert_equal(fba.find(b'def', 2, -1), 3)
    assert_equal(fba.find(b'def', 3, -1), 3)
    assert_equal(fba.find(b'def', 4, -1), -1)
    # XXX more tests please

@filebytearray__tester
def test_filebytearray__reverse():
  with filebytearray('tmp', 'w+', blksize=2) as fba:
    fba[:] = b'abcdefg'
    fba.reverse()
    assert fba == b'gfedcba', fba[:]

@filebytearray__tester
def test_filebytearray__startswith():
  with filebytearray('tmp', 'w+', blksize=2) as fba:
    fba[:] = b'abcdefg'
    assert fba.startswith(b'')
    assert fba.startswith(b'', 10, -20)
    assert fba.startswith(b'abc')
    assert fba.startswith((b'lol', b'abc'))
    assert not fba.startswith((b'lol', b'abc'), 1)
    assert fba.startswith((b'lol', b'bcd'), 1)
    assert fba.startswith((b'lol', b'efg'), -3)
    assert not fba.startswith((b'lol', b'efg'), -2)
    assert not fba.startswith((b'lol', b'efg'), -3, -1)
    assert not fba.startswith((b'l', b'g'), 10)

@filebytearray__tester
def test_filebytearray__endswith():
  with filebytearray('tmp', 'w+', blksize=2) as fba:
    fba[:] = b'abcdefg'
    assert fba.endswith(b'')
    assert fba.endswith(b'', 10, -20)
    assert fba.endswith(b'efg')
    assert fba.endswith((b'lol', b'efg'))
    assert not fba.endswith((b'lol', b'efg'), 0, 5)
    assert fba.endswith((b'lol', b'efg'), 4)
    assert fba.endswith((b'lol', b'abc'), 0, 3)
    assert not fba.endswith((b'lol', b'abc'), 0, 2)
    assert fba.endswith((b'lol', b'efg'), -3)
    assert not fba.endswith((b'lol', b'efg'), -3, -1)
    assert not fba.endswith((b'l', b'g'), 10)
