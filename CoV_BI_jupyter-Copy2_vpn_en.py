import time
import json
import requests
import pandas as pd
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType, ChartType
from bs4 import BeautifulSoup
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot
from retrying import retry
import random
from pyecharts.datasets.coordinates import get_coordinate, search_coordinates_by_keyword
from pyecharts.components import Image
from pyecharts.options import ComponentTitleOpts
from MyQR import myqr
import os
 
QR = myqr.run(
    words="https://geoseis.cn/CoV_en.html",          # 可以是字符串，也可以是网址(前面要加http(s)://)
    version=1,                              # 设置容错率为最高
    level='H',                              # 控制纠错水平，范围是L、M、Q、H，从左到右依次升高
    picture="C:/Users/xuzhen/Pictures/0.jpg",                           # 将二维码和图片合成
    colorized=True,                         # 彩色二维码
    contrast=1.0,                           #用以调节图片的对比度，1.0 表示原始图片，更小的值表示更低对比度，更大反之。默认为1.0
    brightness=1.0,                         #用来调节图片的亮度，其余用法和取值同上
    save_name="C:/Users/xuzhen/Pictures/python.gif",                     # 保存文件的名字，格式可以是jpg,png,bmp,gif
    save_dir=os.getcwd()                    #控制位置
)

def image_base() -> Image:
    image = Image()

    img_src = (
        "https://www.geoseis.cn/wp-content/gallery/pycharm/"
        "python.gif"
    )
    image.add(
        src=img_src,
        style_opts={"width": "200px", "height": "200px", "style": "margin-top: 10px"},
    ).set_global_opts(
        title_opts=ComponentTitleOpts(title="WeChat QR",title_style={"style": "font-size: 18px; font-weight:bold; color:red"},\
                                      subtitle="Scan to follow the realtime update!",subtitle_style={"style": "font-size: 12px; color:red"})
    )
    return image

#title_style = title_style or {"style": "font-size: 18px; font-weight:bold;"}
# 抓取数据(2020年2月24日更新：腾讯网页有变化，新增一个网页存放新增数据)
url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback='
URL = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other&callback='

user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
            (KHTML, like Gecko) Element Browser 5.0', \
            'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
            'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
            'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
            Version/6.0 Mobile/10A5355d Safari/8536.25', \
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/28.0.1468.0 Safari/537.36', \
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)'\
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36']
headers= {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": random.choice(user_agents)} 
try:
    response = requests.get(url, headers = headers , timeout = 30)
    response2 = requests.get(URL, headers = headers , timeout = 30)
    res = response.json()
    res2 = response2.json()
    response_test = requests.get('http://httpbin.org/get', headers=headers, timeout=30)
    print('ip test:',response_test.text)
    print(url)
    print(URL)
    response.raise_for_status()
    response2.raise_for_status()
    
    response.encoding = response.apparent_encoding
    response2.encoding = response2.apparent_encoding
    #print(response.text) 

except requests.exceptions.RequestException as e:
    print('*'*50,str(e))
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    time.sleep(random.random()*3)
    
soup = BeautifulSoup(response.text, "lxml")
soup2 = BeautifulSoup(response2.text, "lxml")
#soup.prettify()
#soup2.prettify()
# print(soup.prettify())
# print("pretty print done!!!!!!!!!!!!!!!!")
# print('\n')

# print(soup2.prettify())
# print("pretty2 print done!!!!!!!!!!!!!!!!")
# print('\n')

#response = requests.get('https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=').json()
data = json.loads(res['data'])
data2 = json.loads(res2['data'])
#print('data:#######################',data)
# print('\n')
# print('data2:#######################',data2)
# print('\n')

#'chinaTotal': {'confirm': 78959, 'heal': 36157, 'dead': 2791, 'nowConfirm': 40011, 'suspect': 2308, 'nowSevere': 7952}, 'chinaAdd': {'confirm': 329, 'heal': 3626, 'dead': 44, 'nowConfirm': -3341, 'suspect': -50, 'nowSevere': -394}, 'isShowAdd': True, 'showAddSwitch': {'all': True, 'confirm': True, 'suspect': True, 'dead': True, 'heal': True, 'nowConfirm': True, 'nowSevere': True}, 'areaTree': [{'name': '中国', 'today': {'confirm': 329, 'isUpdated': True}, 'total': {'confirm': 78959, 'suspect': 2308, 'dead': 2791, 'deadRate': '3.53', 'showRate': False, 'heal': 36157, 'healRate': '45.79', 'showHeal': True}, 'children': [{'name': '湖北', 'today': {'confirm': 318, 'confirmCuts': 0, 'isUpdated': True}, 'total': {'confirm': 65914, 'suspect': 0, 'dead': 2682, 'deadRate': '4.07', 'showRate': False, 'heal': 26403, 'healRate': '40.06', 'showHeal': True}, 'children': [{'name': '武汉', 'today': {'confirm': 313, 'confirmCuts': 0, 'isUpdated': True}, 'total': {'confirm': 48137, 'suspect': 0, 'dead': 2132, 'deadRate': '4.43', 'showRate': False, 'heal': 15826, 'healRate': '32.88', 'showHeal': True}},

# 国内
lastUpdateTime = data['lastUpdateTime']

chinaTotal = data['chinaTotal']

chinaTotal['totalConfirm'] = chinaTotal['confirm']
chinaTotal['totalDead'] = chinaTotal['dead']
chinaTotal['totalHeal'] = chinaTotal['heal']

chinaTotal['nowSuspect'] = chinaTotal['suspect']
chinaTotal['nowConfirm'] = chinaTotal['nowConfirm']
chinaTotal['nowSevere'] = chinaTotal['nowSevere']
del chinaTotal['confirm']
del chinaTotal['dead']
del chinaTotal['heal']

del chinaTotal['suspect']
# del chinaTotal['nowConfirm']
# del chinaTotal['nowSevere']

sum = chinaTotal['totalConfirm']  + chinaTotal['nowSuspect'] 
chinaAdd = data['chinaAdd']
chinaAdd['AddedtotalConfirm'] = chinaAdd['confirm']
chinaAdd['AddedtotalDead'] = chinaAdd['dead']
chinaAdd['AddedtotalHeal'] = chinaAdd['heal']

chinaAdd['AddednowSuspect'] = chinaAdd['suspect']
chinaAdd['AddednowConfirm'] = chinaAdd['nowConfirm']
chinaAdd['AddednowSevere'] = chinaAdd['nowSevere']
del chinaAdd['confirm']
del chinaAdd['dead']
del chinaAdd['heal']

del chinaAdd['suspect']
del chinaAdd['nowConfirm']
del chinaAdd['nowSevere']

areaTree = data['areaTree']

china_data = areaTree[0]['children']       #province block
china_list = []
for x in range(len(china_data)):
    province = china_data[x]['name']  #province name
    province_list = china_data[x]['children']  #city blocks under a province
    for y in range(len(province_list)):        #loop city lists under a province
        city = province_list[y]['name']        #city names     
        total = province_list[y]['total']      #累计数据 under 'total' block it's a list of statistics: confirm/suspect/dead/heal
        today = province_list[y]['today']      #新增数据 for a city: today's info (confirm under 'today' block means no. confirmed for that city)
        
        china_dict = {'province': province, 'city': city, 'total': total, 'today': today}  
        china_list.append(china_dict)
        
foreign_data = data2['foreignList']
country_List = []
for y in range(len(foreign_data)):
    country_List.append(foreign_data[y]['name'])
#     for z in country_list:
#         \"confirmAdd\":851,\"confirmAddCut\":0,\"confirm\":5186,\"suspect\":0,\"dead\":31,\"heal\":31,
print('country list:{}'.format(country_List))
        

# 定义数据处理函数
#累计确诊
def confirm(x):
    confirm = eval(str(x))['confirm']
    return confirm
#累计死亡
def dead(x):
    dead = eval(str(x))['dead']
    return dead
#累计治愈
def heal(x):
    heal = eval(str(x))['heal']
    return heal
# 现有疑似
def suspect(x):
    suspect = eval(str(x))['suspect']
    return suspect

# 现有确诊
def nowConfirm(x):
    nowConfirm = eval(str(x))['nowConfirm']
    return nowConfirm
# 现有重症
def nowSevere(x):
    nowSevere = eval(str(x))['nowSevere']
    return nowSevere

# 现有疑似
def deadRate(x):
    deadRate = eval(str(x))['deadRate']
    return deadRate
# 现有疑似
def healRate(x):
    healRate = eval(str(x))['healRate']
    return healRate

china_data = pd.DataFrame(china_list)
#print('china_data:##########')
#print(china_data.head())

# 函数映射
#累计确诊/死亡/治愈
china_data['confirm'] = china_data['total'].map(confirm)      
china_data['dead'] = china_data['total'].map(dead)
china_data['heal'] = china_data['total'].map(heal)
#现有疑似/确诊/重症/
china_data['suspect'] = china_data['total'].map(suspect)
# china_data['nowConfirm'] = china_data['total'].map(nowConfirm)
# china_data['nowSevere'] = china_data['total'].map(nowSevere)
#新增累计确诊/死亡/治愈
china_data['addconfirm'] = china_data['today'].map(confirm)
# china_data['adddead'] = china_data['today'].map(dead)
# china_data['addheal'] = china_data['today'].map(heal)
#新增现有疑似/确诊/重症
# china_data['addsuspect'] = china_data['today'].map(suspect)
# china_data['addnowConfirm'] = china_data['today'].map(addnowConfirm)
# china_data['addnowSevere'] = china_data['today'].map(addnowSevere)
china_data['deadRate'] = china_data['total'].map(deadRate)
china_data['healRate'] = china_data['total'].map(healRate)

china_data = china_data[
    ["province", "city", "confirm", "suspect", "dead", "heal", "addconfirm"]] #info N/A today: "addsuspect", "adddead", "addheal"
#china_data.head()


#Global数据处理
foreignList = pd.DataFrame(data2['foreignList'])
print('foreignList: {}'.format(foreignList))
foreign_data = list(zip(foreignList['name'], foreignList['confirm']))
print('foreign_data: {}'.format(foreign_data))

global_data = pd.DataFrame(data2['foreignList'])
# global_data['confirm'] = global_data['name'].map(confirm)
# global_data['suspect'] = global_data['name'].map(suspect)
# global_data['dead'] = global_data['name'].map(dead)
# global_data['heal'] = global_data['name'].map(heal)
# global_data['deadRate'] = global_data['total'].map(deadRate)
# global_data['healRate'] = global_data['total'].map(healRate)

# global_data['addconfirm'] = global_data['name'].map(confirmAdd)

#print(type(global_data))
#print("global data before merge:######################", global_data)
print('\n')
global_data = pd.DataFrame(foreign_data, columns=['name','confirm'])
#global_data.reindex(global_data['name'])
#print(global_data)
tmp_jp = global_data.loc[4,'confirm'] + global_data.loc[3,'confirm']
print("JP_Mainland+cruiser:-----------",tmp_jp)
#加一行‘日本’
global_data.loc[len(global_data)+1] = ('日本',tmp_jp)
global_data.loc[len(global_data)+2] = ('中国', chinaTotal['totalConfirm']) 

world_name = pd.read_excel("国家中英文对照Echarts_clean_name.xlsx")
#print("df_global_data2merge: ########## ", global_data)
#print(world_name)
global_data = pd.merge(global_data, world_name, left_on="name", right_on="中文", how="inner")
print("global data after merge:######################", global_data)
# global_data = global_data[
#     ["name", "英文", "confirm", "suspect", "dead", "heal", "addconfirm"]] # info N/A today: "addsuspect", "adddead", "addheal"]]
# global_data.head()

# 日数据处理
chinaDayList = pd.DataFrame(data2['chinaDayList'])
chinaDayList = chinaDayList[['confirm', 'suspect', 'dead','heal','nowConfirm', 'nowSevere', 'deadRate', 'healRate','date']] #deadRate是网页隐藏元素！
#chinaDayList.head()

# 日新增数据处理
chinaDayAddList = pd.DataFrame(data2['chinaDayAddList'])
chinaDayAddList = chinaDayAddList[[ 'confirm', 'suspect', 'dead', 'heal', 'deadRate', 'healRate','date']]
#chinaDayAddList.head()


# 数据可视化
#print("chinaTotal.values:")
#print(chinaTotal.values())
chinaTotal_p1 = [chinaTotal['totalConfirm'], chinaTotal['totalDead'], chinaTotal['totalHeal']]
chinaTotal_p2 = [chinaTotal['nowSuspect'], chinaTotal['nowConfirm'], chinaTotal['nowSevere']]
chinaAdd_p3 = [chinaAdd['AddedtotalConfirm'], chinaAdd['AddedtotalDead'], chinaAdd['AddedtotalHeal']]
chinaAdd_p4 = [chinaAdd['AddednowSuspect'], chinaAdd['AddednowConfirm'], chinaAdd['AddednowSevere']]

# 饼图
total_pie = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width='500px', height='350px', bg_color="transparent"))
        .add("", [list(z) for z in zip(['totalConfirm ', 'totalDead    ', 'totalHeal   '], chinaTotal_p1)],
             center=["48%", "60%"], radius=[70, 85], )
        .add("", [list(z) for z in zip(['nowSuspect ', 'nowConfirm ', 'nowSevere   '], chinaTotal_p2)],
             center=["48%", "60%"], radius=[45, 60], )
        .add("", [list(z) for z in zip(['AddConfirm ', 'AddDead      ', 'AddHeal     '], chinaAdd_p3)],
             center=["48%", "60%"], radius=[20, 35], )
        .add("", [list(z) for z in zip(['AddnowSuspect', 'AddnowConfirm', 'AddnowSevere'], chinaAdd_p4)],
             center=["48%", "60%"], radius=[0, 10], )
#         .add("", [list(z) for z in zip(chinaAdd.keys(), chinaAdd.values())], center=["48%", "60%"], radius=[0, 35])
        .set_global_opts(title_opts=opts.TitleOpts(title="Pie_China_CoV", pos_bottom=0,
                                                   title_textstyle_opts=opts.TextStyleOpts(color="#00FFFF")),
                         legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="#FFFFFF")))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}")))
#print("global_data:################ ",global_data)
print('\n')
# 全球疫情地图
world_map = (
    Map(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add("", [list(z) for z in zip(list(global_data["英文"]), list(global_data["confirm"]))], "world",
             is_map_symbol_show=False)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False),
                         toolbox_opts=opts.ToolboxOpts(orient='vertical', pos_right="10%"))
        .set_global_opts(visualmap_opts=opts.VisualMapOpts(is_piecewise=True, background_color="transparent",
                                                           textstyle_opts=opts.TextStyleOpts(color="#F5FFFA"),
                                                           pieces=[
                                                               {"min": 101, "label": '>100', "color": "#893448"},
                                                               {"min": 10, "max": 100, "label": '10-100',
                                                                "color": "#fb8146"},
                                                               {"min": 1, "max": 9, "label": '1-9',
                                                                "color": "#fff2d1"},
                                                           ])))

# 中国疫情地图绘制
# 数据处理
#省份汇总数据也可以直接读取
area_data = china_data.groupby("province")["confirm"].sum().reset_index()
area_data.columns = ["province", "confirm"]


area_map = (
    Map(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add("", [list(z) for z in zip(list(area_data["province"]), list(area_data["confirm"]))], "china",
             is_map_symbol_show=False, label_opts=opts.LabelOpts(color="#fff"),
             tooltip_opts=opts.TooltipOpts(is_show=True), zoom=1.2, center=[105, 30])
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="China CoV Distribution", pos_top='5%',
                                                   title_textstyle_opts=opts.TextStyleOpts(color="#FF0000")),
                         visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pos_right=0, pos_bottom=0,
                                                           textstyle_opts=opts.TextStyleOpts(color="#F5FFFA"),
                                                           pieces=[
                                                               {"min": 1001, "label": '>1000', "color": "#893448"},
                                                               {"min": 500, "max": 1000, "label": '500-1000',
                                                                "color": "#ff585e"},
                                                               {"min": 101, "max": 499, "label": '101-499',
                                                                "color": "#fb8146"},
                                                               {"min": 10, "max": 100, "label": '10-100',
                                                                "color": "#ffb248"},
                                                               {"min": 0, "max": 9, "label": '0-9',
                                                                "color": "#fff2d1"}])))

city_data = china_data.groupby('city')['confirm'].sum().reset_index()
city_data.columns = ["city", "confirm"]

def is_city(item):
    '''
    判断一个城市能否在Geo地图上被找到
    :param item: 城市名
    :return: T/F
    '''

    lists_1 = []
    lists_1.append(item)
    lists_2 = [10]
    geo = Geo()
    geo.add_schema(maptype="china")
    try:
        geo.add("确诊城市", [list(z) for z in zip(lists_1, lists_2)])
        return True
    except TypeError as e:
        return False


city_index = []
i = 0
for item in city_data['city']:
    if is_city(item) == False:
        city_index.append(i)
    i += 1
print("未通过geos函数的城市:$$$$$$$$$$$$$$$$$$", city_data['city'][city_index])
# 设置匹配阈值
#COORDINATES.cutoff = 0.7
#print(search_coordinates_by_keyword(city_area_list[10][:2]))
##############清除不存在的地点，否则Geo会报错###############
# 城市坐标处理，清洗数据需要注意模糊查询

for x in city_index:
    del (city_data['city'][x])
    del (city_data['confirm'][x])
    
#严重确诊城市：
city_index_ = []
i = 0
for item in city_data['confirm']:
    if item > 500:
        city_index_.append(i)
    i += 1

serious_city = []  # 严重城市
serious_submit = []  # 严重人数
for y in city_index_:
    serious_city.append(list(city_data['city'])[y])
    serious_submit.append(list(city_data['confirm'])[y])
    
#一般确诊城市：    
city_index__ = []
i = 0
for item in city_data['confirm']:
    if item < 1001:
        city_index__.append(i)
    i += 1

cfm_city = []  # 一般确诊城市
cfm_submit = []  # 一般确诊人数
for z in city_index__:
    cfm_city.append(list(city_data['city'])[z])
    cfm_submit.append(list(city_data['confirm'])[z])
    
list_1 = ["拉萨"]
list_2 = [1]
print('\n')
print("print serious city############:")
#print(serious_city,serious_submit)
print([list(z) for z in zip(list(serious_city), list(serious_submit))])
print('\n')
print("一般确诊城市:########")
print([list(z) for z in zip(cfm_city, cfm_submit)])
print('###########################\n')
area_heat_geo = (
    Geo(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS, bg_color='transparent'))
        .add_schema(maptype="china", zoom=1.2, center=[105, 30])
        .add("Less Plagued", [list(z) for z in zip(cfm_city, cfm_submit)], symbol_size=6)
        .add("Less Plagued", [list(z) for z in zip(list_1, list_2)], symbol_size=6)  # 孤独拉萨
        .add("Less Plagued", [list(z) for z in zip(list(serious_city), list(serious_submit))],  # 感染者超1000的城市
             type_=ChartType.EFFECT_SCATTER, effect_opts=opts.EffectOpts(is_show=True, color="black",
                                                                         symbol_size=10, scale=3, period=1))
        .add("Badly Plagued", [list(z) for z in zip(list(serious_city), list(serious_submit))],type_=ChartType.HEATMAP)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(range_size=[0, 10, 50, 100, 200, 500, 50000], orient='horizontal', max_=500,is_calculable=True,     
                                          pos_bottom=0),
        title_opts=opts.TitleOpts(title="China CoV HeatMap", pos_top='5%'),
        legend_opts=opts.LegendOpts(pos_bottom='10%', pos_left=0)))

# 每日数据趋势
line = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.CHALK, bg_color="transparent"))
        .add_xaxis(list(chinaDayList["date"]))
        .add_yaxis("      totalConfirm        ", list(chinaDayList["confirm"]), is_smooth=True, yaxis_index=1)
        .add_yaxis("totalDead            ", list(chinaDayList["dead"]), is_smooth=True, yaxis_index=1)
        .add_yaxis("totalHeal            ", list(chinaDayList["heal"]), is_smooth=True, yaxis_index=1)
        .add_yaxis("nowSuspect          ", list(chinaDayList["suspect"]), is_smooth=True, yaxis_index=1)
        .add_yaxis("      nowConfirm          ", list(chinaDayList["nowConfirm"]), is_smooth=True, yaxis_index=1)
        .add_yaxis("nowSevere           ", list(chinaDayList["nowSevere"]), is_smooth=True, yaxis_index=1)
        .add_yaxis("deadRate            ", list(chinaDayList["deadRate"]), is_smooth=True, yaxis_index=1)
        .add_yaxis("healRate", list(chinaDayList["healRate"]), is_smooth=True, yaxis_index=1)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(legend_opts=opts.LegendOpts(pos_left='center')))

bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.CHALK, bg_color="transparent"))
        .add_xaxis(list(chinaDayAddList["date"]))
        .add_yaxis("chinaDayAddConfirm  ", list(chinaDayAddList["confirm"]))
        .add_yaxis("chinaDayAddSuspect  ", list(chinaDayAddList["suspect"]))
        .add_yaxis("chinaDayAddDead     ", list(chinaDayAddList["dead"]))
        .add_yaxis("chinaDayAddHeal", list(chinaDayAddList["heal"]))
        .extend_axis(yaxis=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(legend_opts=opts.LegendOpts(pos_left='center'),
                         yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         datazoom_opts=opts.DataZoomOpts())).overlap(line)

big_title = (
    Pie()
        .set_global_opts(
        title_opts=opts.TitleOpts(title="2019-nCov",
                                  title_textstyle_opts=opts.TextStyleOpts(font_size=40, color='#FFFFFF',
                                                                          border_radius=True, border_color="white"),
                                  pos_top=0)))

times = (
    Pie()
        .set_global_opts(
        title_opts=opts.TitleOpts(subtitle=("Updated: " + lastUpdateTime),
                                  subtitle_textstyle_opts=opts.TextStyleOpts(font_size=13, color='#FFFFFF'),
                                  pos_top=0))
)


# total_pie = (
#     Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width='500px', height='350px', bg_color="transparent"))
#         .add("", [list(z) for z in zip(['累计确诊  ', '现有疑似  ', '累计死亡  ', '累计治愈  '], chinaTotal.values())],
#              center=["50%", "60%"], radius=[75, 100], )
#         .add("", [list(z) for z in zip(chinaAdd.keys(), chinaAdd.values())], center=["50%", "60%"], radius=[0, 50])
#         .set_global_opts(title_opts=opts.TitleOpts(title="全国总量", pos_bottom=0,
#                                                    title_textstyle_opts=opts.TextStyleOpts(color="#00FFFF")),
#                          legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="#FFFFFF")))
#         .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}")))



confirms = (Pie().
            set_global_opts(title_opts=opts.TitleOpts(title="CFM", pos_left='center', pos_top='center',
                                                      title_textstyle_opts=opts.TextStyleOpts(color='#FFFFFF'))))
confirms_people = (Pie().
                   set_global_opts(title_opts=opts.TitleOpts(title=(str(chinaTotal['totalConfirm']) + "   "),
                                                             pos_top='15%', pos_left='center',
                                                             subtitle=("         Added: " + str(chinaAdd['AddedtotalConfirm'])),
                                                             item_gap=1,
                                                             title_textstyle_opts=opts.TextStyleOpts(color="#00FFFF",
                                                                                                     font_size=30),
                                                             subtitle_textstyle_opts=opts.TextStyleOpts(color="#00BFFF")
                                                             )))
suspects = (Pie().
            set_global_opts(title_opts=opts.TitleOpts(title="Suspect", pos_left='center', pos_top='center',
                                                      title_textstyle_opts=opts.TextStyleOpts(color='#FFFFFF'))))
suspects_people = (Pie().
                   set_global_opts(title_opts=opts.TitleOpts(title=(str(chinaTotal['nowSuspect']) + "   "),
                                                             pos_top='15%', pos_left='center',
                                                             subtitle=("         Added :" + str(chinaAdd['AddednowSuspect'])),
                                                             item_gap=1,
                                                             title_textstyle_opts=opts.TextStyleOpts(color="#FF00FF",
                                                                                                     font_size=30),
                                                             subtitle_textstyle_opts=opts.TextStyleOpts(color="#EE82EE")
                                                             )))
deads = (Pie().set_global_opts(title_opts=opts.TitleOpts(title="Dead", pos_left='center', pos_top='center',
                                                   title_textstyle_opts=opts.TextStyleOpts(color='#FFFFFF'))))
          
deads_people = (Pie().set_global_opts(title_opts=opts.TitleOpts(title=(str(chinaTotal['totalDead']) + "   "),
                                                          pos_top='15%', pos_left='center',
                                                          subtitle=("         Added :" + str(chinaAdd['AddedtotalDead'])),
                                                          item_gap=1,
                                                          title_textstyle_opts=opts.TextStyleOpts(color="#FF0000",
                                                                                                  font_size=30),
                                                          subtitle_textstyle_opts=opts.TextStyleOpts(color="#F08080")
                                                          )))
heals = (Pie().set_global_opts(title_opts=opts.TitleOpts(title="Heal", pos_left='center', pos_top='center',
                                                   title_textstyle_opts=opts.TextStyleOpts(color='#FFFFFF'))))
heals_people = (Pie().set_global_opts(title_opts=opts.TitleOpts(title=(str(chinaTotal['totalHeal']) + "   "),
                                                          pos_top='15%', pos_left='center',
                                                          subtitle=("         Added :" + str(chinaAdd['AddedtotalHeal'])),
                                                          item_gap=1,
                                                          title_textstyle_opts=opts.TextStyleOpts(color="#00FF00",
                                                                                                  font_size=30),
                                                          subtitle_textstyle_opts=opts.TextStyleOpts(color="#98FB98")
                                                          )))

confirm_liquid = (Liquid().add("confirm_ratio", [(chinaTotal['totalConfirm'] / sum)], tooltip_opts=opts.TooltipOpts(),
                 label_opts=opts.LabelOpts(color="#00FFFF",
                                       font_size=15,
                                       formatter=JsCode(
                                           """function (param) {
                     return (Math.floor(param.value * 10000) / 100) + '%';
                 }"""
                                       ),
                                       position="inside",
                                       ),
             )
)

suspect_liquid = (
    Liquid()
        .add("suspectRate", [(chinaTotal['nowSuspect'] / sum)], tooltip_opts=opts.TooltipOpts(),
             label_opts=opts.LabelOpts(color="#FF00FF",
                                       font_size=15,
                                       formatter=JsCode(
                                           """function (param) {
                     return (Math.floor(param.value * 10000) / 100) + '%';
                 }"""
                                       ),
                                       position="inside",
                                       ),
             )
)

dead_liquid = (
    Liquid()
        .add("deadRate", [(chinaTotal['totalDead'] / sum)], tooltip_opts=opts.TooltipOpts(),
             label_opts=opts.LabelOpts(color="#FF0000",
                                       font_size=15,
                                       formatter=JsCode(
                                           """function (param) {
                     return (Math.floor(param.value * 10000) / 100) + '%';
                 }"""
                                       ),
                                       position="inside",
                                       ),
             )
)

heal_liquid = (
    Liquid()
        .add("healRate", [(chinaTotal['totalHeal'] / sum)], tooltip_opts=opts.TooltipOpts(),
             label_opts=opts.LabelOpts(color="#00FF00",
                                       font_size=15,
                                       formatter=JsCode(
                                           """function (param) {
                     return (Math.floor(param.value * 10000) / 100) + '%';
                 }"""
                                       ),
                                       position="inside",
                                       ),
             )
)

wc = (
    WordCloud()
        .add("", [list(z) for z in zip(list(city_data["city"]), list(city_data["confirm"]))],
             word_gap=0, word_size_range=[10, 30]))

# 图片汇总

# page = (Page(page_title="2019-nCov",layout=Page.DraggablePageLayout)
page = (Page(page_title="2019-nCov")
        .add(world_map)
        .add(total_pie)
        .add(area_map)
        .add(area_heat_geo)
        .add(bar)
        .add(big_title)
        .add(times)
        .add(confirms)
        .add(confirms_people)
        .add(suspects)
        .add(suspects_people)
        .add(deads)
        .add(deads_people)
        .add(heals)
        .add(heals_people)
        .add(confirm_liquid)
        .add(suspect_liquid)
        .add(dead_liquid)
        .add(heal_liquid)
        .add(wc)
        .add(image_base())
        ).render("2019-nCov-RealTime.html")
with open("2019-nCov-RealTime.html", "r+", encoding='utf-8') as html:
    html_bf = BeautifulSoup(html, 'lxml')
    divs = html_bf.select('.chart-container')
    divs[0][
        "style"] = "width:605px;height:274px;position:absolute;top:36px;left:333px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[1][
        'style'] = "width:411px;height:303px;position:absolute;top:5px;left:0px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[2][
        "style"] = "width:309px;height:405px;position:absolute;top:313px;left:961px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[3][
        "style"] = "width:305px;height:405px;position:absolute;top:310px;left:0px;border-style:solid;border-color:#444444;border-width:0px;"

    divs[4][
        "style"] = "width:646px;height:304px;position:absolute;top:312px;left:312px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[5][
        "style"] = "width:250px;height:55px;position:absolute;top:2px;left:440px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[6][
        "style"] = "width:200px;height:30px;position:absolute;top:11px;left:675px;border-style:solid;border-color:#444444;border-width:0px;"

    divs[7][
        'style'] = "width:60px;height:75px;position:absolute;top:5px;left:1060px;border-style:solid;border-color:#DC143C;border-width:3px;border-radius:25px 0px 0px 0px"
    divs[8][
        "style"] = "width:130px;height:75px;position:absolute;top:5px;left:1120px;border-style:solid;border-color:#DC143C;border-width:3px;"
    divs[9][
        "style"] = "width:60px;height:75px;position:absolute;top:80px;left:1060px;border-style:solid;border-color:#DC143C;border-width:3px;"
    divs[10][
        "style"] = "width:130px;height:75px;position:absolute;top:80px;left:1120px;border-style:solid;border-color:#DC143C;border-width:3px;"
    divs[11][
        "style"] = "width:60px;height:75px;position:absolute;top:155px;left:1060px;border-style:solid;border-color:#DC143C;border-width:3px;"
    divs[12][
        "style"] = "width:130px;height:75px;position:absolute;top:155px;left:1120px;border-style:solid;border-color:#DC143C;border-width:3px;"
    divs[13][
        "style"] = "width:60px;height:75px;position:absolute;top:230px;left:1060px;border-style:solid;border-color:#DC143C;border-width:3px;"
    divs[14][
        "style"] = "width:130px;height:75px;position:absolute;top:230px;left:1120px;border-style:solid;border-color:#DC143C;border-width:3px;border-radius:0px 0px 25px 0px"

    divs[15][
        "style"] = "width:160px;height:160px;position:absolute;top:-35px;left:920px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[16][
        "style"] = "width:160px;height:160px;position:absolute;top:40px;left:865px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[17][
        "style"] = "width:160px;height:160px;position:absolute;top:115px;left:920px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[18][
        "style"] = "width:160px;height:160px;position:absolute;top:188px;left:865px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[19][
        "style"] = "width:1280px;height:120px;position:absolute;top:600px;left:0px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[20][
        "style"] = "width:200px;height:200px;position:absolute;top:10px;left:1280px;border-style:solid;border-color:#444444;border-width:0px;"
    body = html_bf.find("body")
    body["style"] = "background-color:#333333;"
    print('$$$$$$$$$$$$$$$$$$$$$')
    html_new = str(html_bf)
    html.seek(0, 0)
    
    html.truncate()
    print('???????????')
    html.write(html_new)
#    make_snapshot(snapshot, '2019-nCov数据一览2.html', "2019-nCoV数据一览2.png")
    html.close()

