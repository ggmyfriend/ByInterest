from urllib import parse as parse
from urllib import request as request
import re
#查找该urlstr的text中需要的信息
def FindInfo(urlstr):
    regex = r'''<li class="role-item.*?">.*?<a target="_blank" href="(.*?)"''' \
            '''.*?\[(.*?)\]</span>(.*?)</a>.*?<span class="di">(.*?)<b>(.*?)</b></span>.*?<span class="di">'''\
            '''(.*?)<b>(.*?)</b></span>.*?<span class="di">(.*?)<b>(.*?)</b></span>.*?<p class="time">(.*?：)(.*?)[</span>]*</p>.*?'''\
            '''<p class="price">(.*?)</p>.*?</li>'''
    HerosInfo = []
    for i in re.findall(regex,urlstr,re.DOTALL):
        HeroInfo = []
        for j in i:
            if j[0] == '<':
                HeroInfo.append(j.split('>')[1])
            else:
                HeroInfo.append(j)
        HerosInfo.append(HeroInfo)
    for i in HerosInfo:
        print(i)
    return HerosInfo
#取得每个人的信息一个数组
def getRoleInfoList():
    RoleInfo = []
    area_name = "电信全国一区"
    world_id = "3016"
    world_name = "仙侣情缘"
    pageNum = '1'
    urlstr = GetUrlText(area_name=area_name,world_name=world_name,world_id=world_id,pageNum=pageNum)
    MaxPage = get_max_page(urlstr)
    RoleInfo.extend(FindInfo(urlstr))
    for i in range(2,MaxPage):
        urlstr = GetUrlText(area_name=area_name,world_name=world_name,world_id=world_id,pageNum=str(i))
        RoleInfo.extend(FindInfo(urlstr=urlstr))
    return RoleInfo
#获取url的html文本
def GetUrlText(area_name,world_name,world_id,pageNum):
    urlWoldId = "http://tl.cyg.changyou.com/goods/public?world_id="
    urlWorldName = "&world_name="
    urlAreaName = "&area_name="
    urlPage = "&have_chosen=&page_num="
    urlEnd = "#goodsTag"

    QuoteAName = parse.quote(parse.quote(area_name))
    QuoteWName = parse.quote(parse.quote(world_name))

    comUrl = urlWoldId + world_id + urlWorldName + QuoteWName + urlAreaName + QuoteAName + urlPage + pageNum + urlEnd
    urlrequest = request.Request(comUrl)
    urlrequest.add_header('User-Agent',"Mozilla/5.0 (Windows NT 6.1; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    urlOpen = request.urlopen(urlrequest)
    webtext = urlOpen.read().decode("utf-8")
    return webtext
#获取页面的最大值
def get_max_page(urlstr):
    regex = r'''<a href=.*? class="num"><span class="span">(.*?)</span></a>'''
    numberPage = []
    for i in re.findall(regex, urlstr, re.DOTALL):
        try:
            numberPage.append(int(i))
        except ValueError as e:
            print("ValueError",e)
    numberPage.sort()
    return numberPage[-1]
#主函数
f = open(r"E:\pythonFile\畅易阁抓取\TLBB.txt","w",encoding="utf-8")
RoleInfo = getRoleInfoList()
for i in RoleInfo:
    for j in i:
        f.writelines(j+" ")
    f.writelines("\n")
f.close()

