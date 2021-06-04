def fs_sync__stat_to_str(s, props=None):
  if props is None: props = ("mode","uid","gid","size","mtime")
  s = {k:getattr(s, "st_"+k) for k in props}
  s = {k:(oct(v) if k in ("mode",) else v) for k,v in s.items()}
  s = {k:(int(v) if k in ("mtime","atime","ctime") else v) for k,v in s.items()}
  return s
def fs_sync__soft_lstat(p, default=None, as_str=True, props=None):
  try: s = os.lstat(p)
  except FileNotFoundError: return default
  else: return fs_sync__stat_to_str(s, props=props) if as_str else s
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

@fs_sync__tester
def test_fs_sync__1_first_sync_archive(**K):
  K.setdefault("archive", True)
  lstat = fs_sync__soft_lstat
  tar_xf(io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data), directory="src")
  def assert_path_does_not_start_with_slash(_, path, *a): assert_notequal(path[:1].replace("\\", "/"), "/")
  fs_sync("src", "dst", verbose=1, onverbose=assert_path_does_not_start_with_slash, **K)
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
  tar_xf(io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data), directory="src")
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
  tar_xf(io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data), directory="src")
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

#@fs_sync__tester
#def test_fs_sync__x_remove_source_non_empy_folder():
#  tar_xf(io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data), directory="src")
#  fs_sync("src", "dst", remove_source_dirs=True)  # XXX it currently raising, what's the expected behavior ?
