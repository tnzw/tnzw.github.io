def test_indices_len__timing_sum_range_1_10000_2():
  from timeit import timeit
  indices = (1, 10000, 2)
  def timeit_indices_len(): indices_len(indices)
  def timeit_sum_range(): sum(1 for _ in range(*indices))
  a = timeit(timeit_indices_len, number=1000)
  b = timeit(timeit_sum_range, number=1000)
  print(f"  sum(1 for _ in range{indices}) {b}s, indices_len{indices} {a}s")
  assert a < b, f"{a} > {b}"
  #indices_len 0.0005306
  #sum_range 0.3618361

def test_indices_len():
  def sum_range(indices): return sum(1 for _ in range(*indices))
  def test(indices):
    assert_equal(indices_len(indices), sum_range(indices))
  test((1, 100, 1))
  test((1, 100, 20))
  test((1, 100, 200))
  test((109, -1, -6))
  test((-1, -1, -1))
