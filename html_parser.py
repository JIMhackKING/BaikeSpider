# coding:utf-8
from bs4 import BeautifulSoup
import re
import urlparse
import bs4

class HtmlParser(object):
    """HTML 解析器"""
    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all("a", href=re.compile(r"/item/\w+"))
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        res_data = {}

        res_data['url'] = page_url

        # <dd class="lemmaWgt-lemmaTitle-title"><h1>单片机</h1>
        title_node = soup.find("dd", class_="lemmaWgt-lemmaTitle-title").find("h1")
        res_data['title'] = title_node.get_text()

        # <div class="lemma-summary" label-module="lemmaSummary">
        summary_node = soup.find("div", class_="lemma-summary")
        res_data['summary'] = summary_node.get_text()

        try:
            content_node = soup.find("div", {"class":"main-content"})
            content_tags = content_node.find("div", {"class":"anchor-list"}).next_siblings
            content = ""
            for tag in content_tags:
                # The NavigableString haven't get_text() arrtibute
                if not isinstance(tag, bs4.element.NavigableString):
                    # Remove the excess blank
                    content += re.sub("\n\n+", "\n", tag.get_text())
            res_data['content'] = content
        except AttributeError:
            res_data['content'] = ""

        return res_data

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, "html5lib", from_encoding="utf-8")
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data