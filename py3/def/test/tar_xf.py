def test_tar_xf_1_a_ab_abc_abcf_abe_ad():
  tmpdir = tempfile.mkdtemp()
  try:
    f = io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data)
    tar_xf(f, directory=tmpdir)
    assert os.path.isdir(os.path.join(tmpdir, "a"))
    assert os.path.isdir(os.path.join(tmpdir, "a", "b"))
    assert os.path.isdir(os.path.join(tmpdir, "a", "b", "c"))
    assert os.path.isfile(os.path.join(tmpdir, "a", "d"))
    assert os.path.isfile(os.path.join(tmpdir, "a", "b", "e"))
    assert os.path.isfile(os.path.join(tmpdir, "a", "b", "c", "f"))
  finally:
    shutil.rmtree(tmpdir)
def test_tar_xf_2_ab_abc_abcf_abe_ad():
  tmpdir = tempfile.mkdtemp()
  try:
    f = io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data)
    f.seek(512, 0)
    tar_xf(f, directory=tmpdir)
    assert os.path.isdir(os.path.join(tmpdir, "a"))
    assert os.path.isdir(os.path.join(tmpdir, "a", "b"))
    assert os.path.isdir(os.path.join(tmpdir, "a", "b", "c"))
    assert os.path.isfile(os.path.join(tmpdir, "a", "d"))
    assert os.path.isfile(os.path.join(tmpdir, "a", "b", "e"))
    assert os.path.isfile(os.path.join(tmpdir, "a", "b", "c", "f"))
  finally:
    shutil.rmtree(tmpdir)
def test_tar_xf_3_long_filenames_with_long_links():
  tmpdir = tempfile.mkdtemp()
  try:
    f = io.BytesIO(tar_long_filenames_with_long_links_data)
    # summary:
    # long_link 123...
    # 123... DATA
    # long_link 123...
    # long_link abc...
    # abc... link to 123...
    # long_link abc...
    # long_link zxy...
    # zxy... -> abc...
    tar_xf(f, directory=tmpdir)
    assert os.path.isfile(os.path.join(tmpdir, "1234567890"*11))
    assert os.path.isfile(os.path.join(tmpdir, "abcdefghijklmnopqrstuvwxyz"*4))
    assert os.path.islink(os.path.join(tmpdir, "zyxwvutsrqponmlkjihgfedcba"*4))
    assert_equal(os.lstat(os.path.join(tmpdir, "1234567890"*11)).st_nlink, 2)
    assert_equal(os.lstat(os.path.join(tmpdir, "abcdefghijklmnopqrstuvwxyz"*4)).st_nlink, 2)
    assert_equal(os.readlink(os.path.join(tmpdir, "zyxwvutsrqponmlkjihgfedcba"*4)), "abcdefghijklmnopqrstuvwxyz"*4)
  finally:
    shutil.rmtree(tmpdir)
