def test_fs_mkdir_relative():
  tmpdir = tempfile.mkdtemp()
  pwd = os.getcwd()
  try:
    os.chdir(tmpdir)
    assert_equal(fs_mkdir("a"), None)
    assert_equal(fs_mkdir("a/b"), None)
    assert_equal(fs_mkdir("a/b/c"), None)
    assert os.path.isdir("a/b/c")
    assert_isinstance(fs_mkdir("a/b/c"), FileExistsError)
    assert_isinstance(fs_mkdir("a/b/c/d/e"), FileNotFoundError)
  finally:
    os.chdir(pwd)
    shutil.rmtree(tmpdir)
def test_fs_mkdir_absolute():
  tmpdir = tempfile.mkdtemp()
  try:
    assert_equal(fs_mkdir(os.path.join(tmpdir, "a")), None)
    assert_equal(fs_mkdir(os.path.join(tmpdir, "a/b")), None)
    assert_equal(fs_mkdir(os.path.join(tmpdir, "a/b/c")), None)
    assert os.path.isdir(os.path.join(tmpdir, "a/b/c"))
    assert_isinstance(fs_mkdir(os.path.join(tmpdir, "a/b/c")), FileExistsError)
    assert_isinstance(fs_mkdir(os.path.join(tmpdir, "a/b/c/d/e")), FileNotFoundError)
  finally:
    shutil.rmtree(tmpdir)
def test_fs_mkdir_relative_exist_ok():
  tmpdir = tempfile.mkdtemp()
  pwd = os.getcwd()
  try:
    os.chdir(tmpdir)
    assert_equal(fs_mkdir("a", exist_ok=True), None)
    assert_equal(fs_mkdir("a/b", exist_ok=True), None)
    assert_equal(fs_mkdir("a/b/c", exist_ok=True), None)
    assert os.path.isdir("a/b/c")
    assert_equal(fs_mkdir("a/b/c", exist_ok=True), None)
    assert_isinstance(fs_mkdir("a/b/c/d/e", exist_ok=True), FileNotFoundError)
  finally:
    os.chdir(pwd)
    shutil.rmtree(tmpdir)
def test_fs_mkdir_relative_parents():
  tmpdir = tempfile.mkdtemp()
  pwd = os.getcwd()
  try:
    os.chdir(tmpdir)
    assert_equal(fs_mkdir("a/b/c", parents=True), None)
    assert os.path.isdir("a/b/c")
    assert_isinstance(fs_mkdir("a/b/c", parents=True), FileExistsError)
    assert_isinstance(fs_mkdir("aa/bb/cc", parents=0), FileNotFoundError)
    assert_isinstance(fs_mkdir("aa/bb/cc", parents=-1), FileNotFoundError)
    assert_equal(fs_mkdir("aa/bb/cc", parents=-2), None)
    assert os.path.isdir("aa/bb/cc")
  finally:
    os.chdir(pwd)
    shutil.rmtree(tmpdir)
def test_fs_mkdir_absolute_parents():
  tmpdir = tempfile.mkdtemp()
  try:
    assert_equal(fs_mkdir(os.path.join(tmpdir, "a/b/c"), parents=True), None)
    assert os.path.isdir(os.path.join(tmpdir, "a/b/c"))
    assert_isinstance(fs_mkdir(os.path.join(tmpdir, "a/b/c"), parents=True), FileExistsError)
    assert_isinstance(fs_mkdir(os.path.join(tmpdir, "aa/bb/cc"), parents=0), FileNotFoundError)
    assert_isinstance(fs_mkdir(os.path.join(tmpdir, "aa/bb/cc"), parents=-1), FileNotFoundError)
    assert_equal(fs_mkdir(os.path.join(tmpdir, "aa/bb/cc"), parents=-2), None)
    assert os.path.isdir(os.path.join(tmpdir, "aa/bb/cc"))
  finally:
    shutil.rmtree(tmpdir)
def test_fs_mkdir_relative_parents_exist_ok():
  tmpdir = tempfile.mkdtemp()
  pwd = os.getcwd()
  try:
    os.chdir(tmpdir)
    assert_equal(fs_mkdir("a/b/c", parents=True, exist_ok=True), None)
    assert os.path.isdir("a/b/c")
    assert_equal(fs_mkdir("a/b/c", parents=True, exist_ok=True), None)
    assert_isinstance(fs_mkdir("aa/bb/cc", parents=0, exist_ok=True), FileNotFoundError)
    assert_isinstance(fs_mkdir("aa/bb/cc", parents=-1, exist_ok=True), FileNotFoundError)
    assert_equal(fs_mkdir("aa/bb/cc", parents=-2, exist_ok=True), None)
    assert os.path.isdir("aa/bb/cc")
  finally:
    os.chdir(pwd)
    shutil.rmtree(tmpdir)

# Other versions

#def test_fs_mkdir_relative():
#  tmpdir = tempfile.mkdtemp()
#  pwd = os.getcwd()
#  try:
#    os.chdir(tmpdir)
#    fs_mkdir("a")
#    fs_mkdir("a/b")
#    fs_mkdir("a/b/c")
#    assert os.path.isdir("a/b/c")
#    assert_raise(FileExistsError, lambda: fs_mkdir("a/b/c"))
#    assert_raise(FileNotFoundError, lambda: fs_mkdir("a/b/c/d/e"))
#  finally:
#    os.chdir(pwd)
#    shutil.rmtree(tmpdir)
#def test_fs_mkdir_relative_soft():
#  tmpdir = tempfile.mkdtemp()
#  pwd = os.getcwd()
#  try:
#    os.chdir(tmpdir)
#    assert_equal(fs_mkdir.soft("a"), None)
#    assert_equal(fs_mkdir.soft("a/b"), None)
#    assert_equal(fs_mkdir.soft("a/b/c"), None)
#    assert os.path.isdir("a/b/c")
#    assert_isinstance(fs_mkdir.soft("a/b/c"), FileExistsError)
#    assert_isinstance(fs_mkdir.soft("a/b/c/d/e"), FileNotFoundError)
#  finally:
#    os.chdir(pwd)
#    shutil.rmtree(tmpdir)
#def test_fs_mkdir_absolute():
#  tmpdir = tempfile.mkdtemp()
#  try:
#    fs_mkdir(os.path.join(tmpdir, "a"))
#    fs_mkdir(os.path.join(tmpdir, "a/b"))
#    fs_mkdir(os.path.join(tmpdir, "a/b/c"))
#    assert os.path.isdir(os.path.join(tmpdir, "a/b/c"))
#    assert_raise(FileExistsError, lambda: fs_mkdir(os.path.join(tmpdir, "a/b/c")))
#    assert_raise(FileNotFoundError, lambda: fs_mkdir(os.path.join(tmpdir, "a/b/c/d/e")))
#  finally:
#    shutil.rmtree(tmpdir)
#def test_fs_mkdir_relative_exist_ok():
#  tmpdir = tempfile.mkdtemp()
#  pwd = os.getcwd()
#  try:
#    os.chdir(tmpdir)
#    fs_mkdir("a", exist_ok=True)
#    fs_mkdir("a/b", exist_ok=True)
#    fs_mkdir("a/b/c", exist_ok=True)
#    assert os.path.isdir("a/b/c")
#    fs_mkdir("a/b/c", exist_ok=True)
#    assert_raise(FileNotFoundError, lambda: fs_mkdir("a/b/c/d/e", exist_ok=True))
#  finally:
#    os.chdir(pwd)
#    shutil.rmtree(tmpdir)
#def test_fs_mkdir_relative_parents():
#  tmpdir = tempfile.mkdtemp()
#  pwd = os.getcwd()
#  try:
#    os.chdir(tmpdir)
#    fs_mkdir("a/b/c", parents=True)
#    assert os.path.isdir("a/b/c")
#    assert_raise(FileExistsError, lambda: fs_mkdir("a/b/c", parents=True))
#    assert_raise(FileNotFoundError, lambda: fs_mkdir("aa/bb/cc", parents=0))
#    assert_raise(FileNotFoundError, lambda: fs_mkdir("aa/bb/cc", parents=-1))
#    fs_mkdir("aa/bb/cc", parents=-2)
#    assert os.path.isdir("aa/bb/cc")
#  finally:
#    os.chdir(pwd)
#    shutil.rmtree(tmpdir)
#def test_fs_mkdir_absolute_parents():
#  tmpdir = tempfile.mkdtemp()
#  try:
#    fs_mkdir(os.path.join(tmpdir, "a/b/c"), parents=True)
#    assert os.path.isdir(os.path.join(tmpdir, "a/b/c"))
#    assert_raise(FileExistsError, lambda: fs_mkdir(os.path.join(tmpdir, "a/b/c"), parents=True))
#    assert_raise(FileNotFoundError, lambda: fs_mkdir(os.path.join(tmpdir, "aa/bb/cc"), parents=0))
#    assert_raise(FileNotFoundError, lambda: fs_mkdir(os.path.join(tmpdir, "aa/bb/cc"), parents=-1))
#    fs_mkdir(os.path.join(tmpdir, "aa/bb/cc"), parents=-2)
#    assert os.path.isdir(os.path.join(tmpdir, "aa/bb/cc"))
#  finally:
#    shutil.rmtree(tmpdir)
#def test_fs_mkdir_relative_parents_exist_ok():
#  tmpdir = tempfile.mkdtemp()
#  pwd = os.getcwd()
#  try:
#    os.chdir(tmpdir)
#    fs_mkdir("a/b/c", parents=True, exist_ok=True)
#    assert os.path.isdir("a/b/c")
#    fs_mkdir("a/b/c", parents=True, exist_ok=True)
#    assert_raise(FileNotFoundError, lambda: fs_mkdir("aa/bb/cc", parents=0, exist_ok=True))
#    assert_raise(FileNotFoundError, lambda: fs_mkdir("aa/bb/cc", parents=-1, exist_ok=True))
#    fs_mkdir("aa/bb/cc", parents=-2, exist_ok=True)
#    assert os.path.isdir("aa/bb/cc")
#  finally:
#    os.chdir(pwd)
#    shutil.rmtree(tmpdir)
