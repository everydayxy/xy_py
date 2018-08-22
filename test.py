def testFun():
  temp = [lambda x ,i=i : i*x for i in range(4)]
  return temp

for everyLambda in testFun():
  print (everyLambda(2))


