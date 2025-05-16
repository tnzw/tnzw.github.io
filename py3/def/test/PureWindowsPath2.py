def PureWindowsPath2__test():
  print('/!\\ All tests are disabled because I made PureWindowsPath2 with the '
        'same behavior as PureWindowsPath (last comparison python 3.11). DO '
        'NOT USE PureWindowsPath2 IN YOUR CODE NOW PLEASE!')

r'''
def PureWindowsPath2__stress_paths():
  #for a in ('', '.', '..', 'C:', '1:', '\\\\a\\b'):
  #  for b in ('', '\\', '\\\\', '\\\\\\'):
  #    for c in ('', '.', '..', 'a', 'a.', 'a.b', 'a.b.', 'a.b.c'):
  #      for d in ('', '\\', '\\\\'):
  #        yield a + b + c + d
  return (
    '', '.', '..', '\\', '\\\\', '\\\\\\',
    'a', '.\\a', '..\\a', '\\a', '\\\\a', '\\\\a\\', '\\\\a\\\\', '\\\\\\a',
    'a.', '.\\a.', '..\\a.', '\\a.', '\\\\a.', '\\\\\\a.',
    'a.b.', '.\\a.b.', '..\\a.b.', '\\a.b.', '\\\\a.b.', '\\\\\\a.b.',
    'a.b.c', '.\\a.b.c', '..\\a.b.c', '\\a.b.c', '\\\\a.b.c', '\\\\\\a.b.c',
    '.a', '.\\.a', '..\\.a', '\\.a', '\\\\.a', '\\\\\\.a',
    '.a.', '.\\.a.', '..\\.a.', '\\.a.', '\\\\.a.', '\\\\\\.a.',
    '.a.b.', '.\\.a.b.', '..\\.a.b.', '\\.a.b.', '\\\\.a.b.', '\\\\\\.a.b.',
    '.a.b.c', '.\\.a.b.c', '..\\.a.b.c', '\\.a.b.c', '\\\\.a.b.c', '\\\\\\.a.b.c',
    '.a.b.c\\\\', '.\\.a.b.c\\\\', '..\\.a.b.c\\\\', '\\.a.b.c\\\\', '\\\\.a.b.c\\\\', '\\\\\\.a.b.c\\\\',
    '..a', '.\\..a', '\\..a', # XXX
    '..a.b', '.\\..a.b', '\\..a.b', # XXX
  )

def PureWindowsPath2__compare_attribute(attr):
  PPP, PPP2 = pathlib.PureWindowsPath, PureWindowsPath2
  for _ in PureWindowsPath2__stress_paths():
    p = getattr(PPP(_), attr)
    p2 = getattr(PPP2(_), attr)
    if attr == 'parent':
      assert_equal(p2.parts, p.parts, info=(attr, _))
    elif attr == 'parents':
      p2 = [_.parts for _ in p2]
      p = [_.parts for _ in p]
      assert_equal(p2, p, info=(attr, _))
    else:
      assert_equal(type(p2), type(p), info=(attr, _))
      assert_equal(p2, p, info=(attr, _))

def PureWindowsPath2__compare_method(attr, *a):
  PPP, PPP2 = pathlib.PureWindowsPath, PureWindowsPath2
  for _ in PureWindowsPath2__stress_paths():
    try: ppp = PPP(_); p = getattr(ppp, attr)(*a)
    except ValueError:
      assert_raise(ValueError, lambda: getattr(PPP2(_), attr)(*a))
    else:
      ppp2 = PPP2(_); p2 = getattr(ppp2, attr)(*a)
      if attr in ('joinpath', 'relative_to'): p, p2 = p.parts, p2.parts
      assert_equal(type(p2), type(p), info=(attr, _, *a))
      if attr in ('__hash__', 'is_absolute'): p, p2 = (p, ppp.parts), (p2, ppp2.parts)
      assert_equal(p2, p, info=(attr, _, *a))

def PureWindowsPath2__compare_frompath_method(attr):
  for _ in PureWindowsPath2__stress_paths():
    PureWindowsPath2__compare_method(attr, _)

def test_PureWindowsPath2__anchor(): return PureWindowsPath2__compare_attribute('anchor')
def test_PureWindowsPath2__drive(): return PureWindowsPath2__compare_attribute('drive')
def test_PureWindowsPath2__root(): return PureWindowsPath2__compare_attribute('root')
def test_PureWindowsPath2__parts(): return PureWindowsPath2__compare_attribute('parts')
def test_PureWindowsPath2__parent(): return PureWindowsPath2__compare_attribute('parent')  # returned types differ, of course
def test_PureWindowsPath2__parents(): return PureWindowsPath2__compare_attribute('parents')  # returned types differ, of course
def test_PureWindowsPath2__name(): return PureWindowsPath2__compare_attribute('name')
def test_PureWindowsPath2__stem(): return PureWindowsPath2__compare_attribute('stem')
def test_PureWindowsPath2__suffix(): return PureWindowsPath2__compare_attribute('suffix')
def test_PureWindowsPath2__suffixes(): return PureWindowsPath2__compare_attribute('suffixes')

def test_PureWindowsPath2__hash__(): return PureWindowsPath2__compare_method('__hash__')
def test_PureWindowsPath2__fspath__(): return PureWindowsPath2__compare_method('__fspath__')
def test_PureWindowsPath2__is_absolute(): return PureWindowsPath2__compare_method('is_absolute')
def test_PureWindowsPath2__is_reserved(): return PureWindowsPath2__compare_method('is_reserved')
def test_PureWindowsPath2__as_posix(): return PureWindowsPath2__compare_method('as_posix')
def test_PureWindowsPath2__as_uri(): return PureWindowsPath2__compare_method('as_uri')

def test_PureWindowsPath2__joinpath(): return PureWindowsPath2__compare_frompath_method('joinpath')
def test_PureWindowsPath2__relative_to(): return PureWindowsPath2__compare_frompath_method('relative_to')
def test_PureWindowsPath2__is_relative_to(): return PureWindowsPath2__compare_frompath_method('is_relative_to')
#def test_PureWindowsPath2__match(): XXX
#def test_PureWindowsPath2__normalize(): XXX

def test_PureWindowsPath2__from_parts():
  PPP, PPP2 = pathlib.PureWindowsPath, PureWindowsPath2
  if hasattr('_from_parts', PPP):
    assert_equal(PPP2(parts=('C:\\', 'a')).parts, PPP._from_parts(('C:\\', 'a')).parts)
    assert_equal(PPP2(parts=('\\\\c\\d\\', 'a')).parts, PPP._from_parts(('\\\\c\\d\\', 'a')).parts)
    assert_equal(PPP2(parts=('\\', 'a')).parts, PPP._from_parts(('\\', 'a')).parts)
    assert_equal(PPP2(parts=('', 'a')).parts, PPP._from_parts(('', 'a')).parts)
    assert_equal(PPP2(parts=('a',)).parts, PPP._from_parts(('a',)).parts)
    assert_equal(PPP2(parts=('a\\a',)).parts, PPP._from_parts(('a\\a',)).parts)
  else:
    print('/!\\ \'_from_parts\' now dropped!')

def test_PureWindowsPath2__original_inconsistencies():
  PPP = pathlib.PureWindowsPath

  #assert_equal(PPP('\\\\.\\').__fspath__(), '\\\\.\\\\')  # wait what? (inconsistent @ python 3.11)
  #assert_equal(PPP('\\\\.\\').anchor, '\\\\.\\\\')  # hm… (inconsistent @ python 3.11)
  #assert_equal(PPP('\\\\.\\').root, '\\')  # hm… (inconsistent @ python 3.11)
  #assert_equal(PPP('\\\\.\\\\').__fspath__(), '\\')  # ok (python 3.11)
  #assert_equal(PPP('\\\\.\\\\').anchor, '\\')  # ok (python 3.11)
  assert_equal(PPP('\\\\.\\').__fspath__(), '\\\\.\\')  # now consistent
  assert_equal(PPP('\\\\.\\').anchor, '\\\\.\\')  # now consistent
  assert_equal(PPP('\\\\.\\').root, '')  # now consistent
  assert_equal(PPP('\\\\.\\\\').__fspath__(), '\\\\.\\\\')  # now consistent
  assert_equal(PPP('\\\\.\\\\').anchor, '\\\\.\\\\')  # now consistent
  assert_equal(PPP('\\\\.\\\\').root, '\\')  # consistent
'''
