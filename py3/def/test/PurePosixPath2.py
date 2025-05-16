def PurePosixPath2__test():
  print('/!\\ All tests are disabled because I made PurePosixPath2 with the '
        'same behavior as PurePosixPath (last comparison python 3.11). DO '
        'NOT USE PurePosixPath2 IN YOUR CODE NOW PLEASE!')

r'''
def PurePosixPath2__stress_paths():
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

def PurePosixPath2__compare_attribute(attr):
  PPP, PPP2 = pathlib.PurePosixPath, PurePosixPath2
  for _ in PurePosixPath2__stress_paths():
    p = getattr(PPP(_), attr)
    p2 = getattr(PPP2(_), attr)
    #if attr == 'suffixes':  # suffixes types differs from list to tuple
    #  assert_equal(p2, tuple(p), info=_)
    if attr == 'parent':
      assert_equal(p2.parts, p.parts, info=(attr, _))
    elif attr == 'parents':
      p2 = [_.parts for _ in p2]
      p = [_.parts for _ in p]
      assert_equal(p2, p, info=(attr, _))
    else:
      assert_equal(type(p2), type(p), info=(attr, _))
      assert_equal(p2, p, info=(attr, _))

def PurePosixPath2__compare_method(attr, *a):
  PPP, PPP2 = pathlib.PurePosixPath, PurePosixPath2
  for _ in PurePosixPath2__stress_paths():
    try: p = getattr(PPP(_), attr)(*a)
    except ValueError: assert_raise(ValueError, lambda: getattr(PPP2(_), attr)(*a))
    else:
      p2 = getattr(PPP2(_), attr)(*a)
      if attr in ('joinpath', 'relative_to'): p, p2 = p.parts, p2.parts
      assert_equal(type(p2), type(p), info=(attr, _, *a))
      assert_equal(p2, p, info=(attr, _, *a))

def PurePosixPath2__compare_frompath_method(attr):
  for _ in PurePosixPath2__stress_paths():
    PurePosixPath2__compare_method(attr, _)

def test_PurePosixPath2__anchor(): return PurePosixPath2__compare_attribute('anchor')
def test_PurePosixPath2__drive(): return PurePosixPath2__compare_attribute('drive')
def test_PurePosixPath2__root(): return PurePosixPath2__compare_attribute('root')
def test_PurePosixPath2__parts(): return PurePosixPath2__compare_attribute('parts')
def test_PurePosixPath2__parent(): return PurePosixPath2__compare_attribute('parent')  # returned types differ, of course
def test_PurePosixPath2__parents(): return PurePosixPath2__compare_attribute('parents')  # returned types differ, of course
def test_PurePosixPath2__name(): return PurePosixPath2__compare_attribute('name')
def test_PurePosixPath2__stem(): return PurePosixPath2__compare_attribute('stem')
def test_PurePosixPath2__suffix(): return PurePosixPath2__compare_attribute('suffix')
def test_PurePosixPath2__suffixes(): return PurePosixPath2__compare_attribute('suffixes')  # returned types differ (tuple != list)

def test_PurePosixPath2__hash__(): return PurePosixPath2__compare_method('__hash__')
def test_PurePosixPath2__fspath__(): return PurePosixPath2__compare_method('__fspath__')
def test_PurePosixPath2__is_absolute(): return PurePosixPath2__compare_method('is_absolute')
def test_PurePosixPath2__is_reserved(): return PurePosixPath2__compare_method('is_reserved')
def test_PurePosixPath2__as_posix(): return PurePosixPath2__compare_method('as_posix')
def test_PurePosixPath2__as_uri(): return PurePosixPath2__compare_method('as_uri')

def test_PurePosixPath2__joinpath(): return PurePosixPath2__compare_frompath_method('joinpath')
def test_PurePosixPath2__relative_to(): return PurePosixPath2__compare_frompath_method('relative_to')
def test_PurePosixPath2__is_relative_to(): return PurePosixPath2__compare_frompath_method('is_relative_to')
#def test_PurePosixPath2__match(): XXX
#def test_PurePosixPath2__normalize(): XXX

def test_PurePosixPath2__from_parts():
  PPP, PPP2 = pathlib.PurePosixPath, PurePosixPath2
  if hasattr('_from_parts', PPP):
    assert_equal(PPP2(parts=('/', 'a')).parts, PPP._from_parts(('/', 'a')).parts)
    assert_equal(PPP2(parts=('', 'a')).parts, PPP._from_parts(('', 'a')).parts)
    assert_equal(PPP2(parts=('a',)).parts, PPP._from_parts(('a',)).parts)
    assert_equal(PPP2(parts=('a/a',)).parts, PPP._from_parts(('a/a',)).parts)
  else:
    print('/!\\ \'_from_parts\' now dropped!')
'''
