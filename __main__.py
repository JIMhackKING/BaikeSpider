# coding:utf-8
from spider_main import SpiderMain
import urllib
import time
from tkinter import *
from tkinter import ttk
import re

def start(*args):
    s=e1.get()
    # Python 编码问题，文件内的标点使用 UTF-8 编码，但 s 是 Unicode 编码
    keywords = re.split(r"[;,；，]".decode("utf-8"), s)
    master.destroy()
    for i in keywords:
        url_word = urllib.quote(i.encode("utf-8"))
        root_url = "https://baike.baidu.com/item/" + url_word
        obj_spider = SpiderMain()
        # thread_craw 是多线程爬取方法，craw 是单线程爬取方法
        obj_spider.thread_craw(root_url, 10000)
        time.sleep(5)

master = Tk()
frame1 = Frame(master)
frame1.pack()

frame2 = Frame(master)
frame2.pack()

ttk.Label(frame1, text="如有多项用逗号或分号隔开").pack()
middle = ttk.Label(frame1, text="关键词：")
middle.pack(side=LEFT)

e1 = ttk.Entry(frame1)
e1.pack(side=RIGHT)

confirm = ttk.Button(frame2, text="开始", command=start)
confirm.pack()
master.bind('<Return>', start)

if __name__ == '__main__':
    mainloop()
    