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
    return (data, mu, sigma)


# Cost function
def computeCost(setX, setY, setTheta, sampleSize):
    loss = np.sum(np.square(np.subtract(np.dot(setX, setTheta), setY))) / (2 * sampleSize)
    # loss = np.dot(setX, setTheta)
    return (loss)


# Gradient descent algorithm
def gradientDescent(setX, setY, setTheta, sampleSize):
    alpha = 0.01
    cnt, tn = 0, 0
    jHist = []
    jAlpha = []
    setTAlpha = setTheta.copy()
    setThetaN = setTheta.copy()
    # determine max alpha
    while (True):
        for i in setTheta:
            setTAlpha[tn] = setThetaN[tn] - (alpha * (1 / sampleSize) * np.sum(
                np.multiply(np.subtract(np.dot(setX, setThetaN), setY), np.array(setX[:, tn]).reshape(sampleSize, 1))))
            tn += 1
        tn = 0
        setThetaN = setTAlpha.copy()
        jAlpha.append(computeCost(setX, setY, setTAlpha, sampleSize))
        if (cnt >= 1 and jAlpha[cnt - 1] <= jAlpha[cnt]):
            alpha /= 3
            print("Alpha Calculated as: ", alpha)
            break
        alpha *= 3
        cnt += 1
    # reset counter variable
    cnt, tn = 0, 0
    while (True):
        for i in setTheta:
            setThetaN[tn] = setTheta[tn] - (alpha * (1 / sampleSize) * np.sum(
                np.multiply(np.subtract(np.dot(setX, setTheta), setY), np.array(setX[:, tn]).reshape(sampleSize, 1))))
            tn += 1
        tn = 0
        setTheta = setThetaN.copy()
        jHist.append(computeCost(setX, setY, setTheta, sampleSize))
        if (cnt > 2 and jHist[cnt - 1] - jHist[cnt] < pow(10, -9)):
            print("Number of Iterations: ", cnt)
            break
        cnt += 1
    return (setTheta, jHist)


# import data
data = np.genfromtxt("data//ex1data2.txt", delimiter=",")
# Stores the shape of matrix in list s,where s[0] is the number of rows or the sample size m,
s = data.shape
# sampleSize,number of features
m, n = s[0], s[1] - 1
# Extract the training result set
metricSet = np.array(data[:, n]).reshape(m, 1)
# Scale FeatureSet and Add Ones
dataSetX, mu, sigma = featureNormalization(np.array(data[:, 0:n]).reshape(m, n), m, n)
# Add Ones column
featureSet = np.concatenate((np.ones((m, 1), dtype=float), dataSetX), axis=1)
# Theta Starting from 0
theta = np.zeros((n + 1, 1), dtype=float)
loss = computeCost(featureSet, metricSet, theta, m)
theta, jHist = gradientDescent(featureSet, metricSet, theta, m)
print("Theta: ", theta)
# Predicting the Price of a house with area as 1650 sq.ft and 3 bedrooms
houseSet = np.concatenate((np.ones((1, 1), dtype=int), np.divide(np.subtract(np.array([1650, 3]), mu), sigma).reshape(1, 2)), axis=1)
print("Predicted Price for house with area 1650 sq.ft and 3 Bedrooms is ", np.dot(houseSet, theta))
