# miniparser.py Version 2.4.1
#   This is free and unencumbered software released into the public domain.
#   SPDX: Unlicense <http://unlicense.org/>
#   Contributors: 2023-2024 <tnzw@github.triton.ovh>

# I also translate this lib to javascript

def miniparser():
  _module__name__ = 'miniparser'
  _module__doc__ = f"""A module instance of {_module__name__}, please see {_module__name__}.__doc__ for more information."""
  _module__name__ = _module__name__ if __name__ == '__main__' else (__name__ + '.' + _module__name__)
  try: _module__class__ = __builtins__.__class__
  except AttributeError:
    class _module__class__:
      def __init__(self, name): self.__name__ = name
  export = _module__class__(_module__name__)
  export.__doc__ = _module__doc__
  # beginning of module #

  __all__ = [
    'BOF', 'ENDPOS', 'EOF', 'NOTHING', 'ONE', 
    'atomic', 'block', 'chain', 'critical', 'edit', 'editmatch', 'editvalue',
    'error', 'func', 'had', 'had_not', 'has', 'has_not', 'istring',
    'match_copy', 'match_freeze', 'match_frommatch', 'match_fromrematch',
    'match_getend', 'match_getendpos', 'match_getslice', 'match_getslicelen',
    'match_getpos', 'match_getspan', 'match_getstart', 'match_getstring',
    'match_getvalue', 'match_getvalueasslice', 'match_hasvalue', 'match_new',
    'match_setvalue', 'mkparser', 'one_in', 'one_not_in', 'optional', 'read',
    'ref', 'regexp', 'search', 'select', 'some', 'some_sep', 'step_search',
    'string', 'v_match', 'v_set', 'v_slice', 'v_unset']

  _module__undefined = []
  # a `match` is a list|tuple with -> (string, pos, endpos, start, end[, value])
  def match_new(string, pos, endpos, start, end, value=_module__undefined):
    if value is _module__undefined: return [string, pos, endpos, start, end]
    return [string, pos, endpos, start, end, value]
  def match_frommatch(m, *, string=_module__undefined, pos=_module__undefined, endpos=_module__undefined, start=_module__undefined, end=_module__undefined, value=_module__undefined, getvalue=True):
    if value is not _module__undefined: v = [value]
    elif getvalue: v = match_getvalueasslice(m)
    else: v = []
    return [
      match_getstring(m) if string is _module__undefined else string,
      match_getpos   (m) if    pos is _module__undefined else    pos,
      match_getendpos(m) if endpos is _module__undefined else endpos,
      match_getstart (m) if  start is _module__undefined else  start,
      match_getend   (m) if    end is _module__undefined else    end,
      *v]
  def match_fromrematch(m): return [m.string, m.pos, m.endpos, *m.span(), m.group()]
  def match_getstring(m): return m[0]
  def match_getpos   (m): return m[1]
  def match_getendpos(m): return m[2]
  def match_getspan  (m): return (m[3], m[4])
  def match_getstart (m): return m[3]
  def match_getend   (m): return m[4]
  def match_getvalueasslice(m): return m[5:6]
  def match_getvalue (m, default=_module__undefined):
    v = match_getvalueasslice(m)
    if v: return v[0]
    if default is _module__undefined: return match_getslice(m)
    return default
  def match_setvalue (m, v):
    if len(m) == 5: m.append(v)
    else: m[5] = v
    return v
  def match_hasvalue (m):
    return bool(match_getvalueasslice(m))
  def match_getslice(m):
    s = match_getstart(m)
    e = match_getend(m)
    if s < 0: return None
    return match_getstring(m)[s:e]
  def match_getslicelen(m):
    l = match_getend(m) - match_getstart(m)
    if l < 0: return 0
    return l
  def match_copy     (m): return [*m]
  def match_freeze   (m): return (*m,)

  # "Pre-compiled" components

  def NOTHING(string, pos, endpos, *a, **kw):  # `(?:|)`
    yield match_new(string, pos, endpos, pos, pos)
  def ONE(string, pos, endpos, *a, **kw):  # `.`
    if pos < endpos: yield match_new(string, pos, endpos, pos, pos + 1)
  def EOF(string, pos, endpos, *a, **kw):  # `$` or `\Z`
    if pos == len(string): yield match_new(string, pos, endpos, pos, pos)
  def BOF(string, pos, endpos, *a, **kw):  # `^` or `\A`
    if pos == 0: yield match_new(string, pos, endpos, 0, 0)
  def ENDPOS(string, pos, endpos, *a, **kw):
    if pos == endpos: yield match_new(string, pos, endpos, endpos, endpos)

  # Leaf components

  def read(size):  # `.{size}`
    def read(string, pos, endpos, *a, **kw):
      endpos2 = pos + size
      if endpos2 <= endpos: yield match_new(string, pos, endpos, pos, endpos2)
    return read

  def string(pattern):  # `abc`
    def string(string, pos, endpos, *a, **kw):
      endpos2 = min(endpos, pos + len(pattern))
      if string[pos:endpos2] == pattern:
        yield match_new(string, pos, endpos, pos, endpos2)
    return string

  def istring(pattern):  # `(?i:abc)`
    pattern = pattern.lower()
    def istring(string, pos, endpos, *a, **kw):
      endpos2 = min(endpos, pos + len(pattern))
      if string[pos:endpos2].lower() == pattern:
        yield match_new(string, pos, endpos, pos, endpos2)
    return istring

  def regexp(pattern, method='match'):
    def regexp(string, pos, endpos, *a, **kw):
      m = getattr(pattern, method)(string, pos, endpos)
      if m: yield match_new(string, pos, endpos, *m.span())  # keep groups? no, miniparser is not designed for groups.
    return regexp

  def one_in(set):  # `[abc]`
    def one_in(string, pos, endpos, *a, **kw):
      if pos < endpos and string[pos] in set: yield match_new(string, pos, endpos, pos, pos + 1)
    return one_in

  def one_not_in(set):  # `[^abc]`
    def one_not_in(string, pos, endpos, *a, **kw):
      if pos < endpos and string[pos] not in set: yield match_new(string, pos, endpos, pos, pos + 1)
    return one_not_in

  def one_cond(cond):
    def one_cond(string, pos, endpos, *a, **kw):
      if pos < endpos and cond(string[pos]): yield match_new(string, pos, endpos, pos, pos + 1)
    return one_cond

  # One-component algorithms

  def optional(comp, default=_module__undefined, *, possessive=False):  # `...?`
    has_default = default is not _module__undefined
    possessive = bool(possessive)
    def optional(string, pos, endpos, *a, **kw):
      for m in comp(string, pos, endpos, *a, **kw):
        yield m
        if possessive: return
      if has_default: yield match_new(string, pos, endpos, pos, pos, default)
      else:           yield match_new(string, pos, endpos, pos, pos)
    return optional

  def has(comp):  # `(?=...)`
    def has(string, pos, endpos, *a, **kw):
      for m in comp(string, pos, endpos, *a, **kw):
        yield match_new(string, pos, endpos, pos, pos, *match_getvalueasslice(m))
        return
    return has

  def has_not(comp):  # `(?!...)`
    def has_not(string, pos, endpos, *a, **kw):
      for m in comp(string, pos, endpos, *a, **kw):
        return
      yield match_new(string, pos, endpos, pos, pos)
    return has_not

  def had(comp, size):  # `(?<=...)`
    def had(string, pos, endpos, *a, **kw):
      for m in comp(string, max(pos - size, 0), pos, *a, **kw):
        if match_getend(m) == pos:
          yield match_new(string, pos, endpos, pos, pos, *match_getvalueasslice(m))
          return
    return had

  def had_not(comp, size):  # `(?<!...)`
    def had_not(string, pos, endpos, *a, **kw):
      for m in comp(string, max(pos - size, 0), pos, *a, **kw):
        if match_getend(m) == pos:
          return
      yield match_new(string, pos, endpos, pos, pos)
    return had_not

  def atomic(comp):  # `(?>...)`
    def atomic(*a, **kw):
      for m in comp(*a, **kw):
        yield m
        return
    return atomic

  # Multi-component algorithms

  def select(*comps, getindexvalue=False, getindex=False, possessive=False):  # `...|...`
    getindexvalue = bool(getindexvalue)
    getindex = bool(getindex)
    possessive = bool(possessive)
    def select(*a, **kw):
      for i, comp in enumerate(comps):
        for m in comp(*a, **kw):
          if getindexvalue: yield match_frommatch(m, value=[i, match_getvalue(m)])
          elif getindex: yield match_frommatch(m, value=i)
          else: yield m
          if possessive: return
    return select

  def chain(*comps, getvalues=True, partial=False, lazy=False, possessive=False):
    # `chain(a, b, c, partial=True)` acts like `some(chain(a, some(chain(b, some(c, 0, 1)), 0, 1)), 0, 1)`.
    getvalues = bool(getvalues)
    partial = bool(partial)
    lazy = bool(lazy)
    possessive = bool(possessive)
    if not partial and lazy: raise TypeError('cannot be lazy when partial is not enabled')
    if lazy and possessive: raise TypeError('please do not use lazy along with possessive')
    def chain(string, pos, endpos, *a, **kw):
      if not comps:
        if getvalues: yield match_new(string, pos, endpos, pos, pos, [])
        else:         yield match_new(string, pos, endpos, pos, pos)
        return
      if lazy:  # here partial is True, possessive is False
        if getvalues: yield match_new(string, pos, endpos, pos, pos, [])
        else:         yield match_new(string, pos, endpos, pos, pos)
      stack = [None] * len(comps)
      cur = pos
      i = 0
      while i >= 0:
        g, m = stack[i] or (comps[i](string, cur, endpos, *a, **kw), None)
        try: m = next(g)
        except StopIteration:
          if partial and not lazy:
            if i == 0:
              if getvalues: yield match_new(string, pos, endpos, pos, pos, [])
              else:         yield match_new(string, pos, endpos, pos, pos)
            else:
              if getvalues: yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[i - 1][1]), [match_getvalue(s[1]) for s in stack[:i]])
              else:         yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[i - 1][1]))
            if possessive: return
          i -= 1
        else:
          stack[i] = (g, m)
          cur = match_getend(m)
          if lazy:  # here partial is True, possessive is False
            if getvalues: yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[i][1]), [match_getvalue(s[1]) for s in stack[:i + 1]])
            else:         yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[i][1]))
          for comp in comps[i + 1:]:
            i += 1
            g = comp(string, cur, endpos, *a, **kw)
            try: m = next(g)
            except StopIteration: break
            stack[i] = (g, m)
            cur = match_getend(m)
            if lazy:  # here partial is True, possessive is False
              if getvalues: yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[i][1]), [match_getvalue(s[1]) for s in stack[:i + 1]])
              else:         yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[i][1]))
          else:
            if not lazy:
              if getvalues: yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[-1][1]), [match_getvalue(s[1]) for s in stack])
              #if getvalues: yield match_new(string, pos, endpos, min(match_getstart(s[1]) for s in stack), max(match_getend(s[1]) for s in stack), [match_getvalue(s[1]) for s in stack])
              else:         yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[-1][1]))
              if possessive: return
    return chain

  def some(comp, *repeats, getvalues=True, lazy=False, possessive=False, unsafe=False):
    # usage examples:
    #   some(...) or some(..., 0, None) -> `...*`
    #   some(..., 1, None)              -> `...+`
    #   some(..., 3) or some(..., 3, 3) -> `...{3}`
    #   some(..., 0, 1)                 -> `...{0,1}` or `...?`
    #   some(..., lazy=True)            -> `...*?`
    #   some(..., possessive=True)      -> `...*+`
    # When `unsafe` is falsish, some() stops if m.end doesn't go further.
    l = len(repeats)
    if l == 0: min_repeat = 0; max_repeat = None
    elif l == 1: min_repeat = max_repeat = repeats[0]
    elif l == 2: min_repeat, max_repeat = repeats
    else: raise TypeError(f'some expected at most 3 arguments, got {l + 1}')
    del l
    getvalues = bool(getvalues)
    lazy = bool(lazy)
    possessive = bool(possessive)
    unsafe = bool(unsafe)
    if lazy and possessive: raise TypeError('please do not use lazy along with possessive')
    def some(string, pos, endpos, *a, **kw):
      l = 0
      stack = []
      cur = pos
      if lazy and l >= min_repeat:
        if getvalues: yield match_new(string, pos, endpos, pos, pos, [])
        else:         yield match_new(string, pos, endpos, pos, pos)
      # try to get more and more sub-match
      while max_repeat is None or l < max_repeat:
        g = comp(string, cur, endpos, *a, **kw)
        try: m = next(g)
        except StopIteration: break
        stack.append((g, m)); l += 1
        m_end = match_getend(m)
        # handling unsafe
        if cur < m_end or l < min_repeat or unsafe: cur = m_end
        else: break
        if lazy and l >= min_repeat:
          if getvalues: yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[-1][1]), [match_getvalue(s[1]) for s in stack])
          #if getvalues: yield match_new(string, pos, endpos, min(match_getstart(s[1]) for s in stack), max(match_getend(s[1]) for s in stack), [match_getvalue(s[1]) for s in stack])
          else:         yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[-1][1]))
      while stack:
        if not lazy and l >= min_repeat:
          if getvalues: yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[-1][1]), [match_getvalue(s[1]) for s in stack])
          #if getvalues: yield match_new(string, pos, endpos, min(match_getstart(s[1]) for s in stack), max(match_getend(s[1]) for s in stack), [match_getvalue(s[1]) for s in stack])
          else:         yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[-1][1]))
          if possessive: return
        g, m = stack.pop(); l -= 1
        try: m = next(g)
        except StopIteration: continue
        stack.append((g, m)); l += 1
        cur = match_getend(m)
        if lazy and l >= min_repeat:
          if getvalues: yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[-1][1]), [match_getvalue(s[1]) for s in stack])
          #if getvalues: yield match_new(string, pos, endpos, min(match_getstart(s[1]) for s in stack), max(match_getend(s[1]) for s in stack), [match_getvalue(s[1]) for s in stack])
          else:         yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[-1][1]))
        while max_repeat is None or l < max_repeat:
          g = comp(string, cur, endpos, *a, **kw)
          try: m = next(g)
          except StopIteration: break
          stack.append((g, m)); l += 1
          # handling unsafe
          if cur < m_end or l < min_repeat or unsafe: cur = m_end
          else: break
          if lazy and l >= min_repeat:
            if getvalues: yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[-1][1]), [match_getvalue(s[1]) for s in stack])
            #if getvalues: yield match_new(string, pos, endpos, min(match_getstart(s[1]) for s in stack), max(match_getend(s[1]) for s in stack), [match_getvalue(s[1]) for s in stack])
            else:         yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[-1][1]))
      if not lazy and l >= min_repeat:
        if getvalues: yield match_new(string, pos, endpos, pos, pos, [])
        else:         yield match_new(string, pos, endpos, pos, pos)
    return some

  def search(comp, *, getscanned=False, getvalue=True, scan_edit=None, scan_matches=None, lazy=True, possessive=True):
    getscanned = bool(getscanned)
    scan_matches = getscanned if scan_matches is None else bool(scan_matches)
    lazy = bool(lazy)
    possessive = bool(possessive)
    if getscanned and scan_edit is None: scan_edit = lambda m: match_getvalue(m)
    def search(string, pos, endpos, *a, **kw):
      if lazy:
        for cur in range(pos, endpos + 1):
          for m in comp(string, cur, endpos, *a, **kw):
            if getscanned: yield match_new(string, pos, endpos, pos if scan_matches else match_getstart(m), match_getend(m), [scan_edit(match_new(string, pos, endpos, pos, cur)), match_getvalue(m)])
            else:          yield match_new(string, pos, endpos, pos if scan_matches else match_getstart(m), match_getend(m),                                                      *match_getvalueasslice(m))
            if possessive: return
      else:
        for cur in range(endpos, pos - 1, -1):
          for m in comp(string, cur, endpos, *a, **kw):
            if getscanned: yield match_new(string, pos, endpos, pos if scan_matches else match_getstart(m), match_getend(m), [scan_edit(match_new(string, pos, endpos, pos, cur)), match_getvalue(m)])
            else:          yield match_new(string, pos, endpos, pos if scan_matches else match_getstart(m), match_getend(m),                                                      *match_getvalueasslice(m))
            if possessive: return
    return search

  # Match/Value handling

  def editmatch(comp, editor):
    def editmatch(string, pos, endpos, *a, **kw):
      for m in comp(string, pos, endpos, *a, **kw):
        m2 = editor(m)  # XXX deep check editor() returned value? like using a match_validate()
        if m2 is not None: yield m2
    return editmatch

  def editvalue(comp, editor):
    def editvalue(string, pos, endpos, *a, **kw):
      for m in comp(string, pos, endpos, *a, **kw):
        yield match_frommatch(m, value=editor(match_getvalue(m)))
    return editvalue

  def edit(comp, editor):
    # keep sub match object in value: edit(..., lambda m: m)
    # value as matching: edit(..., lambda m: match_getslice(m))
    def edit(string, pos, endpos, *a, **kw):
      for m in comp(string, pos, endpos, *a, **kw):
        yield match_frommatch(m, value=editor(m))
    return edit

  # Error handling

  def critical(comp, fn):  # raises if no match
    def critical(string, pos, endpos, *a, **kw):
      for m in comp(string, pos, endpos, *a, **kw):
        yield m
      raise fn(string, pos, endpos, *a, **kw)
    return critical

  def error(comp, fn):  # raises if match
    def error(string, pos, endpos, *a, **kw):
      for m in comp(string, pos, endpos, *a, **kw):
        raise fn(m)
      if 0: yield
    return error

  # Component functions and referencing

  #def genfunc(fn):  # kinda useless as you can directly put `fn` as a comp.
  #  def genfunc(string, pos, endpos, *a, **kw):
  #    return fn(string, pos, endpos, *a, **kw)
  #  return genfunc

  def func(fn):
    # func(lambda string, pos, endpos: match_new(string, pos, endpos, pos, endpos))
    def func(string, pos, endpos, *a, **kw):
      m = fn(string, pos, endpos, *a, **kw)
      if m is not None: yield m
    return func

  def ref(fn):
    # REC = chain(..., ref(lambda: REC))
    def ref(string, pos, endpos, *a, **kw):
      comp = fn()
      return comp(string, pos, endpos, *a, **kw)
    return ref

  # Sugar components

  def step_search(step_comp, stop_comp, *, min_steps=0, max_steps=None, getvalues=True, lazy=True, possessive=True, unsafe=False):
    return chain(some(step_comp, min_steps, max_steps, getvalues=getvalues, lazy=lazy, unsafe=unsafe), stop_comp, getvalues=getvalues, possessive=possessive)

  def block(start_comp, step_comp, stop_comp, *, min_steps=0, max_steps=None, lazy=False, possessive=True, unsafe=False):
    return chain(start_comp, some(step_comp, min_steps, max_steps, lazy=lazy, unsafe=unsafe), stop_comp, possessive=possessive)

  def some_sep(comp, sep, *repeats, getvalues=True, lazy=False, **some_k):
    # some_sep(not_hyphens, hyphen)('a-b-c', 0, 5)
    # -> ['a', '-', 'b', '-', 'c']
    # -> ['a', '-', 'b']
    # -> ['a']
    # -> []
    l = len(repeats)
    if l == 0: min_repeat = 0; max_repeat = None
    elif l == 1: min_repeat = max_repeat = repeats[0]
    elif l == 2: min_repeat, max_repeat = repeats
    else: raise TypeError(f'some expected at most 4 arguments, got {l + 1}')
    del l
    comp1 = chain(comp, some(chain(sep, comp, getvalues=getvalues), min_repeat - 1, None if max_repeat is None else max_repeat - 1, getvalues=getvalues, lazy=lazy, **some_k), getvalues=getvalues)
    if getvalues: comp1 = editvalue(comp1, lambda v: [v[0], *(_ for c in v[1] for _ in c)])
    if min_repeat == 0:
      if max_repeat == 0: comp1 = chain(getvalues=getvalues)
      elif lazy: comp1 = select(chain(getvalues=getvalues), comp1)
      else: comp1 = select(comp1, chain(getvalues=getvalues))
    return comp1

  def v_match(comp): return edit(comp, lambda m: m)
  def v_slice(comp): return edit(comp, lambda m: match_getslice(m))
  def v_set  (comp, v): return edit(comp, lambda m: v)
  def v_unset(comp): return editmatch(comp, lambda m: match_new(*m[:5]))

  # Top parser tools

  def mkparser(comp, *, return_match=False):
    def check_int(v, s, d, l, p):
      if v is None: return d
      if type(v) is not int: raise TypeError(f'{p} must be an integer')
      if v < 0: return 0  # raise ValueError(f'{p} must be >= 0')
      if v > l: return l
      return v
    def parser(string, pos=None, endpos=None):
      l = len(string)
      for m in comp(string, check_int(pos, string, 0, l, 'pos'), check_int(endpos, string, l, l, 'endpos')):
        if return_match: return m
        return match_getvalue(m)
    return parser

  # end of module #
  _module__locals = locals()  # is not exported
  for _ in _module__locals:
    if not _.startswith('_module_') and not hasattr(export, _):
      setattr(export, _, _module__locals[_])
  #del export.__priv__
  del export.export
  return export
miniparser = miniparser()
