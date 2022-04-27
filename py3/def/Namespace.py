# Namespace.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class Namespace(object):
  """Try to have same behavior as argparse.Namespace."""
  # in this implementation, we only implement __delegation_methods__.
  def __init__(self, **kw):
    for k, v in kw.items(): setattr(self, k, v)
  def __repr__(self):
    ikw, skw = [], {}
    for k, v in self.__dict__.items():
      if k.isidentifier(): ikw.append(f"{k}={v!r}")
      else: skw[k] = v
    if skw: ikw.append(f"**{skw}")
    return f"{self.__class__.__name__}({', '.join(ikw)})"

  # collections.abc.Mapping like
  def __contains__(self, key): return key in self.__dict__
  def __iter__(self): return iter(self.__dict__)
  def __len__(self): return len(self.__dict__)

  # dict like
  def __eq__(self, other): return isinstance(other, Namespace) and self.__dict__ == other.__dict__
  def __ior__(self, other):
    """from original python dict()/dict.update() behavior, using setattr(self, ...)"""
    if isinstance(other, Namespace): other = other.__dict__
    # class Mapping():
    #   def keys(self): yield key
    #   def __getitem__(self, key): return value
    if hasattr(other, "keys"):
      for k in other.keys(): setattr(self, k, other[k])
    else:
      # class Iterable():
      #   def __iter__(self): yield (key, value)
      it = None
      try: it = iter(other)
      except TypeError: pass
      else:
        for k, v in it: setattr(self, k, v)
      if it is None:
        # class Gettable():
        #   def __getitem__(self, index): return (key, value) or raise IndexError
        i = 0
        while True:
          try: v = other[i]
          except IndexError: break
          k, v = v
          setattr(self, k, v)
          i += 1
    #for k, v in kwarg.items(): setattr(self, k, v)
    return self
  def __or__(self, other):
    self = self.__class__(**self.__dict__)
    self.__ior__(other)
    return self
