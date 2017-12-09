# coding:utf-8
import urllib2
from Queue import Queue

class HtmlDownloader(object):
    """HTML 下载器"""
    def __init__(self):
        self.html_q = Queue()

    def download(self, url):
        if url is None:
            return

        response = urllib2.urlopen(url)
        if response.getcode() != 200:
            return
        html = response.read()

        # For multi-thread
        self.html_q.put((url,html))
        return html
