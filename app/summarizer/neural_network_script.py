"""
Neural_Network implementation

inputLayerSize 	8 	for 8 features of each sentence
hiddenLayerSize 16	
outputLayerSize	1

Equations

Z2 = XW1		...(1)
a2 = f(Z2)		...(2)
Z3 = a2W2		...(3)
yHat = f(Z3)	...(4)

sigmoid function	= 1/(1+e^(-z))

sigmoidPrime 		= derivative of sigmoid function
                    = e^(-z) / (1 + e^(-z))^2

cost function		= J
                    = (1/2) * sum((y-yHat)^2)
                    = error in observed and expected results


TO-DO
Find a solution for dealing with nan values
"""

import numpy as np
from scipy import optimize
import operator
import math
from numpy import array

count = 0

weights_base_path = "/Users/ameyakulkarni/Varta_backend/x_backend_flask/app/summarizer/weights.txt"

def getNNWeights():
    path_to_file = weights_base_path
    fp = open(path_to_file, 'r')
    text = fp.read()
    w1text, w2text = text.split('W2')
    # w1
    w1rows = w1text.split('\n')
    w1 = list()
    for row in w1rows[:-1]:
        r = row.split()
        r = map(lambda x : float(x), r)
        w1.append(r)
    # w2
    w2 = list()
    w2temp = w2text.split('\n')
    w3 = w2temp[1:-1]
    for item in w3:
        itemlist = list()
        itemlist.append(item)
        itemlist = map(lambda x : float(x), itemlist)
        w2.append(itemlist)
    # w2 = w2temp[1:-1]
    # print w2temp[1:-1]
    # print len(w3)
    np_w1 = array(w1)
    np_w2 = array(w2)
    # np_w1 = map(lambda x : float(x), np_w1)
    # np_w2 = map(lambda x: float(x), np_w2)
    fp.close()
    # print np_w2
    # for (x,y), value in np.ndenumerate(np_w2):
    #     print np_w2[x][y]
    """
    for (x, y), value in np.ndenumerate(np_w1):
        print type(np_w1[x][y])
    """
    """
    for (x, y), value in np.ndenumerate(np_w2):
        print type(np_w2[x][y])
    """
    return np_w1, np_w2

class Neural_Network(object):
    def __init__(self):
        #Define Hyperparameters
        self.inputLayerSize = 8
        self.hiddenLayerSize = 16
        self.outputLayerSize = 1

        #Initializing Weight matrices
        #self.W1 = np.random.rand(self.inputLayerSize,self.hiddenLayerSize)
        #self.W2 = np.random.rand(self.hiddenLayerSize,self.outputLayerSize)
        #self.W1 = 0.5*np.random.random_sample((self.inputLayerSize,self.hiddenLayerSize)) + 0.5
        #self.W2 = 0.5*np.random.random_sample((self.hiddenLayerSize, self.outputLayerSize)) +0.5
        self.W1, self.W2 = getNNWeights()
        #self.W1 = np.random.random_sample((self.inputLayerSize, self.hiddenLayerSize)) + 1.0
        #self.W2 = np.random.random_sample((self.hiddenLayerSize, self.outputLayerSize)) + 1.0

    def forward(self,X):
        #Propogate input through the Neural_Network
        self.Z2 = np.dot(X,self.W1)
        self.Z2 = self.Z2-np.median(self.Z2)
        self.a2 = self.sigmoid(self.Z2)
        self.Z3 = np.dot(self.a2,self.W2)
        self.Z3 = self.Z3 - np.median(self.Z3)
        yHat	= self.sigmoid(self.Z3)
        return yHat


    def sigmoid(self,z):
        #Apply the sigmoid function to the input z
        return 1/(1+np.exp(-z))

    def sigmoidPrime(self,z):
        #Gradient of sigmoid
        return np.exp(-z)/((1+np.exp(-z))**2)

    def costFunction(self,X,y):
        #Find cost for given X and y
        self.yHat = self.forward(X)
        J = (0.5)*sum((y-self.yHat)**2)
        return J

    def costFunctionPrime(self,X,y):
        #Compute derivative of cost function with respect to W1 and W2
        self.yHat = self.forward(X)

        delta3 = np.multiply(-(y-self.yHat), self.sigmoidPrime(self.Z3))
        dJdW2 = np.dot(self.a2.T, delta3)

        delta2 = np.dot(delta3, self.W2.T)*self.sigmoidPrime(self.Z2)
        dJdW1 = np.dot(X.T, delta2)
        return dJdW1, dJdW2

    def computeGradients(self, X, y):
        dJdW1, dJdW2 = self.costFunctionPrime(X, y)
        return np.concatenate((dJdW1.ravel(), dJdW2.ravel()))

    def getParams(self):
        #Get W1 and W2 unrolled into vector:
        params = np.concatenate((self.W1.ravel(), self.W2.ravel()))
        return params

    def setParams(self, params):
        W1_start = 0
        W1_end = self.hiddenLayerSize * self.inputLayerSize
        self.W1 = np.reshape(params[W1_start:W1_end], (self.inputLayerSize ,self.hiddenLayerSize))
        W2_end = W1_end + self.hiddenLayerSize*self.outputLayerSize
        self.W2 = np.reshape(params[W1_end:W2_end], (self.hiddenLayerSize, self.outputLayerSize))


    def get_summary(self, X):
        yHat = self.forward(X)
        # print yHat
        count = len(yHat)
        print "yHat len ",count
        #compressed_count = (count*3)/10
        compressed_count = (count*4)/10
        print "compressed yHat len", compressed_count
        print yHat
        final_summary = dict()
        for i in range(0, len(yHat)):
            final_summary[i]=yHat[i][0]
        print "Final array", final_summary, len(final_summary)
        summary = sorted(final_summary.items(), key=operator.itemgetter(1), reverse=True)
        unsorted_summary_indices = [s[0] for s in summary]
        print unsorted_summary_indices
        summary_indices = []
        sorted_summary_indices = []
        print summary[0], len(summary)
        cc = int(1)
        if compressed_count>1.0:
            cc = int(math.ceil(compressed_count))
        for i in range(0, cc):
            #if yHat[summary[i]] > 0.00005:        # applying threshold of 0.7
            summary_indices.append(summary[i])
            sorted_summary_indices.append(unsorted_summary_indices[i])
        #for i in range(0, compressed_count):
        #    summary_indices.append(summary[i])
        #    sorted_summary_indices.append(unsorted_summary_indices[i])
        print "Final Summary unsorted", summary_indices
        print "Final Summary indices unsorted", sorted_summary_indices
        sorted_summary = sorted(summary_indices, key=operator.itemgetter(0))
        sorted_summary_indices = sorted(sorted_summary_indices)
        print "Final Summary sorted", sorted_summary
        print "Final summary indices sorted", sorted_summary_indices
        return sorted_summary_indices


class trainer(object):
    def __init__(self, N):
        #Make Local reference to network:
        self.N = N

    def callbackF(self, params):
        self.N.setParams(params)
        self.J.append(self.N.costFunction(self.X, self.y))

    def costFunctionWrapper(self, params, X, y):
        self.N.setParams(params)
        cost = self.N.costFunction(X, y)
        grad = self.N.computeGradients(X,y)

        return cost, grad

    def train(self, X, y):
        #Make an internal variable for the callback function:
        self.X = X
        self.y = y

        #Make empty list to store costs:
        self.J = []

        params0 = self.N.getParams()

        options = {'maxiter': 200, 'disp' : True}
        _res = optimize.minimize(self.costFunctionWrapper, params0, jac=True, method='BFGS',args=(X, y), options=options, callback=self.callbackF)

        self.N.setParams(_res.x)
        self.optimizationResults = _res


def computeNumericalGradient(N, X, y):
        paramsInitial = N.getParams()
        numgrad = np.zeros(paramsInitial.shape)
        perturb = np.zeros(paramsInitial.shape)
        e = 1e-4

        for p in range(len(paramsInitial)):
            #Set perturbation vector
            perturb[p] = e
            N.setParams(paramsInitial + perturb)
            loss2 = N.costFunction(X, y)

            N.setParams(paramsInitial - perturb)
            loss1 = N.costFunction(X, y)

            #Compute Numerical Gradient
            numgrad[p] = (loss2 - loss1) / (2*e)

            #Return the value we changed to zero:
            perturb[p] = 0

        #Return Params to original value:
        N.setParams(paramsInitial)

        return numgrad
"""
NN = Neural_Network()

yHat = NN.forward(X)
print "yHat -->",yHat

cost1 = NN.costFunction(X,y)
print "initial cost -->",cost1

dJdW1,dJdW2 = NN.costFunctionPrime(X,y)

scalar = 3
NN.W1 = NN.W1 - scalar*dJdW1
NN.W2 = NN.W2 - scalar*dJdW2

cost2 = NN.costFunction(X,y)

print "yHat after one interation -->",NN.forward(X)
print "cost after one iteration -->",cost2

T = trainer(NN)
T.train(X,y)


print NN.costFunctionPrime(X,y)

print NN.forward(X)

print y
"""

if __name__ == '__main__':
    NN = Neural_Network()
    print type(NN.W1),NN.W1.shape
    print type(NN.W2),NN.W2.shape
    """print "yHat initial -->", NN.forward(X)
    print "initial cost", NN.costFunction(X, y)
    T = trainer(NN)
    T.train(X, y)
    print "yHat after training -->", NN.forward(X)
    print "cost after training -->", NN.costFunction(X,y)
    print "-----------Calling feature extractor--------"
"""






