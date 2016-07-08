import numpy as np


##################################################
#
# Gradient Descent for Multiple Variables
#
#################################################

# Functions required for gradient descent

# Feature Normalization
def featureNormalization(data, m, n):
    cnt = 0
    mu = np.mean(data, axis=0)
    sigma = np.std(data, axis=0, ddof=1)
    data = np.divide(np.subtract(data, mu), sigma)
    return (data)


# Cost function
def computeCost(setX, setY, setTheta, sampleSize):
    loss = np.sum(np.square(np.subtract(np.dot(setX, setTheta), setY))) / (2 * sampleSize)
    # loss = np.dot(setX, setTheta)
    return (loss)


# Gradient descent algorithm
def gradientDescent(setX, setY, setTheta, sampleSize):
    alpha = 0.001
    cnt = 0
    jHist = []
    jAlpha = []
    setTAlpha = setTheta
    # determine max alpha
    while (True):
        for i in setTAlpha:
            t0 = setTAlpha[0] - (alpha * (1 / sampleSize) * np.sum(np.multiply(np.subtract(np.dot(setX, setTAlpha), setY), np.array(setX[:, 0]).reshape(97, 1))))
            t1 = setTAlpha[1] - (alpha * (1 / sampleSize) * np.sum(np.multiply(np.subtract(np.dot(setX, setTAlpha), setY), np.array(setX[:, 1]).reshape(97, 1))))
            tx = [t0, t1]
            setTAlpha = np.array(tx).reshape(2, 1)
            jAlpha.append(computeCost(setX, setY, setTAlpha, sampleSize))
        alpha *= 3.33
        if (cnt >= 1 and jAlpha[cnt - 1] >= jAlpha[cnt]):
            print("Alpha Calculated as: ", alpha)
            break
        cnt += 1
    # reset counter variable
    cnt = 0
    #
    while (True):
        t0 = setTheta[0] - (alpha * (1 / sampleSize) * np.sum(np.multiply(np.subtract(np.dot(setX, setTheta), setY), np.array(setX[:, 0]).reshape(97, 1))))
        t1 = setTheta[1] - (alpha * (1 / sampleSize) * np.sum(np.multiply(np.subtract(np.dot(setX, setTheta), setY), np.array(setX[:, 1]).reshape(97, 1))))
        tx = [t0, t1]
        setTheta = np.array(tx).reshape(2, 1)
        jHist.append(computeCost(setX, setY, setTheta, sampleSize))
        if (cnt > 2 and jHist[cnt - 1] - jHist[cnt] < pow(10, -8)):
            print("Number of Iterations: ", cnt)
            break
        cnt += 1
    return (setTheta, jHist)


# import data
data = np.genfromtxt("data//ex1data2.txt", delimiter=",")
# Stores the shape of matrix in list s,where s[0] is the number of rows or the sample size m,
s = data.shape
# sampleSize
m = s[0]
# number of features 0 index
n = s[1] - 1
# Extract the training result set
metricSet = np.array(data[:, n]).reshape(m, 1)
# featureSet = np.array(data[:,0:n]).reshape(m,n)

featureSet = featureNormalization(np.array(data[:, 0:n]).reshape(m, n), m, n)
# Add Ones to the data set (X)
# featureSet = np.concatenate((np.ones((m, 1), dtype=int), np.array(data[:, 0: n]).reshape((m, n))), axis=1)
# Theta Starting from 0
theta = np.zeros((n + 1, 1), dtype=int)
# loss = computeCost(featureSet, metricSet, theta, m)
# theta, jHist = gradientDescent(featureSet, metricSet, theta, s[0])
# print("Theta: ", theta.reshape(1, 2))
