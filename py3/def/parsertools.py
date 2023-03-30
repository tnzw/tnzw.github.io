# parsertools.py Version 0.2.4
# Copyright (c) 2022 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

# XXX make an re parser to get min_length, max_length (and groups and groupindex)
# XXX make error = ParsingError(msg, string, pos)
# XXX select value = (index, value) or just sub value
# XXX selectall value = [value, value, …]
# XXX :thinking:
#   stop() raises StopIteration(ParsingError(…))
#   resume() catches StopIteration and ignore it to continue parsing somewhere else
#   resume(select(
#     chain(match('\\'), select(
#       chain(match('x'), stop(chain(H, H), '')),
#     )),
#     one,
#   ))

# XXX thinking about a way to make chain(some('a'), some('b'), 'bc') eg 'a*b*bc' to match 'aabbc'
#     this could be implemented in pattern _scan()
#     so every _scan Result could return a state only if there is a possibility to _scan differently
#
#       ex chain(some('a'), some('b'), 'bc') scans 'aabbc'
#            some('a') called with no state (None) detects 'aa' with a possibility to match less (state returned)
#            some('b') called with no state (None) detects 'bb' with a possibility to match less (state returned)
#            'bc' does not match 'c'
#          chain() see there are states returned, recall sub pattern with one state change at a time (matrix of state)
#            some('a') match kept in memory by chain()
#            some('b') called with new state, detects 'b' only, with a possibility to match less (state returned)
#            'bc' matches 'bc'
#          chain() returns its match WITH a state, because it still has the some('a') state and some('b') state !

def parsertools():
  __name = __name__ + '.' + parsertools.__name__
  #if __name__ != '__main__': __name = __name__ + '.' + __name
  try: export = __builtins__.__class__(__name)
  except AttributeError: export = object(); export.__name__ = __name
  export.__doc__ = parsertools.__doc__
  export._mk_module = parsertools

  class ParsingError(ValueError):
    def __init__(self, msg, string, pos, *, found=None):  # XXX (…, stoppos=None?, expected=None?)
      # param order inspired by json.JSONDecodeError
      self.msg = msg
      self.string = string
      self.pos = pos
      self.found = found  # XXX testing…
      if type(string) == str:
        errmsg = msg + ': line ' + str(self.lineno) + ' column ' + str(self.col)
      else:
        errmsg = msg + ': position ' + str(pos)
      super().__init__(errmsg)
    @property
    def lineno(self):
      string = self.string
      #if isinstance(string, str): return string[:self.pos].count('\n') + 1
      #if isinstance(string, bytes): return string[:self.pos].count(b'\n') + 1
      return sum(1 for c in string[:self.pos] if c in ('\n', 10, b'\n')) + 1
    @property
    def col(self):
      string = self.string
      i = 0
      if self.pos > 0:
        for i, c in enumerate(string[self.pos - 1::-1], 1):
          if c in ('\n', 10, b'\n'): i -= 1; break
      return i

  def iter_mapping(mapping):
    if type(mapping) in (dict, frozenmapping): return mapping.items()
    if hasattr(mapping, "keys"):
      it = mapping.keys()
      def __iter__():
        for k in it: yield k, mapping[k]
      return __iter__()
    it = iter(mapping)
    def __iter__():
      for k, v in it: yield k, v
    return __iter__()

  class frozenmapping(tuple):
    # is an ordered dict
    __slots__ = ()
    def __new__(cls, *items, **kw):
      match items:
        case i,: return tuple.__new__(cls, (*(_ for __ in (((k, kw.pop(k, v)) for k, v in iter_mapping(i)), ((k, v) for k, v in kw.items())) for _ in __),))
        case (): return tuple.__new__(cls, (*((k, v) for k, v in kw.items()),))
        case _: raise TypeError(f'frozenmapping expected at most 1 argument, got {len(items)}')
    # tuple and dict interface
    def __contains__(self, key): return key in self.keys()
    def __eq__(self, other): return dict(self) == other
    def __ge__(self, other): return dict(self) >= other
    def __getitem__(self, key):
      i = 0
      try:
        while True:
          k, v = tuple.__getitem__(self, i)
          if k == key: return v
          i += 1
      except IndexError: pass
      raise KeyError(key)
    def __gt__(self, other): return dict(self) > other
    def __iter__(self): return self.keys()
    def __le__(self, other): return dict(self) <= other
    def __lt__(self, other): return dict(self) < other
    def __ne__(self, other): return dict(self) != other
    def __repr__(self): return f'{self.__class__.__name__}({{{", ".join(f"{k!r}: {v!r}" for k, v in self.items())}}})'
    # tuple interface
    def __add__(self, other): return TypeError('cannot add')
    def __rmul__(self, other): return TypeError('cannot multiply')
    # dict interface
    def __ior__(self, other): return TypeError('cannot update frozen object')
    def __or__(self, other):
      #return self.__class__(self.items(), **other)  # could raise unexpected TypeError: keywords must be strings
      items = []  # [(key1, value), (key2, value), …]
      keyindex = {}  # {key1: 0, key2: 1, …}
      s = list(self.items()); o = list(iter_mapping(other))
      for i, (k, v) in enumerate(s): items.append((k, v)); keyindex[k] = i
      for k, v in o:
        if k in keyindex: items[keyindex[k]] = (k, v)
        else: items.append((k, v))
      return self.__class__(items)
    def clear(self): return TypeError('connat update frozen object')
    def copy(self): return self
    @staticmethod
    def fromkeys(keys, value=None): return self.__class__((k, value) for k in keys)
    def get(self, key, default=None):
      for k, v in self.items():
        if k == key: return v
      return default
    def items(self): return tuple.__iter__(self)
    def keys(self): return (k for k, _ in self.items())
    def values(self): return (v for _, v in self.items())
    # frozenmapping interface
    #def _replace(self, *items, **kw): return self.__class__((k, v) for c in (self.items(), *items, kw) for k, v in iter_mapping(c))
    def _replace(self, **kw): return self.__class__(self.items(), **kw)

  #frozenmapping((([], 'c'),))  # XXX should raise TypeError: unhashable type: 'list'?

  class params(tuple):
    # works because frozenmapping is an ordered dict like
    __slots__ = ()
    def __new__(cls, *args, **kwargs): return tuple.__new__(cls, (args, frozenmapping(kwargs)))
    @property
    def args(self): return tuple.__getitem__(self, 0)
    @property
    def kwargs(self): return tuple.__getitem__(self, 1)
    def __add__(self, other): return params(*self.args.__add__(other), **self.kwargs)
    #def __eq__(self, other): return tuple(self) == tuple(other)
    def __getattr__(self, key):
      try: return self.kwargs[key]
      except KeyError: pass
      raise AttributeError(key)
    def __getitem__(self, key):
      if type(key) == int: return (*self.args, *self.kwargs.values())[key]
      return self.kwargs[key]
    def __iter__(self): return (_ for i in (self.args, self.kwargs.values()) for _ in i)
    def __or__(self, other): return params(*self.args, **self.kwargs.__or__(other))
    def __repr__(self):
      kwargs = ''
      for k, v in self.kwargs.items():
        if k.isidentifier(): kwargs += f', {k}={v!r}'
        else:
          kwargs = f', **{dict(self.kwargs)}'
          break
      if self.args:
        return f'{self.__class__.__name__}({", ".join(repr(_) for _ in self.args)}{kwargs})'
      return f'{self.__class__.__name__}({kwargs[2:]})'
    def __rmul__(self, other): return params(*self.args.__rmul__(other), **self.kwargs)
    def get(self, key, default=None):
      if type(key) == int:
        try: return [*self.args, *self.kwargs.values()][key]
        except IndexError: pass
        return default
      return self.kwargs.get(key, default)

  class Pattern(params):
    __slots__ = ()
    def __new__(cls, _scan, component, min_length, max_length, groups=None, groupindex=None, *a, **kw):
      return params.__new__(cls, *a, _scan=_scan, component=component, min_length=min_length, max_length=max_length, groups=0 if groups is None else groups, groupindex=frozenmapping(() if groupindex is None else groupindex), **kw)
    def __repr__(self): return f'compile({self.component!r})'
    def fullmatch(self, string, pos=None, endpos=None):
      m = self.match(string, pos, endpos)
      if m is None or m.end() != m.endpos: return
      return m
    def match(self, string, pos=None, endpos=None): return self.scanner(string, pos, endpos).match()
    def scan(self, string, pos=None, endpos=None): return self.scanner(string, pos, endpos).scan()
    def scanner(self, string, pos=None, endpos=None): return Scanner(self, string, pos, endpos)
    def search(self, string, pos=None, endpos=None): return self.scanner(string, pos, endpos).search()
    def parse(self, string, pos=None, endpos=None): return self.scanner(string, pos, endpos).parse()

  class Scanner(params):
    __slots__ = ()
    def __new__(cls, pattern, string, pos, endpos):
      def check_int(v, s):
        if v is None: return len(s)
        if type(v) != int: raise TypeError('value must be integer')
        if v < 0: raise ValueError(f'{v} must be >= 0')
        return v
      return params.__new__(cls, pattern, string, check_int(pos, ()), check_int(endpos, string))
    def scan(self):  # XXX (catches StopIteration?)
      pattern, string, pos, endpos = self
      return pattern._scan(pattern, string, pos, endpos, (None,))
    def parse(self):
      pattern, string, pos, endpos = self
      #return pattern._parse_value_func(pattern, pattern._scan(pattern, string, pos, endpos, (None,)))
      r = pattern._scan(pattern, string, pos, endpos, (None,))
      if r.error is not None: raise r.error
      return r.match.value
    def match(self):
      v = self.scan()
      if v.error: return None
      return v.match
    def search(self):
      m = self.match()
      if m is None:
        pattern, string, pos, endpos = self
        for cur in range(pos + 1, endpos + 1):
          m = Scanner(pattern, string, cur, endpos).match()
          if m is not None: return m

  class Result(params):
    __slots__ = ()
    def __new__(cls, match=None, error=None, stop=None):  # XXX ok?
      return params.__new__(cls, match=match, error=error, stop=bool(stop))

  class Match(params):
    __slots__ = ()
    def __new__(cls, string, pos=None, endpos=None, regs=None, *, regdict=None, groupmatches=None, groupmatchdict=None, value=None):
      if pos is None: pos = 0
      if endpos is None: endpos = len(string)
      ## XXX force int values?
      regs = ((pos, endpos),) if regs is None else (*((a, b) for a, b in regs),)  # copy  ((0, 3), (-1, -1), (1, 2))
      regdict = frozenmapping(() if regdict is None else ((k, (a, b)) for k, (a, b) in iter_mapping(regdict)))  # copy
      groupmatches = (None,) if groupmatches is None else (None, *(_ for _ in groupmatches))
      groupmatchdict = frozenmapping(() if groupmatchdict is None else groupmatchdict)  # copy
      return params.__new__(cls, regdict, groupmatches, groupmatchdict, string=string, pos=pos, endpos=endpos, regs=regs, value=value)
    def __getitem__(self, key):
      return self.group(key)
    def __repr__(self):
      if __name__ == '__main__': name = ''
      else: name = __name__ + '.'
      # XXX how to print Match object
      match = repr(self.group())
      if len(match) > 50: match = match[:23] + '...' + match[-23:]
      value = repr(self.value)
      #if len(value) > 100: value = value[:97] + '...'
      #if len(value) > 50: value = value[:23] + '...' + value[-23:]
      if len(value) > 50: value = value[:47] + '...'
      #return f'<{name}parsertools.{self.__class__.__name__} object; span={self.span()!r}, match={match}, value={value}>'
      return f'<{self.__class__.__name__} object; span={self.span()!r}, match={match}, value={value}>'
      #return f'<{self.__class__.__name__} object; span={self.span()!r}, match={match}>'
    #def __bool__(self): return self.regs[0][0] >= 0
    def end(self): return self.regs[0][1]
    def expand(self, template):
      if type(template) == bytes: lisp = expand_bytes_parser.parse(template)
      else: lisp = expand_str_parser.parse(template)
      e = template[:0]
      gg = (self[0], *self.groups(e))
      gd = self.groupdict(e)
      ggl = len(gg)
      out = []
      for _ in lisp[1:]:
        if _:
          if _[0] == 'group':
            g = _[1]
            if isinstance(g, int):
              if g >= 0 and g < ggl: out.append(gg[g])
              else: raise ValueError(f'invalid group reference {g!r}')  # at position … XXX use parsing error please
            else:
              if g in gd: out.append(gd[g])
              else: raise ValueError(f'unknown group name {g!r}')  # at position … XXX use parsing error please
          else: out.append(_)
      return e.join(out)
    def group(self, *groups):
      regdict, *_ = self
      l = len(groups)
      if l == 0:
        r = self.regs[0]
        return self.string[r[0]:r[1]] if r[0] >= 0 else None
      if l == 1:
        g = groups[0]
        if g is None: raise IndexError('no such group')
        if isinstance(g, int): r = self.regs[groups[0]]
        else:
          if g in regdict: r = regdict[g]
          else: raise IndexError('no such group')
        return self.string[r[0]:r[1]] if r[0] >= 0 else None
      return (*(self.group(g) for g in groups),)
    def groupdict(self, default=None):
      regdict, *_ = self
      return {g: (self.string[r[0]:r[1]] if r[0] >= 0 else default) for g, r in regdict.items()}
    def groups(self, default=None):
      return (*(self.string[r[0]:r[1]] if r[0] >= 0 else default for r in self.regs[1:]),)
    def groupmatch(self, *groups):
      _, groupmatches, groupmatchdict, *_ = self
      l = len(groups)
      if l == 0: return self
      if l == 1:
        g = groups[0]
        if g is None: raise IndexError('no such group')
        if g == 0: return self
        elif isinstance(g, int): return groupmatches[groups[0]]
        else:
          if g in groupmatchdict: return groupmatchdict[g]
          else: raise IndexError('no such group')
      return (*(self.groupmatch(g) for g in groups),)
    def groupmatchdict(self, default=None):
      _, _, groupmatchdict, *_ = self
      return {g: (default if _ is None else _) for g, _ in groupmatchdict.items()}
    def groupmatches(self, default=None):
      _, groupmatches, *_ = self
      return (*((default if _ is None else _) for _ in groupmatches[1:]),)
    def span(self, key=None):
      regdict, *_ = self
      if key is None: return self.regs[0]
      if isinstance(key, int): return self.regs[key]
      if key in regdict: return regdict[key]
      else: raise IndexError('no such group')
    def start(self): return self.regs[0][0]

  def match_get_regdict(match, only_matching=False):
    if only_matching: return {g: match.span(g) for g, v in match.groupdict().items() if v is not None}
    return {g: match.span(g) for g in match.groupdict()}
  def match_get_groupmatches(match, only_matching=False, rebuild=True):
    try: groupmatches = match.groupmatches
    except AttributeError: pass
    else:
      if only_matching: (*(_ for _ in groupmatches() if _ is not None),)
      return groupmatches()
    if rebuild:
      if only_matching: return (*(Match(match.string, match.pos, match.endpos, (match.span(i),)) for i, g in enumerate(match.groups(), 1) if g is not None),)
      return (*(None if g is None else Match(match.string, match.pos, match.endpos, (match.span(i),)) for i, g in enumerate(match.groups(), 1)),)
    return ()
  def match_get_groupmatchdict(match, only_matching=False, rebuild=True):
    try: groupmatchdict = match.groupmatchdict
    except AttributeError: pass
    else:
      if only_matching: return {g: v for g, v in groupmatchdict() if v is not None}
      return groupmatchdict()
    if rebuild:
      if only_matching: return {g: Match(match.string, (match.span(g),)) for g, v in match.groupdict().items() if v is not None}
      return {g: None if v is None else Match(match.string, (match.span(g),)) for g, v in match.groupdict().items()}
    return {}
  #def match_guess_groupindex(match, *default):
  #  if getattr(match, 'groupindex', None): return match.groupindex
  #  # get group regs and possible indices
  #  regdict = match_get_regdict(match)
  #  groupindices = {}
  #  for g, (a, b) in regdict.items():
  #    groupindices[g] = l = []
  #    for i, (c, d) in enumerate(match.regs[1:], 1):
  #      if (a, b) == (c, d): l.append(i)
  #  # get group that have only one possible index to remove the index from others
  #  done = set()
  #  cont = True
  #  while cont:
  #    cont = False
  #    for g, ii in groupindices.items():
  #      if g not in done:
  #        if len(ii) == 1:
  #          cont = True
  #          done.add(g)
  #          for g2, ii2 in groupindices.items():
  #            try:
  #              if g2 not in done: ii2.remove(ii[0])
  #            except ValueError: pass
  #          break
  #  # check for inconsistencies
  #  for g, ii in groupindices.items():
  #    if len(ii) > 1:
  #      if default: return default[0]
  #      raise ValueError('cannot guess groupindex')
  #  # return guessed groupindex
  #  return {g: ii[0] if len(ii) else None for g, ii in groupindices.items()}
  #import re
  #m = re.compile('(?P<lol>lol)(?P<lal>lol)').match('lollol')
  #print(match_guess_groupindex(m))

  def regs_mix_match(regs, *mm):
    # regs_mix_match([(11, 12), (-1, -1), (15, 16), (17, 18)], Match(…regs=[(21, 22), (23, 24), (-1, -1), (27, 28), (-1, -1)]…))
    # -> [(11, 12), (23, 24), (15, 16), (27, 28), (-1, -1)]
    l = len(regs)
    for m in mm:
      for i, g in enumerate(m.groups(), 1):
        if i >= l: regs.append(m.span(i)); l += 1
        elif g is not None: regs[i] = m.span(i)
    return regs
  #def regs_mix(regs, *regss):
  #  # mix_match_regs([(10, 11), (-1, -1), (15, 16), (17, 18)], Match(…regs=[(21, 22), (23, 24), (-1, -1), (27, 28), (-1, -1)]…))
  #  # -> [(10, 11), (23, 24), (15, 16), (27, 28), (-1, -1)]
  #  regs = list(regs); l = len(regs)
  #  for otherregs in regss:
  #    for i, r in enumerate(otherregs[1:], 1):
  #      if i >= l: regs.append((r[0], r[1])); l += 1
  #      elif r[0] >= 0: regs[i] = (r[0], r[1])
  #
  def regs_append_match(regs, *mm):
    for m in mm: regs.extend(m.regs[1:])
    return regs
  def regs_append_pattern(regs, *pp):
    for p in pp: regs.extend([(-1, -1)] * p.groups)
    return regs

  def groupmatches_mix_match(groupmatches, *mm):
    # groupmatches_mix_match([None, m12, m13], Match(…groupmatches=[m21, None, m23, None]…))
    # -> [m21, m12, m23, None]
    l = len(groupmatches)
    for m in mm:
      for i, v in enumerate(match_get_groupmatches(m)):
        if i >= l: groupmatches.append(v); l += 1
        elif v is not None: groupmatches[i] = v
    return groupmatches
  #def groupmatches_mix(groupmatches, *groupmatchess):
  #  groupmatches = list(groupmatches)
  #  l = len(groupmatches)
  #  for othergroupmatches in groupmatchess:
  #    i = 1
  #    for r in othergroupmatches[1:]:
  #      if i >= l:
  #        groupmatches.append(r)
  #        l += 1
  #      elif r is not None:
  #        groupmatches[i] = r
  #      i += 1
  #  return groupmatches
  def groupmatches_append_match(groupmatches, *mm):
    for m in mm: groupmatches.extend(match_get_groupmatches(m))
    return groupmatches
  def groupmatches_append_pattern(groupmatches, *pp):
    for p in pp: groupmatches.extend([None] * p.groups)
    return groupmatches

  def regdict_update_match(regdict, *mm):
    for m in mm:
      for g, v in m.groupdict().items():
        if g not in regdict or v is not None: regdict[g] = m.span(g)
    return regdict
  def regdict_update_pattern(regdict, *pp):
    for p in pp:
      for g in p.groupindex:
        if g not in regdict: regdict[g] = (-1, -1)
    return regdict
  #def regdict_update(regdict, *regdicts):
  #  for otherregdict in regdicts:
  #    #for g in otherregdict:
  #    #  v = otherregdict[g]
  #    for g, v in otherregdict.items():
  #      if g not in regdict or v[0] >= 0:
  #        regdict[g] = (v[0], v[1])
  #  return regdict
  def groupmatchdict_update_match(groupmatchdict, *mm):
    for m in mm:
      for g, v in match_get_groupmatchdict(m).items():
        if g not in groupmatchdict or v is not None: groupmatchdict[g] = v
    return groupmatchdict
  def groupmatchdict_update_pattern(groupmatchdict, *pp):
    for p in pp:
      for g in p.groupindex:
        if g not in groupmatchdict: groupmatchdict[g] = None
    return groupmatchdict
  #def groupmatchdict_update(groupmatchdict, *groupmatchdicts):
  #  for othergroupmatchdict in groupmatchdicts:
  #    #for g in othergroupmatchdict:
  #    #  v = othergroupmatchdict[g]
  #    for g, v in othergroupmatchdict.items():
  #      if g not in groupmatchdict or v is not None:
  #        groupmatchdict[g] = v
  #  return groupmatchdict

  def match_copy(m, **kw):
    regs = list(m.regs)
    regdict = match_get_regdict(m)
    groupmatches = match_get_groupmatches(m)
    groupmatchdict = match_get_groupmatchdict(m)
    if 'start' in kw or 'end' in kw: regs[0] = (kw.pop('start') if 'start' in kw else m.start()), (kw.pop('end') if 'end' in kw else m.end())
    if 'value' in kw: value = kw.pop('value')
    else: value = getattr(m, 'value', None)
    return Match(m.string, m.pos, m.endpos, regs, regdict=regdict, groupmatches=groupmatches, groupmatchdict=groupmatchdict, value=value, **kw)
  def match_advance(m, *mm, **kw):
    start = m.start()
    regs = list(m.regs)
    regdict = match_get_regdict(m)
    groupmatches = list(match_get_groupmatches(m))
    groupmatchdict = match_get_groupmatchdict(m)
    if mm:
      regs_append_match(regs, *mm)
      regdict_update_match(regdict, *mm)
      groupmatches_append_match(groupmatches, *mm)
      groupmatchdict_update_match(groupmatchdict, *mm)
      end = mm[-1].end()
    else:
      end = m.end()
    if 'start' in kw: start = kw.pop('start')
    if 'end' in kw: end = kw.pop('end')
    regs[0] = (start, end)
    return Match(m.string, m.pos, m.endpos, regs, regdict=regdict, groupmatches=groupmatches, groupmatchdict=groupmatchdict, **kw)
  def match_update(m, *mm, **kw):
    regs = list(m.regs)
    regdict = match_get_regdict(m)
    groupmatches = list(match_get_groupmatches(m))
    groupmatchdict = match_get_groupmatchdict(m)
    start = m.start()
    if mm:
      regs_mix_match(regs, *mm)
      regdict_update_match(regdict, *mm)
      groupmatches_mix_match(groupmatches, *mm)
      groupmatchdict_update_match(groupmatchdict, *mm)
      end = mm[-1].end()
    else:
      end = m.end()
    if 'start' in kw: start = kw.pop('start')
    if 'end' in kw: end = kw.pop('end')
    regs[0] = (start, end)
    return Match(m.string, m.pos, m.endpos, regs, regdict=regdict, groupmatches=groupmatches, groupmatchdict=groupmatchdict, **kw)
  def match_advance_from_pattern(m, *pp, **kw):
    regs = list(m.regs)
    regdict = match_get_regdict(m)
    groupmatches = list(match_get_groupmatches(m))
    groupmatchdict = match_get_groupmatchdict(m)
    if pp:
      regs_append_pattern(regs, *pp)
      regdict_update_pattern(regdict, *pp)
      groupmatches_append_pattern(groupmatches, *pp)
      groupmatchdict_update_pattern(groupmatchdict, *pp)
    if 'start' in kw or 'end' in kw: regs[0] = (kw.pop('start') if 'start' in kw else m.start()), (kw.pop('end') if 'end' in kw else m.end())
    return Match(m.string, m.pos, m.endpos, regs, regdict=regdict, groupmatches=groupmatches, groupmatchdict=groupmatchdict, **kw)

  def zip_with_groupindex(elements, groupindex, offset=0):
    # list(zip_with_groupindex([(0, 2), (0, 1), (1, 2)], {'one': 1, 'three': 3})) → [(None, (0, 2)), ('one', (0, 1)), (None, (1, 2))]
    # list(zip_with_groupindex([match1, match2], {'one': 1, 'three': 3}, -1)) → [('one', match1), (None, match2)]
    indexgroup = {i + offset: g for g, i in iter_mapping(groupindex) if i is not None}
    return ((indexgroup.get(i), e) for i, e in enumerate(elements))

  class Component: __slots__ = ()  # is an interface

  def compile(component, references=None):  # XXX add replacer=None parameter, and propagate it to __pattern__(…, replacer=replacer) (remove _simplify_repr to use class list_to_chain(Component) with __pattern__ returning same _scan as chain() one)
    t = type(component)
    if t == list:
      if len(component) == 1: component = group(component[0], _simplify_repr=True)
      else: component = chain(*component, _repr_list=True)  # XXX use _simplify_repr
    elif t == dict:
      if len(component) == 1:
        k, = component.keys()
        #component = group(k, component[k], _simplify_repr=True)
        if type(k) == str: component = group(k, component[k], _simplify_repr=True)
        else: component = group(component[k], _simplify_repr=True)
      else:
        component = select(*component.values(), names=component.keys(), group=True, _simplify_repr=True)
    elif t in (str, bytes): component = match(component, _simplify_repr=True)
    if references is None: references = [None]
    p = component.__pattern__(references)
    return p

  # component classes (ordered by: assertions, one chars, leaves, group/value/error manipulation, nodes, loops)

  # - nothing
  # - eof
  # - bof

  # - one
  # - one_in
  # - one_not_in

  # - match

  # - group
  # - group_reference
  # - ungroup
  # - edit
  # - primitive
  # - critical
  # - critical_pair

  # - has
  # - has_not
  # - optional
  # - chain
  # - select

  # - until
  # - many
  # - search

  # XXX component classes:
  # - join (like chain but value is m[0])
  # - had  (`re.compile('(?<=x*)y')` or `re.compile('(?<=x|)y')` → re.error: look-behind requires fixed-width pattern) (but `re.compile('(?<=x|y)z')` is ok)
  # - had_not
  # - catch_critical (removes `stop` flag XXX find a better name?)
  # - some (like many but default parameter is min_length=0?)
  # - ref (min_length=always 0, max_length=always None, no group, compile(ungroup(ref._get())))

  # ASSERTION COMPONENTS #

  class nothing(Component):
    def __init__(self, *, _simplify_repr=False): self._simplify_repr = bool(_simplify_repr)
    def __repr__(self):
      if self._simplify_repr: return 'NOTHING'
      return f'{self.__class__.__name__}()'
    def __pattern__(self, references):
      return Pattern(self._scan, self, 0, 0)
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      return Result(Match(string, pos, endpos, ((pos, pos),), value=string[pos:pos]))
  NOTHING = nothing(_simplify_repr=True)

  class eof(Component):
    def __init__(self, *, _simplify_repr=False): self._simplify_repr = bool(_simplify_repr)
    def __repr__(self):
      if self._simplify_repr: return 'EOF'
      return f'{self.__class__.__name__}()'
    def __pattern__(self, references):
      return Pattern(self._scan, self, 0, 0)
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      if pos == len(string): return Result(Match(string, pos, endpos, ((pos, pos),), value=string[pos:pos]))
      return Result(error=ParsingError(f'expected end of data', string, pos, found=string[pos:pos]))
  EOF = eof(_simplify_repr=True)

  class bof(Component):
    def __init__(self, *, _simplify_repr=False): self._simplify_repr = bool(_simplify_repr)
    def __repr__(self):
      if self._simplify_repr: return 'BOF'
      return f'{self.__class__.__name__}()'
    def __pattern__(self, references):
      return Pattern(self._scan, self, 0, 0)
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      if pos == 0: return Result(Match(string, pos, endpos, ((pos, pos),), value=string[pos:pos]))
      return Result(error=ParsingError(f'expected beginning of data', string, pos, found=string[pos:pos]))
  BOF = bof(_simplify_repr=True)

  # ONE CHAR COMPONENTS #

  class one(Component):
    def __init__(self, *, _simplify_repr=False): self._simplify_repr = bool(_simplify_repr)
    def __repr__(self):
      if self._simplify_repr: return 'ONE'
      return f'{self.__class__.__name__}()'
    def __pattern__(self, references):
      return Pattern(self._scan, self, 1, 1)
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      pos2 = pos + 1
      if pos2 <= endpos and string[pos:pos2]: return Result(Match(string, pos, endpos, ((pos, pos2),), value=string[pos:pos2]))
      t = type(string)
      element = 'element'
      if t == str: element = 'char'
      elif t in (bytes, bytearray): element = 'byte'
      return Result(error=ParsingError(f'expected one {element}', string, pos, found=string[pos:pos2]))
  ONE = one(_simplify_repr=True)

  class one_in(Component):
    def __init__(self, set): self.set = set
    def __repr__(self): return f'{self.__class__.__name__}({self.set!r})'
    def __pattern__(self, references):
      s = self.set
      #if not isinstance(s, (str, bytes, tuple)): s = tuple(s)
      return Pattern(self._scan, self, 1, 1, set=s)
    @staticmethod
    def _scan(pat, string, pos, endpos, top_match):
      s = pat.set
      i = pos + 1
      if pos < endpos and string[pos] in s: return Result(Match(string, pos, endpos, ((pos, i),), value=string[pos:i]))
      return Result(error=ParsingError(f'expected one in {s!r}', string, pos))

  class one_not_in(Component):
    def __init__(self, set): self.set = set
    def __repr__(self): return f'{self.__class__.__name__}({self.set!r})'
    def __pattern__(self, references):
      s = self.set
      #if not isinstance(s, (str, bytes, tuple)): s = tuple(s)
      return Pattern(self._scan, self, 1, 1, set=s)
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      s = pat.set
      i = pos + 1
      if pos < endpos and string[pos] not in s: return Result(Match(string, pos, endpos, ((pos, i),), value=string[pos:i]))
      return Result(error=ParsingError(f'expected one not in {s!r}', string, pos))

  # LEAF COMPONENTS #

  class match(Component):
    def __init__(self, pattern, ignore_case=False, *, _simplify_repr=False): self.pattern = pattern; self.ignore_case = ignore_case; self._simplify_repr = bool(_simplify_repr)
    def __repr__(self):
      #pattern = self.pattern
      #t = type(pattern)
      #if t in (str, bytes): return f'{pattern!r}'
      if self._simplify_repr: return repr(self.pattern)
      return f'{self.__class__.__name__}({self.pattern!r})'
    def __pattern__(self, references):
      pattern = self.pattern
      l = len(pattern)
      ignore_case = bool(self.ignore_case)
      return Pattern(self._scan, self, l, l, pattern=pattern, cmp=pattern.lower() if ignore_case else pattern, ignore_case=ignore_case)
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      cmp = pat.cmp
      pos2 = pos + len(cmp)
      if pos2 <= endpos and (string[pos:pos2].lower() if pat.ignore_case else string[pos:pos2]) == cmp: return Result(Match(string, pos, endpos, ((pos, pos2),), value=string[pos:pos2]))
      return Result(error=ParsingError(f'expected {pat.pattern!r}', string, pos, found=string[pos:pos2]))

  # GROUP/VALUE/ERROR MANIPULATION COMPONENTS #

  class group(Component):
    def __init__(self, *a, _simplify_repr=False):
      self._simplify_repr = bool(_simplify_repr)
      match a:
        case name, comp: self.named = True; self.name = name; self.comp = comp
        case comp,: self.named = False; self.name = None; self.comp = comp
        case _: XXX
    def __repr__(self):
      if self._simplify_repr:
        if self.named: return f'{{{self._repr_name!r}: {self.comp!r}}}'
        return f'[{self.comp!r}]'
      if self.named: return f'{self.__class__.__name__}({self.name!r}, {self.comp!r})'
      return f'{self.__class__.__name__}({self.comp!r})'
    def __pattern__(self, references):
      if self.named:
        n = self.name
        if type(n) != str: raise TypeError('group() name must be str')
      else: n = None
      l = len(references)
      references.append((n, None))
      p = compile(self.comp, references)
      g = p.groups + 1
      gi = p.groupindex
      if self.named: gi = gi | {self.name: g}
      p2 = Pattern(self._scan, self, p.min_length, p.max_length, g, gi, sub_pattern=p, namedgroup=bool(self.named), groupname=n)
      references[l] = (n, p)
      return p2
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      p = pat.sub_pattern
      rm = (*ref_matches, None)
      m, err, stop = r = p._scan(p, string, pos, endpos, rm)
      if err is not None: return r
      regdict = match_get_regdict(m)
      groupmatchdict = match_get_groupmatchdict(m)
      if pat.namedgroup:
        regdict[pat.groupname] = m.span(0)
        groupmatchdict[pat.groupname] = m
      return Result(Match(m.string, m.pos, m.endpos, m.regs + (m.span(0),), regdict=regdict, groupmatches=match_get_groupmatches(m) + (m,), groupmatchdict=groupmatchdict, value=m.value))

  class ungroup(Component):
    def __init__(self, comp, edit_func=None): self.comp = comp; self.edit_func = edit_func
    def __repr__(self):
      edit_func = self.edit_func
      edit_func = '' if edit_func is None else (f', {edit_func.__name__}' if isfunc(edit_func) else f', {edit_func!r}')
      return f'{self.__class__.__name__}({self.comp!r}{edit_func})'
    def __pattern__(self, references):
      p = compile(self.comp, references)
      return Pattern(self._scan, self, p.min_length, p.max_length, 0, {}, sub_pattern=p, edit_func=self.edit_func)
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      p = pat.sub_pattern; edit_func = pat.edit_func
      m, err, stop = r = p._scan(p, string, pos, endpos, ref_matches)
      if err is None: return Result(Match(string, pos, endpos, m.regs[:1], value=m.value if edit_func is None else edit_func(m)))
      return r

  class group_reference(Component):  # equiv '\\1' or '(?P=name)'
    def __init__(self, name): self.name = name
    def __repr__(self): return f'{self.__class__.__name__}({self.name!r})'
    def __pattern__(self, references):
      n = self.name
      if type(n) == int:
        if n > 0:
          try: g, p = references[n]
          except IndexError: pass
          else:
            if p is None: raise ValueError('cannot refer to an open group')  # re.compile('(\\1)')
            return Pattern(self._scan, self, p.min_length, p.max_length, 0, {}, name=n)
        raise ValueError(f'invalid group reference {n!r}')  # re.compile('\1')
      if type(n) == str:
        for g, p in references[1:]:
          if g == n:
            if p is None: raise ValueError('cannot refer to an open group')  # re.compile('(?P<name>(?P=name))')
            return Pattern(self._scan, self, p.min_length, p.max_length, 0, {}, name=n)
        raise ValueError(f'unknown group name {n!r}')  # re.compile('(?P=name)')
      raise TypeError(f'invalid group name {n!r}')
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      # here, pat.name IS a valid & legit index/name
      n = pat.name
      if type(n) == int:
        try: g, m = ref_matches[n]
        except IndexError: return Result(error=ParsingError('parsing stopped: invalid reference', string, pos))  # inconsistent parent that give a bad ref_matches
      else:
        for g, m in ref_matches[1:]:
          if g == n: break
        else: return Result(error=ParsingError('parsing stopped: invalid reference', string, pos))  # inconsistent parent that give a bad ref_matches
      if m is None: return Result(error=ParsingError('parsing stopped: reference to no match', string, pos))  # re.compile('(?:(a)|\\1)')
      return compile(match(m[0])).scan(string, pos, endpos)

  def isfunc(v): return type(v) == type(lambda:0)

  class edit(Component):
    def __init__(self, comp, edit_func): self.comp = comp; self.edit_func = edit_func
    def __repr__(self):
      edit_func = self.edit_func
      edit_func = edit_func.__name__ if isfunc(edit_func) else repr(edit_func)
      return f'{self.__class__.__name__}({self.comp!r}, {edit_func})'
    def __pattern__(self, references):
      p = compile(self.comp, references)
      return Pattern(self._scan, self, p.min_length, p.max_length, p.groups, p.groupindex, sub_pattern=p, edit_func=self.edit_func)
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      p = pat.sub_pattern; edit_func = pat.edit_func
      m, err, stop = r = p._scan(p, string, pos, endpos, ref_matches)
      if err is None: return Result(match_copy(m, value=edit_func(m)))
      return r

  class primitive(Component):
    def __init__(self, name, comp, edit_func=None):
      self.name = name
      self.comp = comp
      self.edit_func = edit_func
    def __repr__(self):
      edit_func = self.edit_func
      edit_func = f', {edit_func!r}' if edit_func is not None else ''
      return f'{self.__class__.__name__}({self.name!r}, {self.comp!r}{edit_func})'
    def __pattern__(self, references):
      n = self.name
      if type(n) != str: raise TypeError('name must be str')
      p = compile(self.comp, references)
      return Pattern(self._scan, self, p.min_length, p.max_length, 0, {}, sub_pattern=p, name=n, edit_func=self.edit_func)
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      p = pat.sub_pattern
      m, err, stop = r = p._scan(p, string, pos, endpos, ref_matches)
      if err is None:
        ef = pat.edit_func
        if ef is not None: return Result(match_copy(m, value=ef(m)), err, stop)
        return r
      if stop: return r
      return Result(m, ParsingError(f'expected {pat.name}', string, pos))

  class critical(Component):
    def __init__(self, comp, error_msg=None): self.comp = comp; self.error_msg = error_msg
    def __repr__(self):
      comp = self.comp; error_msg = self.error_msg
      error_msg = '' if error_msg is None else f', {error_msg!r}'
      return f'{self.__class__.__name__}({comp!r}{error_msg})'
    def __pattern__(self, references):
      em = self.error_msg
      if em is not None and type(em) != str: raise TypeError('error_msg must be str')
      p = compile(self.comp, references)
      return Pattern(self._scan, self, p.min_length, p.max_length, p.groups, p.groupindex, sub_pattern=p, error_msg=em)
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      p = pat.sub_pattern; em = pat.error_msg
      m, err, stop = r = p._scan(p, string, pos, endpos, ref_matches)
      if err is None or stop: return r
      if em is None: return Result(m, err, True)
      return Result(m, ParsingError(em, string, pos), True)

  class critical_pair(Component):
    def __init__(self, try_comp, crit_comp, error_msg=None):
      self.try_comp = try_comp
      self.crit_comp = crit_comp
      self.error_msg = error_msg
    def __repr__(self):
      error_msg = self.error_msg
      error_msg = '' if error_msg is None else f', {error_msg!r}'
      return f'{self.__class__.__name__}({self.try_comp!r}, {self.crit_comp!r}{error_msg})'
    def __pattern__(self, references):
      em = self.error_msg
      if em is not None and type(em) != str: raise TypeError('error_msg must be str')
      tp = compile(self.try_comp, references)
      cp = compile(self.crit_comp, references)
      return mix_chain_patterns((tp, cp), self._scan, self, error_msg=em)
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      tp, cp = pat.children; em = pat.error_msg
      m, err, stop = r = tp._scan(tp, string, pos, endpos, ref_matches)
      if err is not None: return r
      m2, err, stop = r = cp._scan(cp, string, m.end(), endpos, (*ref_matches, *zip_with_groupindex(match_get_groupmatches(m), tp.groupindex, -1)))
      if err is None: return Result(match_advance(m, m2, value=(m, m2)))
      if stop: return r
      return Result(None, ParsingError(err.msg if em is None else em, string, pos), True)

  # NODE COMPONENTS #

  class has(Component):  # propagate critical? yes
    def __init__(self, comp): self.comp = comp
    def __repr__(self): return f'{self.__class__.__name__}({self.comp!r})'
    def __pattern__(self, references):
      p = compile(self.comp, references)
      return Pattern(self._scan, self, 0, 0, p.groups, p.groupindex, sub_pattern=p)
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      p = pat.sub_pattern
      m, err, stop = r = p._scan(p, string, pos, endpos, ref_matches)
      if err is None: return Result(match_copy(m, start=pos, end=pos))
      return r

  class has_not(Component):  # propagate critical? yes
    def __init__(self, comp): self.comp = comp
    def __repr__(self): return f'{self.__class__.__name__}({self.comp!r})'
    def __pattern__(self, references):
      p = compile(self.comp, references)
      return Pattern(self._scan, self, 0, 0, p.groups, p.groupindex, sub_pattern=p)
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      p = pat.sub_pattern
      m, err, stop = r = p._scan(p, string, pos, endpos, ref_matches)
      if err is None: return Result(error=ParsingError('XXX', string, pos))
      if stop: return r
      return Result(match_advance_from_pattern(Match(string, pos, endpos, ((pos, pos),)), p, value=string[pos:pos]))

  class optional(Component):  # equiv '…?'
    def __init__(self, comp, *d):
      self.comp = comp
      match d:
        case default,: self.has_default = True; self.default = default
        case (): self.has_default = False; self.default = None
        case _: XXX
    def __repr__(self): return f'{self.__class__.__name__}({self.comp!r})'
    def __pattern__(self, references):
      p = compile(self.comp, references)
      return Pattern(self._scan, self, 0, p.max_length, p.groups, p.groupindex, sub_pattern=p, has_default=bool(self.has_default), default=self.default)
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      p = pat.sub_pattern
      m, err, stop = r = p._scan(p, string, pos, endpos, ref_matches)
      if err is None or stop: return r
      if pat.has_default: v = pat.default
      else: v = string[pos:pos]
      return Result(match_advance_from_pattern(Match(string, pos, endpos, ((pos, pos),)), p, value=v))

  def mix_chain_patterns(children, *a, **kw):
    i = iter(children)
    for p in i:
      min_length = p.min_length
      max_length = p.max_length
      groups = p.groups
      groupindex = dict(p.groupindex)
      break
    else:
      return Pattern(*a, min_length=0, max_length=0, groups=0, groupindex=frozenmapping(), children=children, **kw)
    for p in i:
      if min_length is None: pass
      elif p.min_length is None: min_length = None
      else: min_length += p.min_length
      if max_length is None: pass
      elif p.max_length is None: max_length = None
      else: max_length += p.max_length
      mi = 0
      for k, i in p.groupindex.items():
        if i is None:
          if k in groupindex:
            raise ValueError(f'redefinition of group name {k!r}')
          groupindex[k] = None
        else:
          gi = i + groups
          if gi > mi: mi = gi
          if k in groupindex:
            raise ValueError(f'redefinition of group name {k!r} as group {gi}')
          groupindex[k] = gi
      groups += p.groups
      if mi > groups: raise ValueError('inconsistent component: bad groupindex')
    return Pattern(*a, min_length=min_length, max_length=max_length, groups=groups, groupindex=frozenmapping(groupindex), children=children, **kw)

  def mix_select_patterns(children, *a, **kw):
    i = iter(children)
    for p in i:
      min_length = p.min_length
      max_length = p.max_length
      groups = p.groups
      groupindex = dict(p.groupindex)
      break
    else:
      return Pattern(*a, min_length=0, max_length=0, groups=0, groupindex=frozenmapping(), children=children, **kw)
    for p in i:
      if min_length is None: min_length = p.min_length
      elif p.min_length is None: pass
      elif min_length > p.min_length: min_length = p.min_length
      if max_length is None: pass
      elif p.max_length is None: max_length = None
      elif max_length < p.max_length: max_length = p.max_length
      mi = 0
      for k, i in p.groupindex.items():
        if i is None:
          if k in groupindex:
            raise ValueError(f'redefinition of group name {k!r}')
          groupindex[k] = None
        else:
          gi = i + groups
          if gi > mi: mi = gi
          if k in groupindex:
            raise ValueError(f'redefinition of group name {k!r} as group {gi}')
          groupindex[k] = gi
      groups += p.groups
      if mi > groups: raise ValueError('inconsistent component: bad groupindex')
    return Pattern(*a, min_length=min_length, max_length=max_length, groups=groups, groupindex=frozenmapping(groupindex), children=children, **kw)

  class chain(Component):
    def __init__(self, *comps, _repr_list=False): self.comps = list(comps); self._repr_list = bool(_repr_list)
    def __repr__(self):
      if self._repr_list:
        return f'[{", ".join(repr(_) for _ in self.comps)}]'
      return f'{self.__class__.__name__}({", ".join(repr(_) for _ in self.comps)})'
    def __pattern__(self, references):
      pp = (*(compile(_, references) for _ in self.comps),)
      return mix_chain_patterns(pp, self._scan, self)
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      value = []
      mb = None
      cur = pos
      rm = ref_matches
      for p in pat.children:
        m, err, stop = r = p._scan(p, string, cur, endpos, rm)
        if err is not None: return r
        value.append(m)
        if mb is None: mb = match_copy(r.match, value=value)
        else: mb = match_advance(mb, m, value=value)
        #rm = rm + match_get_groupmatches(m)
        rm = (*rm, *zip_with_groupindex(match_get_groupmatches(m), p.groupindex, -1))
        cur = m.end()
      if mb is None: return Result(Match(string, pos, endpos, ((pos, pos),), value=value))
      return Result(mb)

  class select(Component):
    def __init__(self, comp, *comps, get_index=False, names=(), group=False, _simplify_repr=False):
      self._simplify_repr = bool(_simplify_repr)
      self.comps = (comp,) + comps
      self.get_index = get_index
      self.names = list(names)
      self.group = bool(group)
    def _namecomppairs(self):
      n = self.names
      #return (((n[i:i+1] or [None])[0], c) for i, c in enumerate(self.comps))
      return (((n[i:i+1] or [i])[0], c) for i, c in enumerate(self.comps))
    def __repr__(self):
      # works because python dict is ordered dict
      if self._simplify_repr: return f'{{{", ".join(f"{n!r}: {v!r}" for n, v in self._namecomppairs())}}}'
      get_index = f', get_index=True' if self.get_index else ''
      names = f', names={self.names!r}' if len(self.names) else ''
      group = f', group=True' if self.group else ''
      return f'{self.__class__.__name__}({", ".join(repr(_) for _ in self.comps)}{names}{group})'
    def __pattern__(self, references):
      if self.group:
        #pp = (*(compile(group(n, c) if n is not None else group(c), references) for n, c in self._namecomppairs()),)
        pp = (*(compile(group(n, c) if type(n) == str else group(c), references) for n, c in self._namecomppairs()),)
        #pp = (*(compile(group(n, c) if type(n) == str else c, references) for n, c in self._namecomppairs()),)
      else:
        pp = (*(compile(c, references) for c in self.comps),)
      if len(pp) == 0: raise ValueError('invalid select() state')
      return mix_select_patterns(pp, self._scan, self, get_index=bool(self.get_index), names=tuple(self.names))
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      errpos = 0
      errors = []
      n = pat.names
      it = (((n[i:i+1] or [i])[0], p) for i, p in enumerate(pat.children))
      mb = None
      rm = ref_matches
      for i, p in it:
        m, err, stop = r = p._scan(p, string, pos, endpos, rm)
        if err is not None:
          if stop: return r
          if err.pos > errpos: errors[:] = (); errpos = err.pos
          errors.append(err)
          mb = match_advance_from_pattern(Match(string, pos, endpos, ((pos, pos),)) if mb is None else mb, p)
          #rm = rm + ((None, None),) * p.groups  # XXX review it !!! put group names !
          rm = (*rm, *zip_with_groupindex((None,) * p.groups, p.groupindex, -1))
        else:
          value = (i, m) if pat.get_index else m.value
          mb = match_advance(Match(string, pos, endpos, ((pos, pos),)) if mb is None else mb, m, start=m.start(), value=value)
          for i2, p2 in it: mb = match_advance_from_pattern(mb, p2, value=value)
          return Result(mb)
      errmsg = '; '.join(_.msg for _ in errors)
      return Result(error=ParsingError(errmsg, string, pos))

  # LOOP COMPONENTS #

  class until(Component):
    def __init__(self, step_comp, stop_comp, min_repeat=None, max_repeat=None, *, lazy=False):
      self.step_comp = step_comp
      self.stop_comp = stop_comp
      self.min_repeat = min_repeat
      self.max_repeat = max_repeat
      # here, lazy=True means that until() tries to check for stop_pattern as soon as possible
      self.lazy = bool(lazy)  # XXX find another name
    def __repr__(self):
      step_comp = self.step_comp; stop_comp = self.stop_comp; min_repeat = self.min_repeat; max_repeat = self.max_repeat; lazy = self.lazy
      min_repeat = '' if min_repeat is None else f', min_repeat={min_repeat!r}'
      max_repeat = '' if max_repeat is None else f', max_repeat={max_repeat!r}'
      lazy = ', lazy=True' if lazy else ''
      return f'{self.__class__.__name__}({step_comp!r}, {stop_comp!r}{min_repeat}{max_repeat}{lazy})'
    def __pattern__(self, references):
      min_repeat = self.min_repeat
      if min_repeat is None: min_repeat = 0
      elif min_repeat < 0: raise ValueError('min_repeat must be >= 0')
      max_repeat = self.max_repeat
      if max_repeat is None: pass  # inf
      elif max_repeat < 0: raise ValueError('max_repeat must be >= 0')
      elif min_repeat > max_repeat: raise ValueError('min_repeat must be <= max_repeat')
      sp = compile(self.step_comp, references)
      tp = compile(self.stop_comp, references)
      min_length = sp.min_length * min_repeat
      max_length = None if max_repeat is None or sp.max_length is None else sp.max_length * max_repeat
      min_length += tp.min_length
      max_length = None if max_repeat is None or tp.max_length is None else max_length + tp.max_length
      p = mix_chain_patterns([sp, tp], None, self)  # XXX use mix_patterns()?
      return Pattern(self._scan, self, min_length, max_length, p.groups, p.groupindex, step_pattern=sp, stop_pattern=tp, min_repeat=min_repeat, max_repeat=max_repeat, lazy=bool(self.lazy))
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      sp = pat.step_pattern; tp = pat.stop_pattern; min_repeat = pat.min_repeat; max_repeat = pat.max_repeat; lazy = pat.lazy; value = []
      i = 0
      step_not_advancing = False
      _step = i < min_repeat or not lazy and i != max_repeat
      if _step: gm = []; rm = ref_matches
      else: gm = [None] * sp.groups; rm = (*ref_matches, *zip_with_groupindex(gm, sp.groupindex, -1))
      mb = None
      cur = pos
      #_debug = 0  # XXX
      while 1:
        #if _debug == 1000: break
        #_debug += 1
        if _step:
          #print('lazy' if lazy else 'greedy', 'step', i)
          if step_not_advancing: return Result(error=ParsingError('XXX last step error', string, pos))
          m, err, stop = r = sp._scan(sp, string, cur, endpos, rm)
          if err is None:
            i += 1
            value.append(m)
            gm = groupmatches_mix_match(gm, m)
            rm = (*ref_matches, *zip_with_groupindex(gm, sp.groupindex, -1))
            if mb is None: mb = match_advance(Match(string, cur, endpos, (m.span(0),)), m)
            else: mb = match_update(mb, m)
            if cur >= m.end():
              step_not_advancing = True
              if i < min_repeat:
                value.extend([m] * (min_repeat - i))
                i = min_repeat
            else:
              cur = m.end()
            if i >= min_repeat:
              if lazy or i == max_repeat or step_not_advancing: _step = False
          else:
            if stop: return r
            if i < min_repeat: return r  # expected step
            if lazy:
              return r  # XXX use better error, like expected step or stop
            else:  # greedy
              _step = False
        else:
          #print('lazy' if lazy else 'greedy', 'stop', i)
          m, err, stop = r = tp._scan(tp, string, cur, endpos, rm)
          if err is None:
            value.append(m)
            if mb is None: mb = match_advance_from_pattern(Match(string, cur, endpos, (m.span(0),)), sp)
            mb = match_advance(mb, m, value=value)
            return Result(mb)
          else:
            if stop: return r
            if i == max_repeat: return r  # expected stop
            if lazy:
              _step = True
            else:  # greedy
              return r  # XXX use better error, like expected step or stop
      raise RuntimeError('<unreachable code>')

  #class many2(Component):  # equiv '…+' or '…{m,n}' or until(step, NOTHING, min_repeat=m, max_repeat=n)
  #  def __init__(self, comp, min_repeat=None, max_repeat=None):
  #    self.comp = comp
  #    self.min_repeat = min_repeat
  #    self.max_repeat = max_repeat
  #  def __repr__(self):
  #    comp = self.comp; min_repeat = self.min_repeat; max_repeat = self.max_repeat
  #    if max_repeat is not None:
  #      min_repeat = f', {min_repeat!r}'
  #      max_repeat = f', {max_repeat!r}'
  #    else:
  #      min_repeat = '' if min_repeat is None else f', {min_repeat!r}'
  #      max_repeat = ''  # max_repeat is None
  #    return f'{self.__class__.__name__}({comp!r}{min_repeat}{max_repeat})'
  #  def __pattern__(self, references):
  #    min_repeat = self.min_repeat
  #    if min_repeat is None: min_repeat = 1
  #    elif min_repeat < 0: raise ValueError('min_repeat must be >= 0')
  #    max_repeat = self.max_repeat
  #    if max_repeat is None: pass  # inf
  #    elif max_repeat < 0: raise ValueError('max_repeat must be >= 0')
  #    elif min_repeat > max_repeat: raise ValueError('min_repeat must be <= max_repeat')
  #    p = compile(self.comp, references)
  #    min_length = p.min_length * min_repeat
  #    max_length = None if max_repeat is None or p.max_length is None else p.max_length * max_repeat
  #    return Pattern(self._scan, self, min_length, max_length, p.groups, p.groupindex, sub_pattern=p, min_repeat=min_repeat, max_repeat=max_repeat)
  #  @staticmethod
  #  def _scan(pat, string, pos, endpos, ref_matches):
  #    p = pat.sub_pattern; min_repeat = pat.min_repeat; max_repeat = pat.max_repeat
  #    mb = None
  #    rm = ref_matches; gm = None
  #    value = []
  #    cur = pos
  #    i = 0
  #    r = None
  #    while i != max_repeat:
  #      m, err, stop = r = p._scan(p, string, cur, endpos, rm)
  #      if err is not None:
  #        if stop or i < min_repeat: return r
  #        if mb is None: mb = match_advance_from_pattern(Match(string, pos, endpos, ((pos, pos),)), p, value=value)
  #        return Result(mb)
  #      if mb is None: mb = match_copy(m, value=value)
  #      else: mb = match_update(mb, m, value=value)
  #      if cur >= m.end():
  #        value.extend([m] * (min_repeat - i))
  #        return Result(mb)
  #      value.append(m)
  #      cur = m.end()
  #      if gm is None: gm = list(match_get_groupmatches(m))
  #      else: gm = groupmatches_mix_match(gm, m)
  #      rm = (*ref_matches, *zip_with_groupindex(gm, p.groupindex, -1))
  #      i += 1
  #    if i >= min_repeat:
  #      if mb is None: mb = match_advance_from_pattern(Match(string, pos, endpos, ((pos, pos),)), p, value=value)
  #      return Result(mb)
  #    #if r is None: raise RuntimeError('many() inconsistent min_repeat & max_repeat arguments')
  #    return r

  class many(Component):  # equiv '…+' or '…{m,n}' or until(step, NOTHING, min_repeat=m, max_repeat=n)
    def __init__(self, comp, min_repeat=None, max_repeat=None):
      self.comp = comp
      self.min_repeat = min_repeat
      self.max_repeat = max_repeat
    def __repr__(self):
      comp = self.comp; min_repeat = self.min_repeat; max_repeat = self.max_repeat
      if max_repeat is not None:
        min_repeat = ', 1' if min_repeat is None else f', {min_repeat!r}'
        max_repeat = f', {max_repeat!r}'
      else:
        min_repeat = '' if min_repeat is None else f', {min_repeat!r}'
        max_repeat = ''  # max_repeat is None
      return f'{self.__class__.__name__}({comp!r}{min_repeat}{max_repeat})'
    def __pattern__(self, references):
      min_repeat = self.min_repeat
      p = compile(until(self.comp, NOTHING, 1 if min_repeat is None else min_repeat, self.max_repeat), references)
      return Pattern(self._scan, self, p.min_length, p.max_length, p.groups, p.groupindex, sub_pattern=p)
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      p = pat.sub_pattern
      m, err, stop = r = p._scan(p, string, pos, endpos, ref_matches)
      if err is None: return Result(match_copy(m, value=m.value[:-1]))
      return r

  class search(Component):
    def __init__(self, comp): self.comp = comp
    def __repr__(self): return f'{self.__class__.__name__}({self.comp!r})'
    def __pattern__(self, references):
      p = compile(until(ONE, self.comp, lazy=True), references)
      return Pattern(self._scan, self, p.min_length, p.max_length, p.groups, p.groupindex, sub_pattern=p)
    @staticmethod
    def _scan(pat, string, pos, endpos, ref_matches):
      p = pat.sub_pattern
      m, err, stop = r = p._scan(p, string, pos, endpos, ref_matches)
      if err is None: return Result(m.value[-1])
      return r

  def expand_bytes_parser():
    def mk_parser(enc, join):  # XXX use compile replacer to enc() str automatically
      token = primitive  # XXX
      _bsol_dict = {enc(a): enc(b) for a, b in ('\\\\', 'a\a', 'b\b', 'f\f', 'n\n', 'r\r', 't\t', 'v\v')}
      _BSOL = enc('\\')
      _0 = enc('0')

      BSOL = match(_BSOL)
      O = token('octal digit', one_in(enc('01234567')))
      #D47 = one_in(enc('4567'))
      D = token('decimal digit', one_in(enc('0123456789')))
      D1 = one_in(enc('123456789'))
      D03 = one_in(enc('0123'))

      OCTAL_ESCAPE_VALUE = token(
        'octal escape value',
        select(
          chain(
            has(chain(O, O, O)),
            critical(chain(D03, O, O), 'octal escape outside of range 0-0o377')
            ),
          chain(match(_0), optional(O)),
        ),
        lambda m: chr(int(m[0], 8)))  # -> str
        #lambda m: ['octal', int(m[0], 8)])  # -> ['octal', Oo377]

      GROUP_INDEX_ESCAPE_VALUE = token(
        'group index escape value',
        chain(D1, optional(D)),
        lambda m: ['group', int(m[0], 10)])  # -> ['group', 99]

      def parse_group(m):
        # XXX handle \\g<~> bad character in group name '~'
        name = m[0][2:-1]
        try: name = int(name if isinstance(name, str) else bytes(name), 10)  # only works with str and bytes-like object
        except ValueError: pass
        return ['group', name]

      GROUP_NAME_ESCAPE_VALUE = token(
        'group name escape',
        chain(match(enc('g')), critical(chain(match(enc('<')), token('group name', one_not_in(enc('>'))), search(match(enc('>')))))),
        parse_group)  # -> ['group', 99 or 'name']

      CHAR_ESCAPE_VALUE = edit(
        one_in(enc('\\abfnrtv')),
        lambda m: _bsol_dict[m[0]])  # -> str
        #lambda m: ['escaped_char', m[0]])  # -> list

      NON_ASCII_ESCAPE_VALUE = token(
        'non ascii character',
        one_not_in(enc('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')),  # alphanum
        lambda m: m[0])  # -> str
        #lambda m: ['escaped_char', m[0]])  # -> list

      ## XXX
      #ESCAPE1 = token(
      #  'escaped sequence',
      #  chain(BSOL, critical(select(  # XXX on_critical(chain(BSOL, critical(…)), 'bad escape') ??
      #    OCTAL_ESCAPE_VALUE,        # '\\377' or '\\04'
      #    GROUP_INDEX_ESCAPE_VALUE,  # '\\99'
      #    GROUP_NAME_ESCAPE_VALUE,   # '\\g<name>'
      #    CHAR_ESCAPE_VALUE,         # '\\n'
      #    NON_ASCII_ESCAPE_VALUE,    # '\\é'
      #  ), 'bad escape')),
      #  lambda m: m.value[1].value)  # -> list | str
      ## XXX
      #ESCAPE2 = select(
      #  edit(chain(BSOL, select(
      #    OCTAL_ESCAPE_VALUE,        # '\\377' or '\\04'
      #    GROUP_INDEX_ESCAPE_VALUE,  # '\\99'
      #    GROUP_NAME_ESCAPE_VALUE,   # '\\g<name>'
      #    CHAR_ESCAPE_VALUE,         # '\\n'
      #  )), lambda m: m.value[1].value),
      #  #edit(critical_pair(BSOL, NON_ASCII_ESCAPE_VALUE, lambda sr: f'bad escape {sr[0][0]}'), lambda m: XXX),
      #  edit(critical_pair(BSOL, NON_ASCII_ESCAPE_VALUE, 'bad escape'), lambda m: m.value[1].value),
      #)
      # XXX
      ESCAPE = edit(critical_pair(BSOL, select(
        OCTAL_ESCAPE_VALUE,        # '\\377' or '\\04'
        GROUP_INDEX_ESCAPE_VALUE,  # '\\99'
        GROUP_NAME_ESCAPE_VALUE,   # '\\g<name>'
        CHAR_ESCAPE_VALUE,         # '\\n'
        NON_ASCII_ESCAPE_VALUE,    # '\\é'
      ), 'bad escape'), lambda m: m.value[1].value)

      NO_ESCAPE_CHAR = token('unescaped character', one_not_in(_BSOL))  # -> str

      EXPAND_STEP = select(
        ESCAPE,          # '\\…'
        NO_ESCAPE_CHAR,  # '…'
      )  # -> list | str

      def join_expand_steps(m):
        r = ['expand']
        v = e = m.string[:0]
        steps = m.value[:-1]
        if steps:
          for m in steps:
            if isinstance(m.value, list):
              if v: r.append(v); v = e
              r.append(m.value)
            else:
              v += m.value
          if v: r.append(v)
        else:
          r.append(v)
        return r

      EXPAND = edit(
        until(EXPAND_STEP, EOF),
        join_expand_steps)  # -> ['expand', list | str, …]

      return compile(EXPAND)
    return mk_parser(lambda i: i, ''.join), mk_parser(lambda i: i.encode(), b''.join)
  expand_str_parser, expand_bytes_parser = expand_bytes_parser()

  #print(expand_str_parser.parse('\\'))  # XXX "bad escape (end of pattern) at position 0" != "bad escape: position 1", ok?
  #print(expand_str_parser.parse('\\g'))  # XXX "missing < at position 2" != "expected '<': position 2", ok?
  #print(expand_str_parser.parse('\\g<'))  # XXX "missing group name at position 3" != "expected group name: position 3", ok?
  #print(expand_str_parser.parse('\\g<a'))  # XXX "missing >, unterminated name at position 3" != "expected one element: position 4", ok?
  #print(expand_str_parser.parse('\\400'))  # XXX "octal escape value \\400 outside of range 0-0o377 at position 0" != "octal escape outside of range 0-0o377: position 1", ok?
  #print(expand_str_parser.parse('\\c'))  # XXX "bad escape \\c at position 0" != "bad escape: position 0", ok?
                                          #     to get "\c", we have to get partial/error Match() :thinking:
                                          #     to get correct position, we can do a format_error(chain(BSOL, critical(…)), lambda sr: f'bad escape {sr[0]}')
                                          #     → error_msg.format(*scan_result, value=scan_results[0].value, match=scan_result[0], error=scan_result[1]})
                                          #     → but it is incompatible with "missing <" as it rephrase to error…
  #print(expand_str_parser.parse('lol\\n\\0\\1lal\\23\\345\\g<a>\\élul'))

  __locals = locals()
  for __ in __locals.get('__all__', __locals):
    if __ in __locals and not __.startswith('__'):
      setattr(export, __, __locals[__])
  return export

parsertools = parsertools()
#from parsertools import *
#for _ in dir(parsertools): locals()[_] = getattr(parsertools, _)
