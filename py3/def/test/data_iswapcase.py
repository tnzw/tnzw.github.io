def test_data_iswapcase_timing_bytearray():
  from timeit import timeit
  data = bytearray(b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
  def timeit_swapcase(): data[:] = data.swapcase()
  def timeit_iswapcase(): data_iswapcase(data)
  a = timeit(timeit_swapcase, number=1000)
  b = timeit(timeit_iswapcase, number=1000)
  print(f"  bytearray[:] = bytearray.swapcase() {a}s, data_iswapcase(bytearray) {b}s")
  assert a <= b, f"{a} > {b}"
  #swapcase 0.00040353
  #iswapcase 0.02622158
def test_data_iswapcase_timing_str_list():
  from timeit import timeit
  str_array = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
  str_list = [_ for _ in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"]
  def timeit_swapcase(): data = str_array.swapcase()
  def timeit_iswapcase(): data_iswapcase(str_list)
  a = timeit(timeit_swapcase, number=1000)
  b = timeit(timeit_iswapcase, number=1000)
  print(f"  new_str = str.swapcase() {a}s, data_iswapcase(str_list) {b}s")
  assert a <= b, f"{a} > {b}"
  #swapcase 0.00069
  #iswapcase 0.02006
def test_data_iswapcase_timing_str():
  from timeit import timeit
  str_array = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
  def timeit_swapcase(): data = str_array.swapcase()
  def timeit_iswapcase(): data = data_iswapcase([_ for _ in str_array])
  a = timeit(timeit_swapcase, number=1000)
  b = timeit(timeit_iswapcase, number=1000)
  print(f"  new_str = str.swapcase() {a}s, new_str = data_iswapcase([_ for _ in str]) {b}s")
  #swapcase 0.00070
  #iswapcase 0.02098
