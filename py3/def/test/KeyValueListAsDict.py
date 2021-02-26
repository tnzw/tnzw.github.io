def test_KeyValueListAsDict___init__():
  d = KeyValueListAsDict()
  assert_equal(d.list, [])
def test_KeyValueListAsDict___init__emptylist():
  l = []
  d = KeyValueListAsDict(l)
  assert_is(d.list, l)
def test_KeyValueListAsDict_fromdict():
  d = KeyValueListAsDict.fromdict({})
  assert_equal(d.list, [])
def test_KeyValueListAsDict_fromdict_nonempty():
  d = KeyValueListAsDict.fromdict({"a": "b", "c": "d"})
  d.list.sort()
  assert_equal(d.list, [("a", "b"), ("c", "d")])
def test_KeyValueListAsDict_if_not():
  d = KeyValueListAsDict.fromdict({})
  assert not d, f"{d!r} equiv True"
def test_KeyValueListAsDict_if():
  d = KeyValueListAsDict.fromdict({"a": "b"})
  assert d, f"{d!r} equiv False"
def test_KeyValueListAsDict_not_in():
  d = KeyValueListAsDict.fromdict({"c": "d"})
  assert "a" not in d, f"{a!r} in {d!r}"
def test_KeyValueListAsDict_in():
  d = KeyValueListAsDict.fromdict({"c": "d", "a": "b"})
  assert "a" in d, f"{a!r} not in {d!r}"
def test_KeyValueListAsDict_or():
  d = KeyValueListAsDict.fromdict({"c": "d", "a": "b"})
  d2 = d | {"c": "e", "d": "c"}
  d.list.sort()
  d2.list.sort()
  assert_equal(d.list, [("a", "b"), ("c", "d")])
  assert_equal(d2.list, [("a", "b"), ("c", "e"), ("d", "c")])
def test_KeyValueListAsDict_ior():
  d = KeyValueListAsDict.fromdict({"c": "d", "a": "b"})
  d |= {"c": "e", "d": "c"}
  d.list.sort()
  assert_equal(d.list, [("a", "b"), ("c", "e"), ("d", "c")])
def test_KeyValueListAsDict_iter():
  expected = set(("c", "a"))
  d = KeyValueListAsDict.fromdict({"c": "d", "a": "b"})
  for k in d: expected.remove(k)
  assert not expected
def test_KeyValueListAsDict_keys():
  expected = set(("c", "a"))
  d = KeyValueListAsDict.fromdict({"c": "d", "a": "b"})
  for k in d.keys(): expected.remove(k)
  assert not expected
def test_KeyValueListAsDict_items():
  expected = set((("c", "d"), ("a", "b")))
  d = KeyValueListAsDict.fromdict({"c": "d", "a": "b"})
  for k, v in d.items(): expected.remove((k, v))
  assert not expected
def test_KeyValueListAsDict_values():
  expected = set(("d", "b"))
  d = KeyValueListAsDict.fromdict({"c": "d", "a": "b"})
  for v in d.values(): expected.remove(v)
  assert not expected
def test_KeyValueListAsDict_len_empty():
  d = KeyValueListAsDict()
  assert_equal(len(d), 0)
def test_KeyValueListAsDict_len_one():
  d = KeyValueListAsDict([("a", "b")])
  assert_equal(len(d), 1)
def test_KeyValueListAsDict_len_two():
  d = KeyValueListAsDict([("a", "b"), ("a", "c")])
  assert_equal(len(d), 2)
def test_KeyValueListAsDict_copy():
  l = [("a", "b"), ("a", "c")]
  d = KeyValueListAsDict(l)
  d2 = d.copy()
  assert d.list is not d2.list
def test_KeyValueListAsDict_clear():
  l = [("a", "b"), ("a", "c")]
  d = KeyValueListAsDict(l)
  d.clear()
  assert_equal(d.list, [])
  assert_equal(l, [])
  assert_equal(d.list, l)
def test_KeyValueListAsDict___getitem__empty():
  l = [("a", "c"), ("a", "b")]
  d = KeyValueListAsDict(l)
  assert_raise(KeyError, lambda: d["b"])
def test_KeyValueListAsDict___getitem__():
  l = [("a", "c"), ("a", "b")]
  d = KeyValueListAsDict(l)
  assert_equal(d["a"], "c")
  d.list.sort()
  assert_equal(d["a"], "b")
def test_KeyValueListAsDict_get():
  l = [("a", "c"), ("a", "b")]
  d = KeyValueListAsDict(l)
  assert_equal(d.get("a"), "c")
  d.list.sort()
  assert_equal(d.get("a"), "b")
def test_KeyValueListAsDict_getall():
  l = [("a", "c"), ("a", "b")]
  d = KeyValueListAsDict(l)
  assert_equal(d.getall("a"), ["c", "b"])
  d.list.sort()
  assert_equal(d.getall("a"), ["b", "c"])
  assert_equal(d.getall("b", "arbitrary"), "arbitrary")
def test_KeyValueListAsDict_pop():
  l = [("a", "c"), ("a", "b")]
  d = KeyValueListAsDict(l)
  assert_equal(d.pop("a"), "c")
  assert_equal(d.pop("a"), "b")
  assert_raise(KeyError, lambda: d.pop("a"))
def test_KeyValueListAsDict_popall():
  l = [("a", "c"), ("a", "b")]
  d = KeyValueListAsDict(l)
  assert_equal(d.popall("a"), ["c", "b"])
  assert_equal(d.popall("a"), [])
def test_KeyValueListAsDict_popitem():
  l = [("a", "c"), ("a", "b")]
  d = KeyValueListAsDict(l)
  assert_equal(d.popitem(), ("a", "b"))
  assert_equal(d.popitem(), ("a", "c"))
  assert_raise(KeyError, lambda: d.popitem())
def test_KeyValueListAsDict_popallitems():
  l = [("a", "c"), ("a", "b")]
  d = KeyValueListAsDict(l)
  assert_equal(d.popallitems(), [("a", "c"), ("a", "b")])
  assert_equal(d.popallitems(), [])
  assert d.list is l
def test_KeyValueListAsDict_replace():
  l = [("a", "c"), ("b", "d"), ("a", "b")]
  d = KeyValueListAsDict(l)
  d.replace("a", "e")
  assert_equal(l, [("a", "e"), ("b", "d"), ("a", "b")])
def test_KeyValueListAsDict_replace_empty():
  l = [("a", "c"), ("a", "b")]
  d = KeyValueListAsDict(l)
  assert_raise(KeyError, lambda: d.replace("b", "e"))
def test_KeyValueListAsDict_replaceall():
  l = [("a", "c"), ("b", "d"), ("a", "b")]
  d = KeyValueListAsDict(l)
  d.replaceall("a", ("e", "f", "g"))
  assert_equal(l, [("a", "e"), ("b", "d"), ("a", "f"), ("a", "g")])
def test_KeyValueListAsDict_replaceall_appends_False():
  l = [("a", "c"), ("b", "d"), ("a", "b")]
  d = KeyValueListAsDict(l)
  assert_raise(IndexError, lambda: d.replaceall("a", ("e", "f", "g"), appends=False))
def test_KeyValueListAsDict___setitem__():
  l = [("a", "c"), ("b", "e"), ("a", "b")]
  d = KeyValueListAsDict(l)
  d["a"] = "e"
  assert_equal(l, [("a", "e"), ("b", "e")])
def test_KeyValueListAsDict_set():
  l = [("a", "c"), ("b", "e"), ("a", "b")]
  d = KeyValueListAsDict(l)
  d.set("a", "e")
  assert_equal(l, [("a", "e"), ("b", "e")])
def test_KeyValueListAsDict_setall_more():
  l = [("a", "c"), ("b", "e"), ("a", "b")]
  d = KeyValueListAsDict(l)
  d.setall("a", ("f", "g", "h"))
  assert_equal(l, [("a", "f"), ("b", "e"), ("a", "g"), ("a", "h")])
def test_KeyValueListAsDict_setall_less():
  l = [("a", "c"), ("b", "e"), ("a", "b")]
  d = KeyValueListAsDict(l)
  d.setall("a", ("f",))
  assert_equal(l, [("a", "f"), ("b", "e")])
def test_KeyValueListAsDict_sort():
  l = [("a", "c"), ("b", "e"), ("a", "b")]
  d = KeyValueListAsDict(l)
  d.sort()
  assert_equal(l, [("a", "b"), ("a", "c"), ("b", "e")])
def test_KeyValueListAsDict_setdefault_existing():
  l = [("a", "c"), ("b", "e"), ("a", "b")]
  d = KeyValueListAsDict(l)
  d.setdefault("a", "h")
  assert_equal(l, [("a", "c"), ("b", "e"), ("a", "b")])
def test_KeyValueListAsDict_setdefault():
  l = [("a", "c"), ("b", "e"), ("a", "b")]
  d = KeyValueListAsDict(l)
  d.setdefault("c", "h")
  assert_equal(l, [("a", "c"), ("b", "e"), ("a", "b"), ("c", "h")])
def test_KeyValueListAsDict_update():
  l = [("a", "c"), ("b", "e"), ("a", "b")]
  d = KeyValueListAsDict(l)
  d2 = KeyValueListAsDict([("g", "h"), ("a", "i"), ("a", "j")])
  d.update(d2, c="o")
  assert_equal(l, [("a", "i"), ("b", "e"), ("a", "j"), ("g", "h"), ("c", "o")])
def test_KeyValueListAsDict___delitem__():
  l = [("a", "c"), ("b", "e"), ("a", "b")]
  d = KeyValueListAsDict(l)
  def delete(d, k): del d[k]
  del d["a"]
  assert_equal(l, [("b", "e")])
  assert_raise(KeyError, lambda: delete(d, "a"))
