# -*- coding:utf-8 -*-

import  requests
import json
import time
import random

# 下载某一页信息
def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36',
    }
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.text
    return None

# 解析该页的数据
def parse_one_page(html):
    data = json.loads(html)['cmts']
    for item in data:
        yield{
            'comment':item['content'],
            'date':item['time'].split(' ')[0],
            'rate':item['score'],
            'city':item['cityName'],
            'nickname':item['nickName']
        }

# 保存 txt 文档
def save_to_text():
    for i in range(1,1001):
        # url 可以通过手机抓包获得
        url = 'http://m.maoyan.com/mmdb/comments/movie/248566.json?_v_=yes&offset=' + str(i)
        html = get_one_page(url)
        print('正在保存第%d页。'% i)
        for item in parse_one_page(html):
            with open('dianyan.txt','a',encoding='utf-8') as f:
                f.write(item['date'] + ',' + item['nickname']  + ',' + item['city'] + ','
                        + str(item['rate']) + ',' + item['comment'] + '\n')
            time.sleep(8 + float(random.randint(1,100)) / 20)

if __name__ == "__main__":
    save_to_text()
