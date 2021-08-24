def re_compilesearch__assert_match(regexp, matching, message=None, *, exact_match=True):
  match = regexp.search(matching)
  assert match, message or f"{regexp.pattern!r} does not match {matching!r}"
  if exact_match:
    assert match.span() == (0, len(matching)), f"wrong match, span {match.span()!r} != {(0, len(matching))!r}"

def test_re_compilesearch():
  assert_match = re_compilesearch__assert_match
  assert_match(re_compilesearch("rik"), "rik")
  assert_match(re_compilesearch("rik"), "πικ")
  assert_match(re_compilesearch("cœur"), "coeur")
  assert_match(re_compilesearch("coeur"), "cœur")
  assert_match(re_compilesearch("STRAß", re.I), "Strass")
  assert_match(re_compilesearch("STRASS", re.I), "Straß")
  assert_match(re_compilesearch("abthvfficde"), "abthvfficde")
  assert_match(re_compilesearch("abthvfficde"), "abᵺvﬃcde")
  assert_match(re_compilesearch("abthvfficde"), "abtƕfﬁcde")

def test_re_compilesearch__mk_translater():
  assert_equal(re_compilesearch._mk_translater({"ryo":["AB", "CD"]}), {"ryo":"(?:ryo|AB|CD)","AB":"(?:ryo|AB|CD)","CD":"(?:ryo|AB|CD)"})
