#!python3 -i

def test_generator__auto_close_call():
  def generator_mock(mock):
    mock.append('__enter__')
    try:
      mock.append('yield')
      yield 'value';
    finally:
      mock.append('__exit__')

  ######################
  # __exit__ echoed after for statement because the generator reached its end.

  mock = ['for']
  for _ in generator_mock(mock):
    mock.append(_)
  mock.append('endfor')
  assert_equal(','.join(mock), 'for,__enter__,yield,value,__exit__,endfor')

  mock = ['gen']
  gen = generator_mock(mock)
  mock.append('for')
  for _ in gen:
    mock.append(_)
  mock.append('endfor')
  #mock.append('del gen')
  #del gen
  assert_equal(','.join(mock), 'gen,for,__enter__,yield,value,__exit__,endfor')

  ######################
  # __exit__ echoed after for statement because the generator is used only in the for statement.

  mock = ['for']
  for _ in generator_mock(mock):
    mock.append(_)
    mock.append('break')
    break
  mock.append('endfor')
  assert_equal(','.join(mock), 'for,__enter__,yield,value,break,__exit__,endfor')

  mock = ['try']
  try:
    mock.append('for')
    for _ in generator_mock(mock):
      mock.append(_)
      mock.append('raise')
      raise ValueError('test')
    mock.append('endfor')
  except ValueError:
    mock.append('except')
  mock.append('endtry')
  assert_equal(','.join(mock), 'try,for,__enter__,yield,value,raise,__exit__,except,endtry')

  ######################
  # __exit__ echoed on del because generator had not ended and gen.__del__ closes it.

  mock = ['gen']
  gen = generator_mock(mock)
  mock.append('for')
  for _ in gen:
    mock.append(_)
    mock.append('break')
    break
  mock.append('endfor')
  mock.append('del gen')
  del gen
  assert_equal(','.join(mock), 'gen,for,__enter__,yield,value,break,endfor,del gen,__exit__')

  mock = ['gen']
  gen = generator_mock(mock)
  mock.append('try')
  try:
    mock.append('for')
    for _ in gen:
      mock.append(_)
      mock.append('raise')
      raise ValueError('test')
    mock.append('endfor')
  except ValueError:
    mock.append('except')
  mock.append('endtry')
  mock.append('del gen')
  del gen
  assert_equal(','.join(mock), 'gen,try,for,__enter__,yield,value,raise,except,endtry,del gen,__exit__')

def test_generator__GeneratorExit_handling():
  def gen():
    no_more_yield = False
    _ = 'start'; mock.append(_); yielded.append(_); sent.append((yield _)); yielded_after.append(_)
    try:
      _ = 'try'; mock.append(_); yielded.append(_); sent.append((yield _)); yielded_after.append(_)
    except GeneratorExit:
      no_more_yield = True
      _ = 'GeneratorExit'; mock.append(_)
      raise
    finally:
      _ = 'finally'; mock.append(_)
      if not no_more_yield:
        yielded.append(_); sent.append((yield _)); yielded_after.append(_)

  # yield until the end
  yielded = []; sent = []; yielded_after = []; mock = []
  for _ in gen(): pass
  assert_equal(mock, ['start', 'try', 'finally'])
  assert_equal(yielded, mock)
  assert_equal(yielded_after, ['start', 'try', 'finally'])

  yielded = []; sent = []; yielded_after = []; mock = []
  g = gen()  # g = gen() does not need to go on try/except as, in python, gen() process only starts at first send()
  try: g.send(None); g.send(1); g.send(2); g.send(3)
  except StopIteration: pass
  else: assert False, "should have ended!"
  assert_equal(mock, ['start', 'try', 'finally'])
  assert_equal(yielded, mock)
  assert_equal(yielded_after, ['start', 'try', 'finally'])
  assert_equal(sent, [1, 2, 3])

  # stop at first yield, before `try`
  yielded = []; sent = []; yielded_after = []; mock = []
  for _ in gen(): break
  assert_equal(mock, ['start'])
  assert_equal(yielded, mock)
  assert_equal(yielded_after, [])

  yielded = []; sent = []; yielded_after = []; mock = []
  try:
    for _ in gen(): raise ValueError()
  except ValueError: pass
  assert_equal(mock, ['start'])
  assert_equal(yielded, mock)
  assert_equal(yielded_after, [])

  yielded = []; sent = []; yielded_after = []; mock = []
  g = gen()
  try: g.send(None)
  except StopIteration: assert False, "Unexpected end of generator"
  finally: g.close()
  assert_equal(mock, ['start'])
  assert_equal(yielded, mock)
  assert_equal(yielded_after, [])
  assert_equal(sent, [])

  # stop at second yield, in `try`
  yielded = []; sent = []; yielded_after = []; mock = []
  i = 0
  for _ in gen():
    if i == 1: break
    i += 1
  assert_equal(mock, ['start', 'try', 'GeneratorExit', 'finally'])
  assert_equal(yielded, ['start', 'try'])
  assert_equal(yielded_after, ['start'])

  yielded = []; sent = []; yielded_after = []; mock = []
  i = 0
  try:
    for _ in gen():
      if i == 1: raise ValueError()
      i += 1
  except ValueError: pass
  assert_equal(mock, ['start', 'try', 'GeneratorExit', 'finally'])
  assert_equal(yielded, ['start', 'try'])
  assert_equal(yielded_after, ['start'])

  yielded = []; sent = []; yielded_after = []; mock = []
  g = gen()
  try: g.send(None); g.send(1)
  except StopIteration: assert False, "Unexpected end of generator"
  finally: g.close()
  assert_equal(mock, ['start', 'try', 'GeneratorExit', 'finally'])
  assert_equal(yielded, ['start', 'try'])
  assert_equal(yielded_after, ['start'])
  assert_equal(sent, [1])

  # stop at third yield, in `finally`
  yielded = []; sent = []; yielded_after = []; mock = []
  i = 0
  for _ in gen():
    if i == 2: break
    i += 1
  assert_equal(mock, ['start', 'try', 'finally'])
  assert_equal(yielded, mock)
  assert_equal(yielded_after, ['start', 'try'])

  yielded = []; sent = []; yielded_after = []; mock = []
  i = 0
  try:
    for _ in gen():
      if i == 2: raise ValueError()
      i += 1
  except ValueError: pass
  assert_equal(mock, ['start', 'try', 'finally'])
  assert_equal(yielded, mock)
  assert_equal(yielded_after, ['start', 'try'])

  yielded = []; sent = []; yielded_after = []; mock = []
  g = gen()
  try: g.send(None); g.send(1); g.send(2)
  except StopIteration: assert False, "Unexpected end of generator"
  finally: g.close()
  assert_equal(mock, ['start', 'try', 'finally'])
  assert_equal(yielded, mock)
  assert_equal(yielded_after, ['start', 'try'])
  assert_equal(sent, [1, 2])
  
  def gen():
    try: yield
    except GeneratorExit: raise ValueError()

  g = gen()
  g.send(None)
  assert_raise(ValueError, lambda: g.close())

  def gen():
    try: yield
    except GeneratorExit: raise ValueError()
    finally: raise TypeError()

  g = gen()
  g.send(None)
  assert_raise(TypeError, lambda: g.close())

###########################################################################################
# Never yield in a finally! Because yielding after a GeneratorExit() kills the generator. #
###########################################################################################

def test_generator__yielding_finally():

  _last_fd = 2
  def yielding_fopen(path):
    nonlocal _last_fd
    yield f'fopening {path!r}'
    os_calls.append(('fopen', path))
    _last_fd += 1
    return _last_fd
  def yielding_fclose(fd):
    yield f'fclosing {fd!r}'
    os_calls.append(('fclose', fd))
  def fclose(fd):
    os_calls.append(('fclose', fd))

  def gen():
    _noerr = _yieldable = True
    # __enter__()
    src_fd = dst_fd = None
    try:
      src_fd = yield from yielding_fopen('src')
      dst_fd = yield from yielding_fopen('dst')
      # suite...
      yield 'suite'
    # __exit__()
    except GeneratorExit:
      _yieldable = False
      if _noerr: raise
    except: _noerr = False; raise
    finally:
      # deferred one: closing(dst)
      _force = True
      try:
        if _yieldable and dst_fd is not None: dst_fd = yield from yielding_fclose(dst_fd)
      except GeneratorExit:
        _yieldable = False
        if _noerr: raise
      except: _force = False; _noerr = False; raise
      finally:
        try:
          if _force and dst_fd is not None: fclose(dst_fd)
        finally:
          # deferred two: closing(src)
          _force = True
          try:
            if _yieldable and src_fd is not None: src_fd = yield from yielding_fclose(src_fd)
          except GeneratorExit:
            _yieldable = False
            if _noerr: raise
          except: _force = False; _noerr = False; raise
          finally:
            if _force and src_fd is not None: fclose(src_fd)

  _last_fd = 2; os_calls = []
  g = gen()
  assert_equal(g.send(None), "fopening 'src'")
  g.close()
  assert_equal(os_calls, [])

  _last_fd = 2; os_calls = []
  g = gen()
  assert_equal(g.send(None), "fopening 'src'")
  assert_equal(g.send(None), "fopening 'dst'")
  g.close()
  assert_equal(os_calls, [('fopen', 'src'), ('fclose', 3)])

  _last_fd = 2; os_calls = []
  g = gen()
  assert_equal(g.send(None), "fopening 'src'")
  assert_equal(g.send(None), "fopening 'dst'")
  assert_equal(g.send(None), 'suite')
  g.close()
  assert_equal(os_calls, [('fopen', 'src'), ('fopen', 'dst'), ('fclose', 4), ('fclose', 3)])

  _last_fd = 2; os_calls = []
  g = gen()
  assert_equal(g.send(None), "fopening 'src'")
  assert_equal(g.send(None), "fopening 'dst'")
  assert_equal(g.send(None), 'suite')
  assert_equal(g.send(None), 'fclosing 4')
  g.close()
  assert_equal(os_calls, [('fopen', 'src'), ('fopen', 'dst'), ('fclose', 4), ('fclose', 3)])

  _last_fd = 2; os_calls = []
  g = gen()
  assert_equal(g.send(None), "fopening 'src'")
  assert_equal(g.send(None), "fopening 'dst'")
  assert_equal(g.send(None), 'suite')
  assert_equal(g.send(None), 'fclosing 4')
  assert_equal(g.send(None), 'fclosing 3')
  g.close()
  assert_equal(os_calls, [('fopen', 'src'), ('fopen', 'dst'), ('fclose', 4), ('fclose', 3)])

  _last_fd = 2; os_calls = []
  g = gen()
  assert_equal(g.send(None), "fopening 'src'")
  assert_equal(g.send(None), "fopening 'dst'")
  assert_equal(g.send(None), 'suite')
  assert_equal(g.send(None), 'fclosing 4')
  assert_equal(g.send(None), 'fclosing 3')
  assert_raise(StopIteration, lambda: g.send(None))
  assert_equal(os_calls, [('fopen', 'src'), ('fopen', 'dst'), ('fclose', 4), ('fclose', 3)])

def test_generator__yielding_finally__raise():

  _last_fd = 2
  def yielding_fopen(path):
    nonlocal _last_fd
    yield f'fopening {path!r}'
    os_calls.append(('fopen', path))
    _last_fd += 1
    return _last_fd
  def yielding_fclose(fd):
    yield f'fclosing {fd!r}'
    os_calls.append(('fclose', fd))
  def fclose(fd):
    os_calls.append(('fclose', fd))

  def gen():
    _noerr = _yieldable = True
    # __enter__()
    src_fd = dst_fd = None
    try:
      src_fd = yield from yielding_fopen('src')
      dst_fd = yield from yielding_fopen('dst')
      # suite...
      yield 'suite'
      raise ValueError('simulated error during the suite process')
      # caution, using `yield` in `except` or `finally` statements in `suite...`
      # the default behavior of a GeneratorExit() is to ignore the raise in `suite...` as it should be raised on a g.send() instead of a g.close().
      # (eg GeneratorExit() could be raise from ValueError() finally yield, then the ValueError would be ignored by [1])
      # ...unless you manually set _noerr to False! (that I don't recommand)
    # __exit__()
    except GeneratorExit:  # [1]
      _yieldable = False
      if _noerr: raise
    except: _noerr = False; raise
    finally:
      # deferred one: closing(dst)
      _force = True
      try:
        if _yieldable and dst_fd is not None: dst_fd = yield from yielding_fclose(dst_fd)
      except GeneratorExit:
        _yieldable = False
        if _noerr: raise
      except: _force = False; _noerr = False; raise
      finally:
        try:
          if _force and dst_fd is not None: fclose(dst_fd)
        finally:
          # deferred two: closing(src)
          _force = True
          try:
            if _yieldable and src_fd is not None: src_fd = yield from yielding_fclose(src_fd)
          except GeneratorExit:
            _yieldable = False
            if _noerr: raise
          except: _force = False; _noerr = False; raise
          finally:
            if _force and src_fd is not None: fclose(src_fd)

  _last_fd = 2; os_calls = []
  g = gen()
  assert_equal(g.send(None), "fopening 'src'")
  g.close()
  assert_equal(os_calls, [])

  _last_fd = 2; os_calls = []
  g = gen()
  assert_equal(g.send(None), "fopening 'src'")
  assert_equal(g.send(None), "fopening 'dst'")
  g.close()
  assert_equal(os_calls, [('fopen', 'src'), ('fclose', 3)])

  _last_fd = 2; os_calls = []
  g = gen()
  assert_equal(g.send(None), "fopening 'src'")
  assert_equal(g.send(None), "fopening 'dst'")
  assert_equal(g.send(None), 'suite')
  g.close()
  assert_equal(os_calls, [('fopen', 'src'), ('fopen', 'dst'), ('fclose', 4), ('fclose', 3)])

  _last_fd = 2; os_calls = []
  g = gen()
  assert_equal(g.send(None), "fopening 'src'")
  assert_equal(g.send(None), "fopening 'dst'")
  assert_equal(g.send(None), 'suite')
  assert_equal(g.send(None), 'fclosing 4')
  assert_raise(ValueError, lambda: g.close())
  assert_equal(os_calls, [('fopen', 'src'), ('fopen', 'dst'), ('fclose', 4), ('fclose', 3)])

  _last_fd = 2; os_calls = []
  g = gen()
  assert_equal(g.send(None), "fopening 'src'")
  assert_equal(g.send(None), "fopening 'dst'")
  assert_equal(g.send(None), 'suite')
  assert_equal(g.send(None), 'fclosing 4')
  assert_equal(g.send(None), 'fclosing 3')
  assert_raise(ValueError, lambda: g.close())
  assert_equal(os_calls, [('fopen', 'src'), ('fopen', 'dst'), ('fclose', 4), ('fclose', 3)])

  _last_fd = 2; os_calls = []
  g = gen()
  assert_equal(g.send(None), "fopening 'src'")
  assert_equal(g.send(None), "fopening 'dst'")
  assert_equal(g.send(None), 'suite')
  assert_equal(g.send(None), 'fclosing 4')
  assert_equal(g.send(None), 'fclosing 3')
  assert_raise(ValueError, lambda: g.send(None))
  assert_equal(os_calls, [('fopen', 'src'), ('fopen', 'dst'), ('fclose', 4), ('fclose', 3)])

def test_generator__yielding_finally__raise_in_finally():

  _last_fd = 2
  def yielding_fopen(path):
    nonlocal _last_fd
    yield f'fopening {path!r}'
    os_calls.append(('fopen', path))
    _last_fd += 1
    return _last_fd
  def yielding_fclose(fd):
    yield f'fclosing {fd!r}'
    os_calls.append(('fclose', fd))
    if fd == 4: raise OSError(errno.EBADF, 'simulated EBADF')
  def fclose(fd):
    os_calls.append(('fclose', fd))
    if fd == 4: raise OSError(errno.EBADF, 'simulated EBADF')

  def gen():
    _noerr = _yieldable = True
    # __enter__()
    src_fd = dst_fd = None
    try:
      src_fd = yield from yielding_fopen('src')
      dst_fd = yield from yielding_fopen('dst')
      # suite...
      yield 'suite'
    # __exit__()
    except GeneratorExit:
      _yieldable = False
      if _noerr: raise
    except: _noerr = False; raise
    finally:
      # deferred one: closing(dst)
      _force = True
      try:
        if _yieldable and dst_fd is not None: dst_fd = yield from yielding_fclose(dst_fd)
      except GeneratorExit:
        _yieldable = False
        if _noerr: raise
      except: _force = False; _noerr = False; raise
      finally:
        try:
          if _force and dst_fd is not None: fclose(dst_fd)
        finally:
          # deferred two: closing(src)
          _force = True
          try:
            if _yieldable and src_fd is not None: src_fd = yield from yielding_fclose(src_fd)
          except GeneratorExit:
            _yieldable = False
            if _noerr: raise
          except: _force = False; _noerr = False; raise
          finally:
            if _force and src_fd is not None: fclose(src_fd)

  _last_fd = 2; os_calls = []
  g = gen()
  assert_equal(g.send(None), "fopening 'src'")
  g.close()
  assert_equal(os_calls, [])

  _last_fd = 2; os_calls = []
  g = gen()
  assert_equal(g.send(None), "fopening 'src'")
  assert_equal(g.send(None), "fopening 'dst'")
  g.close()
  assert_equal(os_calls, [('fopen', 'src'), ('fclose', 3)])

  _last_fd = 2; os_calls = []
  g = gen()
  assert_equal(g.send(None), "fopening 'src'")
  assert_equal(g.send(None), "fopening 'dst'")
  assert_equal(g.send(None), 'suite')
  assert_raise(OSError, lambda: g.close())
  assert_equal(os_calls, [('fopen', 'src'), ('fopen', 'dst'), ('fclose', 4), ('fclose', 3)])

  _last_fd = 2; os_calls = []
  g = gen()
  assert_equal(g.send(None), "fopening 'src'")
  assert_equal(g.send(None), "fopening 'dst'")
  assert_equal(g.send(None), 'suite')
  assert_equal(g.send(None), 'fclosing 4')
  assert_raise(OSError, lambda: g.close())
  assert_equal(os_calls, [('fopen', 'src'), ('fopen', 'dst'), ('fclose', 4), ('fclose', 3)])

  _last_fd = 2; os_calls = []
  g = gen()
  assert_equal(g.send(None), "fopening 'src'")
  assert_equal(g.send(None), "fopening 'dst'")
  assert_equal(g.send(None), 'suite')
  assert_equal(g.send(None), 'fclosing 4')
  assert_equal(g.send(None), 'fclosing 3')
  assert_raise(OSError, lambda: g.close())
  assert_equal(os_calls, [('fopen', 'src'), ('fopen', 'dst'), ('fclose', 4), ('fclose', 3)])

  _last_fd = 2; os_calls = []
  g = gen()
  assert_equal(g.send(None), "fopening 'src'")
  assert_equal(g.send(None), "fopening 'dst'")
  assert_equal(g.send(None), 'suite')
  assert_equal(g.send(None), 'fclosing 4')
  assert_equal(g.send(None), 'fclosing 3')
  assert_raise(OSError, lambda: g.send(None))
  assert_equal(os_calls, [('fopen', 'src'), ('fopen', 'dst'), ('fclose', 4), ('fclose', 3)])

