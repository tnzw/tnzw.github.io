def opennewfile__tester(fn):
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

@opennewfile__tester
def test_opennewfile():
  with open("hey", "w") as f: assert_equal(f.name, "hey")
  with open(b"hoo", "w") as f: assert_equal(f.name, b"hoo")  # check open behavior
  with opennewfile("lol") as f: assert_equal(f.name, "lol")
  with opennewfile("lol") as f: assert_equal(f.name, "lol_1")
  with opennewfile("lol") as f: assert_equal(f.name, "lol_2")
  with opennewfile(b"lol") as f: assert_equal(f.name, b"lol_3")
  with opennewfile(".lol") as f: assert_equal(f.name, ".lol")
  with opennewfile(".lol") as f: assert_equal(f.name, ".lol_1")
  with opennewfile(b".lol") as f: assert_equal(f.name, b".lol_2")
  with opennewfile("a.lol") as f: assert_equal(f.name, "a.lol")
  with opennewfile("a.lol") as f: assert_equal(f.name, "a_1.lol")
  with opennewfile(b"a.lol") as f: assert_equal(f.name, b"a_2.lol")
  with opennewfile(b"b.lol") as f: assert_equal(f.name, b"b.lol")
  with opennewfile(b"b.lol") as f: assert_equal(f.name, b"b_1.lol")
  with opennewfile("b.lol") as f: assert_equal(f.name, "b_2.lol")

  with opennewfile( "name.ext", base_format="{n} ({i}){e}") as f: assert_equal(f.name,  "name.ext")
  with opennewfile( "name.ext", base_format="{n} ({i}){e}") as f: assert_equal(f.name,  "name (1).ext")
  with opennewfile(b"name.ext", base_format="{n} ({i}){e}") as f: assert_equal(f.name, b"name (2).ext")

  with opennewfile("nfo", first_open=False) as f: assert_equal(f.name, "nfo_1")
  with opennewfile("nfo", first_open=False) as f: assert_equal(f.name, "nfo_2")
  with opennewfile("nfo", first_open=False, start_index=15) as f: assert_equal(f.name, "nfo_15")

@opennewfile__tester
def test_opennewfile__invalid_base_format():
  with opennewfile("name.ext", base_format="invalid format") as f: assert_equal(f.name, "name.ext")
  assert_raise(ValueError, lambda: opennewfile("name.ext", base_format="invalid format"))
  assert_raise(ValueError, lambda: opennewfile("name2.ext", base_format="invalid format", first_open=False))

@opennewfile__tester
def test_opennewfile__bytes_base_format():
  with opennewfile( "name.ext", base_format=b"{n}({i}){e}") as f: assert_equal(f.name,  "name.ext")
  with opennewfile( "name.ext", base_format=b"{n}({i}){e}") as f: assert_equal(f.name,  "name(1).ext")
  with opennewfile(b"name.ext", base_format=b"{n}({i}){e}") as f: assert_equal(f.name, b"name(2).ext")

@opennewfile__tester
def test_opennewfile__custom_base_format():
  class base64_formatter(object):  # yes... just for a test case uh
    def format(self, **k):
      encoding = ("UTF-8", "surrogateescape")  # lossless
      result = base64.b64encode(repr((k["name"], k["index"], k["extension"])).encode(*encoding)).replace(b"+", b"-").replace(b"/", b"_").rstrip(b"=")
      if isinstance(k["base"], str): return result.decode()
      return result

  with opennewfile( "name.ext", base_format=base64_formatter()) as f: assert_equal(f.name,  "name.ext")
  with opennewfile( "name.ext", base_format=base64_formatter()) as f: assert_equal(f.name,  "KCduYW1lJywgMSwgJy5leHQnKQ")
  with opennewfile( "name.ext", base_format=base64_formatter()) as f: assert_equal(f.name,  "KCduYW1lJywgMiwgJy5leHQnKQ")
  with opennewfile(b"name.ext", base_format=base64_formatter()) as f: assert_equal(f.name, b'KGInbmFtZScsIDEsIGInLmV4dCcp')

  class random_formatter(object):  # usefull for an `mktemp` like method
    def format(self, **k):
      encoding = ("UTF-8", "surrogateescape")  # lossless
      base = k["base"]
      k = {k: (v.decode(*encoding) if isinstance(v, bytes) else v) for k, v in k.items()}
      k["rand"] = base64.b64encode(os.urandom(3)).replace(b"+", b"-").replace(b"/", b"_").rstrip(b"=").decode()
      result = "{base}.{rand}".format(**k)
      if isinstance(base, bytes): return result.encode(*encoding)
      return result

  with opennewfile( "rand.ext", base_format=random_formatter(), first_open=False) as f: print("   'rand.ext'", repr(f.name)), assert_notequal(f.name,  "rand.ext")
  with opennewfile(b"rand.ext", base_format=random_formatter(), first_open=False) as f: print("  b'rand.ext'", repr(f.name)), assert_notequal(f.name, b"rand.ext")
