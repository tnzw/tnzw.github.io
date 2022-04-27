def test_zip2__1():
  assert_equal(
    list(zip2('abcde', range(3), range(4))),
    [('a', 0, 0), ('b', 1, 1), ('c', 2, 2), ('d', None, 3), ('e', None, None)]
  )
def test_zip2__2():
  assert_equal(
    list(zip2('a', 'bc', 'def')),
    [('a', 'b', 'd'), (None, 'c', 'e'), (None, None, 'f')]
  )
def test_zip2__default_1():
  assert_equal(
    list(zip2('a', 'bc', 'def', 'gh', default='x')),
    [('a', 'b', 'd', 'g'), ('x', 'c', 'e', 'h'), ('x', 'x', 'f', 'x')]
  )

def test_zip2__timing_todel_stress():
  from timeit import timeit
  data = bytearray(b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
  def timeit_zip2():
    for i in zip2((range(n) for n in range(10))):
      pass
  a = timeit(timeit_zip2, number=1000)
  print(f"  zip2() {a}s")
def test_zip2__timing_nostress():
  from timeit import timeit
  data = bytearray(b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
  def timeit_zip2():
    for i in zip2((range(10) for n in range(10))):
      pass
  a = timeit(timeit_zip2, number=1000)
  print(f"  zip2() {a}s")
