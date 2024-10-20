def diff__recompile(result, n):
  ll = [[] for _ in range(n)]
  for ii, line in result:
    for i in ii:
      ll[i].append(line)
  return ll

def diff__u(a, b):
  s = ""
  for ii, line in diff((str(_) + '\n' for _ in a), (str(_) + '\n' for _ in b)):
    end = "\n\\ No newline at end of file\n" if line[-1] != "\n" else ""
    if ii == (0, 1): s += f" {line}{end}"
    elif ii == (0,): s += f"-{line}{end}"
    elif ii == (1,): s += f"+{line}{end}"
    else:            s += f"?{line}{end}"
  return s

def diff__x(*iterables):
  s = ""
  l = len(iterables)
  for ii, line in diff(*((str(_) + '\n' for _ in it) for it in iterables)):
    ss = ["x"] * l
    for i in ii: ss[i] = ' '
    s2 = "".join(ss)
    end = "\n\\ No newline at end of file\n" if line[-1] != "\n" else ""
    s += s2 + ":" + line + end
  return s

def diff__tester(iterables, is_in=None):
  iterables = [list(_) for _ in iterables]
  assert_equal(diff__recompile(diff(*iterables), len(iterables)), iterables)
  if is_in is not None:
    if len(iterables) == 2: assert_in(diff__u(*iterables), is_in)
    else: assert_in(diff__x(*iterables), is_in)

def test_diff__1():
  # diff 0 and 1:
  # a a
  # b c
  # d e
  # e g
  # c

  # `diff -u 0 1` result :
  #  a
  # -b
  # -d
  # -e
  #  c
  # +e
  # +g

  # `diff -u 1 0` result :
  #  a
  # -c
  # +b
  # +d
  #  e
  # -g
  # +c

  diff__tester(
    (
      ["e","e","g"],
      ["e","e","f"],
    ),
    ("""\
 e
 e
-g
+f
""",)
  )

  diff__tester(
    (
      ["a","b","d","e","c"],
      ["a","c","e","g"],
    ),
    ("""\
 a
-b
-d
-e
 c
+e
+g
""", """\
 a
-b
-d
+c
 e
-c
+g
""",)
  )

  diff__tester(
    (
      ["a","b","c","d","e","e"],
      ["A","b","c","e","e"],
    ),
    ("""\
-a
+A
 b
 c
-d
 e
 e
""",)
  )

  diff__tester(
    (
      ["1","x","z","o"],
      ["2","o","y","o"],
    ),
    ("""\
-1
-x
-z
+2
 o
+y
+o
""",)
  )

def test_diff__2():
  # diff:
  # a a a k k
  # b c k a
  # d e
  # e g
  # c

  diff__tester(
    (
      ["a", "b", "d", "e", "c", "k"],
      ["a", "c", "e", "g"],
      ["a", "k"],
      ["k", "a"],
      ["k"],
    ),
    ("""\
   xx:a
xx   :k
 xxxx:b
 xxxx:d
x xxx:c
  xxx:e
 xxxx:c
 xxxx:k
x xxx:g
xxx x:a
""",)
  )

  diff__tester(
    (
      ["k", "a"],
      ["k"],
      ["a", "k"],
      ["a", "b", "d", "e", "c", "k"],
      ["a", "c", "e", "g"],
    ),
    ("""\
  xxx:k
 x   :a
xxx x:b
xxx x:d
xxxx :c
xxx  :e
xxx x:c
xx  x:k
xxxx :g
""",)
  )

  diff__tester(
    (
      ["a", "b", "d", "e", "c", "k"],
      ["k", "a"],
      ["a", "k"],
      ["k"],
      ["a", "c", "e", "g"],
    )
  )

  # diff__tester(
    # (
      # ["a","b","c","d","e","e"],
      # ["A","b","c","e","e"],
      # ["A","b","C","D","e","e"],
    # ),
    # ("""\
 # xx:a
# x  :A
 # b
 # c
# -d
 # e
 # e
# """,)
  # )

  diff__tester(
    (
      ["a","b","c","d","e","e"],
      ["A","b","c","e","e"],
      ["A","b","c","D","e","e"],
    ),
    ("""\
x  :A
 xx:a
   :b
   :c
 xx:d
xx :D
   :e
   :e
""",)
  )

  diff__tester(
    (
      'aZY', 'YZc', 'Yde',  # diffing non sorted iterables
    ),
    ("""\
x  :Y
 xx:a
  x:Z
 xx:Y
x x:c
xx :d
xx :e
""",)
  )

  diff__tester(
    (
      'aYZ', 'YZc', 'Yde',  # upper cased letters are sorted alphabeticaly, always 'Y' first, then 'Z'. 'acde' are noise.
    ),
    ("""\
 xx:a
   :Y
  x:Z
x x:c
xx :d
xx :e
""",)
  )
