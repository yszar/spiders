# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiechengItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    hotel_id = scrapy.Field()
    hotel_name = scrapy.Field()
    # 酒店名称
    city = scrapy.Field()
    address = scrapy.Field()
    star = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    score = scrapy.Field()
    dpscore = scrapy.Field()
    dpcount = scrapy.Field()
    amount = scrapy.Field()