import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial as sps
from random import *

class binaryWord:

    def __init__(self, word):   # Initializes the binaryWord object with a given binary sequence
        word = str(word)
        self.word = np.array([], dtype='u1')
        for x in word:
            self.word = np.append(self.word, x)

    def __len__(self):
        return len(self.word)

    def __iter__(self):
        for x in self.word:
            yield x


class stateList:

    def __init__(self, *args):  # Initializes the stateList object with a chosen amount of states/binaryWords

        self.sList = np.array([],dtype=binaryWord)
        for word in args:
            self.sList = np.append(self.sList,word)
            self.lengthOfWord = len(word.word)

    def __iter__(self):
        for x in self.sList:
            yield x

    def __len__(self):
        return len(self.sList)

    def __getitem__(self, item):
        return self.sList[item]


class network:

    @classmethod
    def hammingDistance(cls,s1,s2):
        s1 = s1.word
        s2 = s2.word
        return sps.distance.hamming(s1, s2)*len(s1)

    def __init__(self, sList=stateList()):   # Initializes network object within which the network can learn and be tested
        self.sList = sList
        self.wMatrix = np.zeros([len(self.sList[0]),len(self.sList[0])])

    def trainCorrelationMatrix(self):    # Trains a network to the list of states provided within a stateList
        for x in self.sList:
            for y,i in zip(x,range(len(x))):
                for z,j in zip(x, range(len(x))):
                    self.wMatrix[i,j] += (2*int(x.word[i])-1)*(2*int(x.word[j])-1)
        np.fill_diagonal(self.wMatrix, 0)

    def activateInitial(self, initial, it_num=None):     # Activates the network at the given initial state and runs it until there is no more change, then outputs the final state
        init = list(str(initial))
        init = list(map(int, init))
        if len(initial) < self.sList.lengthOfWord:
            for x in range(self.sList.lengthOfWord-len(initial)):
                init.append(0)
        if not it_num:
            while True:
                change = 0
                rList = list(range(len(initial)))
                shuffle(rList)
                for x in rList:
                    if np.dot(init,self.wMatrix[:,x]) >=0:
                        if init[x] != 1:
                            init[x] = 1
                            change += 1
                    elif np.dot(init,self.wMatrix[:,x]) <0:
                        if init[x] != 0:
                            init[x] = 0
                            change += 1

                if change == 0:
                    break
            return init

        else:
            for x in range(it_num):
                change = 0
                rList = list(range(len(initial)))
                shuffle(rList)
                for x in rList:
                    if np.dot(init,self.wMatrix[:,x]) >=0:
                        if init[x] != 1:
                            init[x] = 1
                            change += 1
                    elif np.dot(init,self.wMatrix[:,x]) <0:
                        if init[x] != 0:
                            init[x] = 0
                            change += 1
                if change == 0:
                    break
            return init