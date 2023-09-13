def posixpath2__stress_paths():
  #for a in ('', '.', '..'):
  #  for b in ('', '/', '//', '///'):
  #    for c in ('', '.', '..', 'a', 'a.', 'a.b', 'a.b.', 'a.b.c'):
  #      for d in ('', '/', '//'):
  #        yield a + b + c + d
  return (
    '', '.', '..', '/', '//', '///',
    'a', './a', '../a', '/a', '//a', '///a',
    'a.', './a.', '../a.', '/a.', '//a.', '///a.',
    'a.b.', './a.b.', '../a.b.', '/a.b.', '//a.b.', '///a.b.',
    'a.b.c', './a.b.c', '../a.b.c', '/a.b.c', '//a.b.c', '///a.b.c',
    '.a', './.a', '../.a', '/.a', '//.a', '///.a',
    '.a.', './.a.', '../.a.', '/.a.', '//.a.', '///.a.',
    '.a.b.', './.a.b.', '../.a.b.', '/.a.b.', '//.a.b.', '///.a.b.',
    '.a.b.c', './.a.b.c', '../.a.b.c', '/.a.b.c', '//.a.b.c', '///.a.b.c',
    '.a.b.c//', './.a.b.c//', '../.a.b.c//', '/.a.b.c//', '//.a.b.c//', '///.a.b.c//',
    '..a', './..a', '/..a', # XXX
    '..a.b', './..a.b', '/..a.b', # XXX
  )

def posixpath2__compare_attribute(attr):
  assert_equal(getattr(posixpath, attr, None), getattr(posixpath2, attr, None))

def posixpath2__compare_method(attr, *a, _posixpath2=None):  # XXX rename ..._compare_func
  if _posixpath2 is None: _posixpath2 = posixpath2
  for _ in posixpath2__stress_paths():
    if attr in ('commonpath', 'commonprefix'): aa = [[_, *a]]
    else: aa = [_, *a]
    try: p = getattr(posixpath, attr)(*aa)
    except ValueError as e: assert_raise(ValueError, lambda: getattr(_posixpath2, attr)(*aa), info=('expected', e))
    else:
      p2 = getattr(_posixpath2, attr)(*aa)
      if attr in ('abspath', 'realpath'):
        p = p.replace('\\', '/')
        if p[:1] != '/': p = '/' + p
      assert_equal(type(p2), type(p), info=(attr, *aa))
      assert_equal(p2, p, info=(attr, *aa))

def posixpath2__compare_method2(attr):
  for _ in posixpath2__stress_paths():
    posixpath2__compare_method(attr, _)

def posixpath2__mk_fake_os_module():
  class module: pass
  export = module()
  for _ in ('close', 'fspath', 'fsync', 'lseek', 'lstat', 'mkdir', 'open', 'stat', 'symlink',
            'SEEK_CUR', 'SEEK_END', 'SEEK_SET',
            'O_CREAT', 'O_TRUNC', 'O_WRONLY'):
    setattr(export, _, getattr(os, _))
  export.getcwd = lambda: '/' + os.getcwd().replace('\\', '/')
  #export.getcwd = os.getcwd
  export.sep = '/'
  export.altsep = None
  export.curdir = '.'
  export.pardir = '..'
  export.path = posixpath2._mk_module(export, use_environ=False, get_user_home=lambda u: '/home/' + (u or 'test'))
  return export

def posixpath2__in_tmp_dir(fn):
  def test(*a,**k):
    tmpdir = tempfile.mkdtemp()
    pwd = os.getcwd()
    try:
      os.chdir(tmpdir)
      return fn(posixpath2__mk_fake_os_module(), *a, **k)
    finally:
      os.chdir(pwd)
      shutil.rmtree(tmpdir)
  return test

def test_posixpath2__curdir(): return posixpath2__compare_attribute('curdir')
def test_posixpath2__pardir(): return posixpath2__compare_attribute('pardir')
def test_posixpath2__sep(): return posixpath2__compare_attribute('sep')
def test_posixpath2__extsep(): return posixpath2__compare_attribute('extsep')
def test_posixpath2__pathsep(): return posixpath2__compare_attribute('pathsep')

def test_posixpath2__basename(): return posixpath2__compare_method('basename')
def test_posixpath2__dirname(): return posixpath2__compare_method('dirname')
def test_posixpath2__normpath(): return posixpath2__compare_method('normpath')
def test_posixpath2__isabs(): return posixpath2__compare_method('isabs')
def test_posixpath2__normcase(): return posixpath2__compare_method('normcase')
def test_posixpath2__normpath(): return posixpath2__compare_method('normpath')
def test_posixpath2__split(): return posixpath2__compare_method('split')
def test_posixpath2__splitdrive(): return posixpath2__compare_method('splitdrive')
def test_posixpath2__splitext(): return posixpath2__compare_method('splitext')

def test_posixpath2__commonpath(): return posixpath2__compare_method2('commonpath')
def test_posixpath2__commonprefix(): return posixpath2__compare_method2('commonprefix')
def test_posixpath2__join(): return posixpath2__compare_method2('join')
def test_posixpath2__relpath():
  if os.name == 'nt': print(r'/!\ cannot compare native `posixpath.relpath()` and `posixpath2.relpath()` on windows'); return  # because `posixpath.abspath('..')` has a strange behavior
  return posixpath2__compare_method2('relpath')

@posixpath2__in_tmp_dir
def test_posixpath2__abspath(fos):
  if os.name == 'nt': print(r'/!\ cannot compare native `posixpath.abspath()` and `posixpath2.abspath()` on windows'); return  # because `posixpath.abspath('..')` has a strange behavior
  return posixpath2__compare_method('abspath', _posixpath2=fos.path)

@posixpath2__in_tmp_dir
def test_posixpath2__realpath(fos):
  if os.name == 'nt': print(r'/!\ cannot compare native `posixpath.realpath()` and `posixpath2.realpath()` on windows'); return  # because `posixpath.realpath('..')` has a strange behavior
  return posixpath2__compare_method('realpath', _posixpath2=fos.path)

@posixpath2__in_tmp_dir
def test_posixpath2__expanduser(fos):
  assert_equal(fos.path.expanduser('~/dir'), '/home/test/dir')
  assert_equal(fos.path.expanduser('~yep/dir'), '/home/yep/dir')

@posixpath2__in_tmp_dir
def test_posixpath2__nodetests(fos):
  assert_equal(fos.path.exists('404'), False)
  assert_equal(fos.path.lexists('404'), False)
  assert_equal(fos.path.isdir('404'), False)
  assert_equal(fos.path.isfile('404'), False)
  assert_equal(fos.path.islink('404'), False)
  assert_raise(FileNotFoundError, lambda: fos.path.getsize('404'))
  fos.mkdir('dir')
  assert_equal(fos.path.exists('dir'), True)
  assert_equal(fos.path.lexists('dir'), True)
  assert_equal(fos.path.isdir('dir'), True)
  assert_equal(fos.path.isfile('dir'), False)
  assert_equal(fos.path.islink('dir'), False)
  fos.path.getsize('dir')
  with open2('reg', 'w', os_module=fos): pass
  assert_equal(fos.path.exists('reg'), True)
  assert_equal(fos.path.lexists('reg'), True)
  assert_equal(fos.path.isdir('reg'), False)
  assert_equal(fos.path.isfile('reg'), True)
  assert_equal(fos.path.islink('reg'), False)
  assert_equal(fos.path.getsize('reg'), 0)
  try: fos.symlink('dir', 'dirlink')
  except OSError: print(r'/!\ cannot test with symlinks'); return
  assert_equal(fos.path.exists('dirlink'), True)
  assert_equal(fos.path.lexists('dirlink'), True)
  assert_equal(fos.path.isdir('dirlink'), True)
  assert_equal(fos.path.isfile('dirlink'), False)
  assert_equal(fos.path.islink('dirlink'), True)
  fos.path.getsize('dirlink')
  fos.symlink('reg', 'reglink')
  assert_equal(fos.path.exists('reglink'), True)
  assert_equal(fos.path.lexists('reglink'), True)
  assert_equal(fos.path.isdir('reglink'), False)
  assert_equal(fos.path.isfile('reglink'), True)
  assert_equal(fos.path.islink('reglink'), True)
  assert_equal(fos.path.getsize('reglink'), 0)
  fos.symlink('404', '404link')
  assert_equal(fos.path.exists('404link'), False)
  assert_equal(fos.path.lexists('404link'), True)
  assert_equal(fos.path.isdir('404link'), False)
  assert_equal(fos.path.isfile('404link'), False)
  assert_equal(fos.path.islink('404link'), True)
  assert_raise(FileNotFoundError, lambda: fos.path.getsize('404link'))

def test_posixpath2__lowercase():
  path = posixpath2._mk_module(os, lowercase=True)
  assert_equal(path.commonpath(('HELLO/WORLD', 'hello/you')), 'HELLO')
  assert_equal(path.normcase('HELLO/WORLD'), 'hello/world')
