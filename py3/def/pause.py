def pause():
  print("Press enter to continue...", end="")
  try:
    input()
  except EOFError:
    print()
