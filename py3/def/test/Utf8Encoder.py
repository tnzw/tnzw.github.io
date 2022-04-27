def test_Utf8Encoder():
  assert_equal(Utf8Encoder().encode("lol"), b"lol")
  assert_equal(Utf8Encoder(errors="surrogatepass").encode("lol\ud900lal"), b"lol\xed\xa4\x80lal")
  assert_equal(Utf8Encoder(errors="replace").encode("lol\ud900lal"), b"lol?lal")
  assert_equal(Utf8Encoder(errors="replace", replacement=b"!bim!").encode("lol\ud900lal"), b"lol!bim!lal")
  assert_equal(Utf8Encoder(errors="replace", replacer=lambda c: f"{repr(chr(c))[1:-1]}".encode()).encode("lol\ud900lal"), b"lol\\ud900lal")  # almost equiv to errors=namereplace
