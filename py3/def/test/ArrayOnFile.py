def ArrayOnFile_tester(fn):
  def test(*a,**k):
    tmpdir = tempfile.mkdtemp()
    pwd = os.getcwd()
    try:
      os.chdir(tmpdir)
      #memos = MemOs()
      #memos.fread = lambda path: fs_readfile(path, os_module=memos)
      #memos.fwrite = lambda path, data: fs_writefile(path, data, os_module=memos)
      #a = (memos,) + a
      return fn(*a,**k)
    finally:
      os.chdir(pwd)
      shutil.rmtree(tmpdir)
  return test

def ArrayOnFile_assert_repr(faa, slice):
  reprfaa = repr(faa)
  reprslice = repr(slice)
  assert_equal(reprfaa[:12], "ArrayOnFile(")
  assert_equal(reprfaa[-len(reprslice) - 3:], ", " + reprslice + ")")
  int(reprfaa[12:-len(reprslice) - 3])
  assert len(str(faa)) < 60 + 12


@ArrayOnFile_tester
def test_ArrayOnFile_():
  fb = bytearray(b"0123456789azertyuiop&~|'(-`_^@")  # len 30
  with open(test_ArrayOnFile_.__name__, "wb") as f: f.write(fb)
  with ArrayOnFile.open(test_ArrayOnFile_.__name__, "rw") as fw:

    t = (b"1",b" ",b"0",b"01",b"0 ",b"00", fb, fb + b"x")
    for _ in t: assert (fw > _) == (fb > _), (_, bytes(fw) > _, fw > _, fb > _)
    for _ in t: assert (fw >= _) == (fb >= _), _
    for _ in t: assert (fw < _) == (fb < _), _
    for _ in t: assert (fw <= _) == (fb <= _), _
    for _ in t: assert (fw == _) == (fb == _), _
    for _ in t: assert (fw != _) == (fb != _), _

    ArrayOnFile_assert_repr(fw, slice(0, None, 1))
    assert_equal(fw, fb)  # fw

    ArrayOnFile_assert_repr(fw[:10], slice(0, 10, 1))
    fw[:10] = fw[9::-1]
    fb[:10] = fb[9::-1]
    assert_equal(fw, fb)  # fw[:10]

    ArrayOnFile_assert_repr(fw[1:-1], slice(1, 29, 1))
    ArrayOnFile_assert_repr(fw[1:-1][1:8], slice(2, 9, 1))
    fw[1:-1][1:8] = fw[8:1:-1]
    fb[2:9] = fb[8:1:-1]
    assert_equal(fw, fb)  # fw[1:-1][1:8]

    ArrayOnFile_assert_repr(fw[5::-1], slice(5, None, -1))
    ArrayOnFile_assert_repr(fw[5::-1][1:3], slice(4, 2, -1))
    fw[5::-1][1:3] = fw[10:12]
    fb[4:2:-1] = fb[10:12]
    assert_equal(fw, fb)  # fw[5::-1][1:3]

    ArrayOnFile_assert_repr(fw[1:-1:2], slice(1, 29, 2))
    ArrayOnFile_assert_repr(fw[1:-1:2][1:3], slice(3, 7, 2))
    fw[1:-1:2][1:3] = fw[20:22]
    fb[3:7:2] = fb[20:22]
    assert_equal(fw, fb)  # fw[1:-1:2][1:3]

    ArrayOnFile_assert_repr(fw[-2:0:-2], slice(28, 0, -2))
    ArrayOnFile_assert_repr(fw[-2:0:-2][1:3], slice(26, 22, -2))
    ArrayOnFile_assert_repr(fw[-4:-8:-2], slice(26, 22, -2))
    fw[-2:0:-2][1:3] = fw[:2]
    fb[-4:-8:-2] = fb[:2]
    assert_equal(fw, fb)  # fw[-2:0:-2][1:3]

  assert_raise(OSError, lambda: fw[:])  # unable to read a closed ArrayOnFile

@ArrayOnFile_tester
def test_ArrayOnFile_iadd_imul():
  fb = bytearray(b"0123456789azertyuiop&~|'(-`_^@")  # len 30
  with open(test_ArrayOnFile_iadd_imul.__name__, "wb") as f: f.write(fb)
  with ArrayOnFile.open(test_ArrayOnFile_iadd_imul.__name__, "rw") as fw:
    fb += b"lol"
    fw += b"lol"
    assert_equal(bytes(fw), fb)  # fw += b"lol"
    fb *= 3
    fw *= 3
    assert_equal(bytes(fw), fb)  # fw *= 3
    fb *= -1
    fw *= -1
    assert_equal(bytes(fw), fb)  # fw *= -1

    # iadd and imul are forbidden on slice
    def iadd(o, v): o += v
    def imul(o, v): o *= v
    fw = fw[:]  # here is a slice
    assert_raise(ValueError, lambda: iadd(fw, b"yep"))
    assert_raise(ValueError, lambda: imul(fw, 2))

@ArrayOnFile_tester
def test_ArrayOnFile_resizing__setitem__():
  fb = bytearray(b"0123456789azertyuiop&~|'(-`_^@")  # len 30
  with open(test_ArrayOnFile_resizing__setitem__.__name__, "wb") as f: f.write(fb)
  with ArrayOnFile.open(test_ArrayOnFile_resizing__setitem__.__name__, "rw") as fw:
    # 7 less
    fb[20:] = b"lol"
    fw[20:] = b"lol"
    assert_equal(fw, fb)  # fw[20:] = b"lol"
    # 2 more
    fb[20:] = b"hello"
    fw[20:] = b"hello"
    assert_equal(fw, fb)  # fw[20:] = b"hello"
    # truncate 0
    fb[:] = b""
    fw[:] = b""
    assert_equal(fw, fb)  # fw[:] = b""

    fw += b"012345"
    # resizing setitem are fobidden on slices
    def setitem(o, key, v): o[key] = v
    fw = fw[:]  # here is a slice
    assert_raise(ValueError, lambda: setitem(fw, slice(None), b"1234567890"))
    assert_raise(ValueError, lambda: setitem(fw, slice(None), b"ab"))
    assert_raise(ValueError, lambda: setitem(fw, slice(None), b""))
