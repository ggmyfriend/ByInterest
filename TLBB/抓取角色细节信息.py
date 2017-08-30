from urllib import request as request
import re
import time
import logging
from urllib import parse as parse
#读取文档抓取信息
def read_the_dataset():
    f = open(r"E:\pythonFile\畅易阁抓取\TLBB.txt",encoding="utf-8")
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
            print("ValueError:",e)
        else:
            RoleInfo[-1]=RoleInfo[-1][1:]
            RoleList.append(RoleInfo)
            RoleLine = f.readline()
    return RoleList
#抓取角色细节信息
def GetRoleDetail(RoleList):
    RList = []
    f = open(r"E:\pythonFile\畅易阁抓取\Roletxt.txt", "w", encoding="utf-8")
    for i in range(RoleList.__len__()):
        if i % 20 == 0:
            f.flush()
        time.sleep(1)        #因为网上的免费代理会有广告所以决定还是使用睡眠的机制避免过快访问被干掉
        url = RoleList[i][0]
        urltext = GetUrlStr(url)
        List = GetRoleInfo(urltext)
        print(List,"开始输入")
        for j in List:
            f.write(j + " ")
        f.writelines("\n")
    f.close()
        #RList.append(GetRoleInfo(urltext))
    return RList
#取得url的html文本
def GetUrlStr(url):
    req = request.Request(url)
    req.add_header('User-Agent',"Mozilla/5.0 (Windows NT 6.1; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    urlOpen = request.urlopen(req)
    urltext = urlOpen.read().decode("utf-8")
    return urltext
#获取url的需要信息
def GetRoleInfo(urltext):
    #获取属性攻击的最大值以及该值下的减抗，并且获取穿刺和穿免
    #用正则表达式获取属性和穿刺等特征
    regex = r'''<div id=".*?" class="good-tip small fn-hide">.*?<div class="model-top-line"></div>.*?<div class="model">.*?<div class="c-o-l">.*?<p>(.*?)</p>.*?<p>(.*?)</p>.*?<p>(.*?)</p>.*?<p>(.*?)</p>.*?</div>'''
    reList = re.findall(regex,urltext,re.DOTALL)     #返回值的标签
    for i in range(5):
        for j in range(reList[i].__len__()):
            reList[i] = list(reList[i])
            try:
                reList[i][j] = re.search("[0-9]+",reList[i][j]).group()
            except AttributeError as e:
                pass
    #获取最大值
    reList = reList[:5]
    MaxIndex = 0
    MaxAttribute = 0
    for i in range(4):
        if int(reList[i][0]) >= MaxAttribute:
            MaxAttribute = int(reList[i][0])
            MaxIndex = i
    midList = reList
    reList = midList[MaxIndex]
    reList.append(midList[-1][0])
    reList.append(midList[-1][1])
    #获取血上限气上限闪避命中
    regex = r'''<div class="row2">血上限：<span class="span"><i class=".*?">(.*?)</i></span></div>.*?''' \
            '''<div class="row2">气上限：<span class="span"><i class=".*?">(.*?)</i></span></div>.*?''' \
            '''<div class="row2">命中：<span class="span">(.*?)</span></div>.*?''' \
            '''<div class="row2">闪避：<span class="span">(.*?)</span></div>'''
    RoleAtt = re.findall(regex, urltext, re.DOTALL)[0]
    RoleAtt = list(RoleAtt)
    try:
        RoleAtt[-1] = re.search(r"[0-9]*",RoleAtt[-1]).group()
    except AttributeError as e:
        pass
    try:
        RoleAtt[-2] = re.search(r"[0-9]*", RoleAtt[-2]).group()
    except AttributeError as e:
        pass
    reList.extend(RoleAtt)
    #获取宠物信息
    regex = r'''<p class="row2">融合度：<span class="span">(.*?)</span></p>.*?'''\
            '''<span class="prop">悟性：<i>(.*?)</i></span>.*?'''\
            '''<span class="prop">灵性：<i>(.*?)</i></span>'''
    RolePet = re.findall(regex,urltext,re.DOTALL)
    IsTFT = 0           #是否有三十附体
    for i in RolePet:
        if i[0] == '10' and i[1]=='10' and i[2] == '10':
            IsTFT = 1
            break
    reList.extend(str(IsTFT))
    return reList
'''f = open(r"E:\pythonFile\畅易阁抓取\Roletxt.txt",encoding="utf-8")
urltext = f.read()
print(GetRoleInfo(urltext))'''
dateSet = read_the_dataset()
RoleDetail = GetRoleDetail(RoleList=dateSet)
#logging.basicConfig(filename=r"E:\pythonFile\畅易阁抓取\角色信息抓取log.txt", level=logging.DEBUG)

#logging.info(u"开始写入文件")
