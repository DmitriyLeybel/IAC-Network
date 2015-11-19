import numpy as np
from matplotlib import pyplot as plt
from scipy.misc import toimage
import tkinter.messagebox as tkmb

class Unit:
    def __init__(self,i,j,isInput=False):   # Creates a unit with a given i,j location within an array
        self.i = i
        self.j = j
        self.incomingUnits = [] # Initiates the list of units sending their signal forward to this unit
        self.output = 0
        self.midIncomingUnit = 0    # Used as a helper to assign windows
        self.incomingInhibitory = ()


class Array:
    def __init__(self, anum, size): # Defines a square array of a specified size and # designation
        self.arrayNum = anum
        self.arr = np.empty([size,size],dtype='O')
    def buildArray(self):
        pass

class Layer:
    def __init__(self, lname): # Builds array based on the name given
        self.lname = lname    # e.g S1, C0, C1...
        if self.lname == 'C0':
            self.arrays = [Array(1,19)]
            for i in range(19):
                for j in range(19):
                    self.arrays[0].arr[i,j]= Unit(i,j)
        elif self.lname == 'S1':
            self.arrays=[]
            for n in range(12):
                a = Array(n,19)
                for i in range(19):
                    for j in range(19):
                        a.arr[i,j]= Unit(i,j)
                self.arrays.append(a)
        elif self.lname == 'V0':
            self.arrays = [Array(1,19)]
            for i in range(19):
                for j in range(19):
                    self.arrays[0].arr[i,j]= Unit(i,j)



class Network:
    def __init__(self):
        self.C0 = Layer('C0')
        self.S1 = Layer('S1')
        self.V0 = Layer('V0')
        self.alpha = .25
        self.v = 0

    def connectC0S1(self):
        for array in self.S1.arrays: # Loops over the S1 arrays
            for x in array.arr.ravel(): # For every unit of every array of S1, it connects a window of input units
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
    def connectV(self): # Still needs to connect V0 to S1
        for x in self.V0.arrays[0].arr.ravel(): # Connects inhibitory array to the input array with fixed weights
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
        for x in self.V0.arrays[0].arr.ravel(): # Sets the fixed weights of the input and inhibitory layer
            for iu,y in zip(x.incomingUnits, range(len(x.incomingUnits))):
                if x.i == iu.i and x.j == iu.j:
                    x.incomingUnits[y] = (iu,1)
                else:
                    x.incomingUnits[y] = (iu, 1/3)
        for l in self.S1.arrays:
            for a in l.arr.ravel():
                loc = np.where(l.arr==a)
                a.incomingInhibitory = (self.V0.arrays[0].arr[loc[0],loc[1]][0], 0)




    def defineInput(self, array):
        for x,y in zip(self.C0.arrays[0].arr.flat,range(self.C0.arrays[0].arr.size)):
            x.output = array.flat[y]


    def fire(self, train = False):
        r = 0   # Obtains the v value for the inhibitory calculations
        for iu in self.V0.arrays[0].arr.ravel():
            for cu in iu.incomingUnits:
                r += cu[0].output*cu[1]
        self.v = r
        for arr,ind in zip(self.S1.arrays,range(len(self.S1.arrays))):  # Loops through the S1 arrays
            for u in arr.arr.flat:
                e = sum([n[0].output*n[1] for n in u.incomingUnits])    # Obtains the sums of a unit's incoming values
                if e > 0:
                    loc = np.where(arr.arr==u)

                    u.output = ((1+e)/(1+self.v*u.incomingInhibitory[1]))-1
                    # u.output = e

                if train == True:   # Trains the weights between the S1 and C0 layers
                    setOutputw = u.incomingUnits[u.midIncomingUnit][0].output * self.alpha
                    for iu in range(len(u.incomingUnits)):
                        u.incomingUnits[iu]=(u.incomingUnits[iu][0],setOutputw)
                        u.output = 0
            if train == True:   # Trains the connections between the inhibitory layer and the S1 layer
                setOutputw = self.alpha * arr.arr[9,9].incomingUnits[arr.arr[9,9].midIncomingUnit][0].output
                for set in arr.arr.ravel():
                    set.incomingInhibitory = (set.incomingInhibitory, setOutputw)

    def arrayVisualizeS1(self): # Used to plot all of the arrays
        for a,n in zip(self.S1.arrays,range(12)): # Plots all of the S1 arrays
            array = a.arr
            ph = np.empty(array.shape)
            for i in range(array.shape[0]):
                for j in range(array.shape[1]):
                    ph[i,j]= array[i,j].output
                    img = toimage(ph)
            plt.subplot(5,3,n+1)
            plt.imshow(img)
            plt.title('S1_{0}'.format(n+1))
        ph = np.empty(self.C0.arrays[0].arr.shape)
        for i in range(self.C0.arrays[0].arr.shape[0]): # Plots the input array
                for j in range(self.C0.arrays[0].arr.shape[1]):
                    ph[i,j]= self.C0.arrays[0].arr[i,j].output
                    img = toimage(ph)
        plt.subplot(5,3,13)
        for i in range(self.V0.arrays[0].arr.shape[0]): # Plots the inhibitory array
            for j in range(self.V0.arrays[0].arr.shape[1]):
                ph[i,j]= self.V0.arrays[0].arr[i,j].output
                img = toimage(ph)
        plt.subplot(5,3,13)
        plt.imshow(img)
        # plt.subplot(5,3,13)
        plt.title('C0')
        plt.tight_layout()
        plt.draw()


if __name__ == "__main__":
    n = Network()
    A = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0],
 [0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0],
 [0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
 [0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
 [0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
 [0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
 [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
 [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
 [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
 [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
 [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
 [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]])
    n.connectC0S1()
    n.connectV()
    ran = np.random.random_sample([19,19])
    n.defineInput(A)
    n.fire(train = True)
    ran[:,-5:18] = 0
    n.defineInput(A)
    n.fire()
    print(n.S1.arrays[0].arr[0,0].incomingUnits)     # Example that inspects the incoming units of the first unit of the first array of the S1 layer
    n.arrayVisualizeS1()
    plt.show()
