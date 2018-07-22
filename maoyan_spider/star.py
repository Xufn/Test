from pyecharts import Pie

rate = []
with open('dianyan3.txt',mode='r',encoding='utf-8') as f:
    rows = f.readlines()
    for row in rows:
        if len(row.split(',')) == 5:
            rate.append(row.split(',')[3].replace('\n',''))
a = rate.count('5')+rate.count('4.5')
b = rate.count('4')+rate.count('3.5')
c = rate.count('3')+rate.count('2.5')
d = rate.count('2')+rate.count('1.5')
e = rate.count('1')+rate.count('0.5')

attr = ["五星", "四星", "三星", "二星", "一星"]
v1 = [a,b,c,d,e]
pie = Pie("饼图-星级玫瑰图示例", title_pos='center', width=900)
pie.add("7-17", attr, v1, center=[75, 50], is_random=True,
        radius=[30, 75], rosetype='area',
        is_legend_show=False, is_label_show=True)

pie.render()