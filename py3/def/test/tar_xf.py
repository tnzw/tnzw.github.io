def test_tar_xf_1_a_ab_abc_abcf_abe_ad():
  tmpdir = tempfile.mkdtemp()
  try:
    f = io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data)
    tar_xf(f, directory=tmpdir)
  finally:
    shutil.rmtree(tmpdir)
def test_tar_xf_2_ab_abc_abcf_abe_ad():
  tmpdir = tempfile.mkdtemp()
  try:
    f = io.BytesIO(tar_a_ab_abc_abcf_abe_ad_data)
    f.seek(512, 0)
    tar_xf(f, directory=tmpdir)
  finally:
    shutil.rmtree(tmpdir)
