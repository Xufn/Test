import pymongo
import random
import time
from math import ceil
from selenium import webdriver
from selenium.webdriver.common.by import By


MONGO_HOST = '127.0.0.1'
MONGO_DB = 'Music'
MONGO_COLLECTION = 'comments'

client = pymongo.MongoClient(MONGO_HOST)
db_manager = client[MONGO_DB]


def start_spider(url):
    """ 启动 Chrome 浏览器访问页面 """
    browser = webdriver.Chrome()
    browser.get(url)
    # 等待 5 秒, 让评论数据加载完成
    time.sleep(5)
    """
    网页中有一种节点叫做 iframe，也就是 Frame。Selenium 打开网页后，它默认是在父级
    Frame 里面操作，必须切换到 iframe, 才能定位的到 iframe 里面的元素
    这里使用 switch_to.frame（）方法来切换 Frame
    """
    iframe = browser.find_element_by_class_name('g-iframe')
    browser.switch_to.frame(iframe)
    # 获取【最新评论】总数
    new_comments = browser.find_elements(By.XPATH, "//h3[@class='u-hd4']")[1]
    max_page = get_max_page(new_comments.text)
    current = 1
    is_first = True
    while current <= max_page:
        print('正在爬取第', current, '页的数据')
        if current == 1:
            is_first = True
        else:
            is_first = False
        data_list = get_comments(is_first, browser)
        save_data_to_mongo(data_list)
        go_nextpage(browser)
        # 模拟人为浏览
        time.sleep(9 + float(random.randint(1, 100)) / 20)
        current += 1


def get_comments(is_first, browser):
    """ 获取评论数据 """
    items = browser.find_elements(By.XPATH, "//div[@class='cmmts j-flag']/div[@class='itm']")
    # 首页的数据中包含 15 条精彩评论, 20 条最新评论, 只保留最新评论
    if is_first:
        items = items[15: len(items)]
    data_list = []
    data = {}
    for each in items:
        # 用户 id
        userId = each.find_elements_by_xpath("./div[@class='head']/a")[0]
        userId = userId.get_attribute('href').split('=')[1]
        # 用户昵称
        nickname = each.find_elements_by_xpath("./div[@class='cntwrap']/div/div/a")[0]
        nickname = nickname.text
        # 评论内容
        content = each.find_elements_by_xpath("./div[@class='cntwrap']/div/div")[0]
        content = content.text.split('：')[1]
        # 点赞数
        like = each.find_elements_by_xpath("./div[@class='cntwrap']/div[@class='rp']/a[1]")[0]
        like = like.text
        if like:
            like = like.strip().split('(')[1].split(')')[0]
        else:
            like = '0'
        # 头像地址
        avatar = each.find_elements_by_xpath("./div[@class='head']/a/img")[0]
        avatar = avatar.get_attribute('src')

        data['userId'] = userId
        data['nickname'] = nickname
        data['content'] = content
        data['like'] = like
        data['avatar'] = avatar
        print(data)
        data_list.append(data)
        data = {}
    return data_list

def save_data_to_mongo(data_list):
    """
    一次性插入 20 条评论。
    插入效率高, 降低数据丢失风险
    """
    collection = db_manager[MONGO_COLLECTION]
    try:
        if collection.insert_many(data_list):
            print('成功插入', len(data_list), '条数据')
    except Exception:
        print('插入数据出现异常')

def go_nextpage(browser):
    """ 模拟人为操作, 点击【下一页】 """
    time.sleep(5)
    # 在找'下一页'这个标签的时候，滑动条是没有滑到底，导致在点下一页时，播放条会覆盖在下一页上，导致
    # 报错无法点击下一页，而是点到了播放器上
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    next_button = browser.find_elements(By.XPATH, '//div[@class="n-cmt"]/div/div[@class="m-cmmt"]/div/div/a')[-1]
    time.sleep(3)
    #print(next_button.text)
    if next_button.text == '下一页':
        next_button.click()

def get_max_page(new_comments):
    """ 根据评论总数, 计算出总分页数 """
    print('=== ' + new_comments + ' ===')
    max_page = new_comments.split('(')[1].split(')')[0]
    # 每页显示 20 条最新评论
    offset = 20
    # ceil()函数返回数字的上入整数
    max_page = ceil(int(max_page) / offset)
    print('一共有', max_page, '个分页')
    return max_page

if __name__ == '__main__':
    url = 'https://music.163.com/#/song?id=557581284'  # id 是歌曲名
    start_spider(url)