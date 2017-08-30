#读取traingSet的标签
import numpy as np
import math
import logging
def readSet():
    f = open(r"E:\pythonFile\畅易阁抓取\TrainingSet.txt",encoding="utf-8")
    dataSet = []
    word = f.readline()
    while word != "":
        WList = word.split(" ")

        Nlist = []
        for i in WList:
            try:
                Nlist.append(float(i))
            except ValueError as e:
                pass
        dataSet.append(Nlist)
        word = f.readline()
    f.close()
    return dataSet
#以下k均值的具体算法
#使用一般的欧式距离
def disEclud(vecA,vecB):
    vecA = np.array(vecA)
    vecB = np.array(vecB)
    len = math.sqrt(math.fsum(pow(vecA[0]-vecB[0],2)))
    return len

#初始化质心
def randCent(dataSet,k):
    n = np.shape(dataSet)[1]
    centroids = np.mat(np.zeros((k,n)))
    for i in range(n):
        minJ = min(dataSet[:,i])
        rangJ = float(max(dataSet[:,i]) - minJ)
        centroids[:,i] = minJ + rangJ * np.random.rand(k,1)
    return centroids

# k-means算法计算分类
# dataSet是matrix类型
# k表示子集的个数
# disMeas表示距离函数
# createCent表示一开始生成的质心
def kMeans(dataSet , k , disMeas = disEclud , createCent = randCent):
    logging.basicConfig(filename=r"E:\pythonFile\畅易阁抓取\kMeansLog.txt", level=logging.DEBUG)
    m = np.shape(dataSet)[0]
    clusterAssment = np.mat(np.zeros((m,2)))
    #生成的初始点可能导致问题 如下是一组可以得到解的集合
    '''
    [[  7.16358650e+00  -7.17879141e-02   8.04814975e-01  -1.14809372e+01
   -7.46104599e+00   2.02619934e+00   3.22131906e+00   4.08042542e-01
    4.04850216e-01   3.29485747e-02   2.38665268e+00   4.50294890e-01]
 [  1.79279469e+01  -3.81379262e+00   6.42880796e-01  -6.28149550e+01
   -3.84507167e+00   1.61897403e-01   4.23706943e+00   2.50319147e+00
    5.56289558e+00  -2.74456611e+00   1.44908998e+00   4.17674541e-01]
 [  1.98653938e+00  -2.97488589e+00   3.57617346e-01  -3.43383044e+00
    8.90969242e+00   2.83772767e+00   3.96771922e+00   1.21936431e+00
    3.24297925e+00  -2.20402316e+00   2.41921908e+00   8.87963180e-01]
 [  1.19009319e+01   1.64543295e+00  -2.43145506e-01  -2.34564474e+01
    7.17051584e+00   7.79713368e-01   2.44108838e+00   8.44789123e-01
   -9.97840556e-01   2.80660842e+00  -1.42570240e+00   1.07885008e-01]]
    '''
    centroids = createCent(dataSet,k)
    print(centroids)
    clusterChanged = True
    TimesOfCentCal = 0
    while clusterChanged:
        logging.info("这是第"+str(TimesOfCentCal)+"次")
        clusterChanged = False
        for i in range(m):
            minDist = np.inf
            minIndex = -1
            for j in range(k):
                distJI = disMeas(centroids[j,:],dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI
                    minIndex = j
            if minIndex != clusterAssment[i,0]:
                clusterChanged = True
            clusterAssment[i,:] = minIndex , minDist ** 2
        for cent in range(k):
            ptsInClust = dataSet[np.nonzero(clusterAssment[:,0].A == cent)[0]]
            centroids[cent,:] = np.mean(ptsInClust,axis = 0)
        TimesOfCentCal += 1
    return centroids,clusterAssment

#使数据集变成matrix
#dataSet为内值为float的list
def ChangeDataSet(dataSet):
    dataSet = np.mat(dataSet)
    return dataSet

dataSet = readSet()
dataMat = ChangeDataSet(dataSet)
#centroids , clusterAssment = kMeans(dataMat,4)
