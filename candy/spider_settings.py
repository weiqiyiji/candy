#!/usr/bin/env python
# coding=utf-8

import os

SPIDER_MODULES = ['candy.spiders']
USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/33.0.1750.117 Safari/537.36')

# Pipelines
# ITEM_PIPELINES = {'candy.spiders.sougou.DictFilesPipeline': 1}

# Throttling
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = True
DOWNLOAD_DELAY = 4  # In seconds
CONCURRENT_REQUESTS_PER_DOMAIN = 2

# File download
DICT_DOWNLOAD_DIR = os.path.expanduser(u'~/Documents/sougou_dict')
# FILES_STORE = os.path.expanduser(u'~/Documents/sougou_dict')

# Logging
# LOG_FILE = '/tmp/sougou_spider.log'
