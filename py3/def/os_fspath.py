def os_fspath(path):
  # https://github.com/python/cpython/blob/3.9/Lib/os.py#L1026
  if isinstance(path, (str, bytes)): return path
  path_type = type(path)
  try: path_repr = path_type.__fspath__(path)
  except AttributeError:
    if hasattr(path_type, '__fspath__'): raise
    else: raise TypeError("expected str, bytes or os.PathLike object, not " + path_type.__name__)
  if isinstance(path_repr, (str, bytes)): return path_repr
  else: raise TypeError("expected {}.__fspath__() to return str or bytes, not {}".format(path_type.__name__, type(path_repr).__name__))
