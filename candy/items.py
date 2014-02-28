#!/usr/bin/env python
# coding=utf-8

from scrapy.item import Item, Field

class SougouDictItem(Item):
    file_urls = Field()
