# coding:utf-8

import url_manager, html_downloader, html_parser, html_outputer
import urllib
from threading import Thread
from Queue import Queue
import time

class SpiderMain(object):
    """爬虫主调度器"""
    def __init__(self):
        """调用各个爬虫结构类"""
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
        self.url_q = Queue()  # 存放 URL 的队列，多线程爬虫用

    def craw(self, root_url, count):
        """爬虫主函数"""
        _count = count
        self.urls.add_new_url(root_url)  # 添加新的 URL 到 URL 集合中
        # 当一直有新的 URL 时
        while self.urls.has_new_url():
            try:
                # 获取一个新的 URL
                new_url = self.urls.get_new_url()
                print "craw %d: %s" %(_count - count, urllib.unquote(new_url))
                html_cont = self.downloader.download(new_url)  # 通过下载器下载 HTML 内容
                new_urls, new_data = self.parser.parse(new_url, html_cont)  # 通过解析器解析出特定的数据
                self.urls.add_new_urls(new_urls)  # 向 URL 集合中添加新的 URL 列表
                self.outputer.collect_data(new_data)  # 收集数据，后面保存数据时用

                if count == 0:
                    break
                count -= 1
            except:
                print "craw failed"

        self.outputer.output_html()  # 保存数据

    def thread_craw(self, root_url, count):
        """The same as craw method but run with multi-thread"""
        def _put_url():
            '''向队列中写入新的 URL '''
            fail_count = 0  # 获取新的 URL 失败次数
            _count = count
            self.urls.add_new_url(root_url)
            while True:
                if not self.urls.has_new_url():
                    if fail_count == 8:
                        break
                    time.sleep(3)
                    fail_count += 1
                    continue
                new_url = self.urls.get_new_url()
                self.url_q.put(new_url)
                if _count == 0:
                    break
                _count -= 1

        def _download():
            '''从 URL 队列中提取一个 URL 并下载'''
            while True:
                try:
                    new_url = self.url_q.get(timeout=5)
                except:
                    break
                print "craw %s" % new_url
                self.downloader.download(new_url)

        def _parse():
            '''从 HTML 队列中提取 HTML 并解析'''
            while True:
                try:
                    try:
                        # 从 HTML 队列提取 HTML
                        new_url, html_cont = self.downloader.html_q.get(timeout=10)
                    except:
                        break
                    new_urls, new_data = self.parser.parse(new_url, html_cont)
                    self.urls.add_new_urls(new_urls)
                    self.outputer.collect_data(new_data)

                except:
                    print "craw failed"

        # 将写入 URL、下载 HTML、解析 HTML分成三个步骤，并将下载（IO）分成多个线程执行
        _p_t = Thread(target=_put_url)
        _d_ts = [Thread(target=_download) for i in range(5)]
        _pa_t = Thread(target=_parse)

        _p_t.start()
        for t in _d_ts:
            t.start()
        _pa_t.start()

        _p_t.join()
        for t in _d_ts:
            t.join()
        _pa_t.join()

        self.outputer.output_html()
