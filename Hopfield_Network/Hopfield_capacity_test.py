from Hopfield import *

def randword(n):
    w = []
    for x in range(n):
        w.append(str(randint(0,1)))
    w = ''.join(w)
    return w

def makestatelist(length, amount):
    listOfWords = []
    for x in range(amount):
        binWord = binaryWord(randword(length))
        listOfWords.append(binWord)
    return stateList(*listOfWords)


sList1 = makestatelist(100,5)
n = network(sList1)
n.trainCorrelationMatrix()
dic1 = {}
for x in range(0,101):
    dic1[x] =0
for w in sList1:
    final = n.activateInitial(''.join(w.word), it_num=50)
    wword = list(map(int,list(w.word)))
    dic1[int(sps.distance.hamming(final,wword))] +=1

sList2 = makestatelist(100,10)
n = network(sList2)
n.trainCorrelationMatrix()
dic2 = {}
for x in range(0,101):
    dic2[x] =0
for w in sList1:
    final = n.activateInitial(''.join(w.word), it_num=50)
    wword = list(map(int,list(w.word)))
    dic2[int(sps.distance.hamming(final,wword))] +=1

sList3 = makestatelist(100,15)
n = network(sList3)
n.trainCorrelationMatrix()
dic3 = {}
for x in range(0,101):
    dic3[x] =0
for w in sList3:
    final = n.activateInitial(''.join(w.word), it_num=50)
    wword = list(map(int,list(w.word)))
    dic3[int(sps.distance.hamming(final,wword)*len(final))] +=1
    print(final, wword)