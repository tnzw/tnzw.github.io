def test_parsertools__parsing_error():
  #for _ in dir(parsertools): locals()[_] = getattr(parsertools, _)
  ParsingError = parsertools.ParsingError
  assert_equal(ParsingError('', 'abc\ndef', pos=3).col, 3)
  assert_equal(ParsingError('', 'abc\ndef', pos=4).col, 0)
  assert_equal(ParsingError('', 'abc\ndef', pos=5).col, 1)
  assert_equal(ParsingError('', 'abc\ndef', pos=10).col, 3)

def test_parsertools__frozenmapping():
  #for _ in dir(parsertools): locals()[_] = getattr(parsertools, _)
  frozenmapping = parsertools.frozenmapping
  assert_equal(tuple(frozenmapping({'a': 'b'}).items()), (('a', 'b'),))
  assert_equal(tuple((frozenmapping({'a': 'b'}) | {'b': 'c'}).items()), (('a', 'b'), ('b', 'c')))
  assert_equal(tuple((frozenmapping({'a': 'b'}) | {'a': 'c'}).items()), (('a', 'c'),))
  assert_equal(tuple((frozenmapping({'a': 'b'}) | {2: 'c'}).items()), (('a', 'b'), (2, 'c')))
  #assert_raise(TypeError, lambda: frozenmapping((([], 'c'),)))  # XXX should raise
  assert_raise(TypeError, lambda:frozenmapping({'a': 'b'}) | (([], 'c'),))

def test_parsertools__params():
  #for _ in dir(parsertools): locals()[_] = getattr(parsertools, _)
  params = parsertools.params
  def pt(p): return p.args, p.kwargs
  assert_equal(pt(params(c='d')), ((), {'c': 'd'}))
  assert_equal(pt(params('a', 'b', c='d')), (('a', 'b'), {'c': 'd'}))
  assert_equal(pt(params(**{'2':'d'})), ((), {'2': 'd'}))
  assert_equal(pt(params('a', 'b', c='d') + ('e',)), (('a', 'b', 'e'), {'c': 'd'}))
  assert_equal(pt(params('a', 'b', c='d') | {'e': 'f'}), (('a', 'b'), {'c': 'd', 'e': 'f'}))
  a, b, c = params('a', 'b', c='d')  # expected behavior? yes, useful for match, err, stop = Result(…)

def test_parsertools__match_start_end():
  Match = parsertools.Match
  assert_equal(Match('hello').start(), 0)
  assert_equal(Match('hello', regs=((1, 2),)).start(), 1)
  assert_equal(Match('hello').end(), 5)
  assert_equal(Match('hello', regs=((1, 2),)).end(), 2)

def test_parsertools__match_expand():
  Match = parsertools.Match
  assert_equal(Match('hello').expand('hello'), 'hello')
  assert_equal(Match('hello').expand('\\0'), '\0')
  assert_raise(ValueError, lambda: Match('hello').expand('\\1'))
  assert_equal(Match('hello', regs=((0, 5), (1, 2))).expand('\\1'), 'e')
  assert_equal(Match('hello').expand('\\g<0>'), 'hello')
  # XXX ...
  assert_equal(Match('hello', regs=((0, 5), (1, 2), *(((2, 3),) * 30)), regdict={'a': (1, 2)}).expand('A\\n\\0\\1B\\23\\345\\g<a>\\éC'), 'A\n\0eBl\xe5eéC')

def test_parsertools__match_expand__parsing_errors():
  Match, ParsingError = parsertools.Match, parsertools.ParsingError
  assert_raise(ParsingError, lambda: Match('hello').expand('\\'))
  assert_raise(ParsingError, lambda: Match('hello').expand('\\g'))
  assert_raise(ParsingError, lambda: Match('hello').expand('\\g<'))
  assert_raise(ParsingError, lambda: Match('hello').expand('\\g<a'))
  assert_raise(ParsingError, lambda: Match('hello').expand('\\400'))
  assert_raise(ParsingError, lambda: Match('hello').expand('\\c'))
  assert_raise(ParsingError, lambda: Match('hello').expand('\\g<1a>'))
  assert_raise(ParsingError, lambda: Match('hello').expand('\\g<~>'))

def test_parsertools__match_group():
  Match = parsertools.Match
  assert_equal(Match('hello').group(), 'hello')
  assert_equal(Match('hello').group(0), 'hello')
  assert_raise(IndexError, lambda: Match('hello').group(1))
  assert_equal(Match('hello', regs=((0, 5), (1, 2))).group(1), 'e')
  assert_equal(Match('hello', regs=((0, 5), (-1, -1))).group(1), None)
  assert_raise(IndexError, lambda: Match('hello', regs=((0, 5), (1, 2))).group('a'))
  assert_equal(Match('hello', regs=((0, 5), (1, 2)), regdict={'a': (1, 2)}).group('a'), 'e')
  assert_equal(Match('hello', regs=((0, 5), (1, 2)), regdict={'a': (1, 2)}).group(1, 'a', 1, 'a'), ('e', 'e', 'e', 'e'))

def test_parsertools__match_groupdict():
  Match = parsertools.Match
  assert_equal(Match('hello').groupdict(), {})
  assert_equal(Match('hello', regs=((0, 5), (1, 2)), regdict={'a': (1, 2)}).groupdict(), {'a': 'e'})
  assert_equal(Match('hello', regs=((0, 5), (-1, -1)), regdict={'a': (-1, -1)}).groupdict(), {'a': None})
  assert_equal(Match('hello', regs=((0, 5), (-1, -1)), regdict={'a': (-1, -1)}).groupdict(''), {'a': ''})

def test_parsertools__match_groups():
  Match = parsertools.Match
  assert_equal(Match('hello').groups(), ())
  assert_equal(Match('hello', regs=((0, 5), (1, 2))).groups(), ('e',))
  assert_equal(Match('hello', regs=((0, 5), (-1, -1))).groups(), (None,))
  assert_equal(Match('hello', regs=((0, 5), (-1, -1))).groups(''), ('',))

def test_parsertools__match_span():
  Match = parsertools.Match
  assert_equal(Match('hello').span(), (0, 5))
  assert_equal(Match('hello').span(0), (0, 5))
  assert_raise(IndexError, lambda: Match('hello').span(1))
  assert_equal(Match('hello', regs=((0, 5), (1, 2))).span(1), (1, 2))
  assert_equal(Match('hello', regs=((0, 5), (-1, -1))).span(1), (-1, -1))
  assert_raise(IndexError, lambda: Match('hello', regs=((0, 5), (1, 2))).span('a'))
  assert_equal(Match('hello', regs=((0, 5), (1, 2)), regdict={'a': (1, 2)}).span('a'), (1, 2))

def test_parsertools__parse_groups():
  compile = parsertools.compile
  parser = compile(['a', {'b': 'b', 'c': 'c'}, 'd'])
  assert_equal(parser.match('abd').groups(), ('b', None))
  assert_equal(parser.match('abd').groupdict(), {'b': 'b', 'c': None})
  # XXX ...

# XXX test compile()

def test_parsertools__component_match():
  compile, match = parsertools.compile, parsertools.match
  assert repr(match('lol')) == "match('lol')"
  assert repr(compile(match('lol'))) == "compile(match('lol'))"
  assert compile(match('lol')).match('lol')
  assert compile(match('lol')).match('lol').groups() == ()
  assert compile(match('lol')).match('lol').groupdict() == {}
  assert compile(match('lol')).parse('lol') == 'lol'
  assert compile(match('lol')).match('lal') is None
  assert compile(match('lol')).min_length == 3
  assert compile(match('lol')).max_length == 3
  assert compile(match('lol')).groups == 0
  assert compile(match('lol')).groupindex == {}

def test_parsertools__component_group():
  compile, group = parsertools.compile, parsertools.group
  assert repr(group('lol')) == "group('lol')"
  assert repr(compile(group('lol'))) == "compile(group('lol'))"
  assert compile(group('lol')).match('lol')
  assert compile(group('lol')).match('lol').groups() == ('lol',)
  assert compile(group('lol')).match('lol').groupdict() == {}
  assert compile(group('lol')).parse('lol') == 'lol'
  assert compile(group('lol')).match('lal') is None
  assert compile(group('lol')).min_length == 3
  assert compile(group('lol')).max_length == 3
  assert compile(group('lol')).groups == 1
  assert compile(group('lol')).groupindex == {}
  assert repr(group('g', 'lol')) == "group('g', 'lol')"
  assert repr(compile(group('g', 'lol'))) == "compile(group('g', 'lol'))"
  assert compile(group('g', 'lol')).match('lol')
  assert compile(group('g', 'lol')).match('lol').groups() == ('lol',)
  assert compile(group('g', 'lol')).match('lol').groupdict() == {'g': 'lol'}
  assert compile(group('g', 'lol')).parse('lol') == 'lol'
  assert compile(group('g', 'lol')).match('lal') is None
  assert compile(group('g', 'lol')).min_length == 3
  assert compile(group('g', 'lol')).max_length == 3
  assert compile(group('g', 'lol')).groups == 1
  assert compile(group('g', 'lol')).groupindex == {'g': 1}

def test_parsertools__component_chain():
  compile, group, chain = parsertools.compile, parsertools.group, parsertools.chain

  assert repr(chain()) == "chain()"
  assert repr(compile(chain())) == "compile(chain())"
  assert compile(chain()).match('')
  assert compile(chain()).match('').groups() == ()
  assert compile(chain()).match('').groupdict() == {}
  assert len(compile(chain()).parse('')) == 0
  assert compile(chain()).match('lal')
  assert compile(chain()).min_length == 0
  assert compile(chain()).max_length == 0
  assert compile(chain()).groups == 0
  assert compile(chain()).groupindex == {}

  assert repr(chain('lol')) == "chain('lol')"
  assert repr(compile(chain('lol'))) == "compile(chain('lol'))"
  assert compile(chain('lol')).match('lol')
  assert compile(chain('lol')).match('lol').groups() == ()
  assert compile(chain('lol')).match('lol').groupdict() == {}
  assert len(compile(chain('lol')).parse('lol')) == 1
  assert compile(chain('lol')).match('lal') is None
  assert compile(chain('lol')).min_length == 3
  assert compile(chain('lol')).max_length == 3
  assert compile(chain('lol')).groups == 0
  assert compile(chain('lol')).groupindex == {}

  assert repr(chain('lo', 'l')) == "chain('lo', 'l')"
  assert repr(compile(chain('lo', 'l'))) == "compile(chain('lo', 'l'))"
  assert compile(chain('lo', 'l')).match('lol')
  assert compile(chain('lo', 'l')).match('lol').groups() == ()
  assert compile(chain('lo', 'l')).match('lol').groupdict() == {}
  assert len(compile(chain('lo', 'l')).parse('lol')) == 2
  assert compile(chain('lo', 'l')).match('lal') is None
  assert compile(chain('lo', 'l')).min_length == 3
  assert compile(chain('lo', 'l')).max_length == 3
  assert compile(chain('lo', 'l')).groups == 0
  assert compile(chain('lo', 'l')).groupindex == {}

  assert repr(chain(group('lo'), group('g', 'l'))) == "chain(group('lo'), group('g', 'l'))"
  assert repr(compile(chain(group('lo'), group('g', 'l')))) == "compile(chain(group('lo'), group('g', 'l')))"
  assert compile(chain(group('lo'), group('g', 'l'))).match('lol')
  assert compile(chain(group('lo'), group('g', 'l'))).match('lol').groups() == ('lo', 'l')
  assert compile(chain(group('lo'), group('g', 'l'))).match('lol').groupdict() == {'g': 'l'}
  assert len(compile(chain(group('lo'), group('g', 'l'))).parse('lol')) == 2
  assert compile(chain(group('lo'), group('g', 'l'))).match('lal') is None
  assert compile(chain(group('lo'), group('g', 'l'))).min_length == 3
  assert compile(chain(group('lo'), group('g', 'l'))).max_length == 3
  assert compile(chain(group('lo'), group('g', 'l'))).groups == 2
  assert compile(chain(group('lo'), group('g', 'l'))).groupindex == {'g': 2}

def test_parsertools__component_select():
  compile, group, select = parsertools.compile, parsertools.group, parsertools.select

  assert repr(select('lol')) == "select('lol')"
  assert repr(compile(select('lol'))) == "compile(select('lol'))"
  assert compile(select('lol')).match('lol')
  assert compile(select('lol')).match('lol').groups() == ()
  assert compile(select('lol')).match('lol').groupdict() == {}
  assert compile(select('lol')).parse('lol') == 'lol'
  assert compile(select('lol')).match('lal') is None
  assert compile(select('lol')).min_length == 3
  assert compile(select('lol')).max_length == 3
  assert compile(select('lol')).groups == 0
  assert compile(select('lol')).groupindex == {}

  assert repr(select('lo', 'l')) == "select('lo', 'l')"
  assert repr(compile(select('lo', 'l'))) == "compile(select('lo', 'l'))"
  assert compile(select('lo', 'l')).match('lol')
  assert compile(select('lo', 'l')).match('lol').groups() == ()
  assert compile(select('lo', 'l')).match('lol').groupdict() == {}
  assert compile(select('lo', 'l')).parse('lol') == 'lo'
  assert compile(select('lo', 'l')).parse('lal') == 'l'
  assert compile(select('lo', 'l')).min_length == 1
  assert compile(select('lo', 'l')).max_length == 2
  assert compile(select('lo', 'l')).groups == 0
  assert compile(select('lo', 'l')).groupindex == {}

  assert repr(select('lo', 'l', group=True)) == "select('lo', 'l', group=True)"
  assert repr(compile(select('lo', 'l', group=True))) == "compile(select('lo', 'l', group=True))"
  assert compile(select('lo', 'l', group=True)).match('lol')
  assert compile(select('lo', 'l', group=True)).match('lol').groups() == ('lo', None)
  assert compile(select('lo', 'l', group=True)).match('lol').groupdict() == {}
  assert compile(select('lo', 'l', group=True)).parse('lol') == 'lo'
  assert compile(select('lo', 'l', group=True)).parse('lal') == 'l'
  assert compile(select('lo', 'l', group=True)).min_length == 1
  assert compile(select('lo', 'l', group=True)).max_length == 2
  assert compile(select('lo', 'l', group=True)).groups == 2
  assert compile(select('lo', 'l', group=True)).groupindex == {}

  assert repr(select('lo', 'l', names=[None, 'g'], group=True)) == "select('lo', 'l', names=[None, 'g'], group=True)"
  assert repr(compile(select('lo', 'l', names=[None, 'g'], group=True))) == "compile(select('lo', 'l', names=[None, 'g'], group=True))"
  assert compile(select('lo', 'l', names=[None, 'g'], group=True)).match('lol')
  assert compile(select('lo', 'l', names=[None, 'g'], group=True)).match('lol').groups() == ('lo', None)
  assert compile(select('lo', 'l', names=[None, 'g'], group=True)).match('lol').groupdict() == {'g': None}
  assert compile(select('lo', 'l', names=[None, 'g'], group=True)).parse('lol') == 'lo'
  assert compile(select('lo', 'l', names=[None, 'g'], group=True)).parse('lal') == 'l'
  assert compile(select('lo', 'l', names=[None, 'g'], group=True)).min_length == 1
  assert compile(select('lo', 'l', names=[None, 'g'], group=True)).max_length == 2
  assert compile(select('lo', 'l', names=[None, 'g'], group=True)).groups == 2
  assert compile(select('lo', 'l', names=[None, 'g'], group=True)).groupindex == {'g': 2}

def test_parsertools__component_edit():
  compile, group, edit = parsertools.compile, parsertools.group, parsertools.edit
  def int0(m): return int(m[0])
  assert repr(edit('123', lambda m: int(m[0]))) == "edit('123', <lambda>)"
  assert repr(compile(edit('123', int0))) == "compile(edit('123', int0))"
  assert compile(edit('123', int0)).parse('123') == 123

def test_parsertools__component_group_reference():
  compile, group, chain, select, group_reference = parsertools.compile, parsertools.group, parsertools.chain, parsertools.select, parsertools.group_reference

  assert compile(chain(group('lol'), group_reference(1))).match('lollol')
  assert compile(chain(group('lol'), group_reference(1))).match('lollol').groups() == ('lol',)
  assert compile(chain(group('lol'), group_reference(1))).match('lollol').groupdict() == {}
  assert compile(chain(group('lol'), group_reference(1))).match('lollal') is None
  assert compile(chain(group(select('lo', 'l')), group_reference(1))).match('l') is None
  assert compile(chain(group(select('lo', 'l')), group_reference(1))).match('ll')
  assert compile(chain(group(select('lo', 'l')), group_reference(1))).match('lo') is None
  assert compile(chain(group(select('lo', 'l')), group_reference(1))).match('lol') is None
  assert compile(chain(group(select('lo', 'l')), group_reference(1))).match('lolo')

  assert compile(select(group('lol'), group_reference(1))).match('') is None
  assert compile(select(group('lol'), group_reference(1))).match('lol').groups() == ('lol',)
  assert compile(select(group('lol'), group_reference(1))).match('lol').groupdict() == {}
  assert compile(select(group('lol'), group_reference(1))).match('lal') is None

  assert compile(chain(group('g1', 'lol'), group_reference('g1'))).match('lollol')
  assert compile(chain(group('g1', 'lol'), group_reference('g1'))).match('lollol').groups() == ('lol',)
  assert compile(chain(group('g1', 'lol'), group_reference('g1'))).match('lollol').groupdict() == {'g1': 'lol'}
  assert compile(chain(group('g1', 'lol'), group_reference('g1'))).match('lollal') is None
  assert compile(chain(group('g1', select('lo', 'l')), group_reference('g1'))).match('l') is None
  assert compile(chain(group('g1', select('lo', 'l')), group_reference('g1'))).match('ll')
  assert compile(chain(group('g1', select('lo', 'l')), group_reference('g1'))).match('lo') is None
  assert compile(chain(group('g1', select('lo', 'l')), group_reference('g1'))).match('lol') is None
  assert compile(chain(group('g1', select('lo', 'l')), group_reference('g1'))).match('lolo')

  assert compile(select(group('g1', 'lol'), group_reference('g1'))).match('') is None
  assert compile(select(group('g1', 'lol'), group_reference('g1'))).match('lol').groups() == ('lol',)
  assert compile(select(group('g1', 'lol'), group_reference('g1'))).match('lol').groupdict() == {'g1': 'lol'}
  assert compile(select(group('g1', 'lol'), group_reference('g1'))).match('lal') is None

def test_parsertools__component_one():
  compile, one, ONE = parsertools.compile, parsertools.one, parsertools.ONE
  assert repr(one()) == 'one()'
  assert repr(compile(one())) == 'compile(one())'
  assert repr(ONE) == 'ONE'
  assert repr(compile(ONE)) == 'compile(ONE)'
  assert compile(ONE).match('') is None
  assert compile(ONE).match('a')

def test_parsertools__component_ungroup():
  compile, group, ungroup = parsertools.compile, parsertools.group, parsertools.ungroup
  assert repr(ungroup(group('lol'))) == "ungroup(group('lol'))"
  assert repr(compile(ungroup(group('lol')))) == "compile(ungroup(group('lol')))"
  assert compile(ungroup(group('lol'))).match('lol')
  assert compile(ungroup(group('lol'))).match('lol').groups() == ()
  assert compile(ungroup(group('lol'))).match('lol').groupdict() == {}

def test_parsertools__component_nothing():
  compile, group, nothing, NOTHING = parsertools.compile, parsertools.group, parsertools.nothing, parsertools.NOTHING
  assert repr(nothing()) == 'nothing()'
  assert repr(compile(nothing())) == 'compile(nothing())'
  assert repr(NOTHING) == 'NOTHING'
  assert repr(compile(NOTHING)) == 'compile(NOTHING)'
  assert compile(NOTHING).match('')
  assert compile(NOTHING).match('a')

def test_parsertools__component_eof():
  compile, group, eof, EOF = parsertools.compile, parsertools.group, parsertools.eof, parsertools.EOF
  assert repr(eof()) == 'eof()'
  assert repr(compile(eof())) == 'compile(eof())'
  assert repr(EOF) == 'EOF'
  assert repr(compile(EOF)) == 'compile(EOF)'
  assert compile(EOF).match('')
  assert compile(EOF).match('a') is None
  assert compile(EOF).match('a', 1)

def test_parsertools__component_bof():
  compile, group, bof, BOF = parsertools.compile, parsertools.group, parsertools.bof, parsertools.BOF
  assert repr(bof()) == 'bof()'
  assert repr(compile(bof())) == 'compile(bof())'
  assert repr(BOF) == 'BOF'
  assert repr(compile(BOF)) == 'compile(BOF)'
  assert compile(BOF).match('')
  assert compile(BOF).match('a')
  assert compile(BOF).match('a', 1) is None

def test_parsertools__component_until():
  compile, group, until, EOF = parsertools.compile, parsertools.group, parsertools.until, parsertools.EOF

  assert repr(until('a', EOF)) == "until('a', EOF)"
  assert repr(compile(until('a', EOF))) == "compile(until('a', EOF))"
  assert compile(until('a', EOF)).min_length == 0
  assert compile(until('a', 'b', 2)).min_length == 3

  assert compile(until('a', 'b')).match('b')[0] == 'b'
  assert compile(until('a', 'b', 1)).match('b') is None
  assert compile(until('a', 'b', 0, 0)).match('b')[0] == 'b'

  assert compile(until('a', 'b')).match('aaab')[0] == 'aaab'
  assert compile(until('a', 'b', 2)).match('aaab')[0] == 'aaab'
  assert compile(until('a', 'b', 3)).match('aaab')[0] == 'aaab'
  assert compile(until('a', 'b', 0, 2)).match('aaab') is None
  assert compile(until('a', 'b', 0, 3)).match('aaab')[0] == 'aaab'
  assert compile(until('a', 'b', 1, 2)).match('aaab') is None
  assert compile(until('a', 'b', 2, 3)).match('aaab')[0] == 'aaab'
  assert compile(until('a', 'b', 3, 3)).match('aaab')[0] == 'aaab'

  assert compile(until('a', 'b', lazy=True)).match('aaab')[0] == 'aaab'
  assert compile(until('a', 'b', 2, lazy=True)).match('aaab')[0] == 'aaab'
  assert compile(until('a', 'b', 3, lazy=True)).match('aaab')[0] == 'aaab'
  assert compile(until('a', 'b', 0, 2, lazy=True)).match('aaab') is None
  assert compile(until('a', 'b', 0, 3, lazy=True)).match('aaab')[0] == 'aaab'
  assert compile(until('a', 'b', 1, 2, lazy=True)).match('aaab') is None
  assert compile(until('a', 'b', 2, 3, lazy=True)).match('aaab')[0] == 'aaab'
  assert compile(until('a', 'b', 3, 3, lazy=True)).match('aaab')[0] == 'aaab'

  assert compile(until('a', '')).match('aaab')[0] == 'aaa'
  assert compile(until('a', '', lazy=True)).match('aaab')[0] == ''
  assert compile(until('a', 'ab', lazy=True)).match('aaab')[0] == 'aaab'

  assert compile(until('', '')).match('aaab')[0] == ''
  assert len(compile(until('', '')).parse('aaab')) == 2
  assert compile(until('', '', 2)).match('aaab')[0] == ''
  assert len(compile(until('', '', 2)).parse('aaab')) == 3
  assert compile(until('', '', 2, 3)).match('aaab')[0] == ''
  assert len(compile(until('', '', 2, 3)).parse('aaab')) == 3

def test_parsertools__component_many():
  compile, group, many = parsertools.compile, parsertools.group, parsertools.many

  assert repr(many('a')) == "many('a')"
  assert repr(many('a', 1)) == "many('a', 1)"
  assert repr(many('a', 2, 3)) == "many('a', 2, 3)"
  assert repr(compile(many('a'))) == "compile(many('a'))"
  assert repr(compile(many('a', 1))) == "compile(many('a', 1))"
  assert repr(compile(many('a', 2, 3))) == "compile(many('a', 2, 3))"

  assert compile(many('a')).match('') is None
  assert compile(many('a')).match('a')
  assert compile(many('a')).match('a')[0] == 'a'
  assert compile(many('a')).match('aaa')
  assert compile(many('a')).match('aaa')[0] == 'aaa'

  assert compile(many('a', 0, 2)).match('')
  assert len(compile(many('a', 0, 2)).parse('')) == 0
  assert compile(many('a', 0, 2)).match('a')
  assert compile(many('a', 0, 2)).match('a')[0] == 'a'
  assert compile(many('a', 0, 2)).match('aaa')
  assert compile(many('a', 0, 2)).match('aaa')[0] == 'aa'

  assert compile(many('a', 0, 0)).match('a')[0] == ''
  assert len(compile(many('a', 0, 0)).parse('a')) == 0

  assert len(compile(many('', 2)).parse('')) == 2
  # XXX also test group reference propagation

def test_parsertools__component_one_in():
  compile, one_in = parsertools.compile, parsertools.one_in
  assert repr(one_in('abc')) == "one_in('abc')"
  assert repr(compile(one_in('abc'))) == "compile(one_in('abc'))"
  assert compile(one_in('abc')).match('a')
  assert compile(one_in('abc')).match('b')
  assert compile(one_in('abc')).match('c')
  assert compile(one_in('abc')).match('d') is None

def test_parsertools__component_one_not_in():
  compile, one_not_in = parsertools.compile, parsertools.one_not_in
  assert repr(one_not_in('abc')) == "one_not_in('abc')"
  assert repr(compile(one_not_in('abc'))) == "compile(one_not_in('abc'))"
  assert compile(one_not_in('abc')).match('a') is None
  assert compile(one_not_in('abc')).match('b') is None
  assert compile(one_not_in('abc')).match('c') is None
  assert compile(one_not_in('abc')).match('d')

def test_parsertools__component_optional():
  compile, group, optional = parsertools.compile, parsertools.group, parsertools.optional
  assert repr(optional('a')) == "optional('a')"
  assert repr(compile(optional('a'))) == "compile(optional('a'))"
  assert compile(optional('a')).match('a')[0] == 'a'
  assert compile(optional('a')).match('b')[0] == ''
  assert compile(optional(group('a'))).match('b').groups() == (None,)

def test_parsertools__component_has():
  compile, group, has = parsertools.compile, parsertools.group, parsertools.has
  assert repr(has('a')) == "has('a')"
  assert repr(compile(has('a'))) == "compile(has('a'))"
  assert compile(has('a')).match('a')[0] == ''
  assert compile(has('a')).match('b') is None
  assert compile(has(group('a'))).match('a').groups() == ('a',)

def test_parsertools__component_has_not():
  compile, group, has_not = parsertools.compile, parsertools.group, parsertools.has_not
  assert repr(has_not('a')) == "has_not('a')"
  assert repr(compile(has_not('a'))) == "compile(has_not('a'))"
  assert compile(has_not('a')).match('a') is None
  assert compile(has_not('a')).match('b')[0] == ''
  assert compile(has_not(group('a'))).match('b').groups() == (None,)

def test_parsertools__component_critical():
  compile, critical = parsertools.compile, parsertools.critical
  assert repr(critical('a')) == "critical('a')"
  assert repr(compile(critical('a'))) == "compile(critical('a'))"
  assert compile(critical('a')).match('a')
  assert compile(critical('a')).scan('b').stop

def test_parsertools__component_critical_pair():
  compile, select, critical_pair = parsertools.compile, parsertools.select, parsertools.critical_pair
  assert compile(critical_pair('a', 'b')).match('ab')
  assert compile(critical_pair('a', 'b')).match('aa') is None
  assert compile(select(critical_pair('a', 'b'), 'aa')).match('aa') is None


def test_parsertools__component_search():
  compile, search = parsertools.compile, parsertools.search
  assert compile(search('>')).match('a') is None
  assert compile(search('>')).match('aaa>')

# XXX primitive tests
# XXX test all components…

def test_parsertools__scenario():
  compile, many, ONE = parsertools.compile, parsertools.many, parsertools.ONE
  assert compile(['hello ', {'who': many(ONE)}]).match('hello world').expand('') == ''
  assert compile(['hello ', {'who': many(ONE)}]).match('hello world').expand('He says hello who? Yes, hello \\g<who>, which is also \\1.') == 'He says hello who? Yes, hello world, which is also world.'
