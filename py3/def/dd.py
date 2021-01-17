# dd.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def dd():
  def dd_iter(*args, bs=None, cbs=None, conv=None, count=None, ibs=None, iflag=None, obs=None, oflag=None, seek=None, skip=None, os_module=None, if_os_module=None, of_os_module=None, **kw):
    """\
Copy a file, converting and formatting according to the operands.

  bs=BYTES        read and write up to BYTES bytes at a time (default: 512);
                  overrides ibs and obs
  cbs=BYTES       convert BYTES bytes at a time
  conv=CONVS      convert the file as summed CONV flags
  count=N         copy only N input blocks
  ibs=BYTES       read up to BYTES bytes at a time (default: 512)
  if=FILE         read from FILE
  iflag=FLAGS     read as summed FLAG flags
  obs=BYTES       write BYTES bytes at a time (default: 512)
  of=FILE         write to FILE
  oflag=FLAGS     write as summed FLAG flags
  seek=N          skip N obs-sized blocks at start of output
  skip=N          skip N ibs-sized blocks at start of input
  os_module=OBJ   module to use instead of the `os` module;
                  sets {if,of}_os_module defaults
  if_os_module=OBJ  alternative to os_module for FILE to read
  of_os_module=OBJ  alternative to os_module for FILE to write

Each CONV flag may be:

  CONV_ASCII      from EBCDIC to ASCII
  CONV_EBCDIC     from ASCII to EBCDIC
  CONV_IBM        from ASCII to alternate EBCDIC
  CONV_BLOCK      pad newline-terminated records with spaces to cbs-size
  CONV_UNBLOCK    replace trailing spaces in cbs-size records with newline
  CONV_LCASE      change upper case to lower case
  CONV_UCASE      change lower case to upper case
  CONV_SPARSE     try to seek rather than write the output for NUL input blocks
  CONV_SWAB       swap every pair of input bytes
  CONV_SYNC       pad every input block with NULs to ibs-size; when used
                  with block or unblock, pad with spaces rather than NULs
  CONV_EXCL       fail if the output file already exists
  CONV_NOCREAT    do not create the output file
  CONV_NOTRUNC    do not truncate the output file
  CONV_NOERROR    continue after read errors XXX
  CONV_FDATASYNC  physically write output file data before finishing
  CONV_FSYNC      likewise, but also write metadata

Each FLAG flag may be:

  FLAG_APPEND     append mode (makes sense only for output; conv=CONV_NOTRUNC suggested)
  FLAG_DIRECT     use direct I/O for data
  FLAG_DIRECTORY  fail unless a directory
  FLAG_DSYNC      use synchronized I/O for data
  FLAG_SYNC       likewise, but also for metadata
  FLAG_FULLBLOCK  accumulate full blocks of input (iflag only) XXX
  FLAG_NONBLOCK   use non-blocking I/O
  FLAG_NOATIME    do not update access time
  FLAG_NOCACHE    Request to drop cache.  See also oflag=sync XXX
  FLAG_NOCTTY     do not assign controlling terminal from file
  FLAG_NOFOLLOW   do not follow symlinks
  FLAG_COUNT_BYTES  treat 'count=N' as a byte count (iflag only)
  FLAG_SKIP_BYTES  treat 'skip=N' as a byte count (iflag only)
  FLAG_SEEK_BYTES  treat 'seek=N' as a byte count (oflag only)
  FLaG_FORCE_SEEK  check lseek position after each read/write, move cursor if necessary
"""
    if args and "if" in kw: raise TypeError("dd() got multiple values for argument 'if'")
    if args[1:] and "of" in kw: raise TypeError("dd() got multiple values for argument 'of'")
    ifile, args = (args[0], args[1:]) if args else (kw.pop("if", None), ())
    ofile, args = (args[0], args[1:]) if args else (kw.pop("of", None), ())
    if len(args): raise TypeError("dd() takes from 0 to 2 positional arguments but " + str(len(args) + 2) + " were given")
    for k in kw: raise TypeError(f"dd() got an unexpected keyword argument {k!r}")
    if ifile is None:
      if ofile is None: raise TypeError("dd() missing 2 required positional arguments: 'if' and 'of'")
      raise TypeError("dd() missing 1 required positional argument: 'if'")
    if ofile is None: raise TypeError("dd() missing 1 required positional argument: 'of'")

    if os_module is None: os_module = os
    if if_os_module is None: if_os_module = os_module
    if of_os_module is None: of_os_module = os_module
    if bs is None: bs = 512
    elif bs <= 0: raise ValueError(f"invalid number '{bs}'")
    if ibs is None: ibs = bs
    elif ibs <= 0: raise ValueError(f"invalid number '{ibs}'")
    if obs is None: obs = bs
    elif obs <= 0: raise ValueError(f"invalid number '{obs}'")
    if cbs is not None and cbs <= 0: raise ValueError(f"invalid number '{cbs}'")
    if conv is None: conv = 0
    if iflag is None: iflag = 0
    if oflag is None: oflag = 0
    if count is None: count = -1
    elif count < 0: raise ValueError(f"invalid number '{count}'")
    if skip is None: skip = 0
    elif skip < 0: raise ValueError(f"invalid number '{skip}'")
    if seek is None: seek = 0
    elif seek < 0: raise ValueError(f"invalid number '{seek}'")
    open_iflag = open_oflag = 0

    def hasflag(v, flag): return v & flag == flag

    oascii = hasflag(conv, dd.CONV_ASCII)
    oebcdic = hasflag(conv, dd.CONV_EBCDIC)
    oibm = hasflag(conv, dd.CONV_IBM)
    if len([_ for _ in (oascii, oebcdic, oibm) if _]) > 1: raise ValueError("cannot combine any two of {ascii,ebcdic,ibm}")
    oblock = cbs and hasflag(conv, dd.CONV_BLOCK)
    ounblock = cbs and hasflag(conv, dd.CONV_UNBLOCK)
    if oblock and ounblock: raise ValueError("cannot combine block and unblock")
    olcase = hasflag(conv, dd.CONV_LCASE)
    oucase = hasflag(conv, dd.CONV_UCASE)
    if olcase and oucase: raise ValueError("cannot combine ucase and lcase")
    osparse = hasflag(conv, dd.CONV_SPARSE)
    oswab = hasflag(conv, dd.CONV_SWAB)
    opadibs = hasflag(conv, dd.CONV_SYNC)
    if oblock: ibspad = b" "
    elif ounblock: ibspad = b"\n"
    else: ibspad = b"\0"
    if hasflag(conv, dd.CONV_NOERROR): raise NotImplementedError()
    ofdatasync = hasflag(conv, dd.CONV_FDATASYNC)
    ofsync = hasflag(conv, dd.CONV_FSYNC)

    if hasflag(iflag, dd.FLAG_APPEND): open_iflag |= if_os_module.O_APPEND
    if hasflag(iflag, dd.FLAG_DIRECT): open_iflag |= if_os_module.O_DIRECT
    if hasflag(iflag, dd.FLAG_DIRECTORY): open_iflag |= if_os_module.O_DIRECTORY
    if hasflag(iflag, dd.FLAG_DSYNC): open_iflag |= if_os_module.O_DSYNC
    if hasflag(iflag, dd.FLAG_SYNC): open_iflag |= if_os_module.O_SYNC
    if hasflag(iflag, dd.FLAG_FULLBLOCK): raise NotImplementedError()
    if hasflag(iflag, dd.FLAG_NONBLOCK): open_iflag |= if_os_module.O_NONBLOCK
    if hasflag(iflag, dd.FLAG_NOATIME): open_iflag |= if_os_module.O_NOATIME
    if hasflag(iflag, dd.FLAG_NOCACHE): raise NotImplementedError()
    if hasflag(iflag, dd.FLAG_NOCTTY): open_iflag |= if_os_module.O_NOCTTY
    if hasflag(iflag, dd.FLAG_NOFOLLOW): open_iflag |= if_os_module.O_NOFOLLOW
    ifseek = hasflag(iflag, dd.FLAG_FORCE_SEEK)
    count_bytes = count if hasflag(iflag, dd.FLAG_COUNT_BYTES) else count * ibs
    skip_bytes = skip if hasflag(iflag, dd.FLAG_SKIP_BYTES) else skip * ibs

    if hasflag(conv, dd.CONV_EXCL): open_oflag |= of_os_module.O_EXCL
    if not hasflag(conv, dd.CONV_NOCREAT): open_oflag |= of_os_module.O_CREAT
    if not hasflag(conv, dd.CONV_NOTRUNC): open_oflag |= of_os_module.O_TRUNC
    if hasflag(oflag, dd.FLAG_APPEND): open_oflag |= of_os_module.O_APPEND
    if hasflag(oflag, dd.FLAG_DIRECT): open_oflag |= of_os_module.O_DIRECT
    if hasflag(oflag, dd.FLAG_DIRECTORY): open_oflag |= of_os_module.O_DIRECTORY
    if hasflag(oflag, dd.FLAG_DSYNC): open_oflag |= of_os_module.O_DSYNC
    if hasflag(oflag, dd.FLAG_SYNC): open_oflag |= of_os_module.O_SYNC
    if hasflag(oflag, dd.FLAG_NONBLOCK): open_oflag |= of_os_module.O_NONBLOCK
    if hasflag(oflag, dd.FLAG_NOATIME): open_oflag |= of_os_module.O_NOATIME
    if hasflag(oflag, dd.FLAG_NOCACHE): raise NotImplementedError()
    if hasflag(oflag, dd.FLAG_NOCTTY): open_oflag |= of_os_module.O_NOCTTY
    if hasflag(oflag, dd.FLAG_NOFOLLOW): open_oflag |= of_os_module.O_NOFOLLOW
    ofseek = hasflag(oflag, dd.FLAG_FORCE_SEEK)
    seek_bytes = seek if hasflag(oflag, dd.FLAG_SEEK_BYTES) else seek * obs

    ifd, ofd = None, None

    def swab(bb):
      lb = len(bb)
      return bytes(b for i in range(0, lb - 1, 2) for b in (bb[i+1], bb[i])) + (bb[-1:] if lb % 2 else b"")
    def block(bb, pos):
      r = []
      while bb:
        nli = bb.find(b"\n")
        if pos < cbs:
          l = cbs - pos
          if nli < 0:
            chunk, bb = bb[:l], bb[l:]
            pos += len(chunk)
            r.append(chunk)
          elif nli < l:
            chunk, bb, pos = bb[:nli] + b" " * (l - nli), bb[nli + 1:], 0
            r.append(chunk)
          else:
            chunk, bb, pos = bb[:l], bb[nli + 1:], 0
            r.append(chunk)
        else:
          if nli < 0: bb = b""
          else: bb, pos = bb[nli + 1:], 0
      return b"".join(r), pos
    def unblock(bb, pr, pos, close=False):
      r, lb = [], len(bb)
      while True:
        l = cbs - pos
        if lb < l:
          if close:
            if pos or lb: r.append((pr + bb).rstrip(b" ") + b"\n")
            pos, pr = 0, b""
            break
          bb = (pr + bb).rstrip(b" ")
          if bb: r.append(bb)
          pr = b" " * (lb + len(pr) - len(bb))
          pos += lb
          break
        bb_ = (pr + bb[:l]).rstrip(b" ")
        r.append(bb_ + b"\n")
        bb, pos, lb, pr, bb_ = bb[l:], 0, lb - l, b"", b""
      return b"".join(r), pr, pos

    def read_seek(os_module, fd, size, lseek, fseek):
      # lseek is always defined by callers  -  if lseek is None: lseek = os_module.lseek(fd, 0, os_module.SEEK_CUR)
      chunk = os_module.read(fd, size)
      if fseek:
        newseek = os_module.lseek(fd, 0, os_module.SEEK_CUR)
        if lseek == newseek: lseek = os_module.lseek(fd, len(chunk), os_module.SEEK_CUR)
        else: lseek = newseek
      return chunk, lseek
    def write_seek(os_module, fd, data, lseek, fseek):
      # lseek is always defined by callers  -  if lseek is None: lseek = os_module.lseek(fd, 0, os_module.SEEK_CUR)
      written = os_module.write(fd, data)
      if written <= 0: raise OSError(0, "write error")
      if fseek:
        newseek = os_module.lseek(fd, 0, os_module.SEEK_CUR)
        if lseek == newseek: lseek = os_module.lseek(fd, written, os_module.SEEK_CUR)
        else: lseek = newseek
      return written, lseek
    def exact_read_seek(os_module, fd, size, lseek, fseek):
      chunk, lseek = read_seek(os_module, fd, size, lseek, fseek)
      if not chunk: return chunk, lseek
      read = chunk
      l = len(chunk)
      while l < size:
        chunk, lseek = read_seek(os_module, fd, size - l, lseek, fseek)
        if not chunk: return read, lseek
        read += chunk
        l += len(chunk)
      return read, lseek

    ifd = ofd = None
    try:
      if isinstance(ifile, int): ifd = ifile
      else: ifd = if_os_module.open(ifile, if_os_module.O_RDONLY | getattr(if_os_module, "O_BINARY", 0) | open_iflag)
      try:
        if isinstance(ofile, int): ofd = ofile
        else: ofd = of_os_module.open(ofile, of_os_module.O_WRONLY | getattr(of_os_module, "O_BINARY", 0) | open_oflag)

        data, ldata = bytearray(), 0
        read_loop = True
        pr = b""
        c = 0

        iseek = if_os_module.lseek(ifd, skip_bytes, if_os_module.SEEK_CUR) if ifseek or skip_bytes else None
        oseek = of_os_module.lseek(ofd, seek_bytes, of_os_module.SEEK_CUR) if ofseek or seek_bytes else None
        while read_loop:
          chunk, iseek = exact_read_seek(if_os_module, ifd, ibs, iseek, ifseek)  # reading physical drives on windows requires to read precisely one (or more) blocks (n*512), so we cannot read `ibs - count_bytes`, also, `count_bytes` should be a multiple of `ibs`
          yield chunk  # pass actual read data, before convertions, before count_bytes truncate
          if count_bytes >= 0:
            count_bytes -= len(chunk)
            if count_bytes < 0: chunk = chunk[:count_bytes]
            elif count_bytes == 0: read_loop = False
          if len(chunk) < ibs: read_loop = False
          # apply convertions
          if opadibs and not ounblock and chunk and len(chunk) < ibs: chunk += ibspad * (ibs - len(chunk))
          if olcase: chunk = chunk.lower()
          elif oucase: chunk = chunk.upper()
          if oswab: chunk = swab(chunk)
          if oascii: chunk = bytes(dd.ASCII_CONV_SCHEME[_] for _ in chunk)
          elif oebcdic: chunk = bytes(dd.EBCDIC_CONV_SCHEME[_] for _ in chunk)
          elif oibm: chunk = bytes(dd.IBM_CONV_SCHEME[_] for _ in chunk)
          if oblock: chunk, c = block(chunk, c)
          if ounblock:
            lb = len(chunk)
            chunk, pr, c = unblock(chunk, pr, c, close=not read_loop)
            if opadibs and lb < ibs: chunk += ibspad * (((ibs - lb) // cbs) % ibs)

          data[ldata:] = chunk
          ldata += len(chunk)
          w = 0
          while ldata - w >= obs:
            if osparse and all(c == 0 for c in data[w:w + obs]): written, oseek = obs, of_os_module.lseek(ofd, obs, of_os_module.SEEK_CUR)
            else: written, oseek = write_seek(of_os_module, ofd, data[w:w + obs], oseek, ofseek)
            yield written
            w += written
          data, ldata = data[w:ldata], ldata - w
        w = 0
        while ldata - w > 0:
          written, oseek = write_seek(of_os_module, ofd, data[w:ldata], oseek, ofseek)  # it may fail to write on windows device due to lack of padding, consider using conv=sync.
          yield written
          w += written
        if osparse: of_os_module.ftruncate(ofd, oseek)

        if ofdatasync: of_os_module.fdatasync(ofd)
        if ofsync: of_os_module.fsync(ofd)
      finally:
        if ofd is not None and ofd != ofile: of_os_module.close(ofd)
    finally:
      if ifd is not None and ifd != ifile: if_os_module.close(ifd)
  def dd(*a, **k):
    it = None
    try:
      it = dd_iter(*a, **k)
      for _ in it: pass
    finally:
      if it is not None: it.close()
  dd.iter = dd_iter
  dd.CONV_ASCII       =    0x1
  dd.CONV_EBCDIC      =    0x2
  dd.CONV_IBM         =    0x4
  dd.CONV_BLOCK       =    0x8
  dd.CONV_UNBLOCK     =   0x10
  dd.CONV_LCASE       =   0x20
  dd.CONV_UCASE       =   0x40
  dd.CONV_SPARSE      =   0x80
  dd.CONV_SWAB        =  0x100
  dd.CONV_SYNC        =  0x200
  dd.CONV_EXCL        =  0x400
  dd.CONV_NOCREAT     =  0x800
  dd.CONV_NOTRUNC     = 0x1000
  dd.CONV_NOERROR     = 0x2000
  dd.CONV_FDATASYNC   = 0x4000
  dd.CONV_FSYNC       = 0x8000
  dd.CONVS = {
    "ascii"    : dd.CONV_ASCII    ,
    "ebcdic"   : dd.CONV_EBCDIC   ,
    "ibm"      : dd.CONV_IBM      ,
    "block"    : dd.CONV_BLOCK    ,
    "unblock"  : dd.CONV_UNBLOCK  ,
    "lcase"    : dd.CONV_LCASE    ,
    "ucase"    : dd.CONV_UCASE    ,
    "sparse"   : dd.CONV_SPARSE   ,
    "swab"     : dd.CONV_SWAB     ,
    "sync"     : dd.CONV_SYNC     ,
    "excl"     : dd.CONV_EXCL     ,
    "nocreat"  : dd.CONV_NOCREAT  ,
    "notrunc"  : dd.CONV_NOTRUNC  ,
    "noerror"  : dd.CONV_NOERROR  ,
    "fdatasync": dd.CONV_FDATASYNC,
    "fsync"    : dd.CONV_FSYNC    ,
  }
  dd.FLAG_APPEND      =      0x1
  dd.FLAG_DIRECT      =      0x2
  dd.FLAG_DIRECTORY   =      0x4
  dd.FLAG_DSYNC       =      0x8
  dd.FLAG_SYNC        =     0x10
  dd.FLAG_FULLBLOCK   =     0x20
  dd.FLAG_NONBLOCK    =     0x40
  dd.FLAG_NOATIME     =     0x80
  dd.FLAG_NOCACHE     =    0x100
  dd.FLAG_NOCTTY      =    0x200
  dd.FLAG_NOFOLLOW    =    0x400
  dd.FLAG_COUNT_BYTES =    0x800
  dd.FLAG_SKIP_BYTES  =   0x1000
  dd.FLAG_SEEK_BYTES  =   0x2000
  dd.FLAG_FORCE_SEEK  = 0x100000  # non standard
  dd.FLAGS = {
    "append"     : dd.FLAG_APPEND     ,
    "direct"     : dd.FLAG_DIRECT     ,
    "directory"  : dd.FLAG_DIRECTORY  ,
    "dsync"      : dd.FLAG_DSYNC      ,
    "sync"       : dd.FLAG_SYNC       ,
    "fullblock"  : dd.FLAG_FULLBLOCK  ,
    "nonblock"   : dd.FLAG_NONBLOCK   ,
    "noatime"    : dd.FLAG_NOATIME    ,
    "nochache"   : dd.FLAG_NOCACHE    ,
    "noctty"     : dd.FLAG_NOCTTY     ,
    "nofollow"   : dd.FLAG_NOFOLLOW   ,
    "count_bytes": dd.FLAG_COUNT_BYTES,
    "skip_bytes" : dd.FLAG_SKIP_BYTES ,
    "seek_bytes" : dd.FLAG_SEEK_BYTES ,
    "force_seek" : dd.FLAG_FORCE_SEEK ,
  }
  dd.ASCII_CONV_SCHEME = b"""\
\x00\x01\x02\x03\x9c\x09\x86\x7f\x97\x8d\x8e\x0b\x0c\x0d\x0e\x0f\
\x10\x11\x12\x13\x9d\x85\x08\x87\x18\x19\x92\x8f\x1c\x1d\x1e\x1f\
\x80\x81\x82\x83\x84\x0a\x17\x1b\x88\x89\x8a\x8b\x8c\x05\x06\x07\
\x90\x91\x16\x93\x94\x95\x96\x04\x98\x99\x9a\x9b\x14\x15\x9e\x1a\
\x20\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xd5\x2e\x3c\x28\x2b\x7c\
\x26\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\x21\x24\x2a\x29\x3b\x7e\
\x2d\x2f\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xcb\x2c\x25\x5f\x3e\x3f\
\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\x60\x3a\x23\x40\x27\x3d\x22\
\xc3\x61\x62\x63\x64\x65\x66\x67\x68\x69\xc4\xc5\xc6\xc7\xc8\xc9\
\xca\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x5e\xcc\xcd\xce\xcf\xd0\
\xd1\xe5\x73\x74\x75\x76\x77\x78\x79\x7a\xd2\xd3\xd4\x5b\xd6\xd7\
\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\x5d\xe6\xe7\
\x7b\x41\x42\x43\x44\x45\x46\x47\x48\x49\xe8\xe9\xea\xeb\xec\xed\
\x7d\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\xee\xef\xf0\xf1\xf2\xf3\
\x5c\x9f\x53\x54\x55\x56\x57\x58\x59\x5a\xf4\xf5\xf6\xf7\xf8\xf9\
\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\xfa\xfb\xfc\xfd\xfe\xff\
"""
  dd.EBCDIC_CONV_SCHEME = b"""\
\x00\x01\x02\x03\x37\x2d\x2e\x2f\x16\x05\x25\x0b\x0c\x0d\x0e\x0f\
\x10\x11\x12\x13\x3c\x3d\x32\x26\x18\x19\x3f\x27\x1c\x1d\x1e\x1f\
\x40\x5a\x7f\x7b\x5b\x6c\x50\x7d\x4d\x5d\x5c\x4e\x6b\x60\x4b\x61\
\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\x7a\x5e\x4c\x7e\x6e\x6f\
\x7c\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xd1\xd2\xd3\xd4\xd5\xd6\
\xd7\xd8\xd9\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xad\xe0\xbd\x9a\x6d\
\x79\x81\x82\x83\x84\x85\x86\x87\x88\x89\x91\x92\x93\x94\x95\x96\
\x97\x98\x99\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xc0\x4f\xd0\x5f\x07\
\x20\x21\x22\x23\x24\x15\x06\x17\x28\x29\x2a\x2b\x2c\x09\x0a\x1b\
\x30\x31\x1a\x33\x34\x35\x36\x08\x38\x39\x3a\x3b\x04\x14\x3e\xe1\
\x41\x42\x43\x44\x45\x46\x47\x48\x49\x51\x52\x53\x54\x55\x56\x57\
\x58\x59\x62\x63\x64\x65\x66\x67\x68\x69\x70\x71\x72\x73\x74\x75\
\x76\x77\x78\x80\x8a\x8b\x8c\x8d\x8e\x8f\x90\x6a\x9b\x9c\x9d\x9e\
\x9f\xa0\xaa\xab\xac\x4a\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\
\xb8\xb9\xba\xbb\xbc\xa1\xbe\xbf\xca\xcb\xcc\xcd\xce\xcf\xda\xdb\
\xdc\xdd\xde\xdf\xea\xeb\xec\xed\xee\xef\xfa\xfb\xfc\xfd\xfe\xff\
"""
  dd.IBM_CONV_SCHEME = b"""\
\x00\x01\x02\x03\x37\x2d\x2e\x2f\x16\x05\x25\x0b\x0c\x0d\x0e\x0f\
\x10\x11\x12\x13\x3c\x3d\x32\x26\x18\x19\x3f\x27\x1c\x1d\x1e\x1f\
\x40\x5a\x7f\x7b\x5b\x6c\x50\x7d\x4d\x5d\x5c\x4e\x6b\x60\x4b\x61\
\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\x7a\x5e\x4c\x7e\x6e\x6f\
\x7c\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xd1\xd2\xd3\xd4\xd5\xd6\
\xd7\xd8\xd9\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xad\xe0\xbd\x5f\x6d\
\x79\x81\x82\x83\x84\x85\x86\x87\x88\x89\x91\x92\x93\x94\x95\x96\
\x97\x98\x99\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xc0\x4f\xd0\xa1\x07\
\x20\x21\x22\x23\x24\x15\x06\x17\x28\x29\x2a\x2b\x2c\x09\x0a\x1b\
\x30\x31\x1a\x33\x34\x35\x36\x08\x38\x39\x3a\x3b\x04\x14\x3e\xe1\
\x41\x42\x43\x44\x45\x46\x47\x48\x49\x51\x52\x53\x54\x55\x56\x57\
\x58\x59\x62\x63\x64\x65\x66\x67\x68\x69\x70\x71\x72\x73\x74\x75\
\x76\x77\x78\x80\x8a\x8b\x8c\x8d\x8e\x8f\x90\x9a\x9b\x9c\x9d\x9e\
\x9f\xa0\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\
\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xca\xcb\xcc\xcd\xce\xcf\xda\xdb\
\xdc\xdd\xde\xdf\xea\xeb\xec\xed\xee\xef\xfa\xfb\xfc\xfd\xfe\xff\
"""
  return dd
dd = dd()
dd._required_globals = ["os"]
