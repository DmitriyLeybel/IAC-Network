import numpy as np
from matplotlib import pyplot as plt
from scipy.misc import toimage

class Unit:
    def __init__(self,i,j,isInput=False):
        self.i = i
        self.j = j
        self.incomingUnits = []
        self.output = 0


class Array:
    def __init__(self, anum, size):
        self.arrayNum = anum
        self.arr = np.empty([size,size],dtype='O')
    def buildArray(self):
        pass

class Layer:
    def __init__(self, lname):
        self.lname = lname    # e.g S1, C0, C1...
        if self.lname == 'C0':
            self.arrays = [Array(1,19)]
            for i in range(19):
                for j in range(19):
                    self.arrays[0].arr[i,j]= Unit(i,j)
        if self.lname == 'S1':
            self.arrays=[]
            for n in range(12):
                a = Array(n,19)
                for i in range(19):
                    for j in range(19):
                        a.arr[i,j]= Unit(i,j)
                self.arrays.append(a)


class Network:
    def __init__(self):
        self.C0 = Layer('C0')
        self.S1 = Layer('S1')
        self.alpha = 1

    def connectC0S1(self):
        for array in self.S1.arrays:
            for x in array.arr.ravel():
                if x.i == 0 and x.j == 0:
                    x.incomingUnits = self.C0.arrays[0].arr[x.i:x.i+2,x.j:x.j+2].ravel().tolist()
                elif x.i == 0:
                    x.incomingUnits = self.C0.arrays[0].arr[x.i:x.i+2,x.j-1:x.j+2].ravel().tolist()
                elif x.j == 0:
                    x.incomingUnits = self.C0.arrays[0].arr[x.i-1:x.i+2,x.j:x.j+2].ravel().tolist()
                else:
                    x.incomingUnits = self.C0.arrays[0].arr[x.i-1:x.i+2,x.j-1:x.j+2].ravel().tolist()
                x.incomingUnits = [(u,0) for u in x.incomingUnits ]

    def defineInput(self, array):
        self.C0.arrays[0].arr = array

    def fire(self):
        for arr in self.S1.arrays:
            for u in arr.arr.flat:
                e = sum([n[0].output*n[1] for n in u.incomingUnits])
                if e > 0:
                    u.output = e
                for iu in range(len(u.incomingUnits)):
                    u.incomingUnits[iu]=(u.incomingUnits[iu][0],u.incomingUnits[iu][0].output)

    def arrayVisualize(self,array):

        ph = np.empty(array.shape)
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                ph[i,j]= array[i,j].output

        img = toimage(ph)
        plt.imshow(img)
        plt.show()

if __name__ == '__main__':
    n = Network()
    n.connectC0S1()
    print(n.S1.arrays[0].arr[0,0].incomingUnits)
    n.fire()
