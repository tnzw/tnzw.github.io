# decoder_fromparser.py Version 1.1.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def decoder_fromparser(typename, parser_class, event_names, *, handle_event_names=True, method_name=None, module=None):
  """\
Returns a new subclass of parser_class to add decoder methods to the parser.

Exemple:

    HTMLDecoder = decoder_fromparser(
      "HTMLDecoder",
      html.parser.HTMLParser,
      "starttag endtag startendtag data entityref charref comment decl pi")
    print(HTMLDecoder().decode("<!doctype html><html><body><p>some data</p></body></html>"))

A "parser" is like:

    class Parser(object):
      [def reset(self): ...]
      def feed(self, data): ...
      def close(self): ...
      def handle_<event_name>(self, ...): ...

A "decoder" is like:

    class Decoder(object):
      def transcode(iterable=None, *, stream=False): ...
      [decode = transcode]

The resulting subclass would look like:

    class ParserDecoder(Parser):
      def transcode(iterable=None, *, stream=False): ...
      decode = transcode
      def handle_<event_name>(self, ...): ...
"""
  # code inspired by collections.namedtuple
  typename = str(typename)
  if isinstance(event_names, str): event_names = event_names.replace(",", " ").split()
  event_names = list(map(str, event_names))
  if not typename.isidentifier(): raise ValueError(f'Type names must be valid identifiers: {typename!r}')
  #seen = set()
  for name in event_names:
    if type(name) is not str: raise TypeError('Event names must be strings')
    if not ("_" + name).isidentifier(): raise ValueError(f'Event names must be valid identifiers: {name!r}')
    #if _iskeyword(name): raise ValueError(f'Type names and field names cannot be a keyword: {name!r}')
    #if name in seen: raise ValueError(f'Encountered duplicate event name: {name!r}')
    #seen.add(name)
  #if not event_names: raise ValueError(f'Event names must not be empty')
  def transcode(self, iterable=None, *, stream=False):
    self._transcoded = []
    if iterable is not None: self.feed(iterable)
    if not stream: self.close()  # no need to reset
    e, self._transcoded = self._transcoded, None
    return e
  if method_name is None: class_namespace = {"transcode": transcode, "decode": transcode}
  else:
    method_name = str(method_name)
    if not method_name.isidentifier(): raise ValueError(f'Method names must be valid identifiers: {method_name!r}')
    class_namespace = {method_name: transcode}
  if handle_event_names:
    for _ in event_names:
      exec(f"def handle_{_}(self, *a): self._transcoded.append(({_!r}, a))\nclass_namespace['handle_{_}'] = handle_{_}", {}, {"class_namespace": class_namespace})
  else:
    for _ in event_names:
      exec(f"def handle_{_}(self, *a): self._transcoded.append(a)\nclass_namespace['handle_{_}'] = handle_{_}", {}, {"class_namespace": class_namespace})
  result = type(typename, (parser_class,), class_namespace)
  if module is None: return result
  result.__module__ = module
  return result
