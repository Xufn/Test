# -*- coding:utf-8 -*-

import itchat
from matplotlib import pyplot as plt
import re
import jieba
import numpy as np
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator

def parse_friends():
    itchat.auto_login(hotReload=True)
    text = dict()
    friends = itchat.get_friends(update = True)[0:]
    print(friends)
    male = "male"
    female = "female"
    other = "other"
    for i in friends[1:]:
        sex = i['Sex']
        if sex == 1:
            text[male] = text.get(male, 0) + 1
        elif sex == 2:
            text[female] = text.get(female, 0) + 1
        else:
            text[other] = text.get(other, 0) + 1
    total = len(friends[1:])
    print("男性好友： %.2f%%" % (float(text[male]) / total * 100) + "\n" +
          "女性好友： %.2f%%" % (float(text[female]) / total * 100) + "\n" +
          "不明性别好友： %.2f%%" % (float(text[other]) / total * 100) )
    draw(text)

def draw(datas):
    for key in datas.keys():
        plt.bar(key, datas[key])
    plt.legend()
    plt.xlabel('sex')
    plt.ylabel('rate')
    plt.title("Gender of Alfred's friends")
    plt.show()

def parse_signature():
    itchat.auto_login(hotReload=True)
    siglist = []
    friends = itchat.get_friends(update = True)[1:]
    for i in friends:
        if __name__ == '__main__':
            signature = i["Signature"].strip().replace("span", '').replace("class", '').replace(
                "emoji","")
            pattern = re.compile("lr\d+\w+|[<>/=]")
            signature = pattern.sub("", signature)
            siglist.append(signature)
    text = "".join(siglist)

    with open('text.txt', "w", encoding = "utf-8") as f:
        wordlist = jieba.cut(text, cut_all = True)
        word_space_split = " ".join(wordlist)
        f.write(word_space_split)
        f.close()

def draw_sinature():
    text = open(u'text.txt', encoding = 'utf-8').read()
    coloring = np.array(Image.open('3.png'))
    my_wordcloud = WordCloud(background_color="white", max_words=2000,
                             mask=coloring, min_font_size=10, random_state=42, scale=2,
                             font_path=r"C:\simhei.ttf").generate(text)
    image_colors = ImageColorGenerator(coloring)
    plt.imshow(my_wordcloud.recolor(color_func=image_colors))
    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    parse_friends()
    parse_signature()
    draw_sinature()


