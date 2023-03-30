# Version 20230101
def os_fspath(path):
  # Inspired from https://github.com/python/cpython/blob/3.11/Lib/os.py#L1036
  # __fspath__ AttributeError handling changed.
  if isinstance(path, (str, bytes)): return path
  path_type = type(path)
  try: fspath_func = path_type.__fspath__
  except AttributeError: raise TypeError('expected str, bytes or os.PathLike object, not ' + path_type.__name__) from None
  path_repr = fspath_func(path)
  if isinstance(path_repr, (str, bytes)): return path_repr
  raise TypeError(f'expected {path_type.__name__}.__fspath__() to return str or bytes, not {type(path_repr).__name__}')
