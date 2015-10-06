from Hopfield import *

a = binaryWord(1001110011)
b = binaryWord(1000100100)
c = binaryWord(1101011010)
d = binaryWord(1101110001)
z = stateList(a,c,b,d)
n = network(z)
n.trainCorrelationMatrix(z)
z =n.activateInitial('1001000101')

print(n.wMatrix)
print(z)