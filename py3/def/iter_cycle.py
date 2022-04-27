# iter_cycle.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def iter_cycle(iterable):
  """\
iter_cycle('ABCD') --> A B C D A B C D A B C D ...

Crée un itérateur qui renvoie les éléments de l'itérable en en sauvegardant une
copie. Quand l'itérable est épuisé, renvoie les éléments depuis la sauvegarde.
Répète à l'infini.

Note, cette fonction peut avoir besoin d'un stockage auxiliaire important (en
fonction de la longueur de l'itérable).
"""
  # https://docs.python.org/fr/3/library/itertools.html#itertools.cycle
  l = []
  for _ in iterable:
    l.append(_)
    yield _
  while True: yield from l
