# winreg_ScankeyIterator.py Version 1.0.0
# Copyright (c) 2022 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class winreg_ScankeyIterator:
  __slots__ = ('gi',)
  def __init__(self, gi): self.gi = gi
  #def __del__ let "gi" do the job
  def __iter__(self): return self.gi.__iter__()
  def __next__(self): return self.gi.__next__()
  #def __getattr__(self, name): return getattr(self.gi, name)
  def __enter__(self): return self
  def __exit__(self, *a): self.gi.close()
  def close(self): self.gi.close()
