def test_undefined():
  if undefined: assert False
  assert not undefined
  if undefined == True: assert False
  assert undefined != True
  if undefined == False: assert False
  assert undefined != False
  if undefined == None: assert False
  assert undefined != None
  if undefined == 0: assert False
  assert undefined != 0
  assert undefined == undefined
  if undefined != undefined: assert False
  assert undefined is undefined
  if undefined is not undefined: assert False
  assert repr(undefined) == 'undefined'
  assert str(undefined) == 'undefined'
  def assign(o, k, v): o[k] = v
  assert_raise(AttributeError, lambda: setattr(undefined, 'hello', 'world'))
  assert_raise(TypeError, lambda: assign(undefined, 'hello', 'world'))
  assert_raise(TypeError, lambda: len(undefined))
