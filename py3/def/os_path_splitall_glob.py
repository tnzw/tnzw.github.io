# os_path_splitall_glob.py Version 1.0.1
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_path_splitall_glob(pathcomps, patterncomps, *, os_module=None, ignore_case=None, recursive=False):
  # A pathcomps is a sequence of path components. It is usualy returned by the os_path_splitall() function.
  # It's usualy a tuple (drive, root, comp_name1, comp_name2, ...).
  # This function uses os.sep, os.curdir, os.lstat(), os.listdir() ; os.altsep is useless here ; It may use os.sepb, os.curdirb, os.fsencode() and os.normcase()
  if patterncomps[0] or patterncomps[1]: raise NotImplementedError("Non-relative patterns are unsupported")  # should handle pattern 'C:abc' correctly
  patnames = patterncomps[2:]
  if os_module is None: os_module = os
  # init vars
  if isinstance(pathcomps[0], bytes):
    aA = b'aA'; starstar = b'**'; star = b'*'; qm = b'?'; ac = b'.'; bsol = b'\\'; circ = b'^'; dollar = b'$'; re_spec_chars = b'\\[]{}().?*+^$'; obn = b'[^'; cb = b']'
    try: sep = os_module.sepb
    except AttributeError: sep = None
    if sep is None: sep = os_module.fsencode(sep)
    try: curdir = os_module.curdirb
    except AttributeError: curdir = None
    if curdir is None: curdir = os_module.fsencode(curdir)
  elif isinstance(pathcomps[0], str):
    sep = os_module.sep
    curdir = getattr(os_module, 'curdir', '.')
    aA =  'aA'; starstar =  '**'; star =  '*'; qm =  '?'; ac =  '.'; bsol =  '\\'; circ =  '^'; dollar =  '$'; re_spec_chars =  '\\[]{}().?*+^$'; obn =  '[^'; cb =  ']'
  else:  raise TypeError('pattern must be str or bytes')
  def pcjoin(pc): return pc[0] + pc[1] + sep.join(pc[2:])
  # guess if we want to ignore case
  re_flags = 0
  if ignore_case: re_flags = re.I
  elif ignore_case is None:
    try: normcase = os_module.normcase
    except AttributeError: pass
    else:
      if normcase(aA) != aA: re_flags = re.I
  # so far, I don't handle long separators
  if len(sep) != 1: raise NotImplementedError("Can't handle separator with len != 1")
  lstat_func = os_module.lstat
  def softlstat(p, default=None):
    try: return lstat_func(p)
    except OSError as e:
      if e.errno != errno.ENOENT: raise
    return default
  def escape_re(s):  # uses re_spec_chars
    s2 = s[:0]
    i = 0; l = len(s)
    while i < l:
      c = s[i:i+1]
      if c in re_spec_chars: s2 += bsol + c
      else: s2 += c
      i += 1
    return s2
  nosep_re_s = obn + escape_re(sep) + cb
  def name_to_re(s):  # uses re, bsol, circ, dollar, nosep_re_s, qm, re_flags, re_spec_chars, star, starstar
    s2 = s[:0]
    i = 0; l = len(s)
    while i < l:
      if starstar in s[i:i+2]: s2 += ac + star; i += 2
      elif star in s[i:i+1]: s2 += nosep_re_s + star; i += 1
      elif qm in s[i:i+1]: s2 += nosep_re_s; i += 1
      elif s[i] in re_spec_chars: s2 += bsol + s[i:i+1]; i += 1
      else: s2 += s[i:i+1]; i += 1
    return re.compile(circ + s2 + dollar, re_flags)
  if recursive: patnames = (starstar, *(patnames or ()))
  dirs_only = patnames and not patnames[-1]
  if dirs_only: patnames = patnames[:-1]
  #if not patnames or len(patnames) == 1 and not patnames[0]: raise ValueError(f"unacceptable pattern")
  if not patnames: raise ValueError(f"unacceptable pattern")
  listdir = os_module.listdir
  def walk(pc, st):  # It does not follows symlinks. XXX Should it?
    if not st or stat.S_ISLNK(st.st_mode): return
    try: children = listdir(pcjoin(pc))
    except OSError as e:
      if e.errno == errno.ENOENT: return
      if e.errno == errno.ENOTDIR: return
      raise
    for child in children:
      child = (*pc, child)
      if dirs_only:
        st = softlstat(pcjoin(child))
        if st and stat.S_ISDIR(st.st_mode):
          yield child
          yield from walk(child, st)
      else:
        yield child
        yield from walk(child, softlstat(pcjoin(child)))
  stack = [((), patnames)]
  while stack:
    names, patnames = stack.pop(0)
    if not patnames:
      fullpathcomps = (*pathcomps, *names)
      if dirs_only:
        st = softlstat(pcjoin(fullpathcomps))
        if st and stat.S_ISDIR(st.st_mode):
          yield fullpathcomps
      else: yield fullpathcomps
      continue
    # find any globing name  XXX should it traverse symlinks?
    first_spec_name_index = 0
    for name in patnames:
      if starstar in name:
        #if name != starstar: raise ValueError("Invalid pattern: '**' can only be an entire path component")  # I can handle it with regexps ;)
        simple = False
        break
      if star in name or qm in name:
        simple = True
        break
      first_spec_name_index += 1
    else:
      leaf = (*pathcomps, *names, *patnames)
      if softlstat(pcjoin(leaf)): yield leaf
      continue
    classic_names = patnames[:first_spec_name_index]
    commoncomps = (*pathcomps, *names, *classic_names)
    if simple:
      # handle simple globing ie * and ?
      new_patnames = patnames[first_spec_name_index + 1:]
      name_re = name_to_re(name)
      for child in listdir(pcjoin(commoncomps)):
        if name_re.match(child):
          stack.append((names + (child,), new_patnames))
    else:
      # handle long globing ie **
      fspath = sep.join(patnames[first_spec_name_index:])
      name_re = name_to_re(fspath)
      for pc in walk(commoncomps, softlstat(pcjoin(commoncomps))):
        if name_re.match(pcjoin(pc)):
          yield pc
os_path_splitall_glob._required_globals = ['errno', 'os', 're', 'stat']
