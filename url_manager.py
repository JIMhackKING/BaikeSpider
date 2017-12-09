# coding:utf-8

class UrlManager(object):
    """URL 管理器"""
    def __init__(self):
        # 新的 URL 集合
        self.new_urls = set()
        # 旧的 URL 集合
        self.old_urls = set()
    
    def add_new_url(self, url):
        """添加新的 URL """
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        """添加新的 URL 列表"""
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def has_new_url(self):
        """是否有新的待爬取 URL """
        return len(self.new_urls) != 0

    def get_new_url(self):
        """获取一个新的 URL """
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url
