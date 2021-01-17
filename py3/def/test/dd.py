def dd_tester(fn):
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
def dd_status(*args, status=None, **kw):
  def bytesstr(n):
    suffix = "B"
    for new_suffix in ("K", "M", "G", "T", "P", "E", "Z", "Y"):
      if n / 1024 >= 1:
        n /= 1024
        suffix = new_suffix
      else: break
    #return ("{:." + str(2 if n < 10 else 1) + "f}{}").format(n, suffix)
    #return f"{n:.1f} {suffix}"
    #return "{:." + str(accuracy) + "f} {}".format(n, suffix)
    return (str(n) if isinstance(n, int) else f"{n:.1f}") + f" {suffix}"
  def timestr(n):
    n, m = divmod(n, 60)
    s = f"{m:.3f} s"
    if n == 0: return s
    n, m = divmod(n, 60)
    s = f"{m:.0f} m " + s
    if n == 0: return s
    n, m = divmod(n, 24)
    s = f"{m:.0f} h " + s
    if n == 0: return s
    return f"{n:.0f} j " + s
  if status is None: status = "progress"
  it = None
  try:
    it = dd.iter(*args, **kw)
    if status != "none": ii = i = time.time()
    rr = ww = 0
    for _ in it:
      if isinstance(_, (bytes, bytearray)): rr += len(_)
      elif isinstance(_, int): ww += _
      if status != "none":
        i2 = time.time()
        delta = i2 - i
        if delta > 1:
          idelta = i2 - ii
          #if status == "progress": print("read " + bytesstr(rr) + " (" + bytesstr(rr//idelta) + "/s), written " + bytesstr(ww) + " (" + bytesstr(ww//idelta) + "/s)...", file=sys.stderr)
          #if status == "progress": print("copying " + bytesstr(ww) + " (" + bytesstr(ww//idelta) + "/s)...", file=sys.stderr)
          if status == "progress": print(bytesstr(ww) + " copied, " + timestr(idelta) + ", " + bytesstr(ww//idelta) + "/s...", file=sys.stderr)
          i = i2
    if status != "none" and status != "noxfer":
      idelta = time.time() - ii
      #print("read " + bytesstr(rr) + " (" + bytesstr(rr//idelta) + "/s), written " + bytesstr(ww) + " (" + bytesstr(ww//idelta) + "/s).", file=sys.stderr)
      print(bytesstr(ww) + " copied, " + timestr(idelta) + ", " + bytesstr(ww//idelta) + "/s", file=sys.stderr)
  finally:
    if it is not None: it.close()

@dd_tester
def test_dd_():
  fs_writefile("if", b"1234....abcd")
  dd("if", "of")
  assert_equal(b"1234....abcd", fs_readfile("of"))
@dd_tester
def test_dd_bs4():
  fs_writefile("if", b"1234....abcd")
  dd("if", "of", bs=4)
  assert_equal(b"1234....abcd", fs_readfile("of"))
@dd_tester
def test_dd_bs4_sync_1():
  fs_writefile("if", b"1234....abcd")
  dd("if", "of", bs=4, conv=dd.CONV_SYNC)
  assert_equal(b"1234....abcd", fs_readfile("of"))
@dd_tester
def test_dd_bs4_sync_2():
  fs_writefile("if", b"1234....ab")
  dd("if", "of", bs=4, conv=dd.CONV_SYNC)
  assert_equal(b"1234....ab\0\0", fs_readfile("of"))
@dd_tester
def test_dd_bs4_count1():
  fs_writefile("if", b"1234....abcd")
  dd("if", "of", bs=4, count=1)
  assert_equal(b"1234", fs_readfile("of"))
@dd_tester
def test_dd_bs4_count1_skip2():
  fs_writefile("if", b"1234....abcd")
  dd("if", "of", bs=4, count=1, skip=2)
  assert_equal(b"abcd", fs_readfile("of"))
@dd_tester
def test_dd_bs4_count1_skip2_seek1():
  fs_writefile("if", b"1234....abcd")
  dd("if", "of", bs=4, count=1, skip=2, seek=1)
  assert_equal(b"\0" * 4, fs_readfile("of")[:4])
  assert_equal(b"abcd", fs_readfile("of")[4:])
@dd_tester
def test_dd_bs4_count1_skip2_seek1_swab():
  fs_writefile("if", b"1234....abcd")
  dd("if", "of", bs=4, count=1, skip=2, seek=1, conv=dd.CONV_SWAB)
  assert_equal(b"\0" * 4, fs_readfile("of")[:4])
  assert_equal(b"badc", fs_readfile("of")[4:])
@dd_tester
def test_dd_bs4_count3_skip2_seek1_countbytes():
  fs_writefile("if", b"1234....abcd")
  dd("if", "of", bs=4, count=3, skip=2, seek=1, iflag=dd.FLAG_COUNT_BYTES)
  assert_equal(b"\0" * 4, fs_readfile("of")[:4])
  assert_equal(b"abc", fs_readfile("of")[4:])
@dd_tester
def test_dd_bs4_count3_skip2_seek1_countbytes_swab():
  fs_writefile("if", b"1234....abcd")
  dd("if", "of", bs=4, count=3, skip=2, seek=1, iflag=dd.FLAG_COUNT_BYTES, conv=dd.CONV_SWAB)
  assert_equal(b"\0" * 4, fs_readfile("of")[:4])
  assert_equal(b"bac", fs_readfile("of")[4:])
@dd_tester
def test_dd_cbs1_block():
  fs_writefile("if", b"123\n\n45\n6\n\n\n")
  dd("if", "of", cbs=1, conv=dd.CONV_BLOCK)
  assert_equal(b"1 46  ", fs_readfile("of"))
@dd_tester
def test_dd_cbs2_block():
  fs_writefile("if", b"123\n\n45\n6\n\n\n")
  dd("if", "of", cbs=2, conv=dd.CONV_BLOCK)
  assert_equal(b"12  456     ", fs_readfile("of"))
@dd_tester
def test_dd_cbs3_block():
  fs_writefile("if", b"123\n\n45\n6\n\n\n")
  dd("if", "of", cbs=3, conv=dd.CONV_BLOCK)
  assert_equal(b"123   45 6        ", fs_readfile("of"))
@dd_tester
def test_dd_cbs4_block():
  fs_writefile("if", b"123\n\n45\n6\n\n\n")
  dd("if", "of", cbs=4, conv=dd.CONV_BLOCK)
  assert_equal(b"123     45  6           ", fs_readfile("of"))
@dd_tester
def test_dd_cbs1_unblock_1():
  fs_writefile("if", b"123     45  6           ")
  dd("if", "of", cbs=1, conv=dd.CONV_UNBLOCK)
  assert_equal(b"1\n2\n3\n\n\n\n\n\n4\n5\n\n\n6\n\n\n\n\n\n\n\n\n\n\n\n", fs_readfile("of"))
@dd_tester
def test_dd_cbs2_unblock_1():
  fs_writefile("if", b"123     45  6           ")
  dd("if", "of", cbs=2, conv=dd.CONV_UNBLOCK)
  assert_equal(b"12\n3\n\n\n45\n\n6\n\n\n\n\n\n", fs_readfile("of"))
@dd_tester
def test_dd_cbs3_unblock_1():
  fs_writefile("if", b"123     45  6           ")
  dd("if", "of", cbs=3, conv=dd.CONV_UNBLOCK)
  assert_equal(b"123\n\n  4\n5\n6\n\n\n\n", fs_readfile("of"))
@dd_tester
def test_dd_cbs4_unblock_1():
  fs_writefile("if", b"123     45  6           ")
  dd("if", "of", cbs=4, conv=dd.CONV_UNBLOCK)
  assert_equal(b"123\n\n45\n6\n\n\n", fs_readfile("of"))
@dd_tester
def test_dd_cbs1_unblock_2():
  fs_writefile("if", b"123    45 6          ")
  dd("if", "of", cbs=1, conv=dd.CONV_UNBLOCK)
  assert_equal(b"1\n2\n3\n\n\n\n\n4\n5\n\n6\n\n\n\n\n\n\n\n\n\n\n", fs_readfile("of"))
@dd_tester
def test_dd_cbs2_unblock_2():
  fs_writefile("if", b"123    45 6          ")
  dd("if", "of", cbs=2, conv=dd.CONV_UNBLOCK)
  assert_equal(b"12\n3\n\n 4\n5\n6\n\n\n\n\n\n", fs_readfile("of"))
@dd_tester
def test_dd_cbs3_unblock_2():
  fs_writefile("if", b"123    45 6          ")
  dd("if", "of", cbs=3, conv=dd.CONV_UNBLOCK)
  assert_equal(b"123\n\n 45\n 6\n\n\n\n", fs_readfile("of"))
@dd_tester
def test_dd_cbs4_unblock_2():
  fs_writefile("if", b"123    45 6          ")
  dd("if", "of", cbs=4, conv=dd.CONV_UNBLOCK)
  assert_equal(b"123\n   4\n5 6\n\n\n\n", fs_readfile("of"))
@dd_tester
def test_dd_bs4_cbs1_unblock_sync():
  fs_writefile("if", b"123    45 6          ")
  dd("if", "of", bs=4, cbs=1, conv=dd.CONV_SYNC | dd.CONV_UNBLOCK)
  assert_equal(b"1\n2\n3\n\n\n\n\n4\n5\n\n6\n\n\n\n\n\n\n\n\n\n\n\n\n\n", fs_readfile("of"))
@dd_tester
def test_dd_bs4_cbs2_unblock_sync():
  fs_writefile("if", b"123    45 6          ")
  dd("if", "of", bs=4, cbs=2, conv=dd.CONV_SYNC | dd.CONV_UNBLOCK)
  assert_equal(b"12\n3\n\n 4\n5\n6\n\n\n\n\n\n\n", fs_readfile("of"))
@dd_tester
def test_dd_bs4_cbs3_unblock_sync():
  fs_writefile("if", b"123    45 6          ")
  dd("if", "of", bs=4, cbs=3, conv=dd.CONV_SYNC | dd.CONV_UNBLOCK)
  assert_equal(b"123\n\n 45\n 6\n\n\n\n\n", fs_readfile("of"))
@dd_tester
def test_dd_bs4_cbs4_unblock_sync():
  fs_writefile("if", b"123    45 6          ")
  dd("if", "of", bs=4, cbs=4, conv=dd.CONV_SYNC | dd.CONV_UNBLOCK)
  assert_equal(b"123\n   4\n5 6\n\n\n\n", fs_readfile("of"))
@dd_tester
def test_dd_write_on_device():
  if 0:
    ifile = "C:\\Users\\tc\\Desktop\\EntreLeursMains\\Entre Leurs Mains.mkv"
    lifile = os.stat(ifile).st_size
    tfile = "C:\\Users\\tc\\Desktop\\EntreLeursMains\\Entre Leurs Mains_2.mkv"
    #ofile = "/dev/sdb"
    #ofile = '\\\\.\\PhysicalDrive1'
    ofile = '\\\\?\\GLOBALROOT\\Device\\00000074'
    #test_data = b"XXX"
    #lifile = len(test_data)
    #fs_writefile("if", test_data)
    #lsblk()  # prints block device list
    print("/!\\ Please open diskmgmt.msc to remove all device volumes. (Returned message could be \"Method is not handled\" but still it works)")
    print("writing to device...")
    dd_status(ifile, ofile, bs=32 * 1024, conv=dd.CONV_SYNC | dd.CONV_NOCREAT | dd.CONV_NOTRUNC | dd.CONV_FSYNC, oflag=dd.FLAG_FORCE_SEEK)  # oflag=force_seek is required on windows when writing device
    print("reading from device...")
    dd_status(ofile, tfile, bs=32 * 1024, count=lifile, iflag=dd.FLAG_COUNT_BYTES | dd.FLAG_FORCE_SEEK)  # iflag=force_seek is required on windows when reading device
    print("done")
    #assert_equal(test_data, fs_readfile("tf"))
  else:
    print("please run the test manually (see code)")
