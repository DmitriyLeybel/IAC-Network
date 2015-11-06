from Neocognitron import *
alist = [np.random.rand(19,19), np.random.rand(19,19)]
def feed(arrayList):
    for array in arrayList:
        n = Network()
        n.connectC0S1()
        n.defineInput(array)
        n.fire(train=True)
        array[:,-5:18] = 0
        n.defineInput(array)
        n.fire()
        n.arrayVisualizeS1()
        input('Input Necessary')
        plt.show()
