# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PhoneNumberItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city_name = scrapy.Field()
    phone_number = scrapy.Field()
    get_time = scrapy.Field()


class WubaItem(scrapy.Item):
    province = scrapy.Field()       # 省
    city = scrapy.Field()           # 市
    phone_num = scrapy.Field()      # 电话号码
    name = scrapy.Field()           # 姓名
    infoid = scrapy.Field()         # infoID
    date = scrapy.Field()           # 发布时间
    title = scrapy.Field()          # 标题
    source = scrapy.Field()
    # region = scrapy.Field()         # 区域
    # rental_type = scrapy.Field()    # 租赁形式
    # building = scrapy.Field()       # 楼院
    # room_type = scrapy.Field()      # 户型
    # area = scrapy.Field()           # 面积
    # rent = scrapy.Field()           # 租金
