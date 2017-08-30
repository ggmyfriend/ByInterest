import numpy as np
import math

#获得特征的序号
def GetNeedIndex():
    FeatureIndex = ['6','7','8','10','11','13','15','16','17','19','20','21']
    return FeatureIndex
'''
#价格以及数据集
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

#读取参数
def ReadParem():
    f = open(r"E:\pythonFile\畅易阁抓取\Param.txt", encoding="utf-8")
    word = f.readline().split(" ")
    Param = []
    for i in word:
        try:
            Param.append(float(i))
        except ValueError as e:
            pass
    return Param

#猜想的函数关系
def ProFun(x,Param):
    sum = 0.0
    for i,j in zip(x,Param):
        sum = sum + i*j
    return sum
#测试数据的误差(回归)  ||bi
def ErrorPro():
    dataSet,Price = ReadFile()
    Param = ReadParem()
    HNumber = 0
    for i,j in zip(dataSet,Price):
        if ProFun(i,Param) > int(j):
            HNumber += 1
    Prob = HNumber/dataSet.__len__()
    return Prob
'''

#以下kmeans测试使用
#读取数据
def ReadKMeans():
    f = open(r"E:\pythonFile\畅易阁抓取\TLBB.txt", encoding="utf-8")
    RoleLine = f.readline()
    RoleWeb = []
    while RoleLine != "":
        RoleInfo = RoleLine.split(" ")
        RoleWeb.append(RoleInfo[0])
        RoleLine = f.readline()
    f.close()
    f = open(r"E:\pythonFile\畅易阁抓取\dataSet.txt", encoding="utf-8")
    RoleLine = f.readline()
    Roleinfo = []
    NeedIndex = GetNeedIndex()
    while RoleLine != "":
        RoleInfo = RoleLine.split(" ")
        TempInfo = []
        for i in NeedIndex:
            TempInfo.append(RoleInfo[int(i)])
        RoleInfo = TempInfo
        RoleInfo = map(float,RoleInfo)
        RoleInfo = list(RoleInfo)
        Roleinfo.append(RoleInfo)
        RoleLine = f.readline()
    f.close()
    return RoleWeb,Roleinfo
#读取质心
def ReadCent():
    f = open(r"E:\pythonFile\畅易阁抓取\centroids.txt", encoding="utf-8")
    cent = []
    Line = f.readline()
    while Line != "":
        CentInfo = Line.split()
        floatCent = []
        for i in CentInfo:
            try:
                floatCent.append(float(i))
            except ValueError as e:
                pass
        cent.append(floatCent)
        Line = f.readline()
    f.close()
    return cent
#定义欧式距离
def disEclud(vecA,vecB):
    vecA = np.array(vecA)
    vecB = np.array(vecB)
    len = math.sqrt(math.fsum(pow(vecA-vecB,2)))
    return len
#计算数据集
def kMeanEvalu():
    RoleWeb,dataSet = ReadKMeans()
    cent = ReadCent()
    m = dataSet.__len__()
    labels = np.zeros((m,3))
    for i in range(dataSet.__len__()):
        label = -1
        dist = np.inf
        for j in range(cent.__len__()):
            Tempdist = disEclud(dataSet[i],cent[j])
            if Tempdist < dist:
                label = j
                dist = Tempdist
        labels[i][0] = label
        labels[i][1] = dist
        labels[i][2] = dataSet[i][-1]
    return RoleWeb,labels

Web,label= kMeanEvalu()
f = open(r"E:\pythonFile\畅易阁抓取\可选.txt","w", encoding="utf-8")
Templabel = []
for i,j in zip(Web,label):
    if int(j[0]) == 2:
        Templabel.append([i,j[1],j[2]])
label = np.array(Templabel)
Index = np.array(label[:,1])
Index = np.argsort(Index)
for i in Index:
    if label[i][2][0] == '1':
        f.write(str(label[i][0])+"\n")
f.close()
