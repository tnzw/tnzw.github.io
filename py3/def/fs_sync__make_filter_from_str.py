# fs_sync__make_filter_from_str.py Version 1.0.0
#
#   This is free and unencumbered software released into the public domain.
#
#   Anyone is free to copy, modify, publish, use, compile, sell, or
#   distribute this software, either in source code form or as a compiled
#   binary, for any purpose, commercial or non-commercial, and by any
#   means.
#
#   In jurisdictions that recognize copyright laws, the author or authors
#   of this software dedicate any and all copyright interest in the
#   software to the public domain. We make this dedication for the benefit
#   of the public at large and to the detriment of our heirs and
#   successors. We intend this dedication to be an overt act of
#   relinquishment in perpetuity of all present and future rights to this
#   software under copyright law.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#   IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
#   OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#   ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#   OTHER DEALINGS IN THE SOFTWARE.
#
#   For more information, please refer to <https://unlicense.org/>
#
#   Contributors: 2025 <tnzw@github.triton.ovh>

# TODO avoid to override encode() when _bytestr encoding? Make a codec? How to do it light?
def fs_sync__make_filter_from_str(filter_str, *, encoding=None, use_win32_sep=False, ignorecase=False, disable_wildcards=False, force_match_absolute=False, strip_trailing_spaces=False):
  r"""This creates a function that could be used in the `filter=` parameter of the
`fs_sync()` tool.  Its syntax tries to look like original rsync filter one (see
man rsync for more information) with some additional features.

This filter does not use sys calls at all.  So the merge rules does not exist.

The `encoding` parameter will be used to encode each pattern to bytes using the
`encode()` method (or using bytes() func if encoding='_bytestr').

The `filter_str` syntax:

    RULE [PATTERN_OR_FILENAME]
    RULE,MODIFIERS [PATTERN_OR_FILENAME]

RULE:

  *exclude*, *-* specifies an exclude pattern.
  *include*, *+* specifies an include pattern.
  *hide*, *H* specifies a pattern for hiding files from the transfer.
  *show*, *S* files that match the pattern are not hidden.
  *protect*, *P* specifies a pattern for protecting files from deletion.
  *risk*, *R* files that match the pattern are not protected.
  *clear*, *!* clears the current include/exclude list (takes no arg).
  *HP*, *~* is like the combination of *H* and *P*. (not in rsync)
  *SR*, *=* is like the combination of *S* and *R*. (not in rsync)
  `*` includes pattern and its parent directories. (not in rsync)

MODIFIERS:

  *!* rule should take effect if pattern fails to match.
  *s* applies the rule to the sending side.
  *r* applies the rule to the receiving side.
  *x* use pattern as a python regexp. (not in rsync)

PATTERN_OR_FILENAME:

  Used as normal pattern, it uses rsync wildcard characters `*?[`.
    See man rsync for more info. (/!\ `[]` is not implemented yet)
  Used as python regexp pattern, see python `re` doc for more info.

Python regexp examples:

  `+x /(foo|bar)` would match `foo` and `bar`, but not `foo/bar`.
    -> equiv regexp `\A(foo|bar)\Z`.

  `+x (foo|bar)` would match `foo`, `bar` and `foo/bar`.
    -> equiv regexp `(\A|/)(foo|bar)\Z`.

Encoding examples:

    make_filter('+ /caf\u00e9')                         # => '\\Acaf\u00e9\\Z'
    make_filter('+ /caf\u00e9', encoding='utf8')        # => b'\\Acaf\xc3\xa9\\Z'
    make_filter('+ /caf\xc3\xa9', encoding='_bytestr')  # => b'\\Acaf\xc3\xa9\\Z'
    make_filter('+x /caf\\xc3\\xa9', encoding='utf8')   # => b'\\Acaf\\xc3\\xa9\\Z'
"""
  use_win32_sep = bool(use_win32_sep)  # wether to convert `\` to `/` before matching regexp
  ignorecase = bool(ignorecase)
  disable_wildcards = bool(disable_wildcards)
  force_match_absolute = bool(force_match_absolute)
  if encoding == '_bytestr': encode = lambda s: bytes(ord(c) for c in s)
  elif encoding is None: encode = lambda s: s
  else: encode = lambda s: s.encode(encoding)

  rules = []
  # parse lines
  for line in filter_str.split('\n'):
    orig_line = line
    line = line.lstrip(' ')
    if not line or line[:1] == '#': continue

    # parse RULE
    rule = ''; sr_rule = '--'
    # '-' no rule applied
    # 'p' protect rule applied, could be overriden by another uppercase rule or by fs_sync() parameters
    # 'r' risk rule applied, could be overriden by another uppercase rule or by fs_sync() parameters
    # 'P' protect rule applied, could not be overriden
    # 'R' risk rule applied, could not be overriden
    # 'S' show rule applied
    # 'H' hide rule applied
    if   line[:1] == '-':       rule = '-';       sr_rule = 'Hp'; line = line[1:]
    elif line[:1] == '+':       rule = '+';       sr_rule = 'Sr'; line = line[1:]
    elif line[:1] == '~':       rule = '~';       sr_rule = 'HP'; line = line[1:]
    elif line[:1] == '=':       rule = '=';       sr_rule = 'SR'; line = line[1:]
    elif line[:1] == '*':       rule = '*';       sr_rule = 'Sr'; line = line[1:]
    elif line[:1] == 'H':
      if   line[1:2] == 'P':    rule = 'HP';      sr_rule = 'HP'; line = line[2:]
      elif line[1:2] == 'R':    rule = 'HR';      sr_rule = 'HR'; line = line[2:]
      else:                     rule = 'H';       sr_rule = 'H-'; line = line[1:]
    elif line[:1] == 'S':
      if   line[1:2] == 'P':    rule = 'SP';      sr_rule = 'SP'; line = line[2:]
      elif line[1:2] == 'R':    rule = 'SR';      sr_rule = 'SR'; line = line[2:]
      else:                     rule = 'S';       sr_rule = 'S-'; line = line[1:]
    elif line[:1] == 'P':       rule = 'P';       sr_rule = '-P'; line = line[1:]
    elif line[:1] == 'R':       rule = 'R';       sr_rule = '-R'; line = line[1:]
    elif line[:7] == 'exclude': rule = 'exclude'; sr_rule = 'Hp'; line = line[7:]
    elif line[:7] == 'include': rule = 'include'; sr_rule = 'Sr'; line = line[7:]
    elif line[:4] == 'hide':    rule = 'hide';    sr_rule = 'H-'; line = line[4:]
    elif line[:4] == 'show':    rule = 'show';    sr_rule = 'S-'; line = line[4:]
    elif line[:7] == 'protect': rule = 'protect'; sr_rule = '-P'; line = line[7:]
    elif line[:4] == 'risk':    rule = 'risk';    sr_rule = '-R'; line = line[4:]
    elif line[:1] == '!':
      # rule = '!'
      line = line[1:]
      if line: raise ValueError(f"'!' rule as trailing characters: {orig_line!r}")
      rules[:] = ()
      continue
    elif line[:5] == 'clear':
      # rule = 'clear'
      line = line[5:]
      if line: raise ValueError(f"'!' rule as trailing characters: {orig_line!r}")
      rules[:] = ()
      continue
    else:
      raise ValueError(f"unknown filter rule: {orig_line!r}")

    # parse MODIFIERS
    reverse_match = regexp_pattern = False
    ignorecase_match = ignorecase
    while True:
      if line[:1] == '!':
        if rule in ('-', '+', '~', '=', 'H', 'S', 'P', 'R', 'HP', 'HR', 'SP', 'SR', 'exclude', 'include', 'show', 'hide', 'protect', 'risk'): reverse_match = True; line = line[1:]
        else: raise ValueError(f"invalid modifier {line[:1]!r}: {orig_line!r}")
      elif line[:1] == 'r':
        if   rule == '-':        sr_rule = '-P'; line = line[1:]
        elif rule in ('+', '*'): sr_rule = '-R'; line = line[1:]
        else: raise ValueError(f"invalid modifier {line[:1]!r}: {orig_line!r}")
      elif line[:1] == 's':
        if   rule == '-':        sr_rule = 'H-'; line = line[1:]
        elif rule in ('+', '*'): sr_rule = 'S-'; line = line[1:]
        else: raise ValueError(f"invalid modifier {line[:1]!r}: {orig_line!r}")
      elif line[:1] == 'i':
        if rule in ('HR', 'HP', 'SP', 'SR', 'include', 'exclude', 'show', 'hide', 'protect', 'risk'): raise ValueError(f"invalid modifier {line[:1]!r}: {orig_line!r}")
        ignorecase_match = True; line = line[1:]
      elif line[:1] == 'I':
        if rule in ('HR', 'HP', 'SP', 'SR', 'include', 'exclude', 'show', 'hide', 'protect', 'risk'): raise ValueError(f"invalid modifier {line[:1]!r}: {orig_line!r}")
        ignorecase_match = False; line = line[1:]
      elif line[:1] == 'x':
        if rule in ('*', 'HR', 'HP', 'SP', 'SR', 'include', 'exclude', 'show', 'hide', 'protect', 'risk'): raise ValueError(f"invalid modifier {line[:1]!r}: {orig_line!r}")
        regexp_pattern = True; line = line[1:]
      else:
        break
    # TODO prevent applying same modifier several times
    re_flags = re.I if ignorecase_match else 0
    if line[:1] not in (' ', '_'): raise ValueError(f"invalid modifier {line[:1]!r}: {orig_line!r}")
    line = line[1:]
    if strip_trailing_spaces: line = line.strip(' ')

    # NB: match_fullpath here is not used, but I keep it in the code, maybe one
    #     day I'll write some optimizations using this variable.

    # parse PATTERN_OR_FILENAME as python regexp
    if regexp_pattern:
      match_absolute = force_match_absolute
      match_dir_only = False
      if line[:1] == '/':
        match_absolute = True
        line = line[1:]
      if line[-1:] == '/':
        match_dir_only = True
        line = line[:-1]
      # if not line: raise ValueError(f"empty pattern: {orig_line!r}")  # rsync doesn't fail, it might just produce a never matching pattern
      pattern = line
      if match_absolute:
        pattern = '\\A' + pattern + '\\Z'  # `/foo` -> `\Afoo\Z`
      else:  # always using fullpath match so far
        pattern = '\\A(?:.*/|)' + pattern + '\\Z'  # `foo/bar` -> `\A(?:.*/|)foo/bar\Z` using my_re.match(fullpath)
      pattern = encode(pattern)
      rules.append((*sr_rule, [(re.compile(pattern, re_flags), match_absolute, True, match_dir_only)], reverse_match))

    elif disable_wildcards:
      match_absolute = force_match_absolute
      match_fullpath = match_dir_only = False
      if line[:1] == '/':
        match_absolute = True
        line = line[1:]
      if line[-1:] == '/':
        match_dir_only = True
        line = line[:-1]
      if '/' in line:
        match_fullpath = True
      # if not line: raise ValueError(f"empty pattern: {orig_line!r}")  # rsync doesn't fail, it might just produce a never matching pattern
      pattern = re.escape(line)
      pattern2 = ''
      if rule == '*':  # `* me/project/src/file` -> `\Ame(?:/project(?:/src|)|)\Z` DIR + `\Ame/project/src/file\Z`
        psplit = pattern.split('/')  # re.escape() does not escape `/`
        l = len(psplit)
        if l > 2: pattern2 = '(?:/'.join(psplit[:-1]) + '|)' * (l - 2)
      if match_absolute: a, z = '\\A', '\\Z'  # `/foo` -> `\Afoo\Z`
      elif match_fullpath: a, z = '\\A(?:.*/|)', '\\Z'  # `foo/bar` -> `\A(?:.*/|)foo/bar\Z` using my_re.match(fullpath)
      # elif match_fullpath: a, z = '(?:\\A|/)', '\\Z'  # `foo/bar` -> `(?:\A|/)foo/bar...` using my_re.search(fullpath)
      else: a, z = '\\A(?:.*/|)', '\\Z'  # `foo` -> `\A(?:.*/|)foo\Z` using my_re.match(fullpath)
      # else: a, z = '\\A', '\\Z'  # `foo` -> `\Afoo...` using my_re.match(basename)
      pattern = encode(a + pattern + z)
      if rule == '*' and pattern2:
        pattern2 = encode(a + pattern2 + z)
        rules.append((*sr_rule, [(re.compile(pattern,  re_flags), match_absolute, True, match_dir_only),
                                 (re.compile(pattern2, re_flags), match_absolute, True, True)], reverse_match))
      else:
        rules.append((*sr_rule, [(re.compile(pattern, re_flags), match_absolute, match_fullpath, match_dir_only)], reverse_match))

    # parse PATTERN_OR_FILENAME as rsync pattern
    # XXX make optimizations for specific rule like '*', '**', ...? ex
    #     elif line == '*': rules.append((*sr_rule, [(re.compile('.', re_flags), False, False, False)], reverse_match)); continue
    #     elif line == '**': rules.append((*sr_rule, [(re.compile('.', re_flags), False, True, False)], reverse_match)); continue
    else:
      pattern = []; p = 0
      match_absolute = force_match_absolute
      match_fullpath = match_dir_only = triple_star = double_star = False
      splits = []  # used for rule == '*'
      i = 0; l = len(line)
      while i < l:
        c = line[i]
        if   c in '[]':
          raise NotImplementedError(f"`[]` special chars are not implemented: {orig_line!r}")  # XXX TODO
        elif c == '\\':
          if i + 1 >= l: raise ValueError(f"bad escape (end of line): {orig_line!r}")  # does rsync allow escaping eol?  I do not (so far)
          c2 = line[i + 1]
          if c2 in '*?[]': r = re.escape(c2); pattern.append(r); p += len(r); i += 2
          else: pattern.append('\\\\'); p += 2; i += 1
        elif c == '?':
          pattern.append('[^/]'); p += 4
          i += 1
        elif i + 4 == l and line[i:i + 4] == '/***':
          match_fullpath = triple_star = True
          i += 4
        elif i + 3 == l and line[i:i + 3] == '**/':
          match_fullpath = match_dir_only = double_star = True
          i += 3
        elif i + 2 <= l and line[i:i + 2] == '**':
          match_fullpath = True
          i += 2
          if i == l:
            double_star = True
          else:
            pattern.append('.*?'); p += 3
            while i < l and line[i] == '*': i += 1
        elif c == '*':
          pattern.append('[^/]*?'); p += 6
          i += 1
        elif i == 0 and c == '/':
          match_fullpath = match_absolute = True
          # if i + 1 == l: match_dir_only = True
          i += 1
        elif i + 1 == l and c == '/':
          match_dir_only = True
          i += 1
        elif c == '/':
          pattern.append('/'); p += 1
          match_fullpath = True
          splits.append(p - 1)
          i += 1
        else:
          r = re.escape(c)
          pattern.append(r); p += len(r)
          i += 1
      pattern = ''.join(pattern)
      # if not pattern: raise ValueError(f"empty pattern: {orig_line!r}")  # rsync doesn't fail, it might just produce a never matching pattern
      if rule == '*':  # `* me/project/src/file` -> `\Ame(?:/project(?:/src|)|)\Z` DIR + `\Ame/project/src/file\Z`
        p2split = []; j = 0
        for l in splits:
          p2split.append(pattern[j:l])
          j = l + 1
        splits = None
        p2split.append(pattern[j:])
      if match_absolute: a = '\\A'  # `/foo` -> `\Afoo...`
      elif match_fullpath: a = '\\A(?:.*/|)'  # `foo/bar` -> `\A(?:.*/|)foo/bar...` using my_re.match(fullpath)
      # elif match_fullpath: a = '(?:\\A|/)'  # `foo/bar` -> `(?:\A|/)foo/bar...` using my_re.search(fullpath)
      else: a = '\\A(?:.*/|)'  # `foo` -> `\A(?:.*/|)foo...` using my_re.match(fullpath)
      # else: a = '\\A'  # `foo` -> `\Afoo...` using my_re.match(basename)
      if triple_star:  # pattern ending with `/***`
        pattern1 = encode(a + pattern + '/')
        if rule == '*' and len(p2split) >= 2:
          pattern2 = '(?:/'.join(p2split) + '|)' * (len(p2split) - 1)
          pattern2 = encode(a + pattern2 + '\\Z')
        else:
          pattern2 = encode(a + pattern + '\\Z')
        rules.append((*sr_rule, [(re.compile(pattern1, re_flags), match_absolute, True, False),
                                 (re.compile(pattern2, re_flags), match_absolute, True,  True)], reverse_match))
      elif double_star:  # pattern ending with `**` or `**/`
        pattern = encode(a + pattern)
        if rule == '*' and len(p2split) >= 2:
          pattern2 = '(?:/'.join(p2split[:-1]) + '|)' * (len(p2split) - 2)
          pattern2 = encode(a + pattern2 + '\\Z')
          rules.append((*sr_rule, [(re.compile(pattern,  re_flags), match_absolute, True, match_dir_only),
                                   (re.compile(pattern2, re_flags), match_absolute, True, True)], reverse_match))
        else:
          rules.append((*sr_rule, [(re.compile(pattern, re_flags), match_absolute, True, match_dir_only)], reverse_match))
      # elif single_star:  # pattern ending with `*` or `*/`  # no optimization possible?
      else:
        pattern = encode(a + pattern + '\\Z')
        if rule == '*' and len(p2split) >= 2:
          pattern2 = '(?:/'.join(p2split[:-1]) + '|)' * (len(p2split) - 2)
          pattern2 = encode(a + pattern2 + '\\Z')
          rules.append((*sr_rule, [(re.compile(pattern,  re_flags), match_absolute, True, match_dir_only),
                                   (re.compile(pattern2, re_flags), match_absolute, True, True)], reverse_match))
        else:
          rules.append((*sr_rule, [(re.compile(pattern, re_flags), match_absolute, match_fullpath, match_dir_only)], reverse_match))

  if use_win32_sep:
    if encoding is not None: replacer = lambda s: s.replace(b'\\', b'/')
    else: replacer = lambda s: s.replace('\\', '/')
  else:
    replacer = lambda s: s

  # for rule in rules: print(rule)
  def fs_sync_filter(path, is_dir):
    if use_win32_sep: path = replacer(path)
    S, R = '-', '-'
    for s_rule, r_rule, patterns, reverse_match in rules:
      matches = False
      for r, mabs, mpath, mdir in patterns:
        # print('matching', 'directory' if mdir else 'node', r, 'against', path + ('/' if is_dir else '') if isinstance(path, str) else (b'/' if is_dir else b''))
        if ((mdir and is_dir) or not mdir) and r.match(path): matches = True; break
      if reverse_match: matches = not matches
      # if matches: print('-> match!')
      if matches:
        if S not in ('S', 'H'):
          if s_rule in ('S', 'H') or S not in ('s', 'h'): S = s_rule
        if R not in ('P', 'R'):
          if r_rule in ('P', 'R') or R not in ('p', 'r'): R = r_rule
        if S in ('S', 'H') and R in ('P', 'R'): break
    if S == '-': S = 'S'
    if R == '-': R = 'r'
    return S + R

  return fs_sync_filter

fs_sync__make_filter_from_str._required_globals = ['re']
