def test_zipfile__helloworld():
  # I'm gonna zip an "Hello.txt" file
  filename_ascii = b'Hello.txt'
  data = b'Hello World\n'
  st_mode = 0o100666  # REG file
  st_mtime = 1681291380.5431685  # 1681291380 is 2023-04-12 09:23:00 GMT+0 or 2023-04-12 11:23:00 GMT+2
  #####
  ddt = 0x568c5ae1  # = dosdatetime_fromtimestamp(st_mtime, True) = 2023-04-12 11:23:00 (naive)
  crc32 = 2962613731  # = zlib.crc32(data)
  #####
  CM_STORE = 0
  VM_UNIX = 0x31E
  # 0xA is the version needed used by 7zip when adding normal file entries
  #####
  loc = zipfile_struct_mklocrecord(0xA, 0, CM_STORE, ddt, crc32, len(data), len(data), filename_ascii)  # we may add a comment extrafield to LOC extrafields
  cen = zipfile_struct_mkcenrecord(VM_UNIX, 0xA, 0, CM_STORE, ddt, crc32, len(data), len(data), 0, 0, st_mode << 16, 0, filename_ascii)
  eocd = zipfile_struct_mkeocdrecord(0, 0, 1, 1, len(cen), len(loc) + len(data))
  zipdata = loc + data + cen + eocd
  #open('test.helloworld.zip', 'wb').write(zipdata)
  # splitting like this works!
  #open('test.helloworld.zip.001', 'wb').write(zipdata[:100])
  #open('test.helloworld.zip.002', 'wb').write(zipdata[100:])
  assert_nodiff(list(hexdump.iter(zipdata)), [
    "00000000  50 4B 03 04 0A 00 00 00  00 00 E1 5A 8C 56 E3 E5  |PK.........Z.V..|",
    "00000010  95 B0 0C 00 00 00 0C 00  00 00 09 00 00 00 48 65  |..............He|",
    "00000020  6C 6C 6F 2E 74 78 74 48  65 6C 6C 6F 20 57 6F 72  |llo.txtHello Wor|",
    "00000030  6C 64 0A 50 4B 01 02 1E  03 0A 00 00 00 00 00 E1  |ld.PK...........|",
    "00000040  5A 8C 56 E3 E5 95 B0 0C  00 00 00 0C 00 00 00 09  |Z.V.............|",
    "00000050  00 00 00 00 00 00 00 00  00 00 00 B6 81 00 00 00  |................|",
    "00000060  00 48 65 6C 6C 6F 2E 74  78 74 50 4B 05 06 00 00  |.Hello.txtPK....|",
    "00000070  00 00 01 00 01 00 37 00  00 00 33 00 00 00 00 00  |......7...3.....|"],
    'Hello.txt.zip', 'expected')

def test_zipfile__helloworlddir():
  # I'm gonna zip an "Hello" folder
  filename_ascii = b'Hello/'
  st_mode = 0o40777  # DIR file
  st_mtime = 1681291380.5431685  # 1681291380 is 2023-04-12 09:23:00 GMT+0 or 2023-04-12 11:23:00 GMT+2
  #####
  ddt = 0x568c5ae1  # = dosdatetime_fromtimestamp(st_mtime, True) = 2023-04-12 11:23:00 (naive)
  crc32 = 0
  #####
  CM_STORE = 0
  VM_UNIX = 0x31E
  # 0xA is the version needed used by 7zip when adding normal file entries
  #####
  loc = zipfile_struct_mklocrecord(0x14, 0, CM_STORE, ddt, crc32, 0, 0, filename_ascii)
  cen = zipfile_struct_mkcenrecord(VM_UNIX, 0x14, 0, CM_STORE, ddt, crc32, 0, 0, 0, 0, st_mode << 16, 0, filename_ascii)
  eocd = zipfile_struct_mkeocdrecord(0, 0, 1, 1, len(cen), len(loc))
  zipdata = loc + cen + eocd
  #open('test.helloworlddir.zip', 'wb').write(zipdata)
  assert_nodiff(list(hexdump.iter(zipdata)), [
    "00000000  50 4B 03 04 14 00 00 00  00 00 E1 5A 8C 56 00 00  |PK.........Z.V..|",
    "00000010  00 00 00 00 00 00 00 00  00 00 06 00 00 00 48 65  |..............He|",
    "00000020  6C 6C 6F 2F 50 4B 01 02  1E 03 14 00 00 00 00 00  |llo/PK..........|",
    "00000030  E1 5A 8C 56 00 00 00 00  00 00 00 00 00 00 00 00  |.Z.V............|",
    "00000040  06 00 00 00 00 00 00 00  00 00 00 00 FF 41 00 00  |.............A..|",
    "00000050  00 00 48 65 6C 6C 6F 2F  50 4B 05 06 00 00 00 00  |..Hello/PK......|",
    "00000060  01 00 01 00 34 00 00 00  24 00 00 00 00 00        |....4...$.....|"],
    'Hello.d.zip', 'expected')

def test_zipfile__unicodepath():
  # I'm gonna zip an "Élo oirlde.txt" file
  filename_cp437 = b'\x90lo oirlde.txt'  # IBM Code Page 437 encoding (cp437)
  filename_utf8 = b'\xc3\x89lo oirlde.txt'  # UTF-8 encoding
  data = b'Hello World\n'
  st_mode = 0o100666  # REG file
  st_mtime = 1681291380.5431685  # 1681291380 is 2023-04-12 09:23:00 GMT+0 or 2023-04-12 11:23:00 GMT+2
  #####
  ddt = 0x568c5ae1  # = dosdatetime_fromtimestamp(st_mtime, True) = 2023-04-12 11:23:00 (naive)
  crc32 = 2962613731  # = zlib.crc32(data)
  #####
  BF_UTF8_FILENAME_AND_COMMENT = 0x800
  CM_STORE = 0
  VM_FAT = 0x3F
  VM_UNIX = 0x31E
  EA_NORMAL = 0x80
  #####
  fe = zipfile_struct_mkunicodepathextrafield(zlib_crc32(filename_cp437), filename_utf8)
  nte = zipfile_struct_mkntfstimeextrafield(ntfstime_fromtimestamp(st_mtime, True), 0, 0)
  loc = zipfile_struct_mklocrecord(0xA, 0, CM_STORE, ddt, crc32, len(data), len(data), filename_cp437, fe)
  #loc = zipfile_struct_mklocrecord(0xA, BF_UTF8_FILENAME_AND_COMMENT, CM_STORE, ddt, crc32, len(data), len(data), filename_utf8)  # also works
  cen = zipfile_struct_mkcenrecord(VM_FAT, 0xA, 0, CM_STORE, ddt, crc32, len(data), len(data), 0, 0, EA_NORMAL, 0, filename_cp437, nte + fe)  # 7zip version of CEN
  #cen = zipfile_struct_mkcenrecord(VM_UNIX, 0xA, 0, CM_STORE, ddt, crc32, len(data), len(data), 0, 0, st_mode << 16, 0, filename_cp437, nte + fe)  # also works
  eocd = zipfile_struct_mkeocdrecord(0, 0, 1, 1, len(cen), len(loc) + len(data))
  zipdata = loc + data + cen + eocd
  #open('test.unicodepath.zip', 'wb').write(zipdata)
  assert_nodiff(list(hexdump.iter(zipdata)), [
    "00000000  50 4B 03 04 0A 00 00 00  00 00 E1 5A 8C 56 E3 E5  |PK.........Z.V..|",
    "00000010  95 B0 0C 00 00 00 0C 00  00 00 0E 00 18 00 90 6C  |...............l|",
    "00000020  6F 20 6F 69 72 6C 64 65  2E 74 78 74 75 70 14 00  |o oirlde.txtup..|",
    "00000030  01 17 86 0A 6F C3 89 6C  6F 20 6F 69 72 6C 64 65  |....o..lo oirlde|",
    "00000040  2E 74 78 74 48 65 6C 6C  6F 20 57 6F 72 6C 64 0A  |.txtHello World.|",
    "00000050  50 4B 01 02 3F 00 0A 00  00 00 00 00 E1 5A 8C 56  |PK..?........Z.V|",
    "00000060  E3 E5 95 B0 0C 00 00 00  0C 00 00 00 0E 00 3C 00  |..............<.|",
    "00000070  00 00 00 00 00 00 80 00  00 00 00 00 00 00 90 6C  |...............l|",
    "00000080  6F 20 6F 69 72 6C 64 65  2E 74 78 74 0A 00 20 00  |o oirlde.txt.. .|",
    "00000090  00 00 00 00 01 00 18 00  86 93 41 60 20 6D D9 01  |..........A` m..|",
    "000000A0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|",
    "000000B0  75 70 14 00 01 17 86 0A  6F C3 89 6C 6F 20 6F 69  |up......o..lo oi|",
    "000000C0  72 6C 64 65 2E 74 78 74  50 4B 05 06 00 00 00 00  |rlde.txtPK......|",
    "000000D0  01 00 01 00 78 00 00 00  50 00 00 00 00 00        |....x...P.....|"],
    'Élo oirlde.txt.zip', 'expected-7zip.zip')

def test_zipfile__stream_and_comment():
  # I'm gonna zip an "Hello.txt" file
  filename_ascii = b'Hello.txt'
  comment_ascii = b'Hey!'
  data = b'Hello World\n'
  st_mode = 0o100666  # REG file
  st_mtime = 1681291380.5431685  # 1681291380 is 2023-04-12 09:23:00 GMT+0 or 2023-04-12 11:23:00 GMT+2
  #####
  ddt = 0x568c5ae1  # = dosdatetime_fromtimestamp(st_mtime, True) = 2023-04-12 11:23:00 (naive)
  crc32 = 2962613731  # = zlib.crc32(data)
  #####
  BF_STREAM = 8
  CM_STORE = 0
  VM_UNIX = 0x31E
  # On streaming transfer, 7zip adds automatically zip64 extrafields in case the stream is really big.
  # As 7zip uses version_needed=0x2D if there is zip64 extrafield, and as there is no zip64 extrafield in LOC, I use version_needed=0xA.
  #####
  loc = zipfile_struct_mklocrecord(0xA, BF_STREAM, CM_STORE, ddt, 0, 0, 0, filename_ascii)
  dd = zipfile_struct_mkddrecord(crc32, len(data), len(data))
  cen = zipfile_struct_mkcenrecord(VM_UNIX, 0xA, BF_STREAM, CM_STORE, ddt, crc32, len(data), len(data), 0, 0, st_mode << 16, 0, filename_ascii, b'', comment_ascii)
  eocd = zipfile_struct_mkeocdrecord(0, 0, 1, 1, len(cen), len(loc) + len(data) + len(dd))
  zipdata = loc + data + dd + cen + eocd
  #open('test.stream_and_comment.zip', 'wb').write(zipdata)
  assert_nodiff(list(hexdump.iter(zipdata)), [
    "00000000  50 4B 03 04 0A 00 08 00  00 00 E1 5A 8C 56 00 00  |PK.........Z.V..|",
    "00000010  00 00 00 00 00 00 00 00  00 00 09 00 00 00 48 65  |..............He|",
    "00000020  6C 6C 6F 2E 74 78 74 48  65 6C 6C 6F 20 57 6F 72  |llo.txtHello Wor|",
    "00000030  6C 64 0A 50 4B 07 08 E3  E5 95 B0 0C 00 00 00 0C  |ld.PK...........|",
    "00000040  00 00 00 50 4B 01 02 1E  03 0A 00 08 00 00 00 E1  |...PK...........|",
    "00000050  5A 8C 56 E3 E5 95 B0 0C  00 00 00 0C 00 00 00 09  |Z.V.............|",
    "00000060  00 00 00 04 00 00 00 00  00 00 00 B6 81 00 00 00  |................|",
    "00000070  00 48 65 6C 6C 6F 2E 74  78 74 48 65 79 21 50 4B  |.Hello.txtHey!PK|",
    "00000080  05 06 00 00 00 00 01 00  01 00 3B 00 00 00 43 00  |..........;...C.|",
    "00000090  00 00 00 00                                       |....|"])

def test_zipfile__pipe_to_7zip():
  pass
  # echo Hello World | 7z a -tzip -si Hello.7z.stream.zip
  # 00000000   50 4B 03 04  2D 00 00 00  08 00 AD 91  C3 56 E3 E5  PK..-........V.. loc 504B0304 vn 2D00 bf 0000 cm 0800 ddt AD91C356 crc E3E595B0 csize FFFFFFFF usize FFFFFFFF filelen 0000 extralen 1400
  # 00000010   95 B0 FF FF  FF FF FF FF  FF FF 00 00  14 00 01 00  ................ zip64 extrafield 0100
  # 00000020   10 00 0C 00  00 00 00 00  00 00 11 00  00 00 00 00  ................   efsize 1000 usize 0C00000000000000 csize 1100000000000000
  # 00000030   00 00 01 0C  00 F3 FF 48  65 6C 6C 6F  20 57 6F 72  .......Hello Wor data 010C00F3FF 48656C6C6F20576F726C640A
  # 00000040   6C 64 0A 50  4B 01 02 3F  00 14 00 00  00 08 00 AD  ld.PK..?........ cen 504B0102 vm 3F00 vn 1400 bf 0000 cm 0800 ddt AD91C356
  # 00000050   91 C3 56 E3  E5 95 B0 11  00 00 00 0C  00 00 00 00  ..V.............   crc E3E595B0 csize 11000000 usize 0C000000 filelen 0000
  # 00000060   00 24 00 00  00 00 00 00  00 00 00 00  00 00 00 00  .$..............   extralen 2400 commentlen 0000 sdn 0000 ia 0000 ea 00000000 offset 00000000
  # 00000070   00 0A 00 20  00 00 00 00  00 01 00 18  00 0B 14 6A  ... ...........j ntfs extrafield 0A00 2000 reserved 00000000 tag 0100 asize 1800 0B146A533696D901
  # 00000080   53 36 96 D9  01 00 00 00  00 00 00 00  00 00 00 00  S6..............   0000000000000000 0000000000000000
  # 00000090   00 00 00 00  00 50 4B 05  06 00 00 00  00 01 00 01  .....PK......... eocd 504B0506
  # 000000A0   00 52 00 00  00 43 00 00  00 00 00                  .R...C.....


def test_zipfile__unixtime():
  # I'm gonna zip an "Hello.txt" file
  filename_ascii = b'Hello.txt'
  data = b'Hello World\n'
  st_mode = 0o100666  # REG file
  st_mtime = 1681291380.5431685  # 1681291380 is 2023-04-12 09:23:00 GMT+0 or 2023-04-12 11:23:00 GMT+2
  #####
  ddt = 0x568c5ae1  # = dosdatetime_fromtimestamp(st_mtime, True) = 2023-04-12 11:23:00 (naive)
  crc32 = 2962613731  # = zlib.crc32(data)
  #####
  CM_STORE = 0
  VM_FAT = 0x3F
  EA_NORMAL = 0x80
  #####
  ue = zipfile_struct_mkunixtimeextrafield(int(st_mtime))  # ceil() it before!!
  loc = zipfile_struct_mklocrecord(0xA, 0, CM_STORE, ddt, crc32, len(data), len(data), filename_ascii, ue)  # we don't have to put unixtime extrafield here, but 7zip does.
  cen = zipfile_struct_mkcenrecord(VM_FAT, 0xA, 0, CM_STORE, ddt, crc32, len(data), len(data), 0, 0, EA_NORMAL, 0, filename_ascii, ue)
  eocd = zipfile_struct_mkeocdrecord(0, 0, 1, 1, len(cen), len(loc) + len(data))
  zipdata = loc + data + cen + eocd
  #open('test.unixtime.zip', 'wb').write(zipdata)
  assert_nodiff(list(hexdump.iter(zipdata)), [
    '00000000  50 4B 03 04 0A 00 00 00  00 00 E1 5A 8C 56 E3 E5  |PK.........Z.V..|',
    '00000010  95 B0 0C 00 00 00 0C 00  00 00 09 00 09 00 48 65  |..............He|',
    '00000020  6C 6C 6F 2E 74 78 74 55  54 05 00 01 74 78 36 64  |llo.txtUT...tx6d|',
    '00000030  48 65 6C 6C 6F 20 57 6F  72 6C 64 0A 50 4B 01 02  |Hello World.PK..|',
    '00000040  3F 00 0A 00 00 00 00 00  E1 5A 8C 56 E3 E5 95 B0  |?........Z.V....|',
    '00000050  0C 00 00 00 0C 00 00 00  09 00 09 00 00 00 00 00  |................|',
    '00000060  00 00 80 00 00 00 00 00  00 00 48 65 6C 6C 6F 2E  |..........Hello.|',
    '00000070  74 78 74 55 54 05 00 01  74 78 36 64 50 4B 05 06  |txtUT...tx6dPK..|',
    '00000080  00 00 00 00 01 00 01 00  40 00 00 00 3C 00 00 00  |........@...<...|',
    '00000090  00 00                                             |..|'])


def test_zipfile__ntfstime():
  # I'm gonna zip an "Hello.txt" file
  filename_ascii = b'Hello.txt'
  data = b'Hello World\n'
  st_mode = 0o100666  # REG file
  st_mtime = 1681291380.5431685  # 1681291380 is 2023-04-12 09:23:00 GMT+0 or 2023-04-12 11:23:00 GMT+2
  #####
  ddt = 0x568c5ae1  # = dosdatetime_fromtimestamp(st_mtime, True) = 2023-04-12 11:23:00 (naive)
  crc32 = 2962613731  # = zlib.crc32(data)
  #####
  CM_STORE = 0
  VM_FAT = 0x3F
  EA_NORMAL = 0x80
  #####
  ne = zipfile_struct_mkntfstimeextrafield(ntfstime_fromtimestamp(st_mtime, True), 0, 0)  # 7zip keeps atime=0 and ctime=0 (meaning atime and ctime are unused)
  loc = zipfile_struct_mklocrecord(0xA, 0, CM_STORE, ddt, crc32, len(data), len(data), filename_ascii)  # this time, 7zip does not add ntfstime extrafield
  cen = zipfile_struct_mkcenrecord(VM_FAT, 0xA, 0, CM_STORE, ddt, crc32, len(data), len(data), 0, 0, st_mode << 16, 0, filename_ascii, ne)  # 7zip order of extrafields is ntfstime + unicodepath + unicodecomment
  eocd = zipfile_struct_mkeocdrecord(0, 0, 1, 1, len(cen), len(loc) + len(data))
  zipdata = loc + data + cen + eocd
  #open('test.ntfstime.zip', 'wb').write(zipdata)
  assert_nodiff(list(hexdump.iter(zipdata)), [
    '00000000  50 4B 03 04 0A 00 00 00  00 00 E1 5A 8C 56 E3 E5  |PK.........Z.V..|',
    '00000010  95 B0 0C 00 00 00 0C 00  00 00 09 00 00 00 48 65  |..............He|',
    '00000020  6C 6C 6F 2E 74 78 74 48  65 6C 6C 6F 20 57 6F 72  |llo.txtHello Wor|',
    '00000030  6C 64 0A 50 4B 01 02 3F  00 0A 00 00 00 00 00 E1  |ld.PK..?........|',
    '00000040  5A 8C 56 E3 E5 95 B0 0C  00 00 00 0C 00 00 00 09  |Z.V.............|',
    '00000050  00 24 00 00 00 00 00 00  00 00 00 B6 81 00 00 00  |.$..............|',
    '00000060  00 48 65 6C 6C 6F 2E 74  78 74 0A 00 20 00 00 00  |.Hello.txt.. ...|',
    '00000070  00 00 01 00 18 00 86 93  41 60 20 6D D9 01 00 00  |........A` m....|',
    '00000080  00 00 00 00 00 00 00 00  00 00 00 00 00 00 50 4B  |..............PK|',
    '00000090  05 06 00 00 00 00 01 00  01 00 5B 00 00 00 33 00  |..........[...3.|',
    '000000A0  00 00 00 00                                       |....|'])

def test_zipfile__dir_file_symlink():
  ddt = 0x56ae1070
  #####
  BF_STREAM = 8
  CM_STORE = 0
  VM_FAT = 0x14  # used by jszip
  VM_UNIX = 0x31E  # used by jszip
  EA_DIR = 0x10
  #####
  local_data = b''
  central_data = b''
  count = 0
  offset = 0
  local_data += zipfile_struct_mklocrecord(0xA, 0, CM_STORE, ddt, 0, 0, 0, b'dir/', b'')
  central_data += zipfile_struct_mkcenrecord(VM_FAT, 0xA, 0, CM_STORE, ddt, 0, 0, 0, 0, 0, EA_DIR, offset, b'dir/')
  count += 1
  offset = len(local_data)
  local_data += zipfile_struct_mklocrecord(0xA, BF_STREAM, CM_STORE, ddt, 0, 0, 0, b'dir/file.txt', b'') + b'Hello world\n'
  central_data += zipfile_struct_mkcenrecord(VM_FAT, 0xA, BF_STREAM, CM_STORE, ddt, zlib_crc32(b'Hello world\n'), 12, 12, 0, 0, 0, offset, b'dir/file.txt')  # file
  count += 1
  offset = len(local_data)
  local_data += zipfile_struct_mklocrecord(0xA, BF_STREAM, CM_STORE, ddt, 0, 0, 0, b'dir/symlink_to_file', b'') + b'./file.txt'
  central_data += zipfile_struct_mkcenrecord(VM_UNIX, 0xA, BF_STREAM, CM_STORE, ddt, zlib_crc32(b'./file.txt'), 10, 10, 0, 0, 0o120777 << 16, offset, b'dir/symlink_to_file')  # symlink
  count += 1
  eocd = zipfile_struct_mkeocdrecord(0, 0, count, count, len(central_data), len(local_data))
  zipdata = local_data + central_data + eocd
  #open('test.dir_file_symlink.zip', 'wb').write(zipdata)
  assert_nodiff(list(hexdump.iter(zipdata)), [
    '00000000  50 4B 03 04 0A 00 00 00  00 00 70 10 AE 56 00 00  |PK........p..V..|',
    '00000010  00 00 00 00 00 00 00 00  00 00 04 00 00 00 64 69  |..............di|',
    '00000020  72 2F 50 4B 03 04 0A 00  08 00 00 00 70 10 AE 56  |r/PK........p..V|',
    '00000030  00 00 00 00 00 00 00 00  00 00 00 00 0C 00 00 00  |................|',
    '00000040  64 69 72 2F 66 69 6C 65  2E 74 78 74 48 65 6C 6C  |dir/file.txtHell|',
    '00000050  6F 20 77 6F 72 6C 64 0A  50 4B 03 04 0A 00 08 00  |o world.PK......|',
    '00000060  00 00 70 10 AE 56 00 00  00 00 00 00 00 00 00 00  |..p..V..........|',
    '00000070  00 00 13 00 00 00 64 69  72 2F 73 79 6D 6C 69 6E  |......dir/symlin|',
    '00000080  6B 5F 74 6F 5F 66 69 6C  65 2E 2F 66 69 6C 65 2E  |k_to_file./file.|',
    '00000090  74 78 74 50 4B 01 02 14  00 0A 00 00 00 00 00 70  |txtPK..........p|',
    '000000A0  10 AE 56 00 00 00 00 00  00 00 00 00 00 00 00 04  |..V.............|',
    '000000B0  00 00 00 00 00 00 00 00  00 10 00 00 00 00 00 00  |................|',
    '000000C0  00 64 69 72 2F 50 4B 01  02 14 00 0A 00 08 00 00  |.dir/PK.........|',
    '000000D0  00 70 10 AE 56 D5 E0 39  B7 0C 00 00 00 0C 00 00  |.p..V..9........|',
    '000000E0  00 0C 00 00 00 00 00 00  00 00 00 00 00 00 00 22  |..............."|',
    '000000F0  00 00 00 64 69 72 2F 66  69 6C 65 2E 74 78 74 50  |...dir/file.txtP|',
    '00000100  4B 01 02 1E 03 0A 00 08  00 00 00 70 10 AE 56 2B  |K..........p..V+|',
    '00000110  DF 83 6A 0A 00 00 00 0A  00 00 00 13 00 00 00 00  |..j.............|',
    '00000120  00 00 00 00 00 00 00 FF  A1 58 00 00 00 64 69 72  |.........X...dir|',
    '00000130  2F 73 79 6D 6C 69 6E 6B  5F 74 6F 5F 66 69 6C 65  |/symlink_to_file|',
    '00000140  50 4B 05 06 00 00 00 00  03 00 03 00 AD 00 00 00  |PK..............|',
    '00000150  93 00 00 00 00 00                                 |......|'])

def test_zipfile__zip_stdin():
  # I'm gonna zip an unnamed file, archive "Hello.txt.zip" will be extracted as "Hello.txt" by 7zip.
  filename_ascii = b''
  data = b'Hello World\n'  # stdin data
  st_mtime = 1681291380.5431685  # = time.time()  # 1681291380 is 2023-04-12 09:23:00 GMT+0 or 2023-04-12 11:23:00 GMT+2
  #####
  ddt = 0x568c5ae1  # = dosdatetime_fromtimestamp(st_mtime, True) = 2023-04-12 11:23:00 (naive)
  crc32 = 2962613731  # = zlib.crc32(data)
  #####
  BF_STREAM = 8
  CM_STORE = 0
  VM_FAT = 0x3F
  EA_NORMAL = 0x80
  #####
  ne = zipfile_struct_mkntfstimeextrafield(ntfstime_fromtimestamp(st_mtime, True), 0, 0)  # 7zip keeps atime=0 and ctime=0 (meaning atime and ctime are unused)
  loc = zipfile_struct_mklocrecord(0xA, BF_STREAM, CM_STORE, ddt, 0, 0, 0, filename_ascii)
  dd = zipfile_struct_mkddrecord(crc32, len(data), len(data))
  cen = zipfile_struct_mkcenrecord(VM_FAT, 0xA, BF_STREAM, CM_STORE, ddt, crc32, len(data), len(data), 0, 0, EA_NORMAL, 0, filename_ascii, ne)  # 7zip order of extrafields is ntfstime + unicodepath + unicodecomment
  eocd = zipfile_struct_mkeocdrecord(0, 0, 1, 1, len(cen), len(loc) + len(data) + len(dd))
  zipdata = loc + data + dd + cen + eocd
  #open('test.stdin.zip', 'wb').write(zipdata)
  assert_nodiff(list(hexdump.iter(zipdata)), [
    '00000000  50 4B 03 04 0A 00 08 00  00 00 E1 5A 8C 56 00 00  |PK.........Z.V..|',
    '00000010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 48 65  |..............He|',
    '00000020  6C 6C 6F 20 57 6F 72 6C  64 0A 50 4B 07 08 E3 E5  |llo World.PK....|',
    '00000030  95 B0 0C 00 00 00 0C 00  00 00 50 4B 01 02 3F 00  |..........PK..?.|',
    '00000040  0A 00 08 00 00 00 E1 5A  8C 56 E3 E5 95 B0 0C 00  |.......Z.V......|',
    '00000050  00 00 0C 00 00 00 00 00  24 00 00 00 00 00 00 00  |........$.......|',
    '00000060  80 00 00 00 00 00 00 00  0A 00 20 00 00 00 00 00  |.......... .....|',
    '00000070  01 00 18 00 86 93 41 60  20 6D D9 01 00 00 00 00  |......A` m......|',
    '00000080  00 00 00 00 00 00 00 00  00 00 00 00 50 4B 05 06  |............PK..|',
    '00000090  00 00 00 00 01 00 01 00  52 00 00 00 3A 00 00 00  |........R...:...|',
    '000000A0  00 00                                             |..|'])

def test_zipfile__zip_stdin_no_mtime():
  # I'm gonna zip an unnamed file with no mtime, 7zip uncompressed file will have the same mtime as the archive.
  filename_ascii = b''
  data = b'Hello World\n'  # stdin data
  #####
  ddt = 0  # means no mtime
  crc32 = 2962613731  # = zlib.crc32(data)
  #####
  BF_STREAM = 8
  CM_STORE = 0
  VM_FAT = 0x3F
  EA_NORMAL = 0x80
  #####
  loc = zipfile_struct_mklocrecord(0xA, BF_STREAM, CM_STORE, ddt, 0, 0, 0, filename_ascii)
  dd = zipfile_struct_mkddrecord(crc32, len(data), len(data))
  cen = zipfile_struct_mkcenrecord(VM_FAT, 0xA, BF_STREAM, CM_STORE, ddt, crc32, len(data), len(data), 0, 0, EA_NORMAL, 0, filename_ascii)
  eocd = zipfile_struct_mkeocdrecord(0, 0, 1, 1, len(cen), len(loc) + len(data) + len(dd))
  zipdata = loc + data + dd + cen + eocd
  #open('test.stdin-nomtime.zip', 'wb').write(zipdata)
  assert_nodiff(list(hexdump.iter(zipdata)), [
    '00000000  50 4B 03 04 0A 00 08 00  00 00 00 00 00 00 00 00  |PK..............|',
    '00000010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 48 65  |..............He|',
    '00000020  6C 6C 6F 20 57 6F 72 6C  64 0A 50 4B 07 08 E3 E5  |llo World.PK....|',
    '00000030  95 B0 0C 00 00 00 0C 00  00 00 50 4B 01 02 3F 00  |..........PK..?.|',
    '00000040  0A 00 08 00 00 00 00 00  00 00 E3 E5 95 B0 0C 00  |................|',
    '00000050  00 00 0C 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|',
    '00000060  80 00 00 00 00 00 00 00  50 4B 05 06 00 00 00 00  |........PK......|',
    '00000070  01 00 01 00 2E 00 00 00  3A 00 00 00 00 00        |........:.....|'])

def test_zipfile__zip64_FFFFFFFF():  # XXX
  # DO TEST WITH THESE RESULTS
  size = 0xFFFFFFFF
  ddt = 0x56BE860B
  crc32 = 0
  z64e = zipfile_struct_mkzip64extrafield(size, size)
  # 7zip uses version needed 0x2D because there is a zip64 extrafield on LOC
  loc = zipfile_struct_mklocrecord(0x2D, 0, 0, ddt, crc32, 0xFFFFFFFF, 0xFFFFFFFF, b'huge_FFFFFFFF.bin', z64e)
  # 7zip uses version needed 0x2D because there is a zip64 extrafield on CEN
  cen = zipfile_struct_mkcenrecord(0x3F, 0x2D, 0, 0, ddt, crc32, 0xFFFFFFFF, 0xFFFFFFFF, 0, 0, 0x20, 0, b'huge_FFFFFFFF.bin', z64e)  # 0x20 is (useless) DOS archive bit but used by 7zip https://en.wikipedia.org/wiki/Archive_bit
  eocd64 = zipfile_struct_mkeocd64record(0x2D, 0x2D, 0, 0, 1, 1, len(cen), len(loc) + size) + zipfile_struct_mkeocd64locatorrecord(0, len(cen) + len(loc) + size, 1)
  eocd = zipfile_struct_mkeocdrecord(0, 0, 1, 1, len(cen), 0xFFFFFFFF)
  zipdata = loc + b'\x00' * 31 + cen + eocd64 + eocd
  assert_nodiff(list(hexdump.iter(zipdata)), [
  "00000000  50 4B 03 04 2D 00 00 00  00 00 0B 86 BE 56 00 00  |PK..-........V..|",
  "00000010  00 00 FF FF FF FF FF FF  FF FF 11 00 14 00 68 75  |..............hu|",
  "00000020  67 65 5F 46 46 46 46 46  46 46 46 2E 62 69 6E 01  |ge_FFFFFFFF.bin.|",
  "00000030  00 10 00 FF FF FF FF 00  00 00 00 FF FF FF FF 00  |................|",
  "00000040  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|",
  "00000050  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|",
  "00000060  00 00 50 4B 01 02 3F 00  2D 00 00 00 00 00 0B 86  |..PK..?.-.......|",
  "00000070  BE 56 00 00 00 00 FF FF  FF FF FF FF FF FF 11 00  |.V..............|",
  "00000080  14 00 00 00 00 00 00 00  20 00 00 00 00 00 00 00  |........ .......|",
  "00000090  68 75 67 65 5F 46 46 46  46 46 46 46 46 2E 62 69  |huge_FFFFFFFF.bi|",
  "000000A0  6E 01 00 10 00 FF FF FF  FF 00 00 00 00 FF FF FF  |n...............|",
  "000000B0  FF 00 00 00 00 50 4B 06  06 2C 00 00 00 00 00 00  |.....PK..,......|",
  "000000C0  00 2D 00 2D 00 00 00 00  00 00 00 00 00 01 00 00  |.-.-............|",
  "000000D0  00 00 00 00 00 01 00 00  00 00 00 00 00 53 00 00  |.............S..|",
  "000000E0  00 00 00 00 00 42 00 00  00 01 00 00 00 50 4B 06  |.....B.......PK.|",
  "000000F0  07 00 00 00 00 95 00 00  00 01 00 00 00 01 00 00  |................|",
  "00000100  00 50 4B 05 06 00 00 00  00 01 00 01 00 53 00 00  |.PK..........S..|",
  "00000110  00 FF FF FF FF 00 00                              |.......|"])
  # size 0xFFFFFFFF STORE 2s
  # 00000000   50 4B 03 04  2D 00 00 00  00 00 0B 86  BE 56 00 00  PK..-........V..
  # 00000010   00 00 FF FF  FF FF FF FF  FF FF 11 00  14 00 68 75  ..............hu
  # 00000020   67 65 5F 46  46 46 46 46  46 46 46 2E  62 69 6E 01  ge_FFFFFFFF.bin.
  # 00000030   00 10 00 FF  FF FF FF 00  00 00 00 FF  FF FF FF 00  ................
  # 00000040   00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  ................
  # [..]
  # FFFFFFF0   00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  ................
  # 00000000   00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  ................
  # 00000010   00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  ................
  # 00000020   00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  ................
  # 00000030   00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  ................
  # 00000040   00 00 50 4B  01 02 3F 00  2D 00 00 00  00 00 0B 86  ..PK..?.-.......
  # 00000050   BE 56 00 00  00 00 FF FF  FF FF FF FF  FF FF 11 00  .V..............
  # 00000060   14 00 00 00  00 00 00 00  20 00 00 00  00 00 00 00  ........ .......
  # 00000070   68 75 67 65  5F 46 46 46  46 46 46 46  46 2E 62 69  huge_FFFFFFFF.bi
  # 00000080   6E 01 00 10  00 FF FF FF  FF 00 00 00  00 FF FF FF  n...............
  # 00000090   FF 00 00 00  00 50 4B 06  06 2C 00 00  00 00 00 00  .....PK..,......
  # 000000A0   00 2D 00 2D  00 00 00 00  00 00 00 00  00 01 00 00  .-.-............
  # 000000B0   00 00 00 00  00 01 00 00  00 00 00 00  00 53 00 00  .............S..
  # 000000C0   00 00 00 00  00 42 00 00  00 01 00 00  00 50 4B 06  .....B.......PK.
  # 000000D0   07 00 00 00  00 95 00 00  00 01 00 00  00 01 00 00  ................
  # 000000E0   00 50 4B 05  06 00 00 00  00 01 00 01  00 53 00 00  .PK..........S..
  # 000000F0   00 FF FF FF  FF 00 00                               .......

def test_zipfile__zip64_100000000():  # XXX
  size = 0x100000000
  ddt = 0x56BE8635
  crc32 = 0xD202EF8D
  z64e = zipfile_struct_mkzip64extrafield(size, size)
  loc = zipfile_struct_mklocrecord(0x2D, 0, 0, ddt, crc32, 0xFFFFFFFF, 0xFFFFFFFF, b'huge_100000000.bin', z64e)
  cen = zipfile_struct_mkcenrecord(0x3F, 0x2D, 0, 0, ddt, crc32, 0xFFFFFFFF, 0xFFFFFFFF, 0, 0, 0x20, 0, b'huge_100000000.bin', z64e)  # 0x20 is (useless) DOS archive bit https://en.wikipedia.org/wiki/Archive_bit
  eocd64 = zipfile_struct_mkeocd64record(0x2D, 0x2D, 0, 0, 1, 1, len(cen), len(loc) + size) + zipfile_struct_mkeocd64locatorrecord(0, len(cen) + len(loc) + size, 1)
  eocd = zipfile_struct_mkeocdrecord(0, 0, 1, 1, len(cen), 0xFFFFFFFF)
  zipdata = loc + b'\x00' * 32 + cen + eocd64 + eocd
  assert_nodiff(list(hexdump.iter(zipdata)), [
  "00000000  50 4B 03 04 2D 00 00 00  00 00 35 86 BE 56 8D EF  |PK..-.....5..V..|",
  "00000010  02 D2 FF FF FF FF FF FF  FF FF 12 00 14 00 68 75  |..............hu|",
  "00000020  67 65 5F 31 30 30 30 30  30 30 30 30 2E 62 69 6E  |ge_100000000.bin|",
  "00000030  01 00 10 00 00 00 00 00  01 00 00 00 00 00 00 00  |................|",
  "00000040  01 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|",
  "00000050  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|",
  "00000060  00 00 00 00 50 4B 01 02  3F 00 2D 00 00 00 00 00  |....PK..?.-.....|",
  "00000070  35 86 BE 56 8D EF 02 D2  FF FF FF FF FF FF FF FF  |5..V............|",
  "00000080  12 00 14 00 00 00 00 00  00 00 20 00 00 00 00 00  |.......... .....|",
  "00000090  00 00 68 75 67 65 5F 31  30 30 30 30 30 30 30 30  |..huge_100000000|",
  "000000A0  2E 62 69 6E 01 00 10 00  00 00 00 00 01 00 00 00  |.bin............|",
  "000000B0  00 00 00 00 01 00 00 00  50 4B 06 06 2C 00 00 00  |........PK..,...|",
  "000000C0  00 00 00 00 2D 00 2D 00  00 00 00 00 00 00 00 00  |....-.-.........|",
  "000000D0  01 00 00 00 00 00 00 00  01 00 00 00 00 00 00 00  |................|",
  "000000E0  54 00 00 00 00 00 00 00  44 00 00 00 01 00 00 00  |T.......D.......|",
  "000000F0  50 4B 06 07 00 00 00 00  98 00 00 00 01 00 00 00  |PK..............|",
  "00000100  01 00 00 00 50 4B 05 06  00 00 00 00 01 00 01 00  |....PK..........|",
  "00000110  54 00 00 00 FF FF FF FF  00 00                    |T.........|"])
  # size 0x100000000 STORE 2s
  # 00000000   50 4B 03 04  2D 00 00 00  00 00 35 86  BE 56 8D EF  PK..-.....5..V..
  # 00000010   02 D2 FF FF  FF FF FF FF  FF FF 12 00  14 00 68 75  ..............hu
  # 00000020   67 65 5F 31  30 30 30 30  30 30 30 30  2E 62 69 6E  ge_100000000.bin
  # 00000030   01 00 10 00  00 00 00 00  01 00 00 00  00 00 00 00  ................
  # 00000040   01 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  ................
  # 00000050   00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  ................
  # [..]
  # FFFFFFF0   00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  ................
  # 00000000   00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  ................
  # 00000010   00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  ................
  # 00000020   00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  ................
  # 00000030   00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  ................
  # 00000040   00 00 00 00  50 4B 01 02  3F 00 2D 00  00 00 00 00  ....PK..?.-.....
  # 00000050   35 86 BE 56  8D EF 02 D2  FF FF FF FF  FF FF FF FF  5..V............
  # 00000060   12 00 14 00  00 00 00 00  00 00 20 00  00 00 00 00  .......... .....
  # 00000070   00 00 68 75  67 65 5F 31  30 30 30 30  30 30 30 30  ..huge_100000000
  # 00000080   2E 62 69 6E  01 00 10 00  00 00 00 00  01 00 00 00  .bin............
  # 00000090   00 00 00 00  01 00 00 00  50 4B 06 06  2C 00 00 00  ........PK..,...
  # 000000A0   00 00 00 00  2D 00 2D 00  00 00 00 00  00 00 00 00  ....-.-.........
  # 000000B0   01 00 00 00  00 00 00 00  01 00 00 00  00 00 00 00  ................
  # 000000C0   54 00 00 00  00 00 00 00  44 00 00 00  01 00 00 00  T.......D.......
  # 000000D0   50 4B 06 07  00 00 00 00  98 00 00 00  01 00 00 00  PK..............
  # 000000E0   01 00 00 00  50 4B 05 06  00 00 00 00  01 00 01 00  ....PK..........
  # 000000F0   54 00 00 00  FF FF FF FF  00 00                     T.........

def test_zipfile__data_descriptor_injection():
  #     [local file header with stream flag]
  #     [file data]  that contains:
  #       [injected valid data descriptor] crc32(empty) 0 0
  #       [injected local file without stream] crc32(next data descriptor that contains this crc32) 16 16
  #     [data descriptor]  seen as part of injected file data
  #     [central dir record]  here crc32 must match the correct file data!!!!
  #     [eocd]
  REG_MODE = 0o100644
  FILE_DATA = (
    zipfile_struct_mkddrecord(0, 0, 0) +
    zipfile_struct_mklocrecord(0xA, 0, 0, 0, zlib_crc32(zipfile_struct_mkddrecord(zlib_crc32(b'impossible generate valid crc32'), 16, 16)), 16, 16, b'2'))
  #EOCD_COMMENT = (
  #  zipfile_struct_mkeocdrecord(0, 0, 2, 2, XXX, 31 + len(FILE_DATA)))     # also try with 1 instead of 2

  g = zipfile_archive_pipegen(); next(g)
  data = g.send(('entry', {'path': '1', 'st_mode': REG_MODE}))
  data += g.send(('data', FILE_DATA))
  data += g.send(('close',))
  # XXX now try to add a comment to the eocd record and put fake cen+eocd record
  #   and let's see how 7z handles this ;)
  #   hm, I can't build a valid fake eocd record as I need to put central size + local size == total size - eocd record size (which is possible,
  #     but then I can't parse central records)

  print(data)
  #open(os.path.join(os.path.expanduser('~'), 'Desktop', 'tmp', 'tmp', test.zip'), 'wb').write(data)

if 0:
  try:
    exec(open('E:/tc/py3/pythoncustom.py', 'rb').read(), globals(), globals())
    test_zipfile__data_descriptor_injection()
    input('press enter to continue...')
  except Exception as err:
    print(err)
    input('press enter to continue...')
