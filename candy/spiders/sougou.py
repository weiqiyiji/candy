#!/usr/bin/env python
# coding=utf-8

import os
from datetime import datetime
from urlparse import urljoin, urlparse, parse_qs

from scrapy import log
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spider import Spider
from scrapy.contrib.pipeline.files import FilesPipeline

from candy import spider_settings as settings
from candy.items import SougouDictItem


START_URLS = [
    # 'http://pinyin.sogou.com/dict/list.php?c=76',   # social science
    # 'http://pinyin.sogou.com/dict/list.php?c=436',  # e-sports
    # 'http://pinyin.sogou.com/dict/list.php?c=389',  # life
    # 'http://pinyin.sogou.com/dict/list.php?c=367',  # sports
    'http://pinyin.sogou.com/dict/cate/index/167',  # city
    'http://pinyin.sogou.com/dict/cate/index/96',   # engineering
    'http://pinyin.sogou.com/dict/cate/index/403',  # entertainment
]


class SougouSpider(Spider):
    name = 'sougou'
    start_urls = START_URLS

    def __init__(self, *args, **kwargs):
        super(SougouSpider, self).__init__(*args, **kwargs)
        if not os.path.exists(settings.DICT_DOWNLOAD_DIR):
            os.makedirs(settings.DICT_DOWNLOAD_DIR)

    def parse(self, response):
        sel = Selector(response)

        # Extract dict download links
        dl_btn_sel = sel.css('.dlbtn3')
        if not dl_btn_sel:
            self.log('No download button found in %s' % response.url)
            return
        for link in dl_btn_sel.css('::attr(href)').extract():
            yield Request(link, callback=self.download_dict)

        # Extract next page link
        next_page_link = sel.css('.next::attr(href)').extract()
        if next_page_link:
            yield Request(urljoin(response.url, next_page_link[0]),
                          callback=self.parse)

    def download_dict(self, response):
        query_string_dict = parse_qs(urlparse(response.url).query)
        if 'name' in query_string_dict:
            name = query_string_dict['name'][0].decode('gb18030')
        else:
            name = datetime.now()
        save_path = os.path.join(settings.DICT_DOWNLOAD_DIR, name)
        with open(save_path, 'wb') as fp:
            fp.write(response.body)
        self.log('[%s %s] downloaded to %s' % (name, response.url, save_path))


# class DictFilesPipeline(FilesPipeline):
#     def file_key(self, url):
#         query_string_dict = parse_qs(urlparse(url).query)
#         if 'name' in query_string_dict:
#             return query_string_dict['name'][0]
#         else:
#             return datetime.now()
