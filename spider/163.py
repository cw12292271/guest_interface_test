import requests
import os
import json
import time
import random
from threading import Thread
import jieba
import re
import threading

PATH = os.getcwd()  # 文件存储位置
OFFSET = 10000  # 爬取的偏移量，也可指定起始页面
COMMENTS = []  # 存储评论的list
WORDS = []  # 存储分词的list
FLAG = 0  # 退出的标志
TIME = 0  # 保存文件的休眠时间


# 获取header
def getHeader():
    agent = ['Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
             ]
    i = random.randint(0, len(agent) - 1)
    header = {'User-Agent': agent[i]}
    return header


# 获取URL
def getUrl():
    url = r'http://music.163.com/api/v1/resource/comments/R_SO_4_5260494?limit=100&offset='
    global OFFSET
    global FLAG

    URL = url + str(OFFSET)
    n = OFFSET
    OFFSET = OFFSET + 100  # 爬取一个页面偏移量加100

    if OFFSET > 100000:  # 达到目标则不再爬取，返回空值
        URL = None
        if FLAG == 0:
            FLAG = 2
        print('OFFSET以达10 \n FLAG=%d' % FLAG)
    return URL, n


# 爬取html
def getHtml(url, header):
    req = requests.get(url, headers=header)
    text = req.text
    return text


# 获取评论
def getComment(text):
    theComments = []
    js = json.loads(text)
    coms = js['comments']
    for s in coms:
        st = (s['content']).strip()
        theComments.append(st)
    return theComments


# 存储评论
def saveComment():
    global FLAG
    global LOCK
    with open(PATH + r'\comment.txt', 'a', encoding='utf-8') as commentfile:
        print('打开评论文件')
        while True:  # 不断循环，将评论list中的文件保存下来
            time.sleep(TIME)
            if COMMENTS:

                st = COMMENTS.pop()
                for s in st:
                    commentfile.write(s + '\n')

            else:
                if FLAG == 2:
                    commentfile.close()
                    FLAG = 3
                    print('评论文件关闭')
                    break


# 分词
def participle(comment):
    comment = re.sub('\[|\]|，|！|。|？', '', comment)
    cut = jieba.cut(comment)
    word = ' '.join(cut)
    return word


# 存储分词
def saveWord():
    global FLAG
    global LOCK
    with open(PATH + r'\WORDS.txt', 'a', encoding='utf-8') as wordFile:
        print('打开分词文件')
        while True:
            time.sleep(TIME)
            if WORDS:
                wordFile.write(WORDS.pop())

            else:
                if FLAG == 3:
                    wordFile.close()
                    print('分词文件关闭')
                    FLAG = 4
                    break


def spyder():
    global TIME
    while True:
        try:
            url, n = getUrl()
            header = getHeader()
            if url == None:
                break
            time.sleep(random.randint(5, 10))  # 每爬取一个网页就休眠随机时间
            html = getHtml(url, header)
            comment = getComment(html)
            word = participle(' '.join(comment))
            COMMENTS.append(comment)  # 将获取的评论存储到list中
            WORDS.append(word)  # 将分词存储到list中

            print('已爬取页面：', str(n))
        except BaseException:
            print('爬取页面%d失败' % n)
    TIME = 10  # 爬取即将结束，让存储线程休眠时间增长，保证所有文件都进行存储
    print('%s 线程爬取结束' % threading.current_thread().name)


# 多线程运行爬虫
def run():
    spyderThreads = []
    for i in range(6):
        spyderThreads.append(Thread(target=spyder))

    tc = Thread(target=saveComment)
    tw = Thread(target=saveWord)

    for t in spyderThreads:
        t.start()

    tc.start()
    tw.start()

    for t in spyderThreads:
        t.join()
    tc.join()
    tw.join()


if __name__ == '__main__':
    run()