# -*- coding:utf-8 -*-

import requests
import itchat
from requests.exceptions import RequestException
from threading import Timer
#from __future__ import unicode_literals

def get_news():
    #
    url = 'http://open.iciba.com/dsapi/'
    html = requests.get(url)
    text = html.json()
    #print(text)
    contents = text['content']

    note = text['note']
    print (contents)
    return contents,  note
def send_news():
    itchat.auto_login(hotReload = True)
    try:
        my_friend = itchat.search_friends(name='麻包婆')
        print(my_friend)
        MaBaopo = my_friend[0]["UserName"]
        message1 = get_news()[0]
        message2 = get_news()[1]
        #message3 = get_news()[1][5:]
        with open('juzi.txt','a') as f:
            f.write('\n'.join([message1, message2,]))
            f.write('\n' + '=' * 50 + '\n')

        itchat.send(message1, toUserName = MaBaopo)
        itchat.send(message2, toUserName = MaBaopo)
        #itchat.send(message3, toUserName = MaBaopo)

        t = Timer(86400, send_news)
        t.start()

    except RequestException:
        message4 = u'今天出现了 /bug/^_^^ _ ^'
        itchat.send(message4,toUserName = MaBaoPo)


if __name__ == "__main__":
    send_news()