import numpy as np


class Network:

    def __init__(self, sizeInput, sizeOutput, sizeHidden, learningRate):

        self.input = np.empty(sizeInput)
        self.output = np.empty(sizeOutput)
        # Weight matrices
        self.inputHidden = np.random.rand(sizeInput,sizeHidden)
        self.hiddenOutput = np.random.rand(sizeHidden, sizeOutput)

        self.learningRate = learningRate
        # Bias weight arrays(separate from the weight matrices)
        self.hiddenBias = np.random.rand(sizeHidden)
        self.outputBias = np.random.rand(sizeOutput)

        self.target = []
        # Used for backpropagation of error
        self.inputOfOutput = np.empty(sizeOutput)
        self.hiddenToOutput = np.empty(sizeHidden)
        self.outputErrInfo = []

    def activationFunction(self,val):
        return 1/(1 + np.exp(-val))

    def actDeriv(self,val):
        return self.activationFunction(val)*(1-self.activationFunction(val))

    def assignTarget(self,targetList):
        self.target = np.array(targetList)

    def assignInput(self,listOfValues):
        self.input = listOfValues

    def feedForward(self):
        self.inputToHidden = np.dot(self.input,self.inputHidden)
        # Adds the respective bias values to the hidden neurons
        for node,bias in zip(self.inputToHidden, self.hiddenBias):
            node += bias
        aF = np.vectorize(self.activationFunction)
        # self.hiddenToOutput are the activations of the hidden layer
        self.hiddenToOutput = aF(self.inputToHidden)
        self.inputOfOutput = np.dot(self.hiddenToOutput, self.hiddenOutput)
        for node, bias in zip(self.inputOfOutput, self.outputBias):
            node += bias
        outputOfOutput = aF(self.inputOfOutput)
        self.output = outputOfOutput

    def feedBack(self):
        aFD = np.vectorize(self.actDeriv)
        self.outputErrInfo = (self.target - self.output) *aFD(self.inputOfOutput)
        self.hiddenOutputWeightCorrection = self.learningRate*(np.outer(self.hiddenToOutput,self.outputErrInfo))
        self.outputBiasCorrection = self.learningRate*self.outputErrInfo
        self.hiddenErrCorrSums = np.dot(self.outputErrInfo, self.hiddenOutput)
        self.hiddenErrInfo = self.hiddenErrCorrSums*aFD(self.inputToHidden)
        self.inputHiddenWeightCorrection = self.learningRate*np.outer(self.input, self.hiddenErrInfo)
        self.hiddenBiasCorrection = self.learningRate*self.hiddenErrInfo

    def update(self):
        self.hiddenOutput += self.hiddenOutputWeightCorrection
        self.outputBias += self.outputBiasCorrection
        self.inputHidden += self.inputHiddenWeightCorrection
        self.hiddenBias += self.hiddenBiasCorrection

    def fire(self,cycles):
        for x in range(cycles):
            self.feedForward()
            self.feedBack()
            self.update()
        self.feedForward()
        return self.output


if __name__ == '__main__':
    n = Network(5,5,5,.7)
    n.assignInput([1,0,1,1,0])
    n.assignTarget([1,0,1,0,0])
    print(n.fire(10))



