def fs_synctree_assert_compare_file(a, b, not_equals=False, checks=("mode","uid","gid","size","mtime"), check_not_found=False):
  pp = (a, b)
  stats = {}
  for p in pp:
    stats[p] = None
    try:
      stats[p] = os.lstat(p)
      stats[p] = {k:getattr(stats[p], "st_"+k) for k in checks}
      for _ in ("mode",):
        if _ in stats[p]: stats[p][_] = oct(stats[p][_])
      for _ in ("mtime","atime","ctime"):
        if _ in stats[p]: stats[p][_] = int(stats[p][_])
    except FileNotFoundError: pass
  if check_not_found:
    none_found_message = []
    if stats[a] is None: none_found_message.append(repr(a))
    if stats[b] is None: none_found_message.append(repr(b))
    if none_found_message:
      assert stats[a] and stats[b], "FileNotFound: " + "&".join(none_found_message)
   
  if not_equals:
    assert_notequal(repr(stats[a]), repr(stats[b]))
  else:
    assert_equal(repr(stats[a]), repr(stats[b]))

def test_fs_synctree_1_merge_scenario(**K):
  K.setdefault("action", "merge")
  def onprogress_verbose(*a): print(": ".join(a))  # used for debugging
  tmpdir = tempfile.mkdtemp()
  pwd = os.getcwd()
  try:
    os.chdir(tmpdir)
    for _ in ("src", "dst", "bak"): os.mkdir(_)
    tar_xf(io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data), directory="src")

    assert_equal(fs_synctree("src", "dst", **K), None)                  # first merge !
    fs_synctree_assert_compare_file("src/a", "dst/a")                   # first merge !
    fs_synctree_assert_compare_file("src/a/b", "dst/a/b")               # first merge !
    fs_synctree_assert_compare_file("src/a/b/c", "dst/a/b/c")           # first merge !
    fs_synctree_assert_compare_file("src/a/b/c/f", "dst/a/b/c/f")       # first merge !
    fs_synctree_assert_compare_file("src/a/b/e", "dst/a/b/e")           # first merge !
    fs_synctree_assert_compare_file("src/a/d", "dst/a/d")               # first merge !
    if K.get("backup_directory"):  # merge & update                     # first merge !
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a"))        # first merge !
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b"))      # first merge !
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/c"))    # first merge !
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/c/f"))  # first merge !
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/e"))    # first merge !
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/d"))      # first merge !
      shutil.rmtree("bak")                                              # first merge !
      os.mkdir("bak")                                                   # first merge !

    with open("src/g", "wb") as f: f.write(b"hello")                       # new file & merge
    assert_equal(fs_synctree("src", "dst", **K), None)                     # new file & merge
    fs_synctree_assert_compare_file("src/g", "dst/g")                      # new file & merge
    fs_synctree_assert_compare_file("src/a", "dst/a")                      # new file & merge
    fs_synctree_assert_compare_file("src/a/b", "dst/a/b")                  # new file & merge
    fs_synctree_assert_compare_file("src/a/b/c", "dst/a/b/c")              # new file & merge
    fs_synctree_assert_compare_file("src/a/b/c/f", "dst/a/b/c/f")          # new file & merge
    fs_synctree_assert_compare_file("src/a/b/e", "dst/a/b/e")              # new file & merge
    fs_synctree_assert_compare_file("src/a/d", "dst/a/d")                  # new file & merge
    if K.get("backup_directory") and K.get("action", "merge") == "merge":  # new file & merge
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/g"))           # new file & merge
      os.lstat("bak/a")                                                    # new file & merge
      os.lstat("bak/a/b")                                                  # new file & merge
      os.lstat("bak/a/b/c")                                                # new file & merge
      os.lstat("bak/a/b/c/f")                                              # new file & merge
      os.lstat("bak/a/b/e")                                                # new file & merge
      os.lstat("bak/a/d")                                                  # new file & merge
      shutil.rmtree("bak")                                                 # new file & merge
      os.mkdir("bak")                                                      # new file & merge
    if K.get("backup_directory") and K.get("action", "merge") == "update":
      raise NotImplementedError

    with open("src/a/b/c/f", "wb") as f: f.write(b"world!")                # file update & merge
    assert_equal(fs_synctree("src", "dst", **K), None)                     # file update & merge
    fs_synctree_assert_compare_file("src/g", "dst/g")                      # file update & merge
    fs_synctree_assert_compare_file("src/a", "dst/a")                      # file update & merge
    fs_synctree_assert_compare_file("src/a/b", "dst/a/b")                  # file update & merge
    fs_synctree_assert_compare_file("src/a/b/c", "dst/a/b/c")              # file update & merge
    fs_synctree_assert_compare_file("src/a/b/c/f", "dst/a/b/c/f")          # file update & merge
    fs_synctree_assert_compare_file("src/a/b/e", "dst/a/b/e")              # file update & merge
    fs_synctree_assert_compare_file("src/a/d", "dst/a/d")                  # file update & merge
    if K.get("backup_directory") and K.get("action", "merge") == "merge":  # file update & merge
      os.lstat("bak/g")                                                    # file update & merge
      os.lstat("bak/a")                                                    # file update & merge
      os.lstat("bak/a/b")                                                  # file update & merge
      os.lstat("bak/a/b/c")                                                # file update & merge
      os.lstat("bak/a/b/c/f")                                              # file update & merge
      os.lstat("bak/a/b/e")                                                # file update & merge
      os.lstat("bak/a/d")                                                  # file update & merge
      shutil.rmtree("bak")                                                 # file update & merge
      os.mkdir("bak")                                                      # file update & merge
    if K.get("backup_directory") and K.get("action", "merge") == "update":
      raise NotImplementedError

    os.unlink("src/a/b/c/f")                                               # delete file & merge
    assert_equal(fs_synctree("src", "dst", **K), None)                     # delete file & merge
    fs_synctree_assert_compare_file("src/g", "dst/g")                      # delete file & merge
    fs_synctree_assert_compare_file("src/a", "dst/a")                      # delete file & merge
    fs_synctree_assert_compare_file("src/a/b", "dst/a/b")                  # delete file & merge
    fs_synctree_assert_compare_file("src/a/b/c", "dst/a/b/c")              # delete file & merge
    assert_raise(FileNotFoundError, lambda: os.lstat("src/a/b/c/f"))       # delete file & merge
    os.lstat("dst/a/b/c/f")                                                # delete file & merge
    fs_synctree_assert_compare_file("src/a/b/e", "dst/a/b/e")              # delete file & merge
    fs_synctree_assert_compare_file("src/a/d", "dst/a/d")                  # delete file & merge
    if K.get("backup_directory") and K.get("action", "merge") == "merge":  # delete file & merge
      os.lstat("bak/g")                                                    # delete file & merge
      os.lstat("bak/a")                                                    # delete file & merge
      os.lstat("bak/a/b")                                                  # delete file & merge
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/c"))       # delete file & merge
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/c/f"))     # delete file & merge
      os.lstat("bak/a/b/e")                                                # delete file & merge
      os.lstat("bak/a/d")                                                  # delete file & merge
      shutil.rmtree("bak")                                                 # delete file & merge
      os.mkdir("bak")                                                      # delete file & merge
    if K.get("backup_directory") and K.get("action", "merge") == "update":
      raise NotImplementedError

    shutil.rmtree("src/a/b")                                               # delete folder & merge
    assert_equal(fs_synctree("src", "dst", **K), None)                     # delete folder & merge
    fs_synctree_assert_compare_file("src/g", "dst/g")                      # delete folder & merge
    fs_synctree_assert_compare_file("src/a", "dst/a")                      # delete folder & merge
    assert_raise(FileNotFoundError, lambda: os.lstat("src/a/b"))           # delete folder & merge
    os.lstat("dst/a/b")                                                    # delete folder & merge
    os.lstat("dst/a/b/c")                                                  # delete folder & merge
    assert_raise(FileNotFoundError, lambda: os.lstat("src/a/b/c/f"))       # delete folder & merge
    os.lstat("dst/a/b/c/f")                                                # delete folder & merge
    os.lstat("dst/a/b/e")                                                  # delete folder & merge
    fs_synctree_assert_compare_file("src/a/d", "dst/a/d")                  # delete folder & merge
    if K.get("backup_directory") and K.get("action", "merge") == "merge":  # delete folder & merge
      os.lstat("bak/g")                                                    # delete folder & merge
      os.lstat("bak/a")                                                    # delete folder & merge
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b"))         # delete folder & merge
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/c"))       # delete folder & merge
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/c/f"))     # delete folder & merge
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/e"))       # delete folder & merge
      os.lstat("bak/a/d")                                                  # delete folder & merge
      shutil.rmtree("bak")                                                 # delete folder & merge
      os.mkdir("bak")                                                      # delete folder & merge
    if K.get("backup_directory") and K.get("action", "merge") == "update":
      raise NotImplementedError

    with open("src/a/b", "wb") as f: f.write(b"hey!")                      # new file where there was a folder before & merge
    err = fs_synctree("src", "dst", **K)                                   # new file where there was a folder before & merge
    # XXX if backup: the line below raises because dst/a/b is moves to bak, then src/a/b is copied and worked... this is a different behavior than in non-backup merge
    assert_isinstance(err, OSError)                                        # new file where there was a folder before & merge
    assert_equal(err.syscall, "open")  # non-generic attr                  # new file where there was a folder before & merge
    assert_equal(err.filename, "dst/a/b".replace("/", os.sep))             # new file where there was a folder before & merge
    fs_synctree_assert_compare_file("src/g", "dst/g")                      # new file where there was a folder before & merge
    fs_synctree_assert_compare_file("src/a", "dst/a")                      # new file where there was a folder before & merge
    os.lstat("src/a/b")                                                    # new file where there was a folder before & merge
    os.lstat("dst/a/b")                                                    # new file where there was a folder before & merge
    os.lstat("dst/a/b/c")                                                  # new file where there was a folder before & merge
    assert_raise(FileNotFoundError, lambda: os.lstat("src/a/b/c/f"))       # new file where there was a folder before & merge
    os.lstat("dst/a/b/c/f")                                                # new file where there was a folder before & merge
    os.lstat("dst/a/b/e")                                                  # new file where there was a folder before & merge
    fs_synctree_assert_compare_file("src/a/d", "dst/a/d")                  # new file where there was a folder before & merge
    # remove created file                                                  # new file where there was a folder before & merge
    os.unlink("src/a/b")                                                   # new file where there was a folder before & merge
    if K.get("backup_directory") and K.get("action", "merge") == "merge":  # new file where there was a folder before & merge
      raise NotImplementedError
      #os.lstat("bak/g")                                                    # new file where there was a folder before & merge
      #os.lstat("bak/a")                                                    # new file where there was a folder before & merge
      #assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b"))         # new file where there was a folder before & merge
      #assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/c"))       # new file where there was a folder before & merge
      #assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/c/f"))     # new file where there was a folder before & merge
      #assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/e"))       # new file where there was a folder before & merge
      #os.lstat("bak/a/d")                                                  # new file where there was a folder before & merge
      #shutil.rmtree("bak")                                                 # new file where there was a folder before & merge
      #os.mkdir("bak")                                                      # new file where there was a folder before & merge
      pass
    if K.get("backup_directory") and K.get("action", "merge") == "update":
      raise NotImplementedError

    os.unlink("src/a/d")                                                   # replace file by folder & merge
    os.mkdir("src/a/d")                                                    # replace file by folder & merge
    err = fs_synctree("src", "dst", **K)                                   # replace file by folder & merge
    assert_isinstance(err, OSError)                                        # replace file by folder & merge
    assert_equal(err.syscall, "mkdir")  # non-generic attr                 # replace file by folder & merge
    assert_equal(err.filename, "dst/a/d".replace("/", os.sep))             # replace file by folder & merge
    fs_synctree_assert_compare_file("src/g", "dst/g")                      # replace file by folder & merge
    fs_synctree_assert_compare_file("src/a", "dst/a")                      # replace file by folder & merge
    assert_raise(FileNotFoundError, lambda: os.lstat("src/a/b"))           # replace file by folder & merge
    os.lstat("dst/a/b")                                                    # replace file by folder & merge
    os.lstat("dst/a/b/c")                                                  # replace file by folder & merge
    assert_raise(FileNotFoundError, lambda: os.lstat("src/a/b/c/f"))       # replace file by folder & merge
    os.lstat("dst/a/b/c/f")                                                # replace file by folder & merge
    os.lstat("dst/a/b/e")                                                  # replace file by folder & merge
    os.path.isdir("src/a/d")                                               # replace file by folder & merge
    os.path.isfile("dst/a/d")                                              # replace file by folder & merge
    if K.get("backup_directory") and K.get("action", "merge") == "merge":  # replace file by folder & merge
      raise NotImplementedError
      #os.lstat("bak/g")                                                    # replace file by folder & merge
      #os.lstat("bak/a")                                                    # replace file by folder & merge
      #assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b"))         # replace file by folder & merge
      #assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/c"))       # replace file by folder & merge
      #assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/c/f"))     # replace file by folder & merge
      #assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/e"))       # replace file by folder & merge
      #os.lstat("bak/a/d")                                                  # replace file by folder & merge
      #shutil.rmtree("bak")                                                 # replace file by folder & merge
      #os.mkdir("bak")                                                      # replace file by folder & merge
      pass
    if K.get("backup_directory") and K.get("action", "merge") == "update":
      raise NotImplementedError

  finally:
    os.chdir(pwd)
    shutil.rmtree(tmpdir)

def test_fs_synctree_2_update_scenario():
  return test_fs_synctree_1_merge_scenario(action="update")

def test_fs_synctree_3_mirror_scenario(**K):
  K.setdefault("action", "mirror")
  tmpdir = tempfile.mkdtemp()
  pwd = os.getcwd()
  try:
    os.chdir(tmpdir)
    for _ in ("src", "dst", "bak"): os.mkdir(_)
    tar_xf(io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data), directory="src")

    assert_equal(fs_synctree("src", "dst", **K), None)                  # first mirror !
    fs_synctree_assert_compare_file("src/a", "dst/a")                   # first mirror !
    fs_synctree_assert_compare_file("src/a/b", "dst/a/b")               # first mirror !
    fs_synctree_assert_compare_file("src/a/b/c", "dst/a/b/c")           # first mirror !
    fs_synctree_assert_compare_file("src/a/b/c/f", "dst/a/b/c/f")       # first mirror !
    fs_synctree_assert_compare_file("src/a/b/e", "dst/a/b/e")           # first mirror !
    fs_synctree_assert_compare_file("src/a/d", "dst/a/d")               # first mirror !
    if K.get("backup_directory"):                                       # first mirror !
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a"))        # first mirror !
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b"))      # first mirror !
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/c"))    # first mirror !
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/c/f"))  # first mirror !
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/e"))    # first mirror !
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/d"))      # first mirror !
      shutil.rmtree("bak")                                              # first mirror !
      os.mkdir("bak")                                                   # first mirror !

    with open("src/g", "wb") as f: f.write(b"hello")                    # new file & mirror
    assert_equal(fs_synctree("src", "dst", **K), None)                  # new file & mirror
    fs_synctree_assert_compare_file("src/g", "dst/g")                   # new file & mirror
    fs_synctree_assert_compare_file("src/a", "dst/a")                   # new file & mirror
    fs_synctree_assert_compare_file("src/a/b", "dst/a/b")               # new file & mirror
    fs_synctree_assert_compare_file("src/a/b/c", "dst/a/b/c")           # new file & mirror
    fs_synctree_assert_compare_file("src/a/b/c/f", "dst/a/b/c/f")       # new file & mirror
    fs_synctree_assert_compare_file("src/a/b/e", "dst/a/b/e")           # new file & mirror
    fs_synctree_assert_compare_file("src/a/d", "dst/a/d")               # new file & mirror
    if K.get("backup_directory"):                                       # new file & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/g"))        # new file & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a"))        # new file & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b"))      # new file & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/c"))    # new file & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/c/f"))  # new file & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/e"))    # new file & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/d"))      # new file & mirror
      shutil.rmtree("bak")                                              # new file & mirror
      os.mkdir("bak")                                                   # new file & mirror

    with open("src/a/b/c/f", "wb") as f: f.write(b"world!")           # file update & mirror
    assert_equal(fs_synctree("src", "dst", **K), None)                # file update & mirror
    fs_synctree_assert_compare_file("src/g", "dst/g")                 # file update & mirror
    fs_synctree_assert_compare_file("src/a", "dst/a")                 # file update & mirror
    fs_synctree_assert_compare_file("src/a/b", "dst/a/b")             # file update & mirror
    fs_synctree_assert_compare_file("src/a/b/c", "dst/a/b/c")         # file update & mirror
    fs_synctree_assert_compare_file("src/a/b/c/f", "dst/a/b/c/f")     # file update & mirror
    fs_synctree_assert_compare_file("src/a/b/e", "dst/a/b/e")         # file update & mirror
    fs_synctree_assert_compare_file("src/a/d", "dst/a/d")             # file update & mirror
    if K.get("backup_directory"):                                     # file update & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/g"))      # file update & mirror
      os.lstat("bak/a")                                               # file update & mirror
      os.lstat("bak/a/b")                                             # file update & mirror
      os.lstat("bak/a/b/c")                                           # file update & mirror
      os.lstat("bak/a/b/c/f")                                         # file update & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/e"))  # file update & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/d"))    # file update & mirror
      shutil.rmtree("bak")                                            # file update & mirror
      os.mkdir("bak")                                                 # file update & mirror

    os.unlink("src/a/b/c/f")                                          # delete file & mirror
    assert_equal(fs_synctree("src", "dst", **K), None)                # delete file & mirror
    fs_synctree_assert_compare_file("src/g", "dst/g")                 # delete file & mirror
    fs_synctree_assert_compare_file("src/a", "dst/a")                 # delete file & mirror
    fs_synctree_assert_compare_file("src/a/b", "dst/a/b")             # delete file & mirror
    fs_synctree_assert_compare_file("src/a/b/c", "dst/a/b/c")         # delete file & mirror
    fs_synctree_assert_compare_file("src/a/b/c/f", "dst/a/b/c/f")     # delete file & mirror
    fs_synctree_assert_compare_file("src/a/b/e", "dst/a/b/e")         # delete file & mirror
    fs_synctree_assert_compare_file("src/a/d", "dst/a/d")             # delete file & mirror
    if K.get("backup_directory"):                                     # delete file & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/g"))      # delete file & mirror
      os.lstat("bak/a")                                               # delete file & mirror
      os.lstat("bak/a/b")                                             # delete file & mirror
      os.lstat("bak/a/b/c")                                           # delete file & mirror
      os.lstat("bak/a/b/c/f")                                         # delete file & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/e"))  # delete file & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/d"))    # delete file & mirror
      shutil.rmtree("bak")                                            # delete file & mirror
      os.mkdir("bak")                                                 # delete file & mirror

    shutil.rmtree("src/a/b")                                            # delete folder & mirror
    #if K.get("backup_directory"):
    #  import pdb
    #  pdb.set_trace()
    assert_equal(fs_synctree("src", "dst", **K), None)                  # delete folder & mirror
    fs_synctree_assert_compare_file("src/g", "dst/g")                   # delete folder & mirror
    fs_synctree_assert_compare_file("src/a", "dst/a")                   # delete folder & mirror
    fs_synctree_assert_compare_file("src/a/b", "dst/a/b")               # delete folder & mirror
    fs_synctree_assert_compare_file("src/a/b/c", "dst/a/b/c")           # delete folder & mirror
    fs_synctree_assert_compare_file("src/a/b/c/f", "dst/a/b/c/f")       # delete folder & mirror
    fs_synctree_assert_compare_file("src/a/b/e", "dst/a/b/e")           # delete folder & mirror
    fs_synctree_assert_compare_file("src/a/d", "dst/a/d")               # delete folder & mirror
    if K.get("backup_directory"):                                       # delete folder & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/g"))        # delete folder & mirror
      os.lstat("bak/a")                                                 # delete folder & mirror
      os.lstat("bak/a/b")                                               # delete folder & mirror
      os.lstat("bak/a/b/c")                                             # delete folder & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/c/f"))  # delete folder & mirror
      os.lstat("bak/a/b/e")                                             # delete folder & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/d"))      # delete folder & mirror
      shutil.rmtree("bak")                                              # delete folder & mirror
      os.mkdir("bak")                                                   # delete folder & mirror

    with open("src/a/b", "wb") as f: f.write(b"hey!")                   # new file where there was a folder before & mirror
    assert_equal(fs_synctree("src", "dst", **K), None)                  # new file where there was a folder before & mirror
    fs_synctree_assert_compare_file("src/g", "dst/g")                   # new file where there was a folder before & mirror
    fs_synctree_assert_compare_file("src/a", "dst/a")                   # new file where there was a folder before & mirror
    fs_synctree_assert_compare_file("src/a/b", "dst/a/b")               # new file where there was a folder before & mirror
    fs_synctree_assert_compare_file("src/a/b/c", "dst/a/b/c")           # new file where there was a folder before & mirror
    fs_synctree_assert_compare_file("src/a/b/c/f", "dst/a/b/c/f")       # new file where there was a folder before & mirror
    fs_synctree_assert_compare_file("src/a/b/e", "dst/a/b/e")           # new file where there was a folder before & mirror
    fs_synctree_assert_compare_file("src/a/d", "dst/a/d")               # new file where there was a folder before & mirror
    if K.get("backup_directory"):                                       # new file where there was a folder before & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/g"))        # new file where there was a folder before & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a"))        # new file where there was a folder before & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b"))      # new file where there was a folder before & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/c"))    # new file where there was a folder before & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/c/f"))  # new file where there was a folder before & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/e"))    # new file where there was a folder before & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/d"))      # new file where there was a folder before & mirror
      shutil.rmtree("bak")                                              # new file where there was a folder before & mirror
      os.mkdir("bak")                                                   # new file where there was a folder before & mirror

    os.unlink("src/a/d")                                                # replace file by folder & mirror
    os.mkdir("src/a/d")                                                 # replace file by folder & mirror
    assert_equal(fs_synctree("src", "dst", **K), None)                  # replace file by folder & mirror
    fs_synctree_assert_compare_file("src/g", "dst/g")                   # replace file by folder & mirror
    fs_synctree_assert_compare_file("src/a", "dst/a")                   # replace file by folder & mirror
    fs_synctree_assert_compare_file("src/a/b", "dst/a/b")               # replace file by folder & mirror
    fs_synctree_assert_compare_file("src/a/b/c", "dst/a/b/c")           # replace file by folder & mirror
    fs_synctree_assert_compare_file("src/a/b/c/f", "dst/a/b/c/f")       # replace file by folder & mirror
    fs_synctree_assert_compare_file("src/a/b/e", "dst/a/b/e")           # replace file by folder & mirror
    fs_synctree_assert_compare_file("src/a/d", "dst/a/d")               # replace file by folder & mirror
    if K.get("backup_directory"):                                       # replace file by folder & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/g"))        # replace file by folder & mirror
      os.lstat("bak/a")                                                 # replace file by folder & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b"))      # replace file by folder & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/c"))    # replace file by folder & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/c/f"))  # replace file by folder & mirror
      assert_raise(FileNotFoundError, lambda: os.lstat("bak/a/b/e"))    # replace file by folder & mirror
      os.lstat("bak/a/d")                                               # replace file by folder & mirror
      shutil.rmtree("bak")                                              # replace file by folder & mirror
      os.mkdir("bak")                                                   # replace file by folder & mirror
  finally:
    os.chdir(pwd)
    shutil.rmtree(tmpdir)

def test_fs_synctree_4_clean_scenario():
  tmpdir = tempfile.mkdtemp()
  pwd = os.getcwd()
  try:
    os.chdir(tmpdir)
    for _ in ("src", "dst"): os.mkdir(_)
    tar_xf(io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data), directory="src")

    # first merge !
    assert_equal(fs_synctree("src", "dst", action="merge"), None)
    fs_synctree_assert_compare_file("src/a", "dst/a")
    fs_synctree_assert_compare_file("src/a/b", "dst/a/b")
    fs_synctree_assert_compare_file("src/a/b/c", "dst/a/b/c")
    fs_synctree_assert_compare_file("src/a/b/c/f", "dst/a/b/c/f")
    fs_synctree_assert_compare_file("src/a/b/e", "dst/a/b/e")
    fs_synctree_assert_compare_file("src/a/d", "dst/a/d")

    # new file & clean
    with open("src/g", "wb") as f: f.write(b"hello")
    assert_equal(fs_synctree("src", "dst", action="clean"), None)
    os.lstat("src/g")
    assert_raise(FileNotFoundError, lambda: os.lstat("dst/g"))
    fs_synctree_assert_compare_file("src/a", "dst/a")
    fs_synctree_assert_compare_file("src/a/b", "dst/a/b")
    fs_synctree_assert_compare_file("src/a/b/c", "dst/a/b/c")
    fs_synctree_assert_compare_file("src/a/b/c/f", "dst/a/b/c/f")
    fs_synctree_assert_compare_file("src/a/b/e", "dst/a/b/e")
    fs_synctree_assert_compare_file("src/a/d", "dst/a/d")

    # file update & clean
    with open("src/a/b/c/f", "wb") as f: f.write(b"world!")
    assert_equal(fs_synctree("src", "dst", action="clean"), None)
    os.lstat("src/g")
    assert_raise(FileNotFoundError, lambda: os.lstat("dst/g"))
    fs_synctree_assert_compare_file("src/a", "dst/a")
    fs_synctree_assert_compare_file("src/a/b", "dst/a/b")
    fs_synctree_assert_compare_file("src/a/b/c", "dst/a/b/c")
    fs_synctree_assert_compare_file("src/a/b/c/f", "dst/a/b/c/f", not_equals=True)
    fs_synctree_assert_compare_file("src/a/b/e", "dst/a/b/e")
    fs_synctree_assert_compare_file("src/a/d", "dst/a/d")

    # delete file & clean
    os.unlink("src/a/b/c/f")
    assert_equal(fs_synctree("src", "dst", action="clean"), None)
    os.lstat("src/g")
    assert_raise(FileNotFoundError, lambda: os.lstat("dst/g"))
    fs_synctree_assert_compare_file("src/a", "dst/a")
    fs_synctree_assert_compare_file("src/a/b", "dst/a/b")
    fs_synctree_assert_compare_file("src/a/b/c", "dst/a/b/c")
    fs_synctree_assert_compare_file("src/a/b/c/f", "dst/a/b/c/f")
    fs_synctree_assert_compare_file("src/a/b/e", "dst/a/b/e")
    fs_synctree_assert_compare_file("src/a/d", "dst/a/d")

    # delete folder & clean
    shutil.rmtree("src/a/b")
    assert_equal(fs_synctree("src", "dst", action="clean"), None)
    os.lstat("src/g")
    assert_raise(FileNotFoundError, lambda: os.lstat("dst/g"))
    fs_synctree_assert_compare_file("src/a", "dst/a")
    fs_synctree_assert_compare_file("src/a/b", "dst/a/b")
    fs_synctree_assert_compare_file("src/a/b/c", "dst/a/b/c")
    fs_synctree_assert_compare_file("src/a/b/c/f", "dst/a/b/c/f")
    fs_synctree_assert_compare_file("src/a/b/e", "dst/a/b/e")
    fs_synctree_assert_compare_file("src/a/d", "dst/a/d")

    # new file where there was a folder before & clean
    with open("src/a/b", "wb") as f: f.write(b"hey!")
    assert_equal(fs_synctree("src", "dst", action="clean"), None)
    os.lstat("src/g")
    assert_raise(FileNotFoundError, lambda: os.lstat("dst/g"))
    fs_synctree_assert_compare_file("src/a", "dst/a")           
    os.lstat("src/a/b")
    assert_raise(FileNotFoundError, lambda: os.lstat("dst/a/b"))
    fs_synctree_assert_compare_file("src/a/b/c", "dst/a/b/c")
    fs_synctree_assert_compare_file("src/a/b/c/f", "dst/a/b/c/f")
    fs_synctree_assert_compare_file("src/a/b/e", "dst/a/b/e")
    fs_synctree_assert_compare_file("src/a/d", "dst/a/d")

    # replace file by folder & clean
    os.unlink("src/a/d")
    os.mkdir("src/a/d")
    assert_equal(fs_synctree("src", "dst", action="clean"), None)
    os.lstat("src/g")
    assert_raise(FileNotFoundError, lambda: os.lstat("dst/g"))
    fs_synctree_assert_compare_file("src/a", "dst/a")
    os.lstat("src/a/b")
    assert_raise(FileNotFoundError, lambda: os.lstat("dst/a/b"))
    fs_synctree_assert_compare_file("src/a/b/c", "dst/a/b/c")
    fs_synctree_assert_compare_file("src/a/b/c/f", "dst/a/b/c/f")
    fs_synctree_assert_compare_file("src/a/b/e", "dst/a/b/e")
    os.lstat("src/a/d")
    assert_raise(FileNotFoundError, lambda: os.lstat("dst/a/d"))
  finally:
    os.chdir(pwd)
    shutil.rmtree(tmpdir)

def test_fs_synctree_5_merge_backup_scenario(**K):
  K.setdefault("action", "merge")
  K.setdefault("backup_directory", "bak")
  return test_fs_synctree_1_merge_scenario(**K)

def test_fs_synctree_6_update_backup_scenario(**K):
  K.setdefault("action", "update")
  K.setdefault("backup_directory", "bak")
  return test_fs_synctree_1_merge_scenario(**K)

def test_fs_synctree_7_mirror_backup_scenario(**K):
  K.setdefault("action", "mirror")
  K.setdefault("backup_directory", "bak")
  return test_fs_synctree_3_mirror_scenario(**K)

# XXX test backup directory for clean !
# XXX test file comparison !
