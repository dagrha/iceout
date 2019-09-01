# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IceoutItem(scrapy.Item):
    lake_id = scrapy.Field()
    iceout = scrapy.Field()
    source = scrapy.Field()
    comment = scrapy.Field()
    
