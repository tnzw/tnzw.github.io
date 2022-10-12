# undefined.py Version 1.0.0
# Copyright (c) 2022 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class undefined:
  __slots__ = ()
  def __repr__(self): return 'undefined'
  def __bool__(self): return False
  def __eq__(self, other): return other is undefined
  def __ne__(self, other): return other is not undefined
undefined = undefined()
