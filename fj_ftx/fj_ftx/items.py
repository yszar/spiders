# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FjFtxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 小区名
    community = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 小区均价
    average_price = scrapy.Field()
    # 近期开盘时间
    recent_opening = scrapy.Field()
    # 小区评分
    total_score = scrapy.Field()
    # ==================================
    # 户型
    house_type = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 总价
    total_price = scrapy.Field()
    # 户型评分
    household_rating = scrapy.Field()
    # 标签
    label = scrapy.Field()
    # 地域
    area = scrapy.Field()
