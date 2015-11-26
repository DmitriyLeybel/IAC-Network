import numpy as np
import matplotlib.pyplot as plt


class Network:

    def __init__(self, sizeInput, sizeOutput, sizeHidden, learningRate):

        self.input = np.empty(sizeInput)
        self.output = np.empty(sizeOutput)
        # Weight matrices
        self.inputHidden = np.random.rand(sizeInput,sizeHidden)-.5
        self.hiddenOutput = np.random.rand(sizeHidden, sizeOutput)-.5

        self.learningRate = learningRate
        # Bias weight arrays(separate from the weight matrices)
        self.hiddenBias = np.random.rand(sizeHidden)-.5
        self.outputBias = np.random.rand(sizeOutput)-.5

        self.target = []
        self.targetSetList = []
        # Used for backpropagation of error
        self.inputOfOutput = np.empty(sizeOutput)
        self.hiddenToOutput = np.empty(sizeHidden)
        self.outputErrInfo = []

        self.errorLog = []
        self.errorLogList = []
        self.totalErrorLog = []

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
        self.hiddenErrCorrSums = np.inner(self.outputErrInfo, self.hiddenOutput) # Changed from dot to inner
        self.hiddenErrInfo = self.hiddenErrCorrSums*aFD(self.inputToHidden)
        self.inputHiddenWeightCorrection = self.learningRate*np.outer(self.input, self.hiddenErrInfo)
        self.hiddenBiasCorrection = self.learningRate*self.hiddenErrInfo

    def update(self):
        self.hiddenOutput += self.hiddenOutputWeightCorrection
        self.outputBias += self.outputBiasCorrection
        self.inputHidden += self.inputHiddenWeightCorrection
        self.hiddenBias += self.hiddenBiasCorrection

    def errorCalc(self):
        error = np.sqrt(sum(np.square(self.target-self.output))/len(self.target))
        return error

    def totalError(self):
        sumOfSquaredErrors = 0
        for error in self.totalErrorLog:
            sumOfSquaredErrors +=sum(np.square(error[0]-error[1]))
        self.totalErrorVal = np.sqrt(sumOfSquaredErrors/len(self.totalErrorLog))



    def fire(self,cycles):
        for x in range(cycles):
            self.feedForward()
            self.feedBack()
            self.update()
            #if (x % 1000 == 0):
              #  print(self.errorCalc())
            self.errorLog.append(self.errorCalc())
        self.feedForward()
        return self.output

    def trainSets(self, listOfSets, cycles):
        # Every set will be composed of a tuple, with the first value being the input and the seoond, the target.
        for iter in range(cycles):
            for Set in listOfSets:
                self.assignInput(Set[0])
                self.assignTarget(Set[1])
                # Resets the error log, so you can reuse the variable
                #self.errorLog = []
                self.fire(1)
                #self.totalErrorLog.append((n.target,n.output))
               # self.errorLogList.append(self.errorLog)
            #self.totalError()
        #return self.totalErrorVal


if __name__ == '__main__':
    n = Network(2,1,4,.8)
    n.trainSets([([0,0],[0]),([0,1],[1]),([1,0],[1]),([1,1],[0])],2000)
    # Prints the errors of the sets during training
    # for set,x in zip(n.errorLogList,range(4)):
    #     print('Set {0} Error List:{1}'.format(x+1,set))

    n.assignInput([0,0])
    n.feedForward()
    print(n.input,'-->',n.output)
    print(n.errorCalc())
    n.assignInput([0,1])
    n.feedForward()
    print(n.input,'-->',n.output)
    print(n.errorCalc())
    n.assignInput([1,0])
    n.feedForward()
    print(n.input,'-->',n.output)
    print(n.errorCalc())
    n.assignInput([1,1])
    n.feedForward()
    print(n.input,'-->',n.output)
    # print(n.errorCalc())
    # print('Total Error Value =',n.totalErrorVal)

    # Plots the error(from the training) logs of the sets
    # plt.subplot(221)
    # plt.scatter(list(range(len(n.errorLogList[0]))),n.errorLogList[0])
    # plt.subplot(222)
    # plt.scatter(list(range(len(n.errorLogList[0]))),n.errorLogList[1])
    # plt.subplot(223)
    # plt.scatter(list(range(len(n.errorLogList[0]))),n.errorLogList[2])
    # plt.subplot(224)
    # plt.scatter(list(range(len(n.errorLogList[0]))),n.errorLogList[3])
    # plt.show()

    n.assignInput([1,1])
    n.feedForward()
    print(n.output)
    n.assignInput([1,0])
    n.feedForward()
    print(n.output)
    n.assignInput([0,1])
    n.feedForward()
    print(n.output)
    n.assignInput([0,0])
    n.feedForward()
    print(n.output)
    
    # n.assignTarget([0])
    # n.assignInput([1,0,1,1,0])
    # n.assignTarget([1,0,1,0,0])
    # print(n.fire(20))
    # print(n.errorCalc())