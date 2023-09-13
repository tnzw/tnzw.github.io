def test_HexDumpEncoder():
  hce = HexDumpEncoder()
  assert_equal(hce.encode(b'abcdefghij'), b'00000000  61 62 63 64 65 66 67 68  69 6A                    |abcdefghij|')
  hce = HexDumpEncoder()
  assert_equal(hce.encode(b'abcdefghijklmnopqrstuvwxyz'), b'''\
00000000  61 62 63 64 65 66 67 68  69 6A 6B 6C 6D 6E 6F 70  |abcdefghijklmnop|
00000010  71 72 73 74 75 76 77 78  79 7A                    |qrstuvwxyz|''')
  assert_equal(hce.encode(b'AB', stream=True), b'\n0000001A                                 41 42')
  assert_equal(hce.encode(b'CD'), b' 43 44                  |ABCD|')
  hce = HexDumpEncoder()
  assert_equal(hce.encode(b'abcdefghijklmnop', stream=True), b'''\
00000000  61 62 63 64 65 66 67 68  69 6A 6B 6C 6D 6E 6F 70  |abcdefghijklmnop|''')
  assert_equal(hce.encode(b'qrstuvwxyz'), b'\n00000010  71 72 73 74 75 76 77 78  79 7A                    |qrstuvwxyz|')
  hce = HexDumpEncoder()
  assert_equal(hce.encode(b'abcdefghijklmnopqrstuvw', stream=True), b'''\
00000000  61 62 63 64 65 66 67 68  69 6A 6B 6C 6D 6E 6F 70  |abcdefghijklmnop|
00000010  71 72 73 74 75 76 77''')
  assert_equal(hce.encode(b'xyz'), b' 78  79 7A                    |qrstuvwxyz|')
  assert_equal(hce.encode(b'ABCDEFGHIJ'), b'''\n\
0000001A                                 41 42 43 44 45 46            |ABCDEF|
00000020  47 48 49 4A                                       |GHIJ|''')
