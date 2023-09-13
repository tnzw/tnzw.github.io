def miniparser__test_comp_matches(comp, string, pos, endpos, expected):
  result = [m for m in comp(string, pos, endpos)]
  assert_equal(result, expected)

def miniparser__test_comp_values(comp, string, pos, endpos, expected):
  result = [miniparser.match_getvalue(m) for m in comp(string, pos, endpos)]
  assert_equal(result, expected)

def test_miniparser__string():
  string = miniparser.string
  miniparser__test_comp_matches(string('abc'), 'abce', 0, 4, [['abce', 0, 4, 0, 3, 'abc']])  # /abc/ on 'abce'
  miniparser__test_comp_matches(string('abc'), 'eabce', 1, 5, [['eabce', 1, 5, 1, 4, 'abc']])  # /abc/ on 'eabce'

def test_miniparser__istring():
  istring = miniparser.istring
  miniparser__test_comp_matches(istring('abC'), 'aBce', 0, 4, [['aBce', 0, 4, 0, 3, 'aBc']])  # /abC/i on 'aBce'
  miniparser__test_comp_matches(istring('aBc'), 'eAbce', 1, 5, [['eAbce', 1, 5, 1, 4, 'Abc']])  # /aBc/i on 'eAbce'

def test_miniparser__some():
  string = miniparser.string
  some = miniparser.some
  miniparser__test_comp_values(some(string('a')), 'aaa', 0, 3, [[*'aaa'], [*'aa'], ['a'], []])  # /a*/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 1), 'aaa', 0, 3, [['a']])  # /a{1}/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 2), 'aaa', 0, 3, [[*'aa']])  # /a{2}/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 3), 'aaa', 0, 3, [[*'aaa']])  # /a{3}/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 4), 'aaa', 0, 3, [])  # /a{4}/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 0, None), 'aaa', 0, 3, [[*'aaa'], [*'aa'], ['a'], []])  # /a{0,}/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 1, None), 'aaa', 0, 3, [[*'aaa'], [*'aa'], ['a']])  # /a{1,}/ or /a+/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 2, None), 'aaa', 0, 3, [[*'aaa'], [*'aa']])  # /a{2,}/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 3, None), 'aaa', 0, 3, [[*'aaa']])  # /a{3,}/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 4, None), 'aaa', 0, 3, [])  # /a{4,}/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 0, 3), 'aaaa', 0, 4, [[*'aaa'], [*'aa'], ['a'], []])  # /a{0,3}/ on 'aaaa'
  miniparser__test_comp_values(some(string('a'), 1, 3), 'aaaa', 0, 4, [[*'aaa'], [*'aa'], ['a']])  # /a{1,3}/ on 'aaaa'
  miniparser__test_comp_values(some(string('a'), 2, 3), 'aaaa', 0, 4, [[*'aaa'], [*'aa']])  # /a{2,3}/ on 'aaaa'
  miniparser__test_comp_values(some(string('a'), 3, 3), 'aaaa', 0, 4, [[*'aaa']])  # /a{3,3}/ on 'aaaa'

  miniparser__test_comp_values(some(string('a'), lazy=True), 'aaa', 0, 3, [[], ['a'], [*'aa'], [*'aaa']])  # /a*?/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 1, lazy=True), 'aaa', 0, 3, [['a']])  # /a{1}?/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 2, lazy=True), 'aaa', 0, 3, [[*'aa']])  # /a{2}?/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 3, lazy=True), 'aaa', 0, 3, [[*'aaa']])  # /a{3}?/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 4, lazy=True), 'aaa', 0, 3, [])  # /a{4}?/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 0, None, lazy=True), 'aaa', 0, 3, [[], ['a'], [*'aa'], [*'aaa']])  # /a{0,}?/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 1, None, lazy=True), 'aaa', 0, 3, [['a'], [*'aa'], [*'aaa']])  # /a{1,}?/ or /a+?/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 2, None, lazy=True), 'aaa', 0, 3, [[*'aa'], [*'aaa']])  # /a{2,}?/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 3, None, lazy=True), 'aaa', 0, 3, [[*'aaa']])  # /a{3,}?/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 4, None, lazy=True), 'aaa', 0, 3, [])  # /a{4,}?/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 0, 3, lazy=True), 'aaaa', 0, 4, [[], ['a'], [*'aa'], [*'aaa']])  # /a{0,3}?/ on 'aaaa'
  miniparser__test_comp_values(some(string('a'), 1, 3, lazy=True), 'aaaa', 0, 4, [['a'], [*'aa'], [*'aaa']])  # /a{1,3}?/ on 'aaaa'
  miniparser__test_comp_values(some(string('a'), 2, 3, lazy=True), 'aaaa', 0, 4, [[*'aa'], [*'aaa']])  # /a{2,3}?/ on 'aaaa'
  miniparser__test_comp_values(some(string('a'), 3, 3, lazy=True), 'aaaa', 0, 4, [[*'aaa']])  # /a{3,3}?/ on 'aaaa'

  miniparser__test_comp_values(some(string('a'), possessive=True), 'aaa', 0, 3, [[*'aaa']])  # /a*+/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 1, possessive=True), 'aaa', 0, 3, [['a']])  # /a{1}+/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 2, possessive=True), 'aaa', 0, 3, [[*'aa']])  # /a{2}+/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 3, possessive=True), 'aaa', 0, 3, [[*'aaa']])  # /a{3}+/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 4, possessive=True), 'aaa', 0, 3, [])  # /a{4}+/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 0, None, possessive=True), 'aaa', 0, 3, [[*'aaa']])  # /a{0,}+/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 1, None, possessive=True), 'aaa', 0, 3, [[*'aaa']])  # /a{1,}+/ or /a++/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 2, None, possessive=True), 'aaa', 0, 3, [[*'aaa']])  # /a{2,}+/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 3, None, possessive=True), 'aaa', 0, 3, [[*'aaa']])  # /a{3,}+/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 4, None, possessive=True), 'aaa', 0, 3, [])  # /a{4,}+/ on 'aaa'
  miniparser__test_comp_values(some(string('a'), 0, 3, possessive=True), 'aaaa', 0, 4, [[*'aaa']])  # /a{0,3}+/ on 'aaaa'
  miniparser__test_comp_values(some(string('a'), 1, 3, possessive=True), 'aaaa', 0, 4, [[*'aaa']])  # /a{1,3}+/ on 'aaaa'
  miniparser__test_comp_values(some(string('a'), 2, 3, possessive=True), 'aaaa', 0, 4, [[*'aaa']])  # /a{2,3}+/ on 'aaaa'
  miniparser__test_comp_values(some(string('a'), 3, 3, possessive=True), 'aaaa', 0, 4, [[*'aaa']])  # /a{3,3}+/ on 'aaaa'

def test_miniparser__chain():
  string = miniparser.string
  some = miniparser.some
  chain = miniparser.chain
  miniparser__test_comp_values(chain(string('a'), string('b')), 'ab', 0, 2, [[*'ab']])  # /ab/ on 'ab'
  miniparser__test_comp_values(chain(string('a'), string('c')), 'ab', 0, 2, [])  # /ac/ on 'ab'

  miniparser__test_comp_values(chain(some(string('a')), string('a')), 'aaa', 0, 3, [[[*'aa'], 'a'], [['a'], 'a'], [[], 'a']])  # /a*a/ on 'aaa'
  miniparser__test_comp_values(chain(some(string('a')), string('b')), 'aab', 0, 3, [[[*'aa'], 'b']])  # /a*b/ on 'aab'

  miniparser__test_comp_matches(chain(some(string('a')), some(string('a'))), 'aaa', 0, 3, [  # /a*a/ on 'aaa'
    ['aaa', 0, 3, 0, 3, [[*'aaa'], []]],
    ['aaa', 0, 3, 0, 3, [[*'aa'], ['a']]],
    ['aaa', 0, 3, 0, 2, [[*'aa'], []]],
    ['aaa', 0, 3, 0, 3, [['a'], [*'aa']]],
    ['aaa', 0, 3, 0, 2, [['a'], ['a']]],
    ['aaa', 0, 3, 0, 1, [['a'], []]],
    ['aaa', 0, 3, 0, 3, [[], [*'aaa']]],
    ['aaa', 0, 3, 0, 2, [[], [*'aa']]],
    ['aaa', 0, 3, 0, 1, [[], ['a']]],
    ['aaa', 0, 3, 0, 0, [[], []]]])

def test_miniparser__select():
  string = miniparser.string
  select = miniparser.select
  some = miniparser.some
  miniparser__test_comp_values(select(string('a'), string('b')), 'a', 0, 1, ['a'])  # `a|b` on 'a'
  miniparser__test_comp_values(select(string('a'), string('b')), 'b', 0, 1, ['b'])  # `a|b` on 'b'
  miniparser__test_comp_values(select(some(string('a')), string('b')), 'b', 0, 1, [[], 'b'])  # `a*|b` on 'b'
  miniparser__test_comp_values(select(some(string('a')), some(string('b'))), 'b', 0, 1, [[], ['b'], []])  # `a*|b*` on 'b'
  miniparser__test_comp_matches(select(some(string('a')), some(string('b')), getindex=True), 'b', 0, 1, [  # `a*|b*` on 'b'
    ['b', 0, 1, 0, 0, [0, []]],
    ['b', 0, 1, 0, 1, [1, ['b']]],
    ['b', 0, 1, 0, 0, [1, []]]])

def test_miniparser__atomic():
  string = miniparser.string
  some = miniparser.some
  chain = miniparser.chain
  atomic = miniparser.atomic
  miniparser__test_comp_values(atomic(some(string('a'))), 'aaa', 0, 3, [[*'aaa']])  # /(?>a*)/ on 'aaa'
  miniparser__test_comp_values(chain(atomic(some(string('a'))), string('a')), 'aaa', 0, 3, [])  # /(?>a*)a/ on 'aaa'

def test_miniparser__read():
  read = miniparser.read
  miniparser__test_comp_values(read(0), 'aaa', 0, 3, [''])     # `.{0}`
  miniparser__test_comp_values(read(1), 'aaa', 0, 3, ['a'])    # `.{1}`
  miniparser__test_comp_values(read(2), 'aaa', 0, 3, ['aa'])   # `.{2}`
  miniparser__test_comp_values(read(3), 'aaa', 0, 3, ['aaa'])  # `.{3}`
  miniparser__test_comp_values(read(4), 'aaa', 0, 3, [])       # `.{4}`

def test_miniparser__search():
  string = miniparser.string
  search = miniparser.search
  miniparser__test_comp_matches(search(string('b')), 'fedcbabcdef', 0, 11, [['fedcbabcdef', 0, 11, 4, 5, 'b']])
  miniparser__test_comp_matches(search(string('b'), fullmatch=True), 'fedcbabcdef', 0, 11, [['fedcbabcdef', 0, 11, 0, 5, ['fedc', 'b']]])
  miniparser__test_comp_values(search(string('b'), fullmatch=True, possessive=False), 'fedcbabcdef', 0, 11, [['fedc', 'b'], ['fedcba', 'b']])
  miniparser__test_comp_values(search(string('b'), fullmatch=True, lazy=False, possessive=False), 'fedcbabcdef', 0, 11, [['fedcba', 'b'], ['fedc', 'b']])

def test_miniparser__calc_parser():
  mp = miniparser
  SPACES_OR_NOT = mp.some(mp.one_in(' \t'), 0, None)  # -> unused value
  def with_spaces_or_not(comp): return mp.editvalue(mp.chain(SPACES_OR_NOT, comp), lambda v: v[1])
  INT = with_spaces_or_not(mp.edit(mp.some(mp.one_in('0123456789'), 1, None, possessive=True), lambda m: int(mp.match_getmatched(m), 10)))  # -> int
  FACTOR = with_spaces_or_not(mp.select(
    mp.editvalue(mp.chain(mp.string('('), SPACES_OR_NOT, mp.ref(lambda: EXPR), SPACES_OR_NOT, mp.string(')')), lambda v: v[2]),
    INT,
  ))  # -> int
  MUL_DIV = with_spaces_or_not(mp.one_in('*/'))  # -> string
  PLUS_SUB = with_spaces_or_not(mp.one_in('+-'))  # -> string
  def resolve_op(v):
    value, some_value = v
    if some_value is not None:
      for op, v2 in some_value:
        if   op == '*': value *= v2
        elif op == '+': value += v2
        elif op == '/': value /= v2
        elif op == '-': value -= v2
    return value
  TERM = mp.editvalue(mp.chain(FACTOR, mp.some(mp.chain( MUL_DIV, FACTOR))), resolve_op)  # -> number
  EXPR = mp.editvalue(mp.chain(  TERM, mp.some(mp.chain(PLUS_SUB,   TERM))), resolve_op)  # -> number
  DOC = mp.editvalue(mp.chain(EXPR, SPACES_OR_NOT, mp.EOF), lambda v: v[0])  # -> number
  parse_calc = mp.mkparser(DOC)

  assert_equal(parse_calc('1 + 2'), 3)
  assert_equal(parse_calc('1 + 2 + 3'), 6)
  assert_equal(parse_calc('2 * 3'), 6)
  assert_equal(parse_calc('2 * '), None)
  assert_equal(parse_calc('2 + (3 * 6)'), 20)
  assert_equal(parse_calc('2 / 4 * 5'), 2.5)
  assert_equal(parse_calc('2 / (4 * 5)'), 0.1)
  assert_equal(parse_calc('2 / (4 * 5'), None)
  assert_equal(parse_calc('2 / (20 + 4 * 5)'), 0.05)




def test_miniparser__match_expand_parser():

  def expand_bytes_parser():

    match_getmatched = miniparser.match_getmatched
    match_getstring = miniparser.match_getstring
    match_getstart = miniparser.match_getstart
    match_getend = miniparser.match_getend
    match_getvalue = miniparser.match_getvalue
    ENDPOS = miniparser.ENDPOS
    ONE = miniparser.ONE
    chain = miniparser.chain
    critical = miniparser.critical
    edit = miniparser.edit
    editvalue = miniparser.editvalue
    error = miniparser.error
    has = miniparser.has
    one_in = miniparser.one_in
    one_not_in = miniparser.one_not_in
    optional = miniparser.optional
    parsertop = miniparser.mkparser
    search = miniparser.search
    select = miniparser.select
    some = miniparser.some
    string = miniparser.string

    def mk_parser(enc):
      # vars
      _bsol_dict = {enc(a): enc(b) for a, b in ('\\\\', 'a\a', 'b\b', 'f\f', 'n\n', 'r\r', 't\t', 'v\v')}
      _BSOL = enc('\\')
      _0 = enc('0')
      # https://www.petefreitag.com/cheatsheets/regex/character-classes/
      _lower_ = enc('abcdefghijklmnopqrstuvwxyz')
      _upper_ = enc('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
      _digit_ = enc('0123456789')
      _word_ = _digit_ + _upper_ + enc('_') + _lower_
      _aword_ = _upper_ + enc('_') + _lower_

      # primitives
      BSOL = string(_BSOL)
      O = one_in(enc('01234567'))
      D = one_in(enc('0123456789'))
      D19 = one_in(enc('123456789'))
      D03 = one_in(enc('0123'))

      OCTAL_ESCAPE_VALUE = edit(  # \\(?:OOO|0O?)
        select(
          chain(has(some(O, 3)), critical(chain(D03, O, O), lambda s, p, e: ValueError(f'octal escape value {s[p - 1:e]} outside of range 0-0o377 at position {p - 1}'))),
          chain(string(_0), optional(O)),
        ),
        lambda m: enc(chr(int(match_getmatched(m), 8))))  # -> str

      GROUP_INDEX_ESCAPE_VALUE = edit(  # \\\d\d?
        chain(D19, optional(D)),
        lambda m: ['group', int(match_getmatched(m), 10)])  # -> ['group', 99]

      IDENT = chain(one_in(_aword_), some(one_in(_word_), possessive=True), ENDPOS)
      def isidentifier(string):
        for m in IDENT(string, 0, len(string)): return True
        return False

      def parse_group_name(m):
        name = match_getmatched(m)[2:-1]
        try: name = int(name if isinstance(name, str) else bytes(name), 10)  # only works with str and bytes-like object
        except ValueError:
          # here name is never empty thanks to critical "missing group name..."
          #if not name: raise ValueError(f'missing group name at position {match_getstart(m) + 3}')  # never happens
          if not isidentifier(name): raise ValueError(f'bad character in group name {name!r} at position {match_getstart(m) + 2}') from None
        return ['group', name]

      GROUP_NAME_ESCAPE_VALUE = edit(  # \\g<...>
        chain(
          string(enc('g')),
          critical(string(enc('<')), lambda s, p, e: ValueError(f'missing < at position {p}')),
          critical(one_not_in(enc('>')), lambda s, p, e: ValueError(f'missing group name at position {p}')),
          critical(search(string(enc('>'))), lambda s, p, e: ValueError(f'missing >, unterminated name at position {p - 1}')),
        ),
        parse_group_name)  # -> ['group', 99 or 'name']

      CHAR_ESCAPE_VALUE = edit(  # \\[\\abfnrtv]
        one_in(enc('\\abfnrtv')),
        lambda m: _bsol_dict[match_getmatched(m)])  # -> str

      NON_ASCII_ESCAPE_VALUE = edit(
        one_not_in(enc('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')),  # alphanum
        lambda m: _BSOL + match_getmatched(m))  # -> str

      ESCAPE = editvalue(
        chain(
          BSOL,
          critical(select(
            OCTAL_ESCAPE_VALUE,        # '\\377' or '\\04'
            GROUP_INDEX_ESCAPE_VALUE,  # '\\99'
            GROUP_NAME_ESCAPE_VALUE,   # '\\g<name>'
            CHAR_ESCAPE_VALUE,         # '\\n'
            NON_ASCII_ESCAPE_VALUE,    # '\\é'
            error(ONE, lambda m: ValueError(f'bad escape {match_getstring(m)[match_getstart(m) - 1:match_getend(m)]} at position {match_getstart(m) - 1}')),
          ), lambda s, p, e: ValueError(f'bad escape (end of pattern) at position {p - 1}')),
        ),
        lambda v: v[1])

      NO_ESCAPE_CHAR = one_not_in(_BSOL)  # -> str

      EXPAND_STEP = select(
        ESCAPE,          # '\\…'
        NO_ESCAPE_CHAR,  # '…'
      )  # -> list | str

      def join_expand_steps(m):
        r = ['expand']
        v = e = match_getstring(m)[:0]
        steps = match_getvalue(m)[0]
        if steps:
          for _ in steps:
            if isinstance(_, list):
              if v: r.append(v); v = e
              r.append(_)
            else:
              v += _
          if v: r.append(v)
        else:
          r.append(v)
        return r

      EXPAND = edit(
        critical(chain(some(EXPAND_STEP), ENDPOS), lambda s, p, e: RuntimeError('unexpected parsing error!')),
        join_expand_steps)  # -> ['expand', list | str, …]

      return parsertop(EXPAND)
    return mk_parser(lambda i: i), mk_parser(lambda i: i.encode())
  expand_str_parser, expand_bytes_parser = expand_bytes_parser()

  # Trying to reproduce re.Match.expand() behavior.
  # Here, we are completely outside any re.Match context, so I parsed to lisp
  # to make in re.Match context parsing easier.

  assert_equal(expand_str_parser('hello'), ['expand', 'hello'])
  assert_equal(expand_bytes_parser(b'hello'), ['expand', b'hello'])
  assert_equal(expand_bytes_parser(b'hello\\1world'), ['expand', b'hello', ['group', 1], b'world'])
  assert_equal(expand_str_parser('hello\\23world'), ['expand', 'hello', ['group', 23], 'world'])
  assert_equal(expand_bytes_parser(b'hello\\345world'), ['expand', b'hello\xc3\xa5world'])
  assert_equal(expand_bytes_parser(b'hello\\g<a>world'), ['expand', b'hello', ['group', b'a'], b'world'])
  assert_equal(expand_bytes_parser(b'hello\\g<1>world'), ['expand', b'hello', ['group', 1], b'world'])
  assert_equal(expand_str_parser('lol\\n\\0\\1lal\\23\\345\\g<a>\\élul'), ['expand', 'lol\n\x00', ['group', 1], 'lal', ['group', 23], '\345', ['group', 'a'], '\\élul'])

  assert_equal(assert_raise(ValueError, lambda: expand_str_parser('\\')).args[0], "bad escape (end of pattern) at position 0")
  assert_equal(assert_raise(ValueError, lambda: expand_str_parser('a\\')).args[0], "bad escape (end of pattern) at position 1")
  assert_equal(assert_raise(ValueError, lambda: expand_str_parser('\\g')).args[0], "missing < at position 2")
  assert_equal(assert_raise(ValueError, lambda: expand_str_parser('\\g<')).args[0], "missing group name at position 3")
  assert_equal(assert_raise(ValueError, lambda: expand_str_parser('\\g<a')).args[0], "missing >, unterminated name at position 3")
  assert_equal(assert_raise(ValueError, lambda: expand_str_parser('a\\g<a')).args[0], "missing >, unterminated name at position 4")
  assert_equal(assert_raise(ValueError, lambda: expand_str_parser('\\g<~>')).args[0], "bad character in group name '~' at position 3")
  assert_equal(assert_raise(ValueError, lambda: expand_str_parser('\\g<a~>')).args[0], "bad character in group name 'a~' at position 3")
  assert_equal(assert_raise(ValueError, lambda: expand_str_parser('\\400')).args[0], "octal escape value \\400 outside of range 0-0o377 at position 0")
  assert_equal(assert_raise(ValueError, lambda: expand_str_parser('a\\400')).args[0], "octal escape value \\400 outside of range 0-0o377 at position 1")
  assert_equal(assert_raise(ValueError, lambda: expand_str_parser('\\c')).args[0], "bad escape \\c at position 0")


def test_miniparser__content_type_parser():
  # https://www.rfc-editor.org/rfc/rfc9110#field.content-type
  mp = miniparser
  def v_group0(comp): return mp.edit(comp, lambda m: mp.match_getmatched(m))
  def smartjoin(iterable):
    r = []; n = True
    for i in iterable:
      if isinstance(i, list): r.append(i); n = True
      elif n: r.append(i); n = False
      else: r[-1] = r[-1] + i
    return r
  def v_smartjoin(comp): return mp.editvalue(comp, lambda v: smartjoin(v))
  # https://www.petefreitag.com/cheatsheets/regex/character-classes/
  _lower_ = b'abcdefghijklmnopqrstuvwxyz'
  _upper_ = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  _alpha_ = _upper_ + _lower_
  _digit_ = b'0123456789'
  #_bcharsnospace_ = _digit_ + _alpha_ + b"'()+_,-./:=?"
  #_bchars_ = _bcharsnospace_ + b' '
  _tchars_ = b"!#$%&'*+-.^_`|~" + _digit_ + _alpha_
  _vchars_ = bytes(i for i in range(0x21, 0x7F))  # [\x21-\x7e]
  # https://www.rfc-editor.org/rfc/rfc9110#name-whitespace
  OWS = v_group0(mp.some(mp.one_in(b' \t')))  # optional whitespace
  # https://www.rfc-editor.org/rfc/rfc9110#name-quoted-strings
  obs_text = mp.one_cond(lambda b: b >= 0x80)
  quoted_pair = mp.chain(mp.string(b'\\'), mp.select(mp.one_in(b'\t ' + _vchars_), obs_text))
  qdtext = mp.select(mp.one_in(b'\t ' + bytes(b for b in _vchars_ if b != 0x22 and b != 0x5C)), obs_text)
  quoted_string = mp.chain(mp.string(b'"'), v_smartjoin(mp.some(mp.select(qdtext, quoted_pair))), mp.string(b'"'))
  # https://www.rfc-editor.org/rfc/rfc9110#name-tokens
  token = v_group0(mp.some(mp.one_in(_tchars_), 1, None))
  # https://www.rfc-editor.org/rfc/rfc9110#name-parameters
  parameter_name = token
  parameter_value = mp.select(token, quoted_string)
  parameter = mp.chain(parameter_name, mp.string(b'='), parameter_value)
  parameters = mp.some(mp.chain(OWS, mp.string(b';'), OWS, mp.optional(parameter)))
  # https://www.rfc-editor.org/rfc/rfc9110#name-content-type
  type = token
  subtype = token
  media_type = mp.chain(type, mp.string(b'/'), subtype, parameters)

  parser = mp.mkparser(mp.editvalue(mp.chain(media_type, mp.ENDPOS), lambda v: v[0]))
  # XXX put better assertions
  assert parser(b'text/html')
  assert parser(b'text/html;charset=utf-8')
  assert parser(b'Text/HTML;Charset="utf-8"')
  assert parser(b'text/html; charset="utf-8"')
  assert parser(b'text/html;charset=UTF-8')
  assert parser(b'text/html;charset="u\\tf-8";key=value')
  assert not parser(b'text/html;charset="u\\tf-8";key=')
  assert not parser(b'text/html;charset="u\\tf-8')

# XXX do test_miniparser__regexp():
# XXX do test_miniparser__has():
# XXX do test_miniparser__has_not():
# XXX do test_miniparser__had():
# XXX do test_miniparser__had_not():