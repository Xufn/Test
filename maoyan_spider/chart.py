# -*- coding:utf-8 -*-
from pyecharts import Geo
import importlib,sys
importlib.reload(sys)


#读取城市数据
city = []
with open('dianyan2.txt',mode='r',encoding='utf-8') as f:
    rows = f.readlines()
    for row in rows:
        if len(row.split(',')) == 5:
            city.append(row.split(',')[2].replace('\n', ''))
print(city)

def all_list(arr):
    result = {}
    for i in set(arr):
        result[i] = arr.count(i)

    return result
print(all_list)
data = []

for item in all_list(city):
    data.append((item,all_list(city)[item]))

print(data)

geo = Geo('《邪不压正》观演人群地理位置分布', '数据来源',title_color = '#fff',title_pos = 'center',
        width = 1200,height =600,background_color = '#404a59')
attr,value = geo.cast(data)
geo.add("",attr,value,visual_range=[0,200],visual_text_color='#fff',
        symbol_size=20,is_visualmap=True,is_piecewise=True,
        visual_split_number=6)
geo.render()
