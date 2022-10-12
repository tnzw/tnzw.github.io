#fs_sync = 'def/wip/fs_sync.yieldable.py'; print(f'--- USING {fs_sync}!!! ---'); exec(open(fs_sync, 'rb').read(), globals(), globals())

fs_sync__use_rsync = 0

def fs_sync__stat_to_str(s, props=None, os_module=None):
  if props is None:
    props = ("mode","size","mtime")
    if getattr(os_module, "chown", None): props += ("uid","gid")
  s = {k:getattr(s, "st_"+k) for k in props}
  s = {k:(oct(v) if k in ("mode",) else v) for k,v in s.items()}
  s = {k:(int(v) if k in ("mtime","atime","ctime") else v) for k,v in s.items()}
  return s
def fs_sync__soft_lstat(p, default=None, as_str=True, props=None, os_module=None):
  if os_module is None: os_module = os
  try: s = os_module.lstat(p)
  except FileNotFoundError: return default
  return fs_sync__stat_to_str(s, props=props, os_module=os_module) if as_str else s
def fs_sync__tester(fn):
  def test(*a,**k):
    tmpdir = tempfile.mkdtemp()
    pwd = os.getcwd()
    try:
      os.chdir(tmpdir)
      for _ in ("src", "dst", "bak"): os.mkdir(_)
      return fn(*a,**k)
    finally:
      os.chdir(pwd)
      shutil.rmtree(tmpdir)
  return test



def fs_sync__mkfile(path, data=None, open_mode=None, *, mode=None, mtime=None, atime=None, gid=None, uid=None, close=True, os_module=None):
  if os_module is None:
    os_module = os
    _open = open
    _opt = {}
  else:
    _open = open2
    _opt = {"os_module": os_module}
  if open_mode is None: open_mode = "w" if isinstance(data, str) else "wb"
  fh = None
  try:
    fh = _open(path, open_mode, **_opt)
    if data: fh.write(data)
    if not close: return fh
  finally:
    if close and fh is not None: fh.close()
  if mode is not None: os_module.chmod(path, mode)
  if gid is not None or uid is not None: os_module.chown(path, -1 if uid is None else uid, -1 if gid is None else gid)
  if mtime is not None or atime is not None: os_module.utime(path, (time.time() if atime is None else atime, time.time() if mtime is None else mtime))
def fs_sync__mkdir(path, *, nomkdir=False, mode=None, mtime=None, atime=None, gid=None, uid=None, os_module=None):
  if os_module is None: os_module = os
  if not nomkdir: os_module.mkdir(path)
  if mode is not None: os_module.chmod(path, mode)
  if gid is not None or uid is not None: os_module.chown(path, -1 if uid is None else uid, -1 if gid is None else gid)
  if mtime is not None or atime is not None: os_module.utime(path, (time.time() if atime is None else atime, time.time() if mtime is None else mtime))
def fs_sync__mklnk(path, target, *, os_module=None):
  if os_module is None: os_module = os
  os_module.symlink(target, path)
def fs_sync__mktree(treeschema, file_mode=None, dir_mode=None, auto_mtime=None, auto_data=None, os_module=None):
  if os_module is None: os_module = os
  dirs = []
  if auto_mtime:
    file_mtime = 100
    dir_mtime = 1000000
  if auto_data:
    data = "a"
  for line in treeschema.strip().split("\n"):
    c = line.find("#")
    if c != -1: line = line[:c]
    line = line.strip()
    if not line: continue
    words = line.split()
    path = words.pop(0)
    if path.endswith(("/", "\\")): path, typ = path[:-1], "dir"
    elif path.endswith("@"): path, typ = path[:-1], "lnk"
    #elif path.endswith("|"): path, typ = path[:-1], "pip"
    #elif path.endswith("="): path, typ = path[:-1], "soc"
    #elif path.endswith("&"): path, typ = path[:-1], "bld"
    #elif path.endswith("^"): path, typ = path[:-1], "blc"
    #elif path.startswith("-"): path, typ = path[1:], "noe"
    else: typ = "reg"
    opt = {"os_module": os_module}
    if file_mode is not None and typ == "reg": opt["mode"] = file_mode
    if dir_mode is not None and typ == "dir": opt["mode"] = dir_mode
    if auto_mtime:
      if typ == "reg":
        opt["mtime"] = file_mtime
        file_mtime += 2
      if typ == "dir":
        opt["mtime"] = dir_mtime
        dir_mtime += 2
    if auto_data and typ == "reg":
      opt["data"] = data
      data += bytes((ord(data[-1:]) + 1,)).decode("UTF-8", "surrogateescape")
    for word in words: exec(word, {}, opt)
    if typ == "reg": fs_sync__mkfile(path, **opt)
    elif typ == "dir": os_module.mkdir(path); dirs.append((path, opt))
    elif typ == "lnk": fs_sync__mklnk(path, **opt)
    else: XXX
  for path, opt in dirs: fs_sync__mkdir(path, nomkdir=1, **opt)
def fs_sync__reporttree(*paths, sep="/", top=False, size=False, data=False, mode=False, mtime=False, mtime_for_link=False, uid=False, gid=False, statconverter=None, os_module=None):
  report = []
  if os_module is None:
    os_module = os
    _open = open
    _open_opt = {}
  else:
    _open = open2
    _open_opt = {"os_module": os_module}
  if sep is None: sep = os_module.sep
  #if props is None:
  #  #if os_module.name == "nt": props = ("mode", "mtime")
  #  #else: props = ("mode", "uid", "gid", "mtime")
  #  props = ("mode", "mtime")
  if statconverter is None:
    def statconverter(val, prop):
      if prop == "mode": return oct(val & 0o777)
      if prop in ("mtime", "atime", "ctime"): ival = int(val); return ival if val == ival else val
      return val
  def read(path, text=False):
    with _open(path, "r" if text else "rb", **_open_opt) as f: return f.read()
  def rec(head, tail, noreport=False):
    try: stats = os_module.stat(head + tail, follow_symlinks=False)
    except FileNotFoundError: stats = None
    if stats is None: typ = " (noent)"
    elif stat.S_ISLNK(stats.st_mode): typ = "@"
    elif stat.S_ISDIR(stats.st_mode): typ = sep
    elif stat.S_ISREG(stats.st_mode): typ = ""
    else: XXX
    assert not stats or stats.st_nlink == 1, stats
    if not noreport:
      if typ in ("", sep):
        statstr = " ".join(f"{k}={statconverter(getattr(stats, 'st_' + k), k)}" for k, t in (("mode", mode), ("mtime", mtime), ("uid", uid), ("gid", gid)) if t)
        if typ == "":
          if data: statstr = (statstr + " " if statstr else "") + f"data={read(head + tail)!r}"
          if size: statstr = (statstr + " " if statstr else "") + f"size={stats.st_size!r}"
      elif typ == "@":
        statstr = " ".join(f"{k}={statconverter(getattr(stats, 'st_' + k), k)}" for k, t in (("mtime", mtime_for_link),) if t)
        if data: statstr = (statstr + " " if statstr else "") + f"target={os_module.readlink(head + tail)!r}"
        if size: statstr = (statstr + " " if statstr else "") + f"size={stats.st_size!r}"
      if typ == " (noent)": report.append(f"{tail}{typ}")
      else: report.append(f"{tail}{typ}{' ' if statstr else ''}{statstr}")
    if typ == sep:
      for name in sorted(os_module.listdir(head + tail)):
        rec(head, tail + sep + name)
  #for path in paths: rec(path, path[:0])
  for path in paths: rec("", path, not top)
  return "\n".join(report)
#def fs_sync__chkreportdiff(report1, report2):
#  report = "\n".join(l for l in difflines(report1, report2).split("\n") if not l.startswith(" "))
#  assert not report, "\n" + report
def fs_sync__diff(report1, report2):
  return "\n".join(l for l in difflines(report1, report2).split("\n") if not l.startswith(" "))

def fs_sync__chknoent(path, follow_symlinks=False, os_module=None):  # XXX please use it
  if os_module is None: os_module = os
  try: os_module.stat(path, follow_symlinks=follow_symlinks)
  except FileNotFoundError: return
  assert False, f"expected non-existing: {path!r}"
#def fs_sync__chkdirempty(path, follow_symlinks=False, os_module=None):  # XXX please use it
#  if os_module is None: os_module = os
#  dir = os_module.listdir(path)
#  assert dir == [], f"dir is not empty: {path!r} -> {dir}"
#def fs_sync__chkfile(path, data=None, open_mode=None, *, mode=None, mtime=None, atime=None, gid=None, uid=None, follow_symlinks=False, os_module=None):  # XXX please use it
#  if os_module is None:
#    os_module = os
#    _open = open
#    _opt = {}
#  else:
#    _open = open2
#    _opt = {"os_module": os_module}
#  if open_mode is None: open_mode = "r" if isinstance(data, str) else "rb"
#  fh = None
#  try:
#    stat = os_module.stat(path, follow_symlinks=follow_symlinks)
#    fh = _open(path, open_mode, **_opt)
#    same_data = data == fh.read() if data is not None else True
#    def statstr(val, prop):
#      if prop == "mode": return oct(val & 0o777)
#      return val
#    diffs = {}
#    expected = {}
#    for k, v in (("mode", mode), ("mtime", mtime), ("atime", atime), ("gid", gid), ("uid", uid)):
#      if v is None: continue
#      if k == "mode": v, s = (oct(_ & 0o777) for _ in (v, getattr(stat, "st_" + k)))
#      else: s = getattr(stat, "st_" + k)
#      if v != s:
#        diffs[k] = (s, v)
#        #expected[k] = v
#    if not same_data:
#      diffs["data"] = "<different>"
#      #expected["data"] = "<different>"
#    assert not diffs, f"diffs for: {path!r} -> {diffs}"
#    #assert not expected, f"expected for: {path!r} -> {expected}"
#
#    #if mode is not None: os_module.fchmod(fh.fileno(), mode)
#    #if gid is not None or uid is not None: os_module.fchown(fh.fileno(), -1 if uid is None else uid, -1 if gid is None else gid)
#    #if mtime is not None or atime is not None: os_module.utime(fh.fileno(), (atime, mtime))
#    #if close: return
#    #return fh
#  except FileNotFoundError:
#    assert False, f"expected existing file: {path!r}"
#  except IsADirectoryError:
#    assert False, f"expected file instead of dir: {path!r}"
#  finally:
#    if fh is not None: fh.close()


#def fs_sync__chktree(treeschema):
#  report = ""
#  errored = False
#  for line in treeschema.strip().split("\n"):
#    words = line.strip().split()
#    path = words.pop(0)
#    if path.startswith("#"): continue
#    #if path.endswith(("/-", "\\-")): path, typ = path[:-1], "emp"
#    if path.endswith(("/", "\\")): path, typ = path[:-1], "dir"
#    elif path.endswith("@"): path, typ = path[:-1], "lnk"
#    #elif path.endswith("|"): path, typ = path[:-1], "pip"
#    #elif path.endswith("~"): path, typ = path[:-1], "soc"
#    #elif path.endswith("&"): path, typ = path[:-1], "bld"
#    #elif path.endswith("^"): path, typ = path[:-1], "blc"
#    elif path.startswith("-"): path, typ = path[1:], "noe"
#    else: typ = "reg"
#    opt = {}
#    for word in words: exec(word, {}, opt)
#    try:
#      if typ == "reg": fs_sync__chkfile(path, **opt)
#      elif typ == "emp": fs_sync__chkdirempty(path, **opt)
#      elif typ == "noe": fs_sync__chknoent(path, **opt)
#      else: XXX
#    except (AssertionError, OSError) as err:
#      errored = True
#      report += f"ERROR {line} -> {err}\n"
#    else:
#      report += f"OK {path} {opt}\n"
#  if errored:
#    assert False, "\n" + report

def fs_sync__striplines(text):
  return "\n".join(" ".join(w for w in ls.split()) for l in text.strip().split("\n") for ls in (l.strip(),) if ls)
def fs_sync__assert_report(a, b, message=None, info=None):
  a = fs_sync__striplines(a)
  b = fs_sync__striplines(b)
  #if message is None: message = f"{a}\n !=\n{b}"
  if message is None: message = difflines(a, b)
  if info is None: info = ""
  else: info = f"\n{info}"
  assert a == b, "\n" + str(message) + info




@fs_sync__tester
def test_fs_sync__rsync_no_option():
  try: os.symlink('lol', 'lal')
  except OSError: print('cannot test symlinks!'); supports_symlink = False
  else: supports_symlink = True; os.unlink('lal')
  def grep_notsymlink(s):
    if supports_symlink: return s
    return '\n'.join(line for line in s.split('\n') if '@' not in line)

  cwd = os.getcwd()
  fs_sync__mktree(grep_notsymlink(f"""
    src/file                mode=0o646 mtime=1000 data=b'f1'
    src/emptydir/           mode=0o757 mtime=1002
    src/brokenlink@         target='brokenlinktarget'
    src/filelink@           target='file'
    src/emptydirlink@       target='emptydir'
    src/dirlink@            target='dir'
    #src/outdirlink@         target='../src2'
    src/infinitelink@       target='dir/infinitelink'
    src/abslink@            target='{cwd}/src/file'
    src/dir/                mode=0o757 mtime=2000
    src/dir/file2           mode=0o646 mtime=1004 data=b'f2'
    src/dir/emptydir2/      mode=0o757 mtime=1006
    src/dir/brokenlink2@    target='brokenlink2target'
    src/dir/filelink2@      target='file2'
    src/dir/emptydirlink2@  target='emptydir2'
    src/dir/parfilelink@    target='../file'
    src/dir/looplink@       target='../dir'
    src/dir/infinitelink2@  target='../infinitelink'

    src/quickcheck          mode=0o646 mtime=1234 data=b'a'
    dst/quickcheck          mode=0o646 mtime=1234 data=b'b'
  """))
  tree_report = fs_sync__reporttree("src", "dst", data=1)

  if fs_sync__use_rsync: os.system("rsync src/* dst/")
  else: fs_sync("src", "dst", source_directory=True)

  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1)), """
    +dst/file data=b'f1'
  """)

@fs_sync__tester
def test_fs_sync__rsync_ignoretimes():
  fs_sync__mktree("""
    src/quickcheck          mode=0o646 mtime=1234 data=b'a'
    dst/quickcheck          mode=0o646 mtime=1234 data=b'b'
  """)
  tree_report = fs_sync__reporttree("src", "dst", data=1)

  if fs_sync__use_rsync: os.system("rsync src/* dst/ --ignore-times")
  else: fs_sync("src", "dst", source_directory=True, ignore_times=True)

  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1)), """
    -dst/quickcheck data=b'b'
    +dst/quickcheck data=b'a'
  """)

@fs_sync__tester
def test_fs_sync__rsync_archive():
  try: os.symlink('lol', 'lal')
  except OSError: print('cannot test symlinks!'); supports_symlink = False
  else: supports_symlink = True; os.unlink('lal')
  def grep_notsymlink(s):
    if supports_symlink: return s
    return '\n'.join(line for line in s.split('\n') if '@' not in line)

  cwd = os.getcwd(); sep = os.sep; rcwd = repr(cwd)[1:-1]; rsep = repr(sep)[1:-1]; rrcwd = '\\\\\\\\?\\\\' + rcwd if os.name == 'nt' else rcwd
  fs_sync__mktree(grep_notsymlink(f"""
    src/file                mode=0o646 mtime=1000 data=b'f1'
    src/emptydir/           mode=0o757 mtime=1002
    src/brokenlink@         target='brokenlinktarget'
    src/filelink@           target='file'
    src/emptydirlink@       target='emptydir'
    src/dirlink@            target='dir'
    #src/outdirlink@         target='../src2'
    src/infinitelink@       target='dir/infinitelink'
    src/abslink@            target='{rcwd}/src/file'
    src/dir/                mode=0o757 mtime=2000
    src/dir/file2           mode=0o646 mtime=1004 data=b'f2'
    src/dir/emptydir2/      mode=0o757 mtime=1006
    src/dir/brokenlink2@    target='brokenlink2target'
    src/dir/filelink2@      target='file2'
    src/dir/emptydirlink2@  target='emptydir2'
    src/dir/parfilelink@    target='../file'
    src/dir/looplink@       target='../dir'
    src/dir/infinitelink2@  target='../infinitelink'

    src/update_file_diff_mtime mode=0o646 mtime=1000 data=b'u1'
    dst/update_file_diff_mtime mode=0o646 mtime=1002 data=b'u2'
    src/update_file_diff_size  mode=0o646 mtime=1004 data=b'u1'
    dst/update_file_diff_size  mode=0o646 mtime=1004 data=b'u11'
  """))
  tree_report = fs_sync__reporttree("src", "dst", data=1, mode=1, mtime=1)

  if fs_sync__use_rsync: os.system("rsync src/ dst/ --archive")
  else: fs_sync("src", "dst", source_directory=True, archive=True)

  if os.name == "nt": dir_mode, file_mode = '0o777', '0o666'
  else: dir_mode, file_mode = '0o757', '0o646'
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1, mode=1, mtime=1)), grep_notsymlink(f"""
    -dst/update_file_diff_mtime mode={file_mode} mtime=1002 data=b'u2'
    -dst/update_file_diff_size  mode={file_mode} mtime=1004 data=b'u11'
    +dst/abslink@            target='{rrcwd}{rsep}src{rsep}file'
    +dst/brokenlink@         target='brokenlinktarget'
    +dst/dir/                mode={dir_mode} mtime=2000
    +dst/dir/brokenlink2@    target='brokenlink2target'
    +dst/dir/emptydir2/      mode={dir_mode} mtime=1006
    +dst/dir/emptydirlink2@  target='emptydir2'
    +dst/dir/file2           mode={file_mode} mtime=1004 data=b'f2'
    +dst/dir/filelink2@      target='file2'
    +dst/dir/infinitelink2@  target='../infinitelink'
    +dst/dir/looplink@       target='../dir'
    +dst/dir/parfilelink@    target='../file'
    +dst/dirlink@            target='dir'
    +dst/emptydir/           mode={dir_mode} mtime=1002
    +dst/emptydirlink@       target='emptydir'
    +dst/file                mode={file_mode} mtime=1000 data=b'f1'
    +dst/filelink@           target='file'
    +dst/infinitelink@       target='dir/infinitelink'
    +dst/update_file_diff_mtime mode={file_mode} mtime=1000 data=b'u1'
    +dst/update_file_diff_size  mode={file_mode} mtime=1004 data=b'u1'
  """))

@fs_sync__tester
def test_fs_sync__rsync_archive_copylinks():
  #if os.name == "nt": print("can't check it on windows"); return
  try: os.symlink('lol', 'lal')
  except OSError: print('cannot test on this environment!'); return
  else: supports_symlink = True; os.unlink('lal')

  cwd = os.getcwd(); sep = os.sep; rcwd = repr(cwd)[1:-1]; rsep = repr(sep)[1:-1]; rrcwd = '\\\\\\\\?\\\\' + rcwd if os.name == 'nt' else rcwd
  fs_sync__mktree(f"""
    src/file                mode=0o646 mtime=1000 data=b'f1'
    src/emptydir/           mode=0o757 mtime=1002
    src/brokenlink@         target='brokenlinktarget'
    src/filelink@           target='file'
    src/emptydirlink@       target='emptydir'
    src/dirlink@            target='dir'
    #src/outdirlink@         target='../src2'  # XXX why is this line commented out?
    src/infinitelink@       target='dir/infinitelink'
    src/abslink@            target='{rcwd}/src/file'
    src/dir/                mode=0o757 mtime=2000
    src/dir/file2           mode=0o646 mtime=1004 data=b'f2'
    src/dir/emptydir2/      mode=0o757 mtime=1006
    src/dir/brokenlink2@    target='brokenlink2target'
    src/dir/filelink2@      target='file2'
    src/dir/emptydirlink2@  target='emptydir2'
    src/dir/parfilelink@    target='../file'
    #src/dir/looplink@       target='../dir'  # rsync has no looplink protection (keeps system behavior)
    src/dir/infinitelink2@  target='../infinitelink'  # system conciders it a brokenlink
  """)
  tree_report = fs_sync__reporttree("src", "dst", data=1, mode=1, mtime=1)

  if fs_sync__use_rsync: os.system("rsync src/ dst/ --archive --copy-links")
  else: fs_sync("src", "dst", source_directory=True, archive=True, copy_links=True)

  if os.name == "nt": dir_mode, file_mode = '0o777', '0o666'
  else: dir_mode, file_mode = '0o757', '0o646'
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1, mode=1, mtime=1)), f"""
    +dst/abslink                 mode={file_mode} mtime=1000 data=b'f1'
    +dst/dir/                    mode={dir_mode}  mtime=2000
    +dst/dir/emptydir2/          mode={dir_mode}  mtime=1006
    +dst/dir/emptydirlink2/      mode={dir_mode}  mtime=1006
    +dst/dir/file2               mode={file_mode} mtime=1004 data=b'f2'
    +dst/dir/filelink2           mode={file_mode} mtime=1004 data=b'f2'
    +dst/dir/parfilelink         mode={file_mode} mtime=1000 data=b'f1'
    +dst/dirlink/                mode={dir_mode}  mtime=2000
    +dst/dirlink/emptydir2/      mode={dir_mode}  mtime=1006
    +dst/dirlink/emptydirlink2/  mode={dir_mode}  mtime=1006
    +dst/dirlink/file2           mode={file_mode} mtime=1004 data=b'f2'
    +dst/dirlink/filelink2       mode={file_mode} mtime=1004 data=b'f2'
    +dst/dirlink/parfilelink     mode={file_mode} mtime=1000 data=b'f1'
    +dst/emptydir/               mode={dir_mode}  mtime=1002
    +dst/emptydirlink/           mode={dir_mode}  mtime=1002
    +dst/file                    mode={file_mode} mtime=1000 data=b'f1'
    +dst/filelink                mode={file_mode} mtime=1000 data=b'f1'
  """)

@fs_sync__tester
def test_fs_sync__rsync_archive_copyunsafelinks():
  try: os.symlink('lol', 'lal')
  except OSError: print('cannot test on this environment!'); return
  else: supports_symlink = True; os.unlink('lal')

  cwd = os.getcwd(); sep = os.sep; rcwd = repr(cwd)[1:-1]; rsep = repr(sep)[1:-1]; rrcwd = '\\\\\\\\?\\\\' + rcwd if os.name == 'nt' else rcwd
  fs_sync__mktree(f"""
    src/file                mode=0o646 mtime=1000 data=b'f1'
    src/emptydir/           mode=0o757 mtime=1002
    src/brokenlink@         target='brokenlinktarget'
    src/filelink@           target='file'
    src/emptydirlink@       target='emptydir'
    src/dirlink@            target='dir'
    src/outdirlink@         target='../src2'
    src/infinitelink@       target='dir/infinitelink'
    src/abslink@            target='{rcwd}/src/file'
    src/dir/                mode=0o757 mtime=2000
    src/dir/file2           mode=0o646 mtime=1004 data=b'f2'
    src/dir/emptydir2/      mode=0o757 mtime=1006
    src/dir/brokenlink2@    target='brokenlink2target'
    src/dir/filelink2@      target='file2'
    src/dir/emptydirlink2@  target='emptydir2'
    src/dir/parfilelink@    target='../file'
    src/dir/looplink@       target='../dir'
    src/dir/infinitelink2@  target='../infinitelink'
    src2/                   mode=0o757 mtime=19998
    src2/file3              mode=0o646 mtime=11000 data=b'f3'
  """)
  tree_report = fs_sync__reporttree("src", "dst", data=1, mode=1, mtime=1)

  if fs_sync__use_rsync: os.system("rsync src/ dst/ --archive --copy-unsafe-links")
  else: return assert_raise(TypeError, lambda: fs_sync("src", "dst", source_directory=True, archive=True, copy_unsafe_links=True))  # XXX TypeError: fs_sync() got an unexpected keyword argument 'copy_unsafe_links'

  if os.name == "nt": dir_mode, file_mode = '0o777', '0o666'
  else: dir_mode, file_mode = '0o757', '0o646'
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1, mode=1, mtime=1)), f"""
    +dst/brokenlink@         target='brokenlinktarget'
    +dst/dir/                mode={dir_mode} mtime=2000
    +dst/dir/brokenlink2@    target='brokenlink2target'
    +dst/dir/emptydir2/      mode={dir_mode} mtime=1006
    +dst/dir/emptydirlink2@  target='emptydir2'
    +dst/dir/file2           mode={file_mode} mtime=1004 data=b'f2'
    +dst/dir/filelink2@      target='file2'
    +dst/dir/infinitelink2@  target='../infinitelink'
    +dst/dir/looplink@       target='../dir'
    +dst/dir/parfilelink@    target='../file'
    +dst/dirlink@            target='dir'
    +dst/emptydir/           mode={dir_mode} mtime=1002
    +dst/emptydirlink@       target='emptydir'
    +dst/file                mode={file_mode} mtime=1000 data=b'f1'
    +dst/filelink@           target='file'
    +dst/infinitelink@       target='dir/infinitelink'
    +dst/outdirlink/         mode={dir_mode} mtime=19998
    +dst/outdirlink/file3    mode={file_mode} mtime=11000 data=b'f3'
  """)

@fs_sync__tester
def test_fs_sync__rsync_dirs_copydirlinks():
  #if os.name == "nt": print("can't check it on windows"); return
  try: os.symlink('lol', 'lal')
  except OSError: print('cannot test on this environment!'); return
  else: supports_symlink = True; os.unlink('lal')

  cwd = os.getcwd(); sep = os.sep; rcwd = repr(cwd)[1:-1]; rsep = repr(sep)[1:-1]; rrcwd = '\\\\\\\\?\\\\' + rcwd if os.name == 'nt' else rcwd
  fs_sync__mktree(f"""
    src/file                mode=0o646 mtime=1000 data=b'f1'
    src/emptydir/           mode=0o757 mtime=1002
    src/brokenlink@         target='brokenlinktarget'
    src/filelink@           target='file'
    src/emptydirlink@       target='emptydir'
    src/dirlink@            target='dir'
    src/outdirlink@         target='../src2'
    src/infinitelink@       target='dir/infinitelink'
    src/abslink@            target='{rcwd}/src/file'
    src/dir/                mode=0o757 mtime=2000
    src/dir/file2           mode=0o646 mtime=1004 data=b'f2'
    src/dir/emptydir2/      mode=0o757 mtime=1006
    src/dir/brokenlink2@    target='brokenlink2target'
    src/dir/filelink2@      target='file2'
    src/dir/emptydirlink2@  target='emptydir2'
    src/dir/parfilelink@    target='../file'
    #src/dir/looplink@       target='../dir'  # rsync has no looplink protection (keeps system behavior)
    src/dir/infinitelink2@  target='../infinitelink'
  """)
  tree_report = fs_sync__reporttree("src", "dst", data=1)

  if fs_sync__use_rsync: os.system("rsync src/* dst/ --dirs --copy-dirlinks")
  else: fs_sync("src", "dst", source_directory=True, dirs=True, copy_dirlinks=True)

  if os.name == "nt": dir_mode, file_mode = '0o777', '0o666'
  else: dir_mode, file_mode = '0o757', '0o646'
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1)), f"""
    +dst/dir/
    +dst/dirlink/
    +dst/emptydir/
    +dst/emptydirlink/
    +dst/file          data=b'f1'
  """)

@fs_sync__tester
def test_fs_sync__rsync_archive_copydirlinks():
  if os.name == "nt": print("can't check it on windows"); return

  cwd = os.getcwd(); sep = os.sep; rcwd = repr(cwd)[1:-1]; rsep = repr(sep)[1:-1]; rrcwd = '\\\\\\\\?\\\\' + rcwd if os.name == 'nt' else rcwd
  fs_sync__mktree(f"""
    src/file                mode=0o646 mtime=1000 data=b'f1'
    src/emptydir/           mode=0o757 mtime=1002
    src/brokenlink@         target='brokenlinktarget'
    src/filelink@           target='file'
    src/emptydirlink@       target='emptydir'
    src/dirlink@            target='dir'
    src/outdirlink@         target='../src2'
    src/infinitelink@       target='dir/infinitelink'
    src/abslink@            target='{rcwd}/src/file'
    src/dir/                mode=0o757 mtime=2000
    src/dir/file2           mode=0o646 mtime=1004 data=b'f2'
    src/dir/emptydir2/      mode=0o757 mtime=1006
    src/dir/brokenlink2@    target='brokenlink2target'
    src/dir/filelink2@      target='file2'
    src/dir/emptydirlink2@  target='emptydir2'
    src/dir/parfilelink@    target='../file'
    #src/dir/looplink@       target='../dir'  # rsync has no looplink protection (keeps system behavior)
    src/dir/infinitelink2@  target='../infinitelink'
  """)
  tree_report = fs_sync__reporttree("src", "dst", data=1, mode=1, mtime=1)

  if fs_sync__use_rsync: os.system("rsync src/ dst/ --archive --copy-dirlinks")
  else: fs_sync("src", "dst", source_directory=True, archive=True, copy_dirlinks=True)

  if os.name == "nt": dir_mode, file_mode = '0o777', '0o666'
  else: dir_mode, file_mode = '0o757', '0o646'
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1, mode=1, mtime=1)), f"""
    +dst/abslink@                target='{rrcwd}/src/file'
    +dst/brokenlink@             target='brokenlinktarget'
    +dst/dir/                    mode={dir_mode}  mtime=2000
    +dst/dir/brokenlink2@        target='brokenlink2target'
    +dst/dir/emptydir2/          mode={dir_mode}  mtime=1006
    +dst/dir/emptydirlink2/      mode={dir_mode}  mtime=1006
    +dst/dir/file2               mode={file_mode} mtime=1004 data=b'f2'
    +dst/dir/filelink2@          target='file2'
    +dst/dir/infinitelink2@      target='../infinitelink'
    +dst/dir/parfilelink@        target='../file'
    +dst/dirlink/                mode={dir_mode}  mtime=2000
    +dst/dirlink/brokenlink2@    target='brokenlink2target'
    +dst/dirlink/emptydir2/      mode={dir_mode}  mtime=1006
    +dst/dirlink/emptydirlink2/  mode={dir_mode}  mtime=1006
    +dst/dirlink/file2           mode={file_mode} mtime=1004 data=b'f2'
    +dst/dirlink/filelink2@      target='file2'
    +dst/dirlink/infinitelink2@  target='../infinitelink'
    +dst/dirlink/parfilelink@    target='../file'
    +dst/emptydir/               mode={dir_mode}  mtime=1002
    +dst/emptydirlink/           mode={dir_mode}  mtime=1002
    +dst/file                    mode={file_mode} mtime=1000 data=b'f1'
    +dst/filelink@               target='file'
    +dst/infinitelink@           target='dir/infinitelink'
    +dst/outdirlink@             target='../src2'
  """)

@fs_sync__tester
def test_fs_sync__rsync_archive_ignoreexisting():
  try: os.symlink('lol', 'lal')
  except OSError: print('cannot test symlinks!'); supports_symlink = False
  else: supports_symlink = True; os.unlink('lal')
  def grep_notsymlink(s):
    if supports_symlink: return s
    return '\n'.join(line for line in s.split('\n') if '@' not in line)

  fs_sync__mktree(grep_notsymlink("""
    src/file                mode=0o646 mtime=1000 data=b'f1'
    src/emptydir/           mode=0o757 mtime=1002
    src/brokenlink@         target='brokenlinktarget'
    src/filelink@           target='file'
    src/emptydirlink@       target='emptydir'
    src/dirlink@            target='dir'
    src/outdirlink@         target='../src2'
    src/infinitelink@       target='dir/infinitelink'
    src/dir/                mode=0o757 mtime=2000
    src/dir/file2           mode=0o646 mtime=1004 data=b'f2'
    src/dir/emptydir2/      mode=0o757 mtime=1006
    src/dir/brokenlink2@    target='brokenlink2target'
    src/dir/filelink2@      target='file2'
    src/dir/emptydirlink2@  target='emptydir2'
    src/dir/parfilelink@    target='../file'
    src/dir/looplink@       target='../dir'
    src/dir/infinitelink2@  target='../infinitelink'
    src/dirtoreg/           mode=0o757 mtime=2002
    src/dirtoreg/gnark      mode=0o757 mtime=1008
    src/regtodir            mode=0o646 mtime=1010 data=b'f3'

    dst/file                mode=0o666 mtime=11000 data=b'nf1'
    dst/emptydir/           mode=0o777 mtime=11002
    dst/brokenlink@         target='nbrokenlinktarget'
    dst/filelink@           target='nfile'
    dst/emptydirlink@       target='nemptydir'
    dst/dirlink@            target='ndir'
    dst/outdirlink@         target='../nsrc2'
    dst/infinitelink@       target='ndir/infinitelink'
    dst/dir/                mode=0o777 mtime=12000
    dst/dir/file2           mode=0o666 mtime=11004 data=b'nf2'
    dst/dir/emptydir2/      mode=0o777 mtime=11006
    dst/dir/brokenlink2@    target='nbrokenlink2target'
    dst/dir/filelink2@      target='nfile2'
    dst/dir/emptydirlink2@  target='nemptydir2'
    dst/dir/parfilelink@    target='../nfile'
    dst/dir/looplink@       target='../ndir'
    dst/dir/infinitelink2@  target='../ninfinitelink'
    dst/dirtoreg            mode=0o666 mtime=11008 data=b'nf3'
    dst/regtodir/           mode=0o777 mtime=12002
    dst/regtodir/gnark2     mode=0o777 mtime=11010
  """))
  tree_report = fs_sync__reporttree("src", "dst", data=1, mode=1, mtime=1)

  if fs_sync__use_rsync: os.system("rsync src/ dst/ --archive --ignore-existing")
  else: fs_sync("src", "dst", source_directory=True, archive=True, ignore_existing=True)

  if os.name == "nt": dir_mode, file_mode = '0o777', '0o666'
  else: dir_mode, file_mode = '0o757', '0o646'
  if fs_sync__use_rsync:
    fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1, mode=1, mtime=1)), f"""
      -dst/dir/            mode=0o777 mtime=12000
      +dst/dir/            mode={dir_mode} mtime=2000
      -dst/dir/emptydir2/  mode=0o777 mtime=11006
      +dst/dir/emptydir2/  mode={dir_mode} mtime=1006
      -dst/dirtoreg        mode=0o666 mtime=11008 data=b'nf3'
      -dst/emptydir/       mode=0o777 mtime=11002
      +dst/dirtoreg        mode=0o666 mtime=2002 data=b'nf3'
      +dst/emptydir/       mode={dir_mode} mtime=1002
    """)
  else:
    fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1, mode=1, mtime=1)), f"""
      -dst/dir/            mode=0o777 mtime=12000
      +dst/dir/            mode={dir_mode} mtime=2000
      -dst/dir/emptydir2/  mode=0o777 mtime=11006
      +dst/dir/emptydir2/  mode={dir_mode} mtime=1006
      -dst/emptydir/       mode=0o777 mtime=11002
      +dst/emptydir/       mode={dir_mode} mtime=1002
    """)

@fs_sync__tester
def test_fs_sync__rsync_dirs_ignoreexisting():
  try: os.symlink('lol', 'lal')
  except OSError: print('cannot test symlinks!'); supports_symlink = False
  else: supports_symlink = True; os.unlink('lal')
  def grep_notsymlink(s):
    if supports_symlink: return s
    return '\n'.join(line for line in s.split('\n') if '@' not in line)

  fs_sync__mktree(grep_notsymlink("""
    src/file                mode=0o646 mtime=1000 data=b'f1'
    src/emptydir/           mode=0o757 mtime=1002
    src/brokenlink@         target='brokenlinktarget'
    src/filelink@           target='file'
    src/emptydirlink@       target='emptydir'
    src/dirlink@            target='dir'
    src/outdirlink@         target='../src2'
    src/infinitelink@       target='dir/infinitelink'
    src/dir/                mode=0o757 mtime=2000
    src/dir/file2           mode=0o646 mtime=1004 data=b'f2'
    src/dir/emptydir2/      mode=0o757 mtime=1006
    src/dir/brokenlink2@    target='brokenlink2target'
    src/dir/filelink2@      target='file2'
    src/dir/emptydirlink2@  target='emptydir2'
    src/dir/parfilelink@    target='../file'
    src/dir/looplink@       target='../dir'
    src/dir/infinitelink2@  target='../infinitelink'
    src/dirtoreg/           mode=0o757 mtime=1008
    src/regtodir            mode=0o646 mtime=1010 data=b'f3'

    dst/file                mode=0o666 mtime=11000 data=b'nf1'
    dst/emptydir/           mode=0o777 mtime=11002
    dst/brokenlink@         target='nbrokenlinktarget'
    dst/filelink@           target='nfile'
    dst/emptydirlink@       target='nemptydir'
    dst/dirlink@            target='ndir'
    dst/outdirlink@         target='../nsrc2'
    dst/infinitelink@       target='ndir/infinitelink'
    dst/dir/                mode=0o777 mtime=12000
    dst/dir/file2           mode=0o666 mtime=11004 data=b'nf2'
    dst/dir/emptydir2/      mode=0o777 mtime=11006
    dst/dir/brokenlink2@    target='nbrokenlink2target'
    dst/dir/filelink2@      target='nfile2'
    dst/dir/emptydirlink2@  target='nemptydir2'
    dst/dir/parfilelink@    target='../nfile'
    dst/dir/looplink@       target='../ndir'
    dst/dir/infinitelink2@  target='../ninfinitelink'
    dst/dirtoreg            mode=0o666 mtime=11008 data=b'nf3'
    dst/regtodir/           mode=0o777 mtime=11010
  """))
  tree_report = fs_sync__reporttree("src", "dst", data=1, mode=1, mtime=1)

  if fs_sync__use_rsync: os.system("rsync src/* dst/ --dirs --ignore-existing")
  else: fs_sync("src", "dst", source_directory=True, dirs=True, ignore_existing=True)

  if os.name == "nt": dir_mode, file_mode = '0o777', '0o666'
  else: dir_mode, file_mode = '0o757', '0o646'
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1, mode=1, mtime=1)), f"""
  """)

@fs_sync__tester
def test_fs_sync__rsync_dirs():
  try: os.symlink('lol', 'lal')
  except OSError: print('cannot test symlinks!'); supports_symlink = False
  else: supports_symlink = True; os.unlink('lal')
  def grep_notsymlink(s):
    if supports_symlink: return s
    return '\n'.join(line for line in s.split('\n') if '@' not in line)

  fs_sync__mktree(grep_notsymlink("""
    src/file                mode=0o646 mtime=1000 data=b'f1'
    src/emptydir/           mode=0o757 mtime=1002
    src/brokenlink@         target='brokenlinktarget'
    src/filelink@           target='file'
    src/emptydirlink@       target='emptydir'
    src/dirlink@            target='dir'
    #src/outdirlink@         target='../src2'
    src/infinitelink@       target='dir/infinitelink'
    src/dir/                mode=0o757 mtime=2000
    src/dir/file2           mode=0o646 mtime=1004 data=b'f2'
    src/dir/emptydir2/      mode=0o757 mtime=1006
    src/dir/brokenlink2@    target='brokenlink2target'
    src/dir/filelink2@      target='file2'
    src/dir/emptydirlink2@  target='emptydir2'
    src/dir/parfilelink@    target='../file'
    src/dir/looplink@       target='../dir'
    src/dir/infinitelink2@  target='../infinitelink'
  """))
  tree_report = fs_sync__reporttree("src", "dst", data=1)

  if fs_sync__use_rsync: os.system("rsync src/* dst/ --dirs")
  else: fs_sync("src", "dst", source_directory=True, dirs=True)

  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1)), """
    +dst/dir/
    +dst/emptydir/
    +dst/file       data=b'f1'
  """)

@fs_sync__tester
def test_fs_sync__rsync_links():
  try: os.symlink('lol', 'lal')
  except OSError: print('cannot test on this environment!'); return
  else: supports_symlink = True; os.unlink('lal')

  fs_sync__mktree("""
    src/file                mode=0o646 mtime=1000 data=b'f1'
    src/emptydir/           mode=0o757 mtime=1002
    src/brokenlink@         target='brokenlinktarget'
    src/filelink@           target='file'
    src/emptydirlink@       target='emptydir'
    src/dirlink@            target='dir'
    #src/outdirlink@         target='../src2'
    src/infinitelink@       target='dir/infinitelink'
    src/dir/                mode=0o757 mtime=2000
    src/dir/file2           mode=0o646 mtime=1004 data=b'f2'
    src/dir/emptydir2/      mode=0o757 mtime=1006
    src/dir/brokenlink2@    target='brokenlink2target'
    src/dir/filelink2@      target='file2'
    src/dir/emptydirlink2@  target='emptydir2'
    src/dir/parfilelink@    target='../file'
    src/dir/looplink@       target='../dir'
    src/dir/infinitelink2@  target='../infinitelink'
  """)
  tree_report = fs_sync__reporttree("src", "dst", data=1)

  if fs_sync__use_rsync: os.system("rsync src/* dst/ --links")
  else: fs_sync("src", "dst", source_directory=True, links=True)

  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1)), """
    +dst/brokenlink@    target='brokenlinktarget'
    +dst/dirlink@       target='dir'
    +dst/emptydirlink@  target='emptydir'
    +dst/file           data=b'f1'
    +dst/filelink@      target='file'
    +dst/infinitelink@  target='dir/infinitelink'
  """)

@fs_sync__tester
def test_fs_sync__remove():
  try: os.symlink('lol', 'lal')
  except OSError: print('cannot test symlinks!'); supports_symlink = False
  else: supports_symlink = True; os.unlink('lal')
  def grep_notsymlink(s):
    if supports_symlink: return s
    return '\n'.join(line for line in s.split('\n') if '@' not in line)

  fs_sync__mktree(grep_notsymlink("""
    src/file                mode=0o646 mtime=1000 data=b'f1'
    src/emptydir/           mode=0o757 mtime=1002
    src/brokenlink@         target='brokenlinktarget'
    src/filelink@           target='file'
    src/emptydirlink@       target='emptydir'
    src/dirlink@            target='dir'
    src/outdirlink@         target='../src2'
    src/infinitelink@       target='dir/infinitelink'
    src/dir/                mode=0o757 mtime=2000
    src/dir/file2           mode=0o646 mtime=1004 data=b'f2'
    src/dir/emptydir2/      mode=0o757 mtime=1006
    src/dir/brokenlink2@    target='brokenlink2target'
    src/dir/filelink2@      target='file2'
    src/dir/emptydirlink2@  target='emptydir2'
    src/dir/parfilelink@    target='../file'
    src/dir/looplink@       target='../dir'
    src/dir/infinitelink2@  target='../infinitelink'
  """))
  tree_report = fs_sync__reporttree("src", "dst", data=1)
  if fs_sync__use_rsync: print("  unhandled test for rsync"); return
  else: fs_sync.remove("src/dir", recursive=1, links=1)
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1)), grep_notsymlink(f"""
    -src/dir/
    -src/dir/brokenlink2@ target='brokenlink2target'
    -src/dir/emptydir2/
    -src/dir/emptydirlink2@ target='emptydir2'
    -src/dir/file2 data=b'f2'
    -src/dir/filelink2@ target='file2'
    -src/dir/infinitelink2@ target='../infinitelink'
    -src/dir/looplink@ target='../dir'
    -src/dir/parfilelink@ target='../file'
  """))
  fs_sync.remove("src", source_directory=1, links=1)
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1)), grep_notsymlink(f"""
    -src/brokenlink@ target='brokenlinktarget'
    -src/dir/
    -src/dir/brokenlink2@ target='brokenlink2target'
    -src/dir/emptydir2/
    -src/dir/emptydirlink2@ target='emptydir2'
    -src/dir/file2 data=b'f2'
    -src/dir/filelink2@ target='file2'
    -src/dir/infinitelink2@ target='../infinitelink'
    -src/dir/looplink@ target='../dir'
    -src/dir/parfilelink@ target='../file'
    -src/dirlink@ target='dir'
    -src/emptydir/
    -src/emptydirlink@ target='emptydir'
    -src/file data=b'f1'
    -src/filelink@ target='file'
    -src/infinitelink@ target='dir/infinitelink'
    -src/outdirlink@ target='../src2'
    +
  """))

@fs_sync__tester
def test_fs_sync__move():
  try: os.symlink('lol', 'lal')
  except OSError: print('cannot test symlinks!'); supports_symlink = False
  else: supports_symlink = True; os.unlink('lal')
  def grep_notsymlink(s):
    if supports_symlink: return s
    return '\n'.join(line for line in s.split('\n') if '@' not in line)

  fs_sync__mktree(grep_notsymlink("""
    src/file                mode=0o646 mtime=1000 data=b'f1'
    src/emptydir/           mode=0o757 mtime=1002
    src/brokenlink@         target='brokenlinktarget'
    src/filelink@           target='file'
    src/emptydirlink@       target='emptydir'
    src/dirlink@            target='dir'
    src/outdirlink@         target='../src2'
    src/infinitelink@       target='dir/infinitelink'
    src/dir/                mode=0o757 mtime=2000
    src/dir/file2           mode=0o646 mtime=1004 data=b'f2'
    src/dir/emptydir2/      mode=0o757 mtime=1006
    src/dir/brokenlink2@    target='brokenlink2target'
    src/dir/filelink2@      target='file2'
    src/dir/emptydirlink2@  target='emptydir2'
    src/dir/parfilelink@    target='../file'
    src/dir/looplink@       target='../dir'
    src/dir/infinitelink2@  target='../infinitelink'
  """))
  tree_report = fs_sync__reporttree("src", "dst", data=1)
  if fs_sync__use_rsync: print("  unhandled test for rsync"); return
  else: fs_sync.move("src/dir", "dst/dir", links=1)
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1)), grep_notsymlink(f"""
    -src/dir/
    -src/dir/brokenlink2@ target='brokenlink2target'
    -src/dir/emptydir2/
    -src/dir/emptydirlink2@ target='emptydir2'
    -src/dir/file2 data=b'f2'
    -src/dir/filelink2@ target='file2'
    -src/dir/infinitelink2@ target='../infinitelink'
    -src/dir/looplink@ target='../dir'
    -src/dir/parfilelink@ target='../file'
    +dst/dir/
    +dst/dir/brokenlink2@ target='brokenlink2target'
    +dst/dir/emptydir2/
    +dst/dir/emptydirlink2@ target='emptydir2'
    +dst/dir/file2 data=b'f2'
    +dst/dir/filelink2@ target='file2'
    +dst/dir/infinitelink2@ target='../infinitelink'
    +dst/dir/looplink@ target='../dir'
    +dst/dir/parfilelink@ target='../file'
  """))
  fs_sync.move("src", "dst", source_directory=1, target_directory=1, recursive=1, links=1)
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1)), grep_notsymlink(f"""
    -src/brokenlink@ target='brokenlinktarget'
    -src/dir/
    -src/dir/brokenlink2@ target='brokenlink2target'
    -src/dir/emptydir2/
    -src/dir/emptydirlink2@ target='emptydir2'
    -src/dir/file2 data=b'f2'
    -src/dir/filelink2@ target='file2'
    -src/dir/infinitelink2@ target='../infinitelink'
    -src/dir/looplink@ target='../dir'
    -src/dir/parfilelink@ target='../file'
    -src/dirlink@ target='dir'
    -src/emptydir/
    -src/emptydirlink@ target='emptydir'
    -src/file data=b'f1'
    -src/filelink@ target='file'
    -src/infinitelink@ target='dir/infinitelink'
    -src/outdirlink@ target='../src2'
    +dst/brokenlink@ target='brokenlinktarget'
    +dst/dir/
    +dst/dir/brokenlink2@ target='brokenlink2target'
    +dst/dir/emptydir2/
    +dst/dir/emptydirlink2@ target='emptydir2'
    +dst/dir/file2 data=b'f2'
    +dst/dir/filelink2@ target='file2'
    +dst/dir/infinitelink2@ target='../infinitelink'
    +dst/dir/looplink@ target='../dir'
    +dst/dir/parfilelink@ target='../file'
    +dst/dirlink@ target='dir'
    +dst/emptydir/
    +dst/emptydirlink@ target='emptydir'
    +dst/file data=b'f1'
    +dst/filelink@ target='file'
    +dst/infinitelink@ target='dir/infinitelink'
    +dst/outdirlink@ target='../src2'
  """))

@fs_sync__tester
def test_fs_sync__rsync_copystat():
  if os.name == "nt": print("can't check it on windows"); return
  fs_sync__mktree("""
    src/file                mode=0o646 mtime=3000 data='a'
    dst/file                mode=0o666 mtime=3000 data='b'
  """)
  tree_report = fs_sync__reporttree("src", "dst", data=1, mode=1, mtime=1)

  if fs_sync__use_rsync: os.system("rsync src/* dst/ --archive -vv")
  else: fs_sync("src", "dst", source_directory=True, archive=True)

  if os.name == "nt": dir_mode, file_mode = '0o777', '0o666'
  else: dir_mode, file_mode = '0o757', '0o646'
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1, mode=1, mtime=1)), f"""
    -dst/file mode=0o666 mtime=3000 data=b'b'
    +dst/file mode={file_mode} mtime=3000 data=b'b'
  """)


@fs_sync__tester
def XXXtest_fs_sync__rsync_XXX():
  fs_sync__mktree("""
    #dst/bak/                mode=0o757 mtime=3000
    #dst/file                mode=0o646 mtime=1000 data=b'f1'
    #dst/emptydir/           mode=0o757 mtime=1002
    #dst/brokenlink@         target='brokenlinktarget'
    #dst/filelink@           target='file'
    #dst/emptydirlink@       target='emptydir'
    #dst/dirlink@            target='dir'
    #dst/outdirlink@         target='../src2'
    #dst/infinitelink@       target='dir/infinitelink'
    #dst/dir/                mode=0o757 mtime=2000
    #dst/dir/file2           mode=0o646 mtime=1004 data=b'f2'
    #dst/dir/emptydir2/      mode=0o757 mtime=1006
    #dst/dir/brokenlink2@    target='brokenlink2target'
    #dst/dir/filelink2@      target='file2'
    #dst/dir/emptydirlink2@  target='emptydir2'
    #dst/dir/parfilelink@    target='../file'
    #dst/dir/looplink@       target='../dir'  # rsync has no looplink protection (keeps system behavior)
    #dst/dir/infinitelink2@  target='../infinitelink'

    #src/dirtoreg/           mode=0o757 mtime=2002
    #src/dirtoreg/gnark      mode=0o757 mtime=1008
    #src/regtodir            mode=0o646 mtime=1010 data=b'f3'
    #dst/dirtoreg            mode=0o666 mtime=11008 data=b'nf3'
    #dst/regtodir/           mode=0o777 mtime=12002
    #dst/regtodir/gnark2     mode=0o777 mtime=11010

    #src/backuptest1         mode=0o646 mtime=202 data="a"
    #dst/backuptest1         mode=0o646 mtime=204 data="bc"
    #dst/backuptest1~/       mode=0o757 mtime=206
    #dst/backuptest1~/gnark  mode=0o646 mtime=200

    #src/samereg             mode=0o646 mtime=210 data="same"
    #dst/samereg             mode=0o646 mtime=210 data="same"

    src/ignore_existing@         target='lol'
    dst/ignore_existing/         mode=0o757 mtime=210
    dst/ignore_existing/gnark    mode=0o646 mtime=210 data='b'
    src/ignore_existing2/        mode=0o757 mtime=210
    src/ignore_existing2/gnark   mode=0o646 mtime=210 data='a'
    dst/ignore_existing2@        target='lol'
  """)
  tree_report = fs_sync__reporttree("src", "dst", data=1, mode=1, mtime=1)

  if fs_sync__use_rsync: os.system("rsync src/ dst/ --archive --delete -vv")
  #if fs_sync__use_rsync: os.system("rsync src/* dst/ --recursive --links --ignore-existing -vv")
  #if fs_sync__use_rsync: os.system("rsync src/ dst/ --dirs --delete --backup-dir=bak -vv")
  #if fs_sync__use_rsync: os.system("rsync src/ dst/ --dirs --delete --backup -vv")
  #if fs_sync__use_rsync: os.system("rsync src/ dst/ --archive --ignore-non-existing --remove-source-files -vv")
  #if fs_sync__use_rsync: os.system("rsync src/ dst/ --archive --force -vv")
  else: fs_sync("src", "dst", source_directory=True, archive=True, delete=True, verbose=1)
  #else: fs_sync("src", "dst", source_directory=True, archive=True, verbose=1)

  if os.name == "nt": dir_mode, file_mode = '0o777', '0o666'
  else: dir_mode, file_mode = '0o757', '0o646'
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1, mode=1, mtime=1)), f"""
  """)


@fs_sync__tester
def test_fs_sync__1_first_sync_archive(**K):
  K.setdefault("archive", True)
  lstat = fs_sync__soft_lstat
  fs_sync__mktree("""
    src/a/                mode=0o777 mtime=99999
    src/a/b/              mode=0o777 mtime=9999
    src/a/b/c/            mode=0o777 mtime=999
    src/a/d               mode=0o666 mtime=10000
    src/a/b/e             mode=0o666 mtime=1000
    src/a/b/c/f           mode=0o666 mtime=100
  """)
  tree_report = fs_sync__reporttree('src', 'dst', data=1, mode=1, mtime=1)
  #tar_xf(io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data), directory="src")
  def assert_path_does_not_start_with_slash(_, path, *a): assert_notequal(path[:1].replace("\\", "/"), "/")
  fs_sync("src", "dst", verbose=3, onverbose=assert_path_does_not_start_with_slash, **K)
  if K.get("target_directory"):
    fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree('src', 'dst/src', data=1, mode=1, mtime=1)), '''
      +dst/src/a/ mode=0o777 mtime=99999
      +dst/src/a/b/ mode=0o777 mtime=9999
      +dst/src/a/b/c/ mode=0o777 mtime=999
      +dst/src/a/b/c/f mode=0o666 mtime=100 data=b''
      +dst/src/a/b/e mode=0o666 mtime=1000 data=b''
      +dst/src/a/d mode=0o666 mtime=10000 data=b''
    ''')
    #assert_equal(lstat("src/a"      ), lstat("dst/src/a"      ))
    #assert_equal(lstat("src/a/b"    ), lstat("dst/src/a/b"    ))
    #assert_equal(lstat("src/a/b/c"  ), lstat("dst/src/a/b/c"  ))
    #assert_equal(lstat("src/a/b/c/f"), lstat("dst/src/a/b/c/f"))
    #assert_equal(lstat("src/a/b/e"  ), lstat("dst/src/a/b/e"  ))
    #assert_equal(lstat("src/a/d"    ), lstat("dst/src/a/d"    ))
  else:
    fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree('src', 'dst', data=1, mode=1, mtime=1)), '''
      +dst/a/ mode=0o777 mtime=99999
      +dst/a/b/ mode=0o777 mtime=9999
      +dst/a/b/c/ mode=0o777 mtime=999
      +dst/a/b/c/f mode=0o666 mtime=100 data=b''
      +dst/a/b/e mode=0o666 mtime=1000 data=b''
      +dst/a/d mode=0o666 mtime=10000 data=b''
    ''')
    #assert_equal(lstat("src/a"      ), lstat("dst/a"      ))
    #assert_equal(lstat("src/a/b"    ), lstat("dst/a/b"    ))
    #assert_equal(lstat("src/a/b/c"  ), lstat("dst/a/b/c"  ))
    #assert_equal(lstat("src/a/b/c/f"), lstat("dst/a/b/c/f"))
    #assert_equal(lstat("src/a/b/e"  ), lstat("dst/a/b/e"  ))
    #assert_equal(lstat("src/a/d"    ), lstat("dst/a/d"    ))
  if K.get("backup_dir"):
    assert_equal(lstat("bak/a"  ), None)
    assert_equal(lstat("bak/src"), None)
    assert_equal(lstat("bak/dst"), None)
  # XXX please check why folders are updated again when running mirror for the second time!
  fs_sync("src", "dst", verbose=1, onverbose=lambda *a: throw(AssertionError(sprint(*a, sep=": "))), **K)  # XXX it's seems to be a random error !!
def test_fs_sync__1_first_sync_archive_backup_dir(**K):
  K.setdefault("backup_dir", "bak")
  return test_fs_sync__1_first_sync_archive(**K)
def test_fs_sync__1_first_sync_archive_backup_dir_source_directory(**K):
  K.setdefault("source_directory", True)
  return test_fs_sync__1_first_sync_archive_backup_dir(**K)
def test_fs_sync__1_first_sync_archive_backup_dir_target_directory(**K):
  K.setdefault("target_directory", True)
  return test_fs_sync__1_first_sync_archive_backup_dir(**K)

@fs_sync__tester
def test_fs_sync__2_update_file_sync_archive(**K):
  K.setdefault("archive", True)
  lstat = fs_sync__soft_lstat
  with open("src/a", "w") as f: f.write("hello")
  orig_src_a_stat = lstat("src/a")
  fs_sync("src", "dst", **K)  # first sync
  with open("src/a", "w") as f: f.write("world!")
  fs_sync("src", "dst", **K)
  if K.get("target_directory"):
    assert_equal(lstat("src/a"), lstat("dst/src/a"))
  else:
    assert_equal(lstat("src/a"), lstat("dst/a"))
  if K.get("backup_dir"):
    if K.get("source_directory"):
      assert_equal(lstat("bak/a"), orig_src_a_stat)
    elif K.get("target_directory"):
      assert_equal(lstat("bak/src/a"), orig_src_a_stat)
    else:
      assert_notequal(lstat("bak/dst"), None)
      assert_equal(lstat("bak/dst/a"), orig_src_a_stat)
  # XXX please check why folders are updated again when running mirror for the second time!
  fs_sync("src", "dst", verbose=1, onverbose=lambda *a: throw(AssertionError(sprint(*a, sep=": "))), **K)  # XXX it's seems to be a random error !!
def test_fs_sync__2_update_file_sync_archive_backup_dir(**K):
  K.setdefault("backup_dir", "bak")
  return test_fs_sync__2_update_file_sync_archive(**K)
def test_fs_sync__2_update_file_sync_archive_backup_dir_source_directory(**K):
  K.setdefault("source_directory", True)
  return test_fs_sync__2_update_file_sync_archive_backup_dir(**K)
def test_fs_sync__2_update_file_sync_archive_backup_dir_target_directory(**K):
  K.setdefault("target_directory", True)
  return test_fs_sync__2_update_file_sync_archive_backup_dir(**K)

@fs_sync__tester
def test_fs_sync__3_delete_file_sync_archive(**K):
  K.setdefault("archive", True)
  lstat = fs_sync__soft_lstat
  with open("src/a", "w") as f: f.write("hello")
  orig_src_a_stat = lstat("src/a")
  fs_sync("src", "dst", **K)  # first sync
  os.unlink("src/a")
  fs_sync("src", "dst", **K)
  if K.get("target_directory"):
    if K.get("delete"):    assert_equal(lstat("src/a"), lstat("dst/src/a"))
    else:               assert_notequal(lstat("src/a"), lstat("dst/src/a"))
  else:
    if K.get("delete"):    assert_equal(lstat("src/a"), lstat("dst/a"))
    else:               assert_notequal(lstat("src/a"), lstat("dst/a"))
  if K.get("backup_dir"):
    if K.get("delete"):
      if K.get("source_directory"):
        assert_equal(lstat("bak/a"), orig_src_a_stat)
      elif K.get("target_directory"):
        assert_equal(lstat("bak/src/a"), orig_src_a_stat)
      else:
        assert_notequal(lstat("bak/dst"), None)
        assert_equal(lstat("bak/dst/a"), orig_src_a_stat)
    else:
      assert_equal(lstat("bak/a"), None)
      assert_equal(lstat("bak/src"), None)
      assert_equal(lstat("bak/dst"), None)
  # XXX please check why folders are updated again when running mirror for the second time!
  fs_sync("src", "dst", verbose=1, onverbose=lambda *a: throw(AssertionError(sprint(*a, sep=": "))), **K)  # XXX it's seems to be a random error !!
def test_fs_sync__3_delete_file_sync_archive_backup_dir(**K):
  K.setdefault("backup_dir", "bak")
  return test_fs_sync__3_delete_file_sync_archive(**K)
def test_fs_sync__3_delete_file_sync_archive_backup_dir_source_directory(**K):
  K.setdefault("source_directory", True)
  return test_fs_sync__3_delete_file_sync_archive_backup_dir(**K)
def test_fs_sync__3_delete_file_sync_archive_backup_dir_target_directory(**K):
  K.setdefault("target_directory", True)
  return test_fs_sync__3_delete_file_sync_archive_backup_dir(**K)
def test_fs_sync__3_delete_file_sync_archive_backup_dir_delete(**K):
  K.setdefault("delete", True)
  return test_fs_sync__3_delete_file_sync_archive_backup_dir(**K)

@fs_sync__tester
def test_fs_sync__4_delete_folder_sync_archive(**K):
  K.setdefault("archive", True)
  lstat = fs_sync__soft_lstat
  os.mkdir("src/a")
  with open("src/a/b", "w") as f: f.write("hello")
  orig_src_a_stat = lstat("src/a")
  orig_src_ab_stat = lstat("src/a/b")
  fs_sync("src", "dst", **K)  # first sync
  shutil.rmtree("src/a")
  #if "backup_dir" in K and "delete" in K: time.sleep(1)  # to check mtime in backups
  fs_sync("src", "dst", **K)  # second sync
  if K.get("target_directory"):
    if K.get("delete"):    assert_equal(lstat("src/a"), lstat("dst/src/a"))
    else:
      assert_notequal(lstat("src/a"  ), lstat("dst/src/a"  ))
      assert_notequal(lstat("src/a/b"), lstat("dst/src/a/b"))
  else:
    if K.get("delete"):    assert_equal(lstat("src/a"), lstat("dst/a"))
    else:
      assert_notequal(lstat("src/a"  ), lstat("dst/a"  ))
      assert_notequal(lstat("src/a/b"), lstat("dst/a/b"))
  if K.get("backup_dir"):
    if K.get("delete"):
      if K.get("source_directory"):
        assert_equal(lstat("bak/a"  ), orig_src_a_stat )
        assert_equal(lstat("bak/a/b"), orig_src_ab_stat)
      elif K.get("target_directory"):
        assert_equal(lstat("bak/src/a/b"), orig_src_ab_stat)
      else:
        assert_notequal(lstat("bak/dst"), None)
        assert_notequal(lstat("bak/dst/a"  ), None)  # backup does not copy dir stats (same as rsync behavior)
        assert_equal(lstat("bak/dst/a/b"), orig_src_ab_stat)
    else:
      assert_equal(lstat("bak/a"), None)
      assert_equal(lstat("bak/src"), None)
      assert_equal(lstat("bak/dst"), None)
  # XXX please check why folders are updated again when running mirror for the second time!
  fs_sync("src", "dst", verbose=1, onverbose=lambda *a: throw(AssertionError(sprint(*a, sep=": "))), **K)  # XXX it's seems to be a random error !!
def test_fs_sync__4_delete_folder_sync_archive_backup_dir(**K):
  K.setdefault("backup_dir", "bak")
  return test_fs_sync__4_delete_folder_sync_archive(**K)
def test_fs_sync__4_delete_folder_sync_archive_backup_dir_source_directory(**K):
  K.setdefault("source_directory", True)
  return test_fs_sync__4_delete_folder_sync_archive_backup_dir(**K)
def test_fs_sync__4_delete_folder_sync_archive_backup_dir_target_directory(**K):
  K.setdefault("target_directory", True)
  return test_fs_sync__4_delete_folder_sync_archive_backup_dir(**K)
def test_fs_sync__4_delete_folder_sync_archive_backup_dir_delete(**K):
  K.setdefault("delete", True)
  return test_fs_sync__4_delete_folder_sync_archive_backup_dir(**K)

# XXX continue with
# new file where there was a folder before & merge
# replace file by folder & merge

@fs_sync__tester
def test_fs_sync__5_move_folder():
  fs_sync__mktree("""
    src/a/                mode=0o777 mtime=99999
    src/a/b/              mode=0o777 mtime=9999
    src/a/b/c/            mode=0o777 mtime=999
    src/a/d               mode=0o666 mtime=10000
    src/a/b/e             mode=0o666 mtime=1000
    src/a/b/c/f           mode=0o666 mtime=100
  """)
  #tar_xf(io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data), directory="src")
  inos = \
    os.lstat("src"        ).st_ino,\
    os.lstat("src/a"      ).st_ino,\
    os.lstat("src/a"      ).st_ino,\
    os.lstat("src/a/b"    ).st_ino,\
    os.lstat("src/a/b/c"  ).st_ino,\
    os.lstat("src/a/b/c/f").st_ino,\
    os.lstat("src/a/b/e"  ).st_ino,\
    os.lstat("src/a/d"    ).st_ino
  fs_sync.move("src", "lol")
  assert_equal(inos[0], os.lstat("lol"        ).st_ino)
  assert_equal(inos[1], os.lstat("lol/a"      ).st_ino)
  assert_equal(inos[2], os.lstat("lol/a"      ).st_ino)
  assert_equal(inos[3], os.lstat("lol/a/b"    ).st_ino)
  assert_equal(inos[4], os.lstat("lol/a/b/c"  ).st_ino)
  assert_equal(inos[5], os.lstat("lol/a/b/c/f").st_ino)
  assert_equal(inos[6], os.lstat("lol/a/b/e"  ).st_ino)
  assert_equal(inos[7], os.lstat("lol/a/d"    ).st_ino)

@fs_sync__tester
def test_fs_sync__6_file_matcher():
  lstat = fs_sync__soft_lstat
  fs_sync__mktree("""
    src/a/                mode=0o777 mtime=99999
    src/a/b/              mode=0o777 mtime=9999
    src/a/b/c/            mode=0o777 mtime=999
    src/a/d               mode=0o666 mtime=10000
    src/a/b/e             mode=0o666 mtime=1000
    src/a/b/c/f           mode=0o666 mtime=100
  """)
  #tar_xf(io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data), directory="src")
  calls = []
  def file_matcher_True(src, dst, src_stats, dst_stats):
    calls.append((src, dst, src_stats, dst_stats))
    return True
  def file_matcher_False(src, dst, src_stats, dst_stats):
    calls.append((src, dst, src_stats, dst_stats))
    return False
  def assert_something_was_copied(_, path, *a): assert_equal(path, None)
  copied = []
  def log_copied(_, path, *a): copied.append(path)
  fs_sync("src", "dst", archive=True, file_matcher=file_matcher_True)
  assert_equal(len(calls), 0)  # to avoid copying, please use something else like exclude
  fs_sync("./././src".replace("/", os.sep), "./././dst".replace("/", os.sep), archive=True, file_matcher=file_matcher_True, verbose=1, onverbose=assert_something_was_copied)
  assert_equal([_[0] for _ in calls], [_.replace("/", os.sep) for _ in ("./././src/a/b/c/f", "./././src/a/b/e", "./././src/a/d")])
  calls[:] = []
  fs_sync("./././src".replace("/", os.sep), "./././dst".replace("/", os.sep), archive=True, file_matcher=file_matcher_False, verbose=1, onverbose=log_copied)
  assert_equal(copied, [_.replace("/", os.sep) for _ in ('dst/a/b/c/f', 'dst/a/b/e', 'dst/a/d')])
  assert_equal([_[1] for _ in calls], [_.replace("/", os.sep) for _ in ("./././dst/a/b/c/f", "./././dst/a/b/e", "./././dst/a/d")])

@fs_sync__tester
def test_fs_sync__7_inplace_stress():
  lstat = fs_sync__soft_lstat
  fs_sync__mktree("""
    src/a/                mode=0o777 mtime=99999
    src/a/b/              mode=0o777 mtime=9999
    src/a/b/c/            mode=0o777 mtime=999
    src/a/d               mode=0o666 mtime=10000
    src/a/b/e             mode=0o666 mtime=1000
    src/a/b/c/f           mode=0o666 mtime=100
  """)
  #tar_xf(io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data), directory="src")
  fs_sync.mirror("src", "dst", inplace=True)
  os.utime("dst/a/b/c/f")
  fs_sync.mirror("src", "dst", inplace=False)
  def assert_verbose(_, path, *a): assert_equal(False, True, repr((_, path_, *a)))
  fs_sync.mirror("src", "dst", inplace=False, verbose=1, onverbose=assert_verbose)

@fs_sync__tester
def test_fs_sync__8_copy_function():
  lstat = fs_sync__soft_lstat
  fs_sync__mktree("""
    src/a/                mode=0o777 mtime=99999
    src/a/b/              mode=0o777 mtime=9999
    src/a/b/c/            mode=0o777 mtime=999
    src/a/d               mode=0o666 mtime=10000
    src/a/b/e             mode=0o666 mtime=1000
    src/a/b/c/f           mode=0o666 mtime=100
  """)
  #tar_xf(io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data), directory="src")
  fs_sync.mirror("src", "dst", copy_function=shutil.copyfileobj)
  assert_equal(lstat("src/a/b/c/f"), lstat("dst/a/b/c/f"))

@fs_sync__tester
def test_fs_sync__9_srcfile_dstfolder_1():
  fs_sync__mktree("""
    src/a                mode=0o646 mtime=1000 data=b'a'
    dst/a/               mode=0o757 mtime=1002             # cannot delete non-empty directory: a + could not make way for new regular file: a
    dst/a/b              mode=0o646 mtime=1004 data=b'bb'
  """)
  tree_report = fs_sync__reporttree("src", "dst", data=1)
  if fs_sync__use_rsync: os.system("rsync src/* dst/ -vv")
  else: assert_raise(OSError, lambda: fs_sync("src", "dst", source_directory=True, target_directory=True))
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1)), "")
  if fs_sync__use_rsync: os.system("rsync src/* dst/ --dirs -vv")
  else: assert_raise(OSError, lambda: fs_sync("src", "dst", source_directory=True, target_directory=True, dirs=True))
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1)), "")
  if fs_sync__use_rsync: os.system("rsync src/* dst/ --force -vv")
  else: fs_sync("src", "dst", source_directory=True, target_directory=True, force=True)
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1)), """
    -dst/a/
    -dst/a/b data=b'bb'
    +dst/a   data=b'a'
  """)

@fs_sync__tester
def test_fs_sync__9_srcfile_dstfolder_2():
  fs_sync__mktree("""
    src/a                mode=0o646 mtime=1000 data=b'a'
    dst/a/               mode=0o757 mtime=1002             # cannot delete non-empty directory: a + could not make way for new regular file: a
    dst/a/b              mode=0o646 mtime=1004 data=b'bb'
  """)
  tree_report = fs_sync__reporttree("src", "dst", data=1)
  if fs_sync__use_rsync: os.system("rsync src/* dst/ --delete --dirs -vv")
  else:
    assert_raise(ValueError, lambda: fs_sync("src", "dst", source_directory=True, target_directory=True, delete=True))
    fs_sync("src", "dst", source_directory=True, target_directory=True, delete=True, dirs=True)
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1)), """
    -dst/a/
    -dst/a/b data=b'bb'
    +dst/a   data=b'a'
  """)

@fs_sync__tester
def test_fs_sync__9_srcfile_dstemptyfolder():
  fs_sync__mktree("""
    src/a                mode=0o646 mtime=1000 data=b'a'
    dst/a/               mode=0o757 mtime=1002
  """)
  tree_report = fs_sync__reporttree("src", "dst", data=1)
  if fs_sync__use_rsync: os.system("rsync src/* dst/ -vv")
  else: fs_sync("src", "dst", source_directory=True, target_directory=True)
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1)), """
    -dst/a/
    +dst/a   data=b'a'
  """)

@fs_sync__tester
def test_fs_sync__9_srcabsent_dstfolder():
  fs_sync__mktree("""
    dst/a/               mode=0o757 mtime=1002
    dst/a/b              mode=0o646 mtime=1000 data=b'b'
  """)
  tree_report = fs_sync__reporttree("src", "dst", data=1)
  if fs_sync__use_rsync: os.system("rsync src/ dst/ --delete --dirs -vv")
  else: fs_sync("src", "dst", source_directory=True, target_directory=True, delete=True, dirs=True)
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1)), """
    -dst/a/
    -dst/a/b data=b'b'
    +
  """)

@fs_sync__tester
def test_fs_sync__10_srcfolder_dstfile_1():
  fs_sync__mktree("""
    src/a/               mode=0o757 mtime=1000
    src/a/b              mode=0o646 mtime=1002 data=b'bb'
    dst/a                mode=0o646 mtime=1004 data=b'a'
  """)
  tree_report = fs_sync__reporttree("src", "dst", data=1)
  if fs_sync__use_rsync: os.system("rsync src/* dst/ -vv")
  else: fs_sync("src", "dst", source_directory=True, target_directory=True)
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1)), "")
  if fs_sync__use_rsync: os.system("rsync src/* dst/ --dirs -vv")
  else: fs_sync("src", "dst", source_directory=True, target_directory=True, dirs=True)
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1)), """
    -dst/a data=b'a'
    +dst/a/
  """)

@fs_sync__tester
def test_fs_sync__10_srcfolder_dstfile_2():
  fs_sync__mktree("""
    src/a/               mode=0o757 mtime=1000
    src/a/b              mode=0o646 mtime=1002 data=b'bb'
    dst/a                mode=0o646 mtime=1004 data=b'a'
  """)
  tree_report = fs_sync__reporttree("src", "dst", data=1)
  if fs_sync__use_rsync: os.system("rsync src/ dst/ --recursive -vv")
  else: fs_sync("src", "dst", source_directory=True, target_directory=True, recursive=True)
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1)), """
    -dst/a data=b'a'
    +dst/a/
    +dst/a/b data=b'bb'
  """)

@fs_sync__tester
def test_fs_sync__11_backup_maze():
  fs_sync__mktree("""
    src/a                mode=0o646 mtime=1000 data=b'a'
    src/a~               mode=0o646 mtime=1002 data=b'aa'
    dst/a                mode=0o646 mtime=1004 data=b'aaa'
    dst/a~               mode=0o646 mtime=1006 data=b'aaaa'

    src/b~               mode=0o646 mtime=1000 data=b'b'
    src/b~~              mode=0o646 mtime=1002 data=b'bb'
    dst/b~               mode=0o646 mtime=1004 data=b'bbb'

    src/c~               mode=0o646 mtime=1000 data=b'c'
    dst/c~               mode=0o646 mtime=1002 data=b'cc'
    dst/c~~              mode=0o646 mtime=1004 data=b'ccc'

    dst/d~               mode=0o646 mtime=1006 data=b'dddd'
  """)
  tree_report = fs_sync__reporttree("src", "dst", data=1, mtime=1, mode=1)
  if fs_sync__use_rsync: os.system("rsync src/ dst/ --archive --delete --backup -v")
  else: fs_sync("src", "dst", source_directory=True, target_directory=True, archive=True, delete=True, backup=True)

  if os.name == "nt": dir_mode, file_mode = '0o777', '0o666'
  else: dir_mode, file_mode = '0o757', '0o646'
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst", data=1, mtime=1, mode=1)), f"""
    -dst/a mode={file_mode} mtime=1004 data=b'aaa'
    -dst/a~ mode={file_mode} mtime=1006 data=b'aaaa'
    -dst/b~ mode={file_mode} mtime=1004 data=b'bbb'
    -dst/c~ mode={file_mode} mtime=1002 data=b'cc'
    -dst/c~~ mode={file_mode} mtime=1004 data=b'ccc'
    +dst/a mode={file_mode} mtime=1000 data=b'a'
    +dst/a~ mode={file_mode} mtime=1002 data=b'aa'
    +dst/a~~ mode={file_mode} mtime=1004 data=b'aaa'
    +dst/b~ mode={file_mode} mtime=1000 data=b'b'
    +dst/b~~ mode={file_mode} mtime=1002 data=b'bb'
    +dst/b~~~ mode={file_mode} mtime=1004 data=b'bbb'
    +dst/c~ mode={file_mode} mtime=1000 data=b'c'
    +dst/c~~ mode={file_mode} mtime=1002 data=b'cc'
  """)


@fs_sync__tester
def test_fs_sync__as_func():
  # This api is useful
  # for instance in the case when wanting to have specific verbose name
  # or in the case you want to store func configuration.
  fs_sync__mktree("""
    src/nosync
    src/one/
    src/one/tosync/
    src/one/tosync/a
    dst/nodelete
    dst/two/
  """, file_mode=0o646, dir_mode=0o757, auto_mtime=True, auto_data=True)
  tree_report = fs_sync__reporttree("src", "dst")
  def assert_path_startswith(_, path, *a): assert path.startswith("two"), " ".join(str(v) for v in (_, path, *a))
  my_sync = fs_sync("src", "dst", archive=True, delete=True, verbose=2, onverbose=assert_path_startswith, as_func=True)
  my_sync("one/tosync", "two/tosync", "src", "dst")
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree("src", "dst")), f"""
    +dst/two/tosync/
    +dst/two/tosync/a
  """)



#@fs_sync__tester
#def test_fs_sync__x_remove_source_non_empy_folder():
#  fs_sync__mktree("""
#    src/a/                mode=0o777 mtime=99999
#    src/a/b/              mode=0o777 mtime=9999
#    src/a/b/c/            mode=0o777 mtime=999
#    src/a/d               mode=0o666 mtime=10000
#    src/a/b/e             mode=0o666 mtime=1000
#    src/a/b/c/f           mode=0o666 mtime=100
#  """)
#  #tar_xf(io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data), directory="src")
#  fs_sync("src", "dst", remove_source_dirs=True)  # XXX it currently raising, what's the expected behavior ?


@fs_sync__tester
def test_fs_sync__archive__delete__target_directory():
  fs_sync__mktree('''
    src/a                mode=0o646 mtime=1000 data=b'a'
    # dst/b below should not be removed!
    dst/b                mode=0o646 mtime=1002 data=b'b'
  ''')
  tree_report = fs_sync__reporttree('src', 'dst', data=1)
  if fs_sync__use_rsync: os.system('rsync src/a dst/ --archive --delete --vv')
  else: fs_sync('src/a', 'dst', target_directory=True, archive=True, delete=True)
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree('src', 'dst', data=1)), '''
    +dst/a data=b'a'
  ''')


@fs_sync__tester
def test_fs_sync__archive__delete__yield_all():
  try: os.symlink('lol', 'lal')
  except OSError: print('cannot test symlinks!'); supports_symlink = False
  else: supports_symlink = True; os.unlink('lal')
  def grep_notsymlink(s):
    if supports_symlink: return s
    return '\n'.join(line for line in s.split('\n') if '@' not in line)

  def assert_same(a, b):  # XXX assert_equal2?
    def san(sign, v): return sign + repr(v).replace('\n', '\n' + sign)
    f = True
    res = []
    for k, v in diff(a, b):
      if k == (0, 1): res.append(san(' ', v))
      elif k == (0,): res.append(san('-', v)); f = False
      else:           res.append(san('+', v)); f = False
    assert f, '\n' + '\n'.join(res)
  tmpfile_re = re.compile(r'^(.*[\\/])?(\.[^\\/.]+[^\\/]*\.)([^\\/.]+)$')
  def rename_for_test(path):  # XXX add parameter to fs_sync to control tmp file name, instead of using rename_for_test()
    _ = tmpfile_re.fullmatch(path)
    if _ is None: return path
    return _[1] + _[2] + 'TMP'
  def filter_event(ev):
    match ev:
      case ('os_call', 'utime', (path, (atime, mtime)), *kw):
        return ('os_call', 'utime', (rename_for_test(path), ('>1000000000' if atime > 1000000000 else atime, '>1000000000' if mtime > 1000000000 else mtime)), *kw)
      case ('os_call', call, (path, *a), *kw):
        return ('os_call', call, (rename_for_test(path), *a), *kw)
    return ev
  uid, gid = 0, 0  # XXX

  fs_sync__mktree(grep_notsymlink(f'''
    src/create_empty_folder/ mode=0o777 mtime=9999
    src/create_file mode=0o666 mtime=1000 data=b'a'
    src/create_symlink@ target=b'a'
    src/uptodate_empty_folder/ mode=0o777 mtime=9998

    dst/uptodate_empty_folder/ mode=0o777 mtime=9998
  '''))
  tree_report = fs_sync__reporttree('src', 'dst', data=1, mode=1, mtime=1)
  events = [filter_event(_) for _ in fs_sync('src', 'dst', archive=True, delete=True, yield_all=True)]
  fs_sync__assert_report(fs_sync__diff(tree_report, fs_sync__reporttree('src', 'dst', data=1, mode=1, mtime=1)), grep_notsymlink(f'''
    +dst/create_empty_folder/ mode=0o777 mtime=9999
    +dst/create_file mode=0o666 mtime=1000 data=b'a'
    +dst/create_symlink@ target='a'
  '''))
  assert_same(
    events,
    [
      # START checking folders src & dst
      ('node', 'src', 'dst', '', '', 'src', 'dst'),
      ('os_call', 'lstat', ('src',), {}),
      ('os_call', 'lstat', ('dst',), {}),
      ('skip', 'uptodate', 'dst'),
      ('os_call', 'listdir', ('src',), {}),
      ('os_call', 'listdir', ('dst',), {}),

        #   START checking folder ./create_empty_folder/
        ('node', f'src{os.sep}create_empty_folder', f'dst{os.sep}create_empty_folder', '', '', f'src{os.sep}create_empty_folder', f'dst{os.sep}create_empty_folder'),
        ('os_call', 'lstat', (f'src{os.sep}create_empty_folder',), {}),
        ('os_call', 'lstat', (f'dst{os.sep}create_empty_folder',), {}),
        ('sync', 'create', f'dst{os.sep}create_empty_folder'),
        ('os_call', 'mkdir', (f'dst{os.sep}create_empty_folder',), {}),
        ('os_call', 'listdir', (f'src{os.sep}create_empty_folder',), {}),
        #('os_call', 'listdir', (f'dst{os.sep}create_empty_folder',), {}),  # no need to list an freshly created dir
        ('os_call', 'chmod', (f'dst{os.sep}create_empty_folder', 0o777), {}),
        *(() if os.name == 'nt' else (('os_call', 'chown', (f'dst{os.sep}create_empty_folder', uid, gid), {'follow_symlinks': False}),)),
        ('os_call', 'utime', (f'dst{os.sep}create_empty_folder', ('>1000000000', 9999.0)), {}),
        ('after_sync', 'create', f'dst{os.sep}create_empty_folder'),
        #   END checking folder ./create_empty_folder/

        #   START checking file ./create_file
        ('node', f'src{os.sep}create_file', f'dst{os.sep}create_file', '', '', f'src{os.sep}create_file', f'dst{os.sep}create_file'),
        ('os_call', 'lstat', (f'src{os.sep}create_file',), {}),
        ('os_call', 'lstat', (f'dst{os.sep}create_file',), {}),
        ('sync', 'create', f'dst{os.sep}create_file'),
        #('os_call', 'open', (f'src{os.sep}create_file', 'rb'), {}),
        #('os_call', 'open', (f'dst{os.sep}.create_file.TMP', 'wb'), {}),
        #('os_call', 'read', (fd_src_a, 4096), {}),
        #('os_call', 'write', (fd_src_b, b'a'), {}),
        ('os_call', 'chmod', (f'dst{os.sep}.create_file.TMP', 0o666), {}),
        *(() if os.name == 'nt' else (('os_call', 'chown', (f'dst{os.sep}.create_file.TMP', uid, gid), {'follow_symlinks': False}),)),
        ('os_call', 'utime', (f'dst{os.sep}.create_file.TMP', ('>1000000000', 1000.0)), {}),
        ('os_call', 'replace', (f'dst{os.sep}.create_file.TMP', f'dst{os.sep}create_file'), {}),
        ('after_sync', 'create', f'dst{os.sep}create_file'),
        #   END checking file ./create_file

        #   START checking file ./create_symlink@
        *((
          ('node', f'src{os.sep}create_symlink', f'dst{os.sep}create_symlink', '', '', f'src{os.sep}create_symlink', f'dst{os.sep}create_symlink'),
          ('os_call', 'lstat', (f'src{os.sep}create_symlink',), {}),
          ('os_call', 'lstat', (f'dst{os.sep}create_symlink',), {}),
          ('sync', 'create', f'dst{os.sep}create_symlink'),
          ('os_call', 'readlink', (f'src{os.sep}create_symlink',), {}),
          ('os_call', 'symlink', ('a', f'dst{os.sep}create_symlink',), {}),
          ('after_sync', 'create', f'dst{os.sep}create_symlink'),
        ) if supports_symlink else ()),
        #   END checking file ./create_symlink@

        #   START checking folder ./uptodate_empty_folder/
        ('node', f'src{os.sep}uptodate_empty_folder', f'dst{os.sep}uptodate_empty_folder', '', '', f'src{os.sep}uptodate_empty_folder', f'dst{os.sep}uptodate_empty_folder'),
        ('os_call', 'lstat', (f'src{os.sep}uptodate_empty_folder',), {}),
        ('os_call', 'lstat', (f'dst{os.sep}uptodate_empty_folder',), {}),
        ('skip', 'uptodate', f'dst{os.sep}uptodate_empty_folder'),
        ('os_call', 'listdir', (f'src{os.sep}uptodate_empty_folder',), {}),
        ('os_call', 'listdir', (f'dst{os.sep}uptodate_empty_folder',), {}),
        #('os_call', 'chmod', (f'dst{os.sep}uptodate_empty_folder', 0o777), {}),  # same mode between {src,dst}/uptodate_empty_folder
        ('os_call', 'utime', (f'dst{os.sep}uptodate_empty_folder', ('>1000000000', 9998.0)), {}),
        ('after_skip', 'uptodate', f'dst{os.sep}uptodate_empty_folder'),
        #   END checking folder ./uptodate_empty_folder/

      #('os_call', 'chmod', ('dst', 0o777), {}),  # previous lstat(dst) knows that the dst mode does not need to be updated as it is already equal to src mode
      ('os_call', 'utime', ('dst', ('>1000000000', '>1000000000')), {}),
      ('after_skip', 'uptodate', 'dst'),
      # END checking folders src & dst
    ])
