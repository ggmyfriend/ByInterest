#对数据进行处理，对低于预期值的数据进行处罚，反之则奖励
#读取两个训练数据样本
import math
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
    return RoleList
#参加机器学习的每个特征的位置
def MFeature():
    FeatureName = ['装备评分','修炼评分','进阶评分','价格','属性攻击','减抗','穿刺','减穿','血量','命中','闪避','是否具有三十附体']
    FeatureNum = ['6','7','8','10','11','13','15','16','17','19','20','21']
    PRFunction = ['1','0','-1','1','1','0','-1','-1','1','-1','-1']
    PRdoamin = [[80000,120000],[8000,10000],[2000,4000],[1000,3000],[5500,7000],[0,500],[1000,2000],[0,1000],[300000,400000],[40000,50000],[8000,12000]]
    OverPorR = [0,0,0,1,0,0,0,0,0,0,0]
    return FeatureName,FeatureNum,PRFunction,PRdoamin,OverPorR
#归一化处理阶段
#思路是取一个范围当做能够接受的数据范围，超过则按照函数进行奖励，低则进行处罚，
# （对不同的特征惩罚和奖励的概念可能不同）
#min 和 max为int类型 dataSet为list Feature为int
def PunAndRew(dataSet ,Feature,punishF , min , max , OverPOrR = 0):
    PorR = 1.0
    if OverPOrR == 1:
        PorR = -1.0
    number = 0
    for i in dataSet:
        try:
            TempFNum = int(i[Feature])
            if TempFNum < min:
                punish = - PorR * (punishFunction(min - TempFNum , max - min , punishChoose = punishF) + 1)
            elif TempFNum > max :
                punish = PorR * (punishFunction(TempFNum - max , max - min ,punishChoose = punishF) + 1)
            else:
                punish = (TempFNum - min)/(float)(max-min)
        except ValueError as e:
            pass
        else:
            dataSet[number][Feature] = punish
            number += 1
    return dataSet

#punishChoose用于选择惩罚或奖励函数
# number必须是非负数
def punishFunction(number, scale, punishChoose = 0):
    if number < 0:
        return
    if punishChoose == 0:
        Punishi = 0.0
        try:
            Punishi = number/float(scale)
        except ZeroDivisionError as e:
            print("ZeroDivisionError")
        return Punishi
    if punishChoose > 0:
        Punishi = 0.0
        try:
            Punishi = number/float(scale)
        except ZeroDivisionError as e:
            print("ZeroDivisionError")
        Punishi = Punishi * 2
        return Punishi
    else:
        Punishi = 0.0
        try:
            Punishi = number / float(scale)
        except ZeroDivisionError as e:
            print("ZeroDivisionError")
        Punishi = Punishi / 2
        return Punishi
#归一化
def Normaliztion():
    dataSet = ReadFile()
    FeatureName,FeatureNum,PRFunction,PRdomain,OverPorR = MFeature()
    for j,k,z,i in zip(FeatureNum,PRFunction,PRdomain,OverPorR):
        dataSet = PunAndRew(dataSet,int(j),int(k),z[0],z[1],OverPOrR = i)
    for i in dataSet:
        for j in FeatureNum:
            print(int(i[int(j)]), end=" ")
        print("")
    #写入文件
    f = open(r"E:\pythonFile\畅易阁抓取\dataSet.txt", "w", encoding="utf-8")
    for i in dataSet:
        for j in i:
            f.write(str(j) + " ")
        f.writelines("\n")
    f.close()
    return dataSet

Normaliztion()
'''
data = ReadFile()
dataSet = []
dataSet.append(data[4])
dataSet.append(data[6])
FeatureName, FeatureNum, PRFunction, PRdomain, OverPorR = MFeature()
for j, k, z, i in zip(FeatureNum, PRFunction, PRdomain, OverPorR):
    data = PunAndRew(dataSet, int(j), int(k), z[0], z[1], OverPOrR=i)
for i in dataSet:
    for j in FeatureNum:
        print(int(i[int(j)]), end=" ")
    print()'''
