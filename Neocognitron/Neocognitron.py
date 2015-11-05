import numpy as np
from matplotlib import pyplot as plt
from scipy.misc import toimage

class Unit:
    def __init__(self,i,j,isInput=False):
        self.i = i
        self.j = j
        self.incomingUnits = []
        self.output = 0
        self.midIncomingUnit = 0


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
                    x.midIncomingUnit = 0
                elif x.i == 0:
                    x.incomingUnits = self.C0.arrays[0].arr[x.i:x.i+2,x.j-1:x.j+2].ravel().tolist()
                    x.midIncomingUnit = 1
                elif x.j == 0:
                    x.incomingUnits = self.C0.arrays[0].arr[x.i-1:x.i+2,x.j:x.j+2].ravel().tolist()
                    x.midIncomingUnit = 2
                else:
                    x.incomingUnits = self.C0.arrays[0].arr[x.i-1:x.i+2,x.j-1:x.j+2].ravel().tolist()
                    if x.i and x.j ==19:
                        x.midIncomingUnit = 3
                    elif x.i == 19:
                        x.midIncomingUnit = 4
                    elif x.j == 19:
                        x.midIncomingUnit = 3


                x.incomingUnits = [(u,0) for u in x.incomingUnits ]

    def defineInput(self, array):
        self.C0.arrays[0].arr = array


    def fire(self, train = False):
        for arr in self.S1.arrays:
            for u in arr.arr.flat:
                e = sum([n[0].output*n[1] for n in u.incomingUnits])
                if e > 0:
                    u.output = e
                if train == True:
                    setOutputw = u.incomingUnits[u.midIncomingUnit][0].output * self.alpha
                    for iu in range(len(u.incomingUnits)):
                        u.incomingUnits[iu]=(u.incomingUnits[iu][0],setOutputw)
                        u.output = 0

    def arrayVisualizeS1(self):
        for a,n in zip(self.S1.arrays,range(12)):
            array = a.arr
            ph = np.empty(array.shape)
            for i in range(array.shape[0]):
                for j in range(array.shape[1]):
                    ph[i,j]= array[i,j].output
                    img = toimage(ph)
            plt.imshow(img)
            plt.subplot(4,3,n+1)
        print(ph)
        plt.show()

if __name__ == "__main__":
    n = Network()
    n.connectC0S1()
    ran = np.random.random_sample([19,19])
    n.defineInput(ran)
    n.fire(train = True)
    ran[:,-5:18] = 0
    n.defineInput(ran)
    n.fire()
    print(n.S1.arrays[0].arr[0,0].incomingUnits)     # Example that inspects the incoming units of the first unit of the first array of the S1 layer
    n.arrayVisualizeS1()