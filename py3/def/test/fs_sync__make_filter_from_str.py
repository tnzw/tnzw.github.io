def test_fs_sync__make_filter_from_str():
  # Filter Rules

  # [..]

  # As the list of files/directories to transfer is built, rsync checks each name to be transferred against the list of include/exclude patterns in turn, and the first matching pattern is acted on: if it is an exclude pattern, then that file is skipped; if it is an include pattern then that filename is not skipped; if no matching pattern is found, then the filename is not skipped.
  fn = fs_sync__make_filter_from_str(''); assert fn('any', False) == 'Sr'

  # Rsync builds an ordered list of filter rules as specified on the command-line. Filter rules have the following syntax:

  #     RULE [PATTERN_OR_FILENAME]
  #     RULE,MODIFIERS [PATTERN_OR_FILENAME]

  # You have your choice of using either short or long RULE names, as described below. If you use a short-named rule, the ',' separating the RULE from the MODIFIERS is optional. The PATTERN or FILENAME that follows (when present) must come after either a single space or an underscore (_). Here are the available rule prefixes:

  # exclude, - specifies an exclude pattern.
  # include, + specifies an include pattern.
  # merge, . specifies a merge-file to read for more rules.
  # dir-merge, : specifies a per-directory merge-file.
  # hide, H specifies a pattern for hiding files from the transfer.
  # show, S files that match the pattern are not hidden.
  # protect, P specifies a pattern for protecting files from deletion.
  # risk, R files that match the pattern are not protected.
  # clear, ! clears the current include/exclude list (takes no arg)

  fn = fs_sync__make_filter_from_str('''\
  exclude excluded
  include included
  hide hidden
  show shown
  protect protected
  risk risked
  ''')
  assert fn('excluded', False) == 'Hp'
  assert fn('included', False) == 'Sr'
  assert fn('hidden', False) == 'Hr'
  assert fn('shown', False) == 'Sr'
  assert fn('protected', False) == 'SP'
  assert fn('risked', False) == 'SR'

  fn = fs_sync__make_filter_from_str('''\
  - -
  + +
  H H
  S S
  P P
  R R
  ''')

  assert fn('-', False) == 'Hp'
  assert fn('+', False) == 'Sr'
  assert fn('H', False) == 'Hr'
  assert fn('S', False) == 'Sr'
  assert fn('P', False) == 'SP'
  assert fn('R', False) == 'SR'

  fn = fs_sync__make_filter_from_str('''\
  hide HR
  risk HR
  show SP
  protect SP
  ''')
  assert fn('HR', False) == 'HR'
  assert fn('SP', False) == 'SP'

  fn = fs_sync__make_filter_from_str('''\
  R protected
  clear
  P protected
  ''')
  assert fn('protected', False) == 'SP'

  fn = fs_sync__make_filter_from_str('''\
  R protected
  !
  P protected
  ''')
  assert fn('protected', False) == 'SP'

  assert_raise(ValueError, lambda: fs_sync__make_filter_from_str('clear lol'))

  # When rules are being read from a file, empty lines are ignored, as are comment lines that start with a lq#rq.
  fn = fs_sync__make_filter_from_str('''
  H H

  P P
  ''')
  assert fn('H', False) == 'Hr'
  assert fn('P', False) == 'SP'

  # [..]

  # [..]

  # Include/Exclude Pattern Rules

  # You can include and exclude files by specifying patterns using the '+', '-', etc. filter rules (as introduced in the FILTER RULES section above). The include/exclude rules each specify a pattern that is matched against the names of the files that are going to be transferred. These patterns can take several forms:

  # o if the pattern starts with a / then it is anchored to a particular spot in the hierarchy of files, otherwise it is matched against the end of the pathname. This is similar to a leading ^ in regular expressions. Thus '/foo' would match a name of 'foo' at either the 'root of the transfer' (for a global rule) or in the merge-file's directory (for a per-directory rule). An unqualified 'foo' would match a name of 'foo' anywhere in the tree because the algorithm is applied recursively from the top down; it behaves as if each path component gets a turn at being the end of the filename. Even the unanchored 'sub/foo' would match at any point in the hierarchy where a 'foo' was found within a directory named 'sub'. See the section on ANCHORING INCLUDE/EXCLUDE PATTERNS for a full discussion of how to specify a pattern that matches at the root of the transfer.
  fn = fs_sync__make_filter_from_str('- /foo')
  assert fn('foo', False) == 'Hp'
  assert fn('sub/foo', False) == 'Sr'
  fn = fs_sync__make_filter_from_str('- foo')
  assert fn('foo', False) == 'Hp'
  assert fn('sub/foo', False) == 'Hp'
  fn = fs_sync__make_filter_from_str('- foo', force_match_absolute=True)
  assert fn('foo', False) == 'Hp'
  assert fn('sub/foo', False) == 'Sr'
  fn = fs_sync__make_filter_from_str('- foo/bar')
  assert fn('foo/bar', False) == 'Hp'
  assert fn('sub/foo/bar', False) == 'Hp'
  assert fn('sub/foo/baz', False) == 'Sr'

  # o if the pattern ends with a / then it will only match a directory, not a regular file, symlink, or device.
  fn = fs_sync__make_filter_from_str('- foo/')
  assert fn('foo', False) == 'Sr'
  assert fn('foo', True) == 'Hp'

  # o rsync chooses between doing a simple string match and wildcard matching by checking if the pattern contains one of these three wildcard characters: '*', '?', and '[' .
  # o a '*' matches any path component, but it stops at slashes.
  fn = fs_sync__make_filter_from_str('- foo*bar')
  assert fn('foobar', False) == 'Hp'
  assert fn('foo_bar', False) == 'Hp'
  assert fn('foo__bar', False) == 'Hp'
  assert fn('foo/bar', False) == 'Sr'
  assert fn('_foobar_', False) == 'Sr'

  # o use '**' to match anything, including slashes.
  fn = fs_sync__make_filter_from_str('- foo**bar')
  assert fn('foobar', False) == 'Hp'
  assert fn('foo_bar', False) == 'Hp'
  assert fn('foo__bar', False) == 'Hp'
  assert fn('foo/bar', False) == 'Hp'
  assert fn('foo_/_bar', False) == 'Hp'
  assert fn('_foo/bar_', False) == 'Sr'

  # o a '?' matches any character except a slash (/).
  fn = fs_sync__make_filter_from_str('- foo?bar')
  assert fn('foobar', False) == 'Sr'
  assert fn('foo_bar', False) == 'Hp'
  assert fn('foo__bar', False) == 'Sr'
  assert fn('foo/bar', False) == 'Sr'
  fn = fs_sync__make_filter_from_str('- foo??bar')
  assert fn('foobar', False) == 'Sr'
  assert fn('foo_bar', False) == 'Sr'
  assert fn('foo__bar', False) == 'Hp'
  assert fn('foo/bar', False) == 'Sr'

  # o a '[' introduces a character class, such as [a-z] or [[:alpha:]].
  assert_raise(NotImplementedError, lambda: fs_sync__make_filter_from_str('- [abc]'))
  assert_raise(NotImplementedError, lambda: fs_sync__make_filter_from_str('- [a-z]'))
  assert_raise(NotImplementedError, lambda: fs_sync__make_filter_from_str('- [[:alpha:]]'))

  # o in a wildcard pattern, a backslash can be used to escape a wildcard character, but it is matched literally when no wildcards are present.
  fn = fs_sync__make_filter_from_str(r'- e\s\[\](){}\?\*\/cape')
  assert fn(r'e\s[](){}?*\/cape', False) == 'Hp'

  # o if the pattern contains a / (not counting a trailing /) or a '**', then it is matched against the full pathname, including any leading directories. If the pattern doesn't contain a / or a '**', then it is matched only against the final component of the filename. (Remember that the algorithm is applied recursively so 'full filename' can actually be any portion of a path from the starting directory on down.)
  fn = fs_sync__make_filter_from_str('- dir_name/**')
  assert fn('dir_name', False) == 'Sr'
  assert fn('dir_name', True) == 'Sr'
  assert fn('dir_name/any', False) == 'Hp'
  fn = fs_sync__make_filter_from_str('- dir_name**')
  assert fn('dir_name', False) == 'Hp'
  assert fn('dir_name', True) == 'Hp'
  assert fn('dir_name/any', False) == 'Hp'

  # o a trailing 'dir_name/***' will match both the directory (as if 'dir_name/' had been specified) and everything in the directory (as if 'dir_name/**' had been specified). [..]
  fn = fs_sync__make_filter_from_str('- dir_name/***')
  assert fn('dir_name', False) == 'Sr'
  assert fn('dir_name', True) == 'Hp'
  assert fn('dir_name/any', False) == 'Hp'
  fn = fs_sync__make_filter_from_str('- double***stared')
  assert fn('doublestared', False) == 'Hp'
  assert fn('double/stared', False) == 'Hp'
  assert fn('double_/_stared', False) == 'Hp'

  # [..]

  #     + /some/path/this-file-will-not-be-found
  #     + /file-is-included
  #     - *
  fn = fs_sync__make_filter_from_str(r'''
  + /some/path/this-file-will-not-be-found
  + /file-is-included
  - *
  ''')
  assert fn('some', True) == 'Hp'
  assert fn('file-is-included', False) == 'Sr'

  # This fails because the parent directory lqsomerq is excluded by the oq*cq rule, so rsync never visits any of the files in the lqsomerq or lqsome/pathrq directories. One solution is to ask for all directories in the hierarchy to be included by using a single rule: lq+ */rq (put it somewhere before the lq- *rq rule), and perhaps use the --prune-empty-dirs option. Another solution is to add specific include rules for all the parent dirs that need to be visited. For instance, this set of rules works fine:

  #     + /some/
  #     + /some/path/
  #     + /some/path/this-file-is-found
  #     + /file-also-included
  #     - *
  fn = fs_sync__make_filter_from_str(r'''
  + /some/
  + /some/path/
  + /some/path/this-file-is-found
  + /file-also-included
  - *
  ''')
  assert fn('some', True) == 'Sr'
  assert fn('some/path', True) == 'Sr'
  assert fn('some/path/this-file-is-found', False) == 'Sr'
  assert fn('file-also-included', False) == 'Sr'

  # Here are some examples of exclude/include matching:

  # o '- *.o' would exclude all names matching *.o
  fn = fs_sync__make_filter_from_str('- *.o')
  assert fn('src/obj.o', False) == 'Hp'
  # o '- /foo' would exclude a file (or directory) named foo in the transfer-root directory
  fn = fs_sync__make_filter_from_str('- /foo')
  assert fn('foo', False) == 'Hp'
  assert fn('sub/foo', False) == 'Sr'
  # o '- foo/' would exclude any directory named foo
  fn = fs_sync__make_filter_from_str('- foo/')
  assert fn('src/foo', False) == 'Sr'
  assert fn('src/foo', True) == 'Hp'
  # o '- /foo/*/bar' would exclude any file named bar which is at two levels below a directory named foo in the transfer-root directory
  fn = fs_sync__make_filter_from_str('- /foo/*/bar')
  assert fn('foo/bar', False) == 'Sr'
  assert fn('foo/any/bar', False) == 'Hp'
  # o '- /foo/**/bar' would exclude any file named bar two or more levels below a directory named foo in the transfer-root directory
  fn = fs_sync__make_filter_from_str('- /foo/**/bar')
  assert fn('foo/bar', False) == 'Sr'
  assert fn('foo/any/bar', False) == 'Hp'
  assert fn('foo/any/more/bar', False) == 'Hp'
  # o The combination of '+ */', '+ *.c', and '- *' would include all directories and C source files but nothing else (see also the --prune-empty-dirs option)
  fn = fs_sync__make_filter_from_str(r'''
  + */
  + *.c
  - *
  ''')
  assert fn('src', True) == 'Sr'
  assert fn('src/obj.c', False) == 'Sr'
  assert fn('src/obj.o', False) == 'Hp'
  assert fn('src/lib', True) == 'Sr'
  assert fn('src/lib/lib.c', False) == 'Sr'
  assert fn('src/lib/lib.o', False) == 'Hp'
  assert fn('dist', True) == 'Sr'
  assert fn('dist/prog.out', False) == 'Hp'
  # o The combination of '+ foo/', '+ foo/bar.c', and '- *' would include only the foo directory and foo/bar.c (the foo directory must be explicitly included or it would be excluded by the '*')
  fn = fs_sync__make_filter_from_str(r'''
  + foo/
  + foo/bar.c
  - *
  ''')
  assert fn('foo', True) == 'Sr'
  assert fn('foo/bar.c', False) == 'Sr'
  assert fn('foo/bar.o', False) == 'Hp'
  assert fn('foo/lib', True) == 'Hp'
  assert fn('dist', True) == 'Hp'

  # The following modifiers are accepted after a '+' or '-':

  # o A / specifies that the include/exclude rule should be matched against the absolute pathname of the current item. [..]
  # WONT BE IMPLEMENTED
  # o A ! specifies that the include/exclude should take effect if the pattern fails to match. For instance, '-! */' would exclude all non-directories.
  fn = fs_sync__make_filter_from_str('-! */')
  assert fn('foo', True) == 'Sr'
  assert fn('foo/bar.c', False) == 'Hp'
  assert fn('foo/bar.o', False) == 'Hp'
  assert fn('foo/lib', True) == 'Sr'
  assert fn('dist', True) == 'Sr'
  # o A C is used to indicate that all the global CVS-exclude rules should be inserted as excludes in place of the '-C'. No arg should follow.
  # WONT BE IMPLEMENTED
  # o An s is used to indicate that the rule applies to the sending side. When a rule affects the sending side, it prevents files from being transferred. The default is for a rule to affect both sides unless --delete-excluded was specified, in which case default rules become sender-side only. See also the hide (H) and show (S) rules, which are an alternate way to specify sending-side includes/excludes.
  fn = fs_sync__make_filter_from_str(r'''
  +s foo
  -s bar
  - *
  ''')
  assert fn('foo', False) == 'Sp'
  assert fn('bar', False) == 'Hp'
  # o An r is used to indicate that the rule applies to the receiving side. When a rule affects the receiving side, it prevents files from being deleted. See the s modifier for more info. See also the protect (P) and risk (R) rules, which are an alternate way to specify receiver-side includes/excludes.
  fn = fs_sync__make_filter_from_str(r'''
  +r foo
  -r bar
  - *
  ''')
  assert fn('foo', False) == 'HR'
  assert fn('bar', False) == 'HP'
  # o A p indicates that a rule is perishable, meaning that it is ignored in directories that are being deleted. [..]
  # WONT BE IMPLEMENTED

  # OTHER RSYNC BEHAVIORS
  fn = fs_sync__make_filter_from_str('-   a file with two spaces at start and one at end ')
  assert fn('a file with two spaces at start and one at end', False) == 'Sr'
  assert fn('  a file with two spaces at start and one at end ', False) == 'Hp'
  fn = fs_sync__make_filter_from_str('- /')  # a never matching pattern
  assert fn('a', False) == 'Sr'
  fn = fs_sync__make_filter_from_str('- /', disable_wildcards=True)  # a never matching pattern
  assert fn('a', False) == 'Sr'
  fn = fs_sync__make_filter_from_str('-! /')  # an always matching pattern
  assert fn('a', False) == 'Hp'

  assert_raise(ValueError, lambda: fs_sync__make_filter_from_str('hello'))
  assert_raise(ValueError, lambda: fs_sync__make_filter_from_str('-hello'))

  # OTHER CUSTOM BEHAVIORS
  fn = fs_sync__make_filter_from_str(r'''
  -i case ignored
  -I case not ignored
  - Case Not Ignored Either
  ''', ignorecase=False)
  assert fn('case ignored', False) == 'Hp'
  assert fn('CaSe IgNoRed', False) == 'Hp'
  assert fn('case not ignored', False) == 'Hp'
  assert fn('CaSe Not IgNoRed', False) == 'Sr'
  assert fn('Case Not Ignored Either', False) == 'Hp'
  assert fn('CaSe Not IgNoRed EiThEr', False) == 'Sr'
  fn = fs_sync__make_filter_from_str(r'''
  -i case ignored
  -I case not ignored
  - Case Also Ignored
  ''', ignorecase=True)
  assert fn('case ignored', False) == 'Hp'
  assert fn('CaSe IgNoRed', False) == 'Hp'
  assert fn('case not ignored', False) == 'Hp'
  assert fn('CaSe Not IgNoRed', False) == 'Sr'
  assert fn('Case Also Ignored', False) == 'Hp'
  assert fn('CaSe AlSo IgNoRed', False) == 'Hp'

  ################################################################################

  # fn = fs_sync__make_filter_from_str(r'''
  #   - simple
  #   -_simple2
  #   S *show*
  #   H *hide*
  #   P *protect*
  #   R *risk*
  #   S **SHOW**
  #   H **HIDE**
  #   P **PROTECT**
  #   R **RISK**
  #   +s +s
  #   -s -s
  #   +r +r
  #   -r -r
  #   +sr +sr
  #   -sr -sr
  #   -  file with spaces
  #   - relative/file/with/slash
  #   - e\s\[\](){}\?\*\/cape
  #   - q??mark
  #   - dir/
  #   - /abs
  #   - /db_star/**
  #   - triple_star/***

  #   # custom stuff
  #   -i ignorecase
  #   -I dontIGNORECASE

  #   # exclude nothing -! *
  #   -! *
  # ''')

  # print()
  # for path in r'''
  # simple
  # baseonly/simple
  # baseonly/simple2
  # baseonly/showprotect
  # baseonly/hiderisk
  # baseonly/hiderisk/nope
  # baseonly/-HIDERISK-/yep
  # baseonly/+s
  # baseonly/-s
  # baseonly/+r
  # baseonly/-r
  # baseonly/+sr
  # baseonly/-sr
  # baseonly/ file with spaces
  # baseonly/q..mark
  # baseonly/qabmark
  # relative/file/with/slash
  # rel/relative/file/with/slash
  # e\s[](){}?*\/cape
  # rel/yep/dir/
  # rel/nope/triple_star
  # rel/yep/triple_star/
  # rel/yep/triple_star/yep
  # abs
  # db_star  # nope
  # db_star/yep
  # rel/db_star/nope

  #   # testing custom modifiers
  # iGnOrEcAsE
  # dontignorecase  # nope
  # '''.split('\n'):
  #   for i in range(len(path)):
  #     if path[i:i + 3] == '  #':
  #       path = path[:i]
  #       break
  #   if not path: continue
  #   if path == '/': XXX
  #   if path[-1:] == '/':
  #     is_dir = True
  #     path = path[:-1]
  #   else:
  #     is_dir = False
  #   print('DIR' if is_dir else '   ', path, '->', fn(path, is_dir))

  # fs_sync__make_filter_from_str('- caf\xc3\xa9', encoding='_bytestr')
  # fs_sync__make_filter_from_str(r'-x caf\xc3\xa9', encoding='utf-8')
  # fs_sync__make_filter_from_str('-x café', encoding='utf-8')
  # fs_sync__make_filter_from_str(r'-x caf\xc3\xa9')
  fn = fs_sync__make_filter_from_str('- /caf\u00e9'); assert fn('café', False) == 'Hp'
  fn = fs_sync__make_filter_from_str('- /caf\u00e9', encoding='utf-8'); assert fn(b'caf\xc3\xa9', False) == 'Hp'
  fn = fs_sync__make_filter_from_str('- /caf\xc3\xa9', encoding='_bytestr'); assert fn(b'caf\xc3\xa9', False) == 'Hp'
  fn = fs_sync__make_filter_from_str('-x /caf\\xc3\\xa9', encoding='utf-8'); assert fn(b'caf\xc3\xa9', False) == 'Hp'

  fn = fs_sync__make_filter_from_str('- a[bc]d*e?f', disable_wildcards=True)
  assert fn('a[bc]d*e?f', False) == 'Hp'
  assert fn('a[bc]dXe?f', False) == 'Sr'
  assert fn('a[bc]d*eXf', False) == 'Sr'

  fn = fs_sync__make_filter_from_str('~ hp'); assert fn('hp', False) == 'HP'
  fn = fs_sync__make_filter_from_str('= sr'); assert fn('sr', False) == 'SR'
  fn = fs_sync__make_filter_from_str('SP sp'); assert fn('sp', False) == 'SP'
  fn = fs_sync__make_filter_from_str('HR hr'); assert fn('hr', False) == 'HR'
  fn = fs_sync__make_filter_from_str(r'''
  * me/project/src/file
  * me/project/src/dir/
  + /rel/
  - other
  - dir
  ''', disable_wildcards=True)
  assert fn('me', True) == 'Sr'
  assert fn('me/project', True) == 'Sr'
  assert fn('me/project/src', True) == 'Sr'
  assert fn('me/project/src/file', False) == 'Sr'
  assert fn('me/project/src/dir', False) == 'Hp'
  assert fn('me/project/src/dir', True) == 'Sr'
  assert fn('me/project/src/other', False) == 'Hp'
  assert fn('rel', True) == 'Sr'
  assert fn('rel/me', True) == 'Sr'
  assert fn('rel/me/project', True) == 'Sr'
  assert fn('rel/me/project/src', True) == 'Sr'
  assert fn('rel/me/project/src/file', False) == 'Sr'
  assert fn('rel/me/project/src/other', False) == 'Hp'
  fn = fs_sync__make_filter_from_str(r'''
  * me/project/src/file
  * me/project/src/dir/
  + /rel/
  - *
  ''')
  assert fn('me', True) == 'Sr'
  assert fn('me/project', True) == 'Sr'
  assert fn('me/project/src', True) == 'Sr'
  assert fn('me/project/src/file', False) == 'Sr'
  assert fn('me/project/src/dir', False) == 'Hp'
  assert fn('me/project/src/dir', True) == 'Sr'
  assert fn('me/project/src/other', False) == 'Hp'
  assert fn('rel/me', True) == 'Sr'
  assert fn('rel/me/project', True) == 'Sr'
  assert fn('rel/me/project/src', True) == 'Sr'
  assert fn('rel/me/project/src/file', False) == 'Sr'
  assert fn('rel/me/project/src/other', False) == 'Hp'

  assert_raise(ValueError, lambda: fs_sync__make_filter_from_str('*x abc'))

  # fn = fs_sync__make_filter_from_str('+ 1\n- *')
  fn = fs_sync__make_filter_from_str('* 1\n- *')
  assert fn('1', False) == 'Sr'
  assert fn('1', True) == 'Sr'
  assert fn('2', False) == 'Hp'
  assert fn('2', True) == 'Hp'
  assert fn('1/1', False) == 'Sr'
  assert fn('1/1', True) == 'Sr'
  assert fn('1/2', False) == 'Hp'
  assert fn('1/2', True) == 'Hp'
  # fn = fs_sync__make_filter_from_str('+ 1/2\n- *')
  fn = fs_sync__make_filter_from_str('* 1/2\n- *')
  assert fn('1', False) == 'Hp'
  assert fn('1', True) == 'Sr'
  assert fn('2', False) == 'Hp'
  assert fn('2', True) == 'Hp'
  assert fn('3', False) == 'Hp'
  assert fn('3', True) == 'Hp'
  assert fn('1/1', False) == 'Hp'
  assert fn('1/1', True) == 'Sr'
  assert fn('1/2', False) == 'Sr'
  assert fn('1/2', True) == 'Sr'
  assert fn('1/3', False) == 'Hp'
  assert fn('1/3', True) == 'Hp'
  # fn = fs_sync__make_filter_from_str('+ 1/2/3\n- *')
  fn = fs_sync__make_filter_from_str('* 1/2/3\n- *')
  assert fn('1', False) == 'Hp'
  assert fn('1', True) == 'Sr'
  assert fn('2', False) == 'Hp'
  assert fn('2', True) == 'Hp'
  assert fn('3', False) == 'Hp'
  assert fn('3', True) == 'Hp'
  assert fn('1/1', False) == 'Hp'
  assert fn('1/1', True) == 'Sr'
  assert fn('1/2', False) == 'Hp'
  assert fn('1/2', True) == 'Sr'
  assert fn('1/3', False) == 'Hp'
  assert fn('1/3', True) == 'Hp'
  assert fn('1/2/1', False) == 'Hp'
  assert fn('1/2/1', True) == 'Sr'
  assert fn('1/2/2', False) == 'Hp'
  assert fn('1/2/2', True) == 'Hp'
  assert fn('1/2/3', False) == 'Sr'
  assert fn('1/2/3', True) == 'Sr'

  # fn = fs_sync__make_filter_from_str('+ 1/**\n- *')
  fn2 = fs_sync__make_filter_from_str('* 1/**\n- *')
  fn3 = fs_sync__make_filter_from_str('* 1/***\n- *')
  for fn in [fn2, fn3]:
    assert fn('1', False) == 'Hp'
    assert fn('1', True) == 'Sr'
    assert fn('2', False) == 'Hp'
    assert fn('2', True) == 'Hp'
    assert fn('3', False) == 'Hp'
    assert fn('3', True) == 'Hp'
    assert fn('1/4', False) == 'Sr'
    assert fn('1/5', True) == 'Sr'
  # fn = fs_sync__make_filter_from_str('+ 1/2**\n- *')
  fn2 = fs_sync__make_filter_from_str('* 1/2**\n- *')
  fn3 = fs_sync__make_filter_from_str('* 1/2**\n- *')
  for fn in [fn2, fn3]:
    assert fn('1', False) == 'Hp'
    assert fn('1', True) == 'Sr'
    assert fn('2', False) == 'Hp'
    assert fn('2', True) == 'Hp'
    assert fn('3', False) == 'Hp'
    assert fn('3', True) == 'Hp'
    assert fn('1/1', False) == 'Hp'
    assert fn('1/1', True) == 'Sr'
    assert fn('1/2', False) == 'Sr'
    assert fn('1/2', True) == 'Sr'
    assert fn('1/3', False) == 'Hp'
    assert fn('1/3', True) == 'Hp'
    assert fn('1/24', False) == 'Sr'
    assert fn('1/25', True) == 'Sr'
    assert fn('1/2/4', False) == 'Sr'
    assert fn('1/2/5', True) == 'Sr'
  # fn = fs_sync__make_filter_from_str('+ 1/2/**\n- *')
  fn2 = fs_sync__make_filter_from_str('* 1/2/**\n- *')
  fn3 = fs_sync__make_filter_from_str('* 1/2/***\n- *')
  for fn in [fn2, fn3]:
    assert fn('1', False) == 'Hp'
    assert fn('1', True) == 'Sr'
    assert fn('2', False) == 'Hp'
    assert fn('2', True) == 'Hp'
    assert fn('3', False) == 'Hp'
    assert fn('3', True) == 'Hp'
    assert fn('1/1', False) == 'Hp'
    assert fn('1/1', True) == 'Sr'
    assert fn('1/2', False) == 'Hp'
    assert fn('1/2', True) == 'Sr'
    assert fn('1/3', False) == 'Hp'
    assert fn('1/3', True) == 'Hp'
    assert fn('1/24', False) == 'Hp'
    assert fn('1/25', True) == 'Hp'
    assert fn('1/2/4', False) == 'Sr'
    assert fn('1/2/5', True) == 'Sr'
  # fn = fs_sync__make_filter_from_str('+ 1/2/3/**\n- *')
  fn2 = fs_sync__make_filter_from_str('* 1/2/3/**\n- *')
  fn3 = fs_sync__make_filter_from_str('* 1/2/3/***\n- *')
  for fn in [fn2, fn3]:
    assert fn('1', False) == 'Hp'
    assert fn('1', True) == 'Sr'
    assert fn('2', False) == 'Hp'
    assert fn('2', True) == 'Hp'
    assert fn('3', False) == 'Hp'
    assert fn('3', True) == 'Hp'
    assert fn('1/1', False) == 'Hp'
    assert fn('1/1', True) == 'Sr'
    assert fn('1/2', False) == 'Hp'
    assert fn('1/2', True) == 'Sr'
    assert fn('1/3', False) == 'Hp'
    assert fn('1/3', True) == 'Hp'
    assert fn('1/2/1', False) == 'Hp'
    assert fn('1/2/1', True) == 'Sr'
    assert fn('1/2/2', False) == 'Hp'
    assert fn('1/2/2', True) == 'Hp'
    assert fn('1/2/3', False) == 'Hp'
    assert fn('1/2/3', True) == 'Sr'
    assert fn('1/2/3/4', False) == 'Sr'
    assert fn('1/2/3/5', True) == 'Sr'

  # Filter example
  fn = fs_sync__make_filter_from_str(r'''
  #############################
  # Project integration files

  + /.gitignore
  - /.htaccess

  #################
  # Project files

  + /src/
  * /lib/legacy_module/
  - /lib/*
  ~ /dist/
  +i /*.md
  -i *cache*

  ###################
  # Source clean up

  # hidden files
  - /src/.*
  - /src/**/.*
  # __pycache__ folders
  -x /src/(.*/)?__pycache__/

  ################
  # System files

  ~x /.Trash-[0-9]+/
  ~i /DumpStack.log.tmp
  ~ix /found.[0-9]+/
  ~i /$RECYCLE.BIN
  ~i /pagefile.sys
  ~i /System Volume Information/

  ###################
  # General clean up

  # emacs backup files
  - *~
  # blender backup files
  -ix /src/.*[^/]\.blend[0-9]+

  ################
  # General rule
  - /*
  ''')
  assert_equal(fn('.gitignore', False), 'Sr')
  assert_equal(fn('.vscode', True), 'Hp')
  assert_equal(fn('.htaccess', False), 'Hp')
  assert_equal(fn('README.md', False), 'Sr')
  assert_equal(fn('notes.txt', False), 'Hp')
  assert_equal(fn('src', True), 'Sr')
  assert_equal(fn('src/__pycache__', True), 'Hp')
  assert_equal(fn('src/othercache', True), 'Hp')
  assert_equal(fn('src/main.py', False), 'Sr')
  assert_equal(fn('src/main.py~', False), 'Hp')
  assert_equal(fn('src/.main.py.tmp$', False), 'Hp')
  assert_equal(fn('src/obj', True), 'Sr')
  assert_equal(fn('src/obj/obj.py', False), 'Sr')
  assert_equal(fn('src/obj/obj.py~', False), 'Hp')
  assert_equal(fn('src/obj/.obj.py.tmp$', False), 'Hp')
  assert_equal(fn('lib', True), 'Sr')
  assert_equal(fn('lib/piplib', True), 'Hp')
  assert_equal(fn('lib/legacy_module', True), 'Sr')
  assert_equal(fn('lib/legacy_module/blahblah', False), 'Sr')
  assert_equal(fn('dist', True), 'HP')
  assert_equal(fn('System Volume Information', True), 'HP')
  assert_equal(fn('FOUND.000', True), 'HP')
  assert_equal(fn('$recycle.bin', True), 'HP')

  fn = fs_sync__make_filter_from_str(r'''
  * /Desktop/Synced/
  - /*
  ''')
  assert_equal(fn('Images', True), 'Hp')
  assert_equal(fn('Desktop', True), 'Sr')
  assert_equal(fn('Desktop/Synced', True), 'Sr')
  assert_equal(fn('Desktop/NotSynced', True), 'Sr')  # yes, it's synced, because it does not match `* /Desktop/Synced/` or `- /*`

  fn = fs_sync__make_filter_from_str(r'''
  * /Desktop/Synced/***
  - *
  ''')
  assert_equal(fn('Images', True), 'Hp')
  assert_equal(fn('Desktop', True), 'Sr')
  assert_equal(fn('Desktop/Synced', True), 'Sr')
  assert_equal(fn('Desktop/NotSynced', True), 'Hp')
