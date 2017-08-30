import numpy as np
import math
import logging

'''失败而告终几乎走不通误差太高'''
#获取信息
def ReadFile():
    f = open(r"E:\pythonFile\畅易阁抓取\TLBB.txt", encoding="utf-8")
    RoleLine = f.readline()
    RoleList = []
    while RoleLine != '':
        RoleInfo = RoleLine.split(" ")
        try:
            RoleInfo.remove("装备评分：")
            RoleInfo.remove("修炼评分：")
            RoleInfo.remove("进阶评分：")
            RoleInfo.remove("剩余时间：")
            RoleInfo.remove("\n")
        except ValueError as e:
            print("ValueError:", e)
        else:
            RoleInfo[-1] = RoleInfo[-1][1:]
            RoleList.append(RoleInfo)
            RoleLine = f.readline()
    f = open(r"E:\pythonFile\畅易阁抓取\Roletxt.txt", encoding="utf-8")
    RoleLine = f.readline()
    LineNum = 0
    while RoleLine != '':
        RoleInfo = RoleLine.split(" ")
        RoleList[LineNum].extend(RoleInfo[:-1])
        LineNum += 1
        RoleLine = f.readline()
    FeatureIndex,LabelIndex = GetNeedIndex()
    Index = 0
    Labels = []
    for i in RoleList:
        RoleInfo = []
        Labels.append(i[int(LabelIndex)])
        for j in FeatureIndex:
            RoleInfo.append(int(i[int(j)]))
        RoleInfo.append(1)
        RoleList[Index] = RoleInfo
        Index += 1
    return RoleList,Labels
#获得特征的序号
def GetNeedIndex():
    FeatureIndex = ['6','7','8','11','13','15','16','17','19','20','21']
    LabelsIndex = '10'
    return FeatureIndex,LabelsIndex
#梯度下降的函数
def function(x,Param):
    sum = 0.0
    for i,j in zip(x,Param):
        sum = sum + i*j
    return sum
#使用比较矩阵计算不使用梯度下降
def LinearRegression():
    logging.basicConfig(filename=r"E:\pythonFile\畅易阁抓取\角色信息抓取log.txt", level=logging.DEBUG)
    Step = 0.000000000000001
    dataSet,Price= ReadFile()
    #使用下面这种方法会导致数据跳变从float64 - ufloat32所以存疑
    '''dataMat = np.mat(dataSet)
    PriceMat = np.mat(Price)
    ParaMat = (dataMat.T * dataMat).I * dataMat.T
    ParaMat = ParaMat * PriceMat.T
    print(PriceMat.T)'''
    #所以试试使用梯度下降
    Param = []
    sum_Para = []
    for i in range(dataSet[0].__len__()):
        Param.append(1)
    for i in range(dataSet[0].__len__()):
        sum_Para.append(0)
    ParamPrice = function(dataSet[0], Param)
    print(ParamPrice - int(Price[0]))
    Times = 0
    ErrorP = 1
    while ErrorP > 0.1:
        if Times % 500 == 0:
            logging.info(u"已经运算了"+str(Times)+u"次"+u" 误差为"+str(ErrorP))
        for i in range(dataSet[0].__len__()):
            sum_Para[i] = 0
        for i,j in zip(dataSet,Price):
            for z in range(dataSet[0].__len__()):
                sum_Para[z] = sum_Para[z] + Step * (int(j) - function(i,Param)) * i[z]
        for i in range(dataSet[0].__len__()):
            Param[i] = Param[i] + sum_Para[i]
        Times += 1
        ErrorP = ErrorProb(dataSet, Price, Param)
    print(function(dataSet[0],Param),Price[0])
    return Param

def ErrorProb(dataSet,Price,Param):
    ErrorNumber = 0
    for i, j in zip(dataSet, Price):
        if abs(function(i, Param) - int(j)) > 100:
            ErrorNumber += 1
    Prob = ErrorNumber / dataSet.__len__()
    return Prob

Param = LinearRegression()
f = open(r"E:\pythonFile\畅易阁抓取\Param.txt", "w",encoding="utf-8")
for i in Param:
    f.write(str(i) + " ")
f.close()
