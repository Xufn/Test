# -*- coding:utf-8  -*-

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)

def index_page(i):
    """
    加载出小说的每一章内容
    :param i: 小说的第 i 章
    """
    if i == 1:
        # 小说第一章的 Url 地址
        url = "https://www.xxbiquge.com/0_807/4055527.html"
        browser.get(url)
    # 等待 Content 节点加载出来
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#content')))
    # 调用 get_info() 方法对页面进行解析
    get_info()
    # 寻找下一章点击的节点
    next_p = browser.find_elements(By.XPATH,('//div[@class="bottem2"]/a'))[2]
    # 找到后停顿 30 秒
    time.sleep(30)
    # 点击按钮
    next_p.click()

def get_info():
    """
    提取每一章小说的章章节名及正文
    :return:
    """
    # 找到章节的名字
    name = browser.find_element_by_css_selector('#wrapper > div.content_read > div > div.bookname > h1').text
    print(name)
    # 找到小说正文
    content = browser.find_element_by_id('content').text
    print(content)
    # 将拿到的小说名和对应的正文内容写入 txt 文件中
    with open('雪中悍刀行.txt','a',encoding="utf-8") as f:
        f.write('\n'.join([name, content]))
        f.write('\n\n')

def page_num():
    """
    对小说的进行分析，得到小说总的章节数
    :return: 章节数
    """
    # 目标小说的 URL 地址
    url = 'https://www.xxbiquge.com/0_807/'
    browser = webdriver.Chrome()
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    dd = soup.find_all(name="dd")
    page = len(dd)
    browser.close()
    return page

def main():
    """
    b遍历小说的全部章节
    :return:
    """
    page = page_num()
    print(page)
    for i in range(1,page+1):
        index_page(i)
if __name__ == '__main__':
    main()