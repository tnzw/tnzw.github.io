def fs_sync_stat_to_str(s, props=None):
  if props is None: props = ("mode","uid","gid","size","mtime")
  s = {k:getattr(s, "st_"+k) for k in props}
  s = {k:(oct(v) if k in ("mode",) else v) for k,v in s.items()}
  s = {k:(int(v) if k in ("mtime","atime","ctime") else v) for k,v in s.items()}
  return s
def fs_sync_soft_lstat(p, default=None, as_str=True, props=None):
  try: s = os.lstat(p)
  except FileNotFoundError: return default
  else: return fs_sync_stat_to_str(s, props=props) if as_str else s
def fs_sync_tester(fn):
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

@fs_sync_tester
def test_fs_sync_1_first_sync_archive(**K):
  K.setdefault("archive", True)
  lstat = fs_sync_soft_lstat
  tar_xf(io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data), directory="src")
  fs_sync("src", "dst", **K)
  if K.get("target_directory"):
    assert_equal(lstat("src/a"      ), lstat("dst/src/a"      ))
    assert_equal(lstat("src/a"      ), lstat("dst/src/a"      ))
    assert_equal(lstat("src/a/b"    ), lstat("dst/src/a/b"    ))
    assert_equal(lstat("src/a/b/c"  ), lstat("dst/src/a/b/c"  ))
    assert_equal(lstat("src/a/b/c/f"), lstat("dst/src/a/b/c/f"))
    assert_equal(lstat("src/a/b/e"  ), lstat("dst/src/a/b/e"  ))
    assert_equal(lstat("src/a/d"    ), lstat("dst/src/a/d"    ))
  else:
    assert_equal(lstat("src/a"      ), lstat("dst/a"      ))
    assert_equal(lstat("src/a"      ), lstat("dst/a"      ))
    assert_equal(lstat("src/a/b"    ), lstat("dst/a/b"    ))
    assert_equal(lstat("src/a/b/c"  ), lstat("dst/a/b/c"  ))
    assert_equal(lstat("src/a/b/c/f"), lstat("dst/a/b/c/f"))
    assert_equal(lstat("src/a/b/e"  ), lstat("dst/a/b/e"  ))
    assert_equal(lstat("src/a/d"    ), lstat("dst/a/d"    ))
  if K.get("backup_dir"):
    assert_equal(lstat("bak/a"  ), None)
    assert_equal(lstat("bak/src"), None)
    assert_equal(lstat("bak/dst"), None)
  # XXX please check why folders are updated again when running mirror for the second time!
  fs_sync("src", "dst", verbose=1, onverbose=lambda *a: throw(AssertionError(sprint(*a, sep=": "))), **K)  # XXX it's seems to be a random error !!
def test_fs_sync_1_first_sync_archive_backup_dir(**K):
  K.setdefault("backup_dir", "bak")
  return test_fs_sync_1_first_sync_archive(**K)
def test_fs_sync_1_first_sync_archive_backup_dir_source_directory(**K):
  K.setdefault("source_directory", True)
  return test_fs_sync_1_first_sync_archive_backup_dir(**K)
def test_fs_sync_1_first_sync_archive_backup_dir_target_directory(**K):
  K.setdefault("target_directory", True)
  return test_fs_sync_1_first_sync_archive_backup_dir(**K)

@fs_sync_tester
def test_fs_sync_2_update_file_sync_archive(**K):
  K.setdefault("archive", True)
  lstat = fs_sync_soft_lstat
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
def test_fs_sync_2_update_file_sync_archive_backup_dir(**K):
  K.setdefault("backup_dir", "bak")
  return test_fs_sync_2_update_file_sync_archive(**K)
def test_fs_sync_2_update_file_sync_archive_backup_dir_source_directory(**K):
  K.setdefault("source_directory", True)
  return test_fs_sync_2_update_file_sync_archive_backup_dir(**K)
def test_fs_sync_2_update_file_sync_archive_backup_dir_target_directory(**K):
  K.setdefault("target_directory", True)
  return test_fs_sync_2_update_file_sync_archive_backup_dir(**K)

@fs_sync_tester
def test_fs_sync_3_delete_file_sync_archive(**K):
  K.setdefault("archive", True)
  lstat = fs_sync_soft_lstat
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
def test_fs_sync_3_delete_file_sync_archive_backup_dir(**K):
  K.setdefault("backup_dir", "bak")
  return test_fs_sync_3_delete_file_sync_archive(**K)
def test_fs_sync_3_delete_file_sync_archive_backup_dir_source_directory(**K):
  K.setdefault("source_directory", True)
  return test_fs_sync_3_delete_file_sync_archive_backup_dir(**K)
def test_fs_sync_3_delete_file_sync_archive_backup_dir_target_directory(**K):
  K.setdefault("target_directory", True)
  return test_fs_sync_3_delete_file_sync_archive_backup_dir(**K)
def test_fs_sync_3_delete_file_sync_archive_backup_dir_delete(**K):
  K.setdefault("delete", True)
  return test_fs_sync_3_delete_file_sync_archive_backup_dir(**K)

@fs_sync_tester
def test_fs_sync_4_delete_folder_sync_archive(**K):
  K.setdefault("archive", True)
  lstat = fs_sync_soft_lstat
  os.mkdir("src/a")
  with open("src/a/b", "w") as f: f.write("hello")
  orig_src_a_stat = lstat("src/a")
  orig_src_ab_stat = lstat("src/a/b")
  fs_sync("src", "dst", **K)  # first sync
  shutil.rmtree("src/a")
  fs_sync("src", "dst", **K)
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
        assert_equal(lstat("bak/dst/a"  ), orig_src_a_stat )
        assert_equal(lstat("bak/dst/a/b"), orig_src_ab_stat)
    else:
      assert_equal(lstat("bak/a"), None)
      assert_equal(lstat("bak/src"), None)
      assert_equal(lstat("bak/dst"), None)
  # XXX please check why folders are updated again when running mirror for the second time!
  fs_sync("src", "dst", verbose=1, onverbose=lambda *a: throw(AssertionError(sprint(*a, sep=": "))), **K)  # XXX it's seems to be a random error !!
def test_fs_sync_4_delete_folder_sync_archive_backup_dir(**K):
  K.setdefault("backup_dir", "bak")
  return test_fs_sync_4_delete_folder_sync_archive(**K)
def test_fs_sync_4_delete_folder_sync_archive_backup_dir_source_directory(**K):
  K.setdefault("source_directory", True)
  return test_fs_sync_4_delete_folder_sync_archive_backup_dir(**K)
def test_fs_sync_4_delete_folder_sync_archive_backup_dir_target_directory(**K):
  K.setdefault("target_directory", True)
  return test_fs_sync_4_delete_folder_sync_archive_backup_dir(**K)
def test_fs_sync_4_delete_folder_sync_archive_backup_dir_delete(**K):
  K.setdefault("delete", True)
  return test_fs_sync_4_delete_folder_sync_archive_backup_dir(**K)

# XXX continue with
# new file where there was a folder before & merge
# replace file by folder & merge