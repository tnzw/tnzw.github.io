# miniparser.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

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
    'error', 'func', 'genfunc', 'had', 'had_not', 'has', 'has_not', 'istring',
    'match_copy', 'match_freeze', 'match_frommatch', 'match_fromrematch',
    'match_getend', 'match_getendpos', 'match_getmatched', 'match_getpos',
    'match_getspan', 'match_getstart', 'match_getstring', 'match_getvalue',
    'match_new', 'mkparser', 'one_in', 'one_not_in', 'optional', 'read',
    'ref', 'regexp', 'search', 'select', 'some', 'string', 'v_matched',
    'v_raw']

  _module__undefined = []
  # a `match` is a list|tuple with -> (string, pos, endpos, start, end[, value])
  def match_new(string, pos, endpos, start, end, value=_module__undefined):
    #if value is _module__undefined: return [string, pos, endpos, start, end]
    if value is _module__undefined: return [string, pos, endpos, start, end, string[start:end]]
    return [string, pos, endpos, start, end, value]
  def match_frommatch(m, *, string=_module__undefined, pos=_module__undefined, endpos=_module__undefined, start=_module__undefined, end=_module__undefined, value=_module__undefined):
    return [
      match_getstring(m) if string is _module__undefined else string,
      match_getpos   (m) if    pos is _module__undefined else    pos,
      match_getendpos(m) if endpos is _module__undefined else endpos,
      match_getstart (m) if  start is _module__undefined else  start,
      match_getend   (m) if    end is _module__undefined else    end,
      match_getvalue (m) if  value is _module__undefined else  value]
  def match_fromrematch(m): return [m.string, m.pos, m.endpos, *m.span(), m.group()]
  def match_getstring(m): return m[0]
  def match_getpos   (m): return m[1]
  def match_getendpos(m): return m[2]
  def match_getspan  (m): return (*m[3:4],)
  def match_getstart (m): return m[3]
  def match_getend   (m): return m[4]
  def match_getvalue (m, default=_module__undefined):
    try: return m[5]
    except IndexError: pass
    if default is _module__undefined: return match_getmatched(m)
    return default
  def match_getmatched(m):
    s = match_getstart(m)
    e = match_getend(m)
    if s < 0: return None
    return match_getstring(m)[s:e]
  def match_copy     (m): return [*m]
  def match_freeze   (m): return (*m,)

  # "Pre-compiled" components

  def NOTHING(string, pos, endpos):  # `(?:|)`
    yield match_new(string, pos, endpos, pos, pos)
  def ONE(string, pos, endpos):  # `.`
    if pos < endpos: yield match_new(string, pos, endpos, pos, pos + 1)
  def EOF(string, pos, endpos):  # `$` or `\Z`
    if pos == len(string): yield match_new(string, pos, endpos, pos, pos)
  def BOF(string, pos, endpos):  # `^` or `\A`
    if pos == 0: yield match_new(string, pos, endpos, 0, 0)
  def ENDPOS(string, pos, endpos):
    if pos == endpos: yield match_new(string, pos, endpos, endpos, endpos)

  # Leaf components

  def read(size):  # `.{size}`
    def c(string, pos, endpos):
      endpos2 = pos + size
      if endpos2 <= endpos: yield match_new(string, pos, endpos, pos, endpos2)
    return c

  def string(pattern):  # `abc`
    def string(string, pos, endpos):
      endpos2 = min(endpos, pos + len(pattern))
      if string[pos:endpos2] == pattern:
        yield match_new(string, pos, endpos, pos, endpos2)
    return string

  def istring(pattern):  # `(?i:abc)`
    pattern = pattern.lower()
    def istring(string, pos, endpos):
      endpos2 = min(endpos, pos + len(pattern))
      if string[pos:endpos2].lower() == pattern:
        yield match_new(string, pos, endpos, pos, endpos2)
    return istring

  def regexp(pattern, method='match'):
    def regexp(string, pos, endpos):
      m = getattr(pattern, method)(string, pos, endpos)
      if m: yield match_new(string, pos, endpos, *m.span())  # keep groups? no, miniparser is not designed for groups.
    return regexp

  def one_in(set):  # `[abc]`
    def one_in(string, pos, endpos):
      if pos < endpos and string[pos] in set: yield match_new(string, pos, endpos, pos, pos + 1)
    return one_in

  def one_not_in(set):  # `[^abc]`
    def one_not_in(string, pos, endpos):
      if pos < endpos and string[pos] not in set: yield match_new(string, pos, endpos, pos, pos + 1)
    return one_not_in

  def one_cond(cond):
    def one_cond(string, pos, endpos):
      if pos < endpos and cond(string[pos]): yield match_new(string, pos, endpos, pos, pos + 1)
    return one_cond

  # One-component algorithms

  def has(comp):  # `(?=...)`
    def has(string, pos, endpos):
      for m in comp(string, pos, endpos):
        yield match_new(string, pos, endpos, pos, pos, match_getvalue(m))
        return
    return has

  def has_not(comp):  # `(?!...)`
    def has_not(string, pos, endpos):
      for m in comp(string, pos, endpos):
        return
      yield match_new(string, pos, endpos, pos, pos)
    return has_not

  def had(comp, size):  # `(?<=...)`
    def had(string, pos, endpos):
      for m in comp(string, max(pos - size, 0), pos):
        if match_getend(m) == pos:
          yield match_new(string, pos, endpos, pos, pos, match_getvalue(m))
          return
    return had

  def had_not(comp, size):  # `(?<!...)`
    def had_not(string, pos, endpos):
      for m in comp(string, max(pos - size, 0), pos):
        if match_getend(m) == pos:
          return
      yield match_new(string, pos, endpos, pos, pos)
    return had_not

  def atomic(comp):  # `(?>...)`
    def atomic(string, pos, endpos):
      for m in comp(string, pos, endpos):
        yield m
        return
    return atomic

  # Multi-component algorithms

  def select(*comps, getindex=False):  # `...|...`
    def select(string, pos, endpos):
      for i, comp in enumerate(comps):
        for m in comp(string, pos, endpos):
          if getindex: yield match_frommatch(m, value=[i, match_getvalue(m)])
          else: yield m
    return select

  def chain(comp, *comps):
    comps = (comp,) + comps
    def chain(string, pos, endpos):
      stack = [None] * len(comps)
      cur = pos
      i = 0
      while i >= 0:
        g, m = stack[i] or (comps[i](string, cur, endpos), None)
        try: m = next(g)
        except StopIteration: i -= 1
        else:
          stack[i] = (g, m)
          cur = match_getend(m)
          for comp in comps[i + 1:]:
            i += 1
            g = comp(string, cur, endpos)
            try: m = next(g)
            except StopIteration: break
            stack[i] = (g, m)
            cur = match_getend(m)
          else:
            yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[-1][1]), [match_getvalue(s[1]) for s in stack])
            #yield match_new(string, pos, endpos, min(match_getstart(s[1]) for s in stack), max(match_getend(s[1]) for s in stack), [match_getvalue(s[1]) for s in stack])
    return chain

  def some(comp, *repeats, lazy=False, possessive=False):
    # usage examples:
    #   some(...) or some(..., 0, None) -> `...*`
    #   some(..., 1, None)              -> `...+`
    #   some(..., 3) or some(..., 3, 3) -> `...{3}`
    #   some(..., 0, 1)                 -> `...{0,1}` or `...?`
    #   some(..., lazy=True)            -> `...*?`
    #   some(..., possessive=True)      -> `...*+`
    l = len(repeats)
    if l == 0: min_repeat = 0; max_repeat = None
    elif l == 1: min_repeat = max_repeat = repeats[0];
    elif l == 2: min_repeat, max_repeat = repeats
    else: raise TypeError(f'some expected at most 3 arguments, got {l + 1}')
    del l
    lazy = bool(lazy)
    possessive = bool(possessive)
    if lazy and possessive: raise TypeError('please do not use lazy along with possessive')
    def some(string, pos, endpos):
      l = 0
      stack = []
      cur = pos
      if lazy and l >= min_repeat:
        yield match_new(string, pos, endpos, pos, pos, [])
      # try to get more and more sub-match
      while max_repeat is None or l < max_repeat:
        g = comp(string, cur, endpos)
        try: m = next(g)
        except StopIteration: break
        stack.append((g, m)); l += 1
        cur = match_getend(m)
        if lazy and l >= min_repeat:
          yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[-1][1]), [match_getvalue(s[1]) for s in stack])
          #yield match_new(string, pos, endpos, min(match_getstart(s[1]) for s in stack), max(match_getend(s[1]) for s in stack), [match_getvalue(s[1]) for s in stack])
      while stack:
        if not lazy and l >= min_repeat:
          yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[-1][1]), [match_getvalue(s[1]) for s in stack])
          #yield match_new(string, pos, endpos, min(match_getstart(s[1]) for s in stack), max(match_getend(s[1]) for s in stack), [match_getvalue(s[1]) for s in stack])
          if possessive: return
        g, m = stack.pop(); l -= 1
        try: m = next(g)
        except StopIteration: continue
        stack.append((g, m)); l += 1
        cur = match_getend(m)
        if lazy and l >= min_repeat:
          yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[-1][1]), [match_getvalue(s[1]) for s in stack])
          #yield match_new(string, pos, endpos, min(match_getstart(s[1]) for s in stack), max(match_getend(s[1]) for s in stack), [match_getvalue(s[1]) for s in stack])
        while max_repeat is None or l < max_repeat:
          g = comp(string, cur, endpos)
          try: m = next(g)
          except StopIteration: break
          stack.append((g, m)); l += 1
          cur = match_getend(m)
          if lazy and l >= min_repeat:
            yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[-1][1]), [match_getvalue(s[1]) for s in stack])
            #yield match_new(string, pos, endpos, min(match_getstart(s[1]) for s in stack), max(match_getend(s[1]) for s in stack), [match_getvalue(s[1]) for s in stack])
      if not lazy and l >= min_repeat:
        yield match_new(string, pos, endpos, pos, pos, [])
    return some

  def search(comp, *, fullmatch=False, lazy=True, possessive=True):
    lazy = bool(lazy)
    possessive = bool(possessive)
    def search(string, pos, endpos):
      if lazy:
        for cur in range(pos, endpos + 1):
          for m in comp(string, cur, endpos):
            if fullmatch: yield match_new(string, pos, endpos,     pos                    , match_getend(m), [string[pos:cur], match_getvalue(m)])
            #if fullmatch: yield match_new(string, pos, endpos, min(pos, match_getstart(m)), match_getend(m), [string[pos:cur], match_getvalue(m)])
            else:         yield match_new(string, pos, endpos,          match_getstart(m) , match_getend(m),                   match_getvalue(m) )
            if possessive: return
      else:
        for cur in range(endpos, pos - 1, -1):
          for m in comp(string, cur, endpos):
            if fullmatch: yield match_new(string, pos, endpos,     pos                    , match_getend(m), [string[pos:cur], match_getvalue(m)])
            #if fullmatch: yield match_new(string, pos, endpos, min(pos, match_getstart(m)), match_getend(m), [string[pos:cur], match_getvalue(m)])
            else:         yield match_new(string, pos, endpos,          match_getstart(m) , match_getend(m),                   match_getvalue(m) )
            if possessive: return
    return search

  # Match/Value handling

  def editmatch(comp, editor):
    def editmatch(string, pos, endpos):
      for m in comp(string, pos, endpos):
        yield editor(m)  # XXX deep check editor() returned value? like using a match_validate()
    return editmatch

  def editvalue(comp, editor):
    def editvalue(string, pos, endpos):
      for m in comp(string, pos, endpos):
        yield match_frommatch(m, value=editor(match_getvalue(m)))
    return editvalue

  def edit(comp, editor):
    # keep sub match object in value: edit(..., lambda m: m)
    # value as matching: edit(..., lambda m: match_getmatched(m))
    def edit(string, pos, endpos):
      for m in comp(string, pos, endpos):
        yield match_frommatch(m, value=editor(m))
    return edit

  # Error handling

  def critical(comp, fn):  # raises if no match
    def critical(string, pos, endpos):
      for m in comp(string, pos, endpos):
        yield m
      raise fn(string, pos, endpos)
    return critical

  def error(comp, fn):  # raises if match
    def error(string, pos, endpos):
      for m in comp(string, pos, endpos):
        raise fn(m)
      if 0: yield
    return error

  # Component functions and referencing

  def genfunc(fn):
    def genfunc(string, pos, endpos):
      return fn(string, pos, endpos)
    return genfunc

  def func(fn):
    # func(lambda string, pos, endpos: return match_new(string, pos, endpos, pos, endpos))
    def func(string, pos, endpos):
      yield fn(string, pos, endpos)
    return func

  def ref(fn):
    # REC = chain(..., ref(lambda: REC))
    def ref(string, pos, endpos):
      comp = fn()
      return comp(string, pos, endpos)
    return ref

  # Sugar components

  def optional(comp, default=None, *, possessive=False):  # `...?`
    return editvalue(some(comp, 0, 1, possessive=possessive), lambda v: v[0] if v else default)

  def block(startcomp, stepcomp, stopcomp, *, lazy=False, possessive=True, min_steps=0, max_steps=None):
    subcomp = chain(startcomp, some(stepcomp, min_steps, max_steps, lazy=lazy), stopcomp)
    if possessive: subcomp = atomic(subcomp)
    return subcomp

  def v_matched(comp): return edit(comp, lambda m: match_getmatched(m))
  def v_raw(comp): return edit(comp, lambda m: m)

  # Top parser tools

  def mkparser(comp, return_match=False):
    def check_int(v, s, d, l, p):
      if v is None: return d
      if type(v) is not int: raise TypeError(f'{p} must be an integer')
      if v < 0: return 0  # raise ValueError(f'{p} must be >= 0')
      if v > l: return l
      return v
    def c(string, pos=None, endpos=None):
      l = len(string)
      for m in comp(string, check_int(pos, string, 0, l, 'pos'), check_int(endpos, string, l, l, 'endpos')):
        if return_match: return m
        return match_getvalue(m)
    return c

  # end of module #
  _module__locals = locals()  # is not exported
  for _ in _module__locals:
    if not _.startswith('_module_') and not hasattr(export, _):
      setattr(export, _, _module__locals[_])
  #del export.__priv__
  del export.export
  return export
miniparser = miniparser()
