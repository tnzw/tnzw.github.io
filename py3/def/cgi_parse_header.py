# Version 20230611
# This code is completely copied from
# https://github.com/python/cpython/blob/3.12/Lib/cgi.py#L238
# cgi module is removed in python version 3.13
def cgi_parse_header(line):
  """\
Parse a Content-type like header.

Return the main content-type and a dictionary of options.

"""
  def _parseparam(s):
    while s[:1] == ';':
      s = s[1:]
      end = s.find(';')
      while end > 0 and (s.count('"', 0, end) - s.count('\\"', 0, end)) % 2:
        end = s.find(';', end + 1)
      if end < 0:
        end = len(s)
      f = s[:end]
      yield f.strip()
      s = s[end:]
  parts = _parseparam(';' + line)
  key = parts.__next__()
  pdict = {}
  for p in parts:
    i = p.find('=')
    if i >= 0:
      name = p[:i].strip().lower()
      value = p[i+1:].strip()
      if len(value) >= 2 and value[0] == value[-1] == '"':
        value = value[1:-1]
        value = value.replace('\\\\', '\\').replace('\\"', '"')
      pdict[name] = value
  return key, pdict
