from Hopfield import *

a = binaryWord(1001110101)
b = binaryWord(1001011001)
z = stateList(a,b)
n = network(z)
n.trainCorrelationMatrix(z)

print(n.wMatrix)