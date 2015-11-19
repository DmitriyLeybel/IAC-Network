import numpy as np


class Network:

    def __init__(self, sizeInput, sizeOutput, sizeHidden, learningRate):
        self.input = np.empty(sizeInput)
        self.output = np.empty(sizeOutput)
        self.inputHidden = np.empty([sizeInput,sizeHidden])
        self.hiddenOutput = np.empty([sizeHidden, sizeOutput])
        self.learningRate = learningRate
        self.hiddenBias = 0
        self.outputBias = 0

    def activationFunction(self,val):
        return 1/(1 + np.exp(-val))

    def actDeriv(self,val):
        self.activationFunction(val)*(1-self.activationFunction(val))

    def feedForward(self):
        # Multiply inputHiddenArray by input array
        # Use the hidden unit array and multiply it by the hiddenOutput array
        #Return Output array






