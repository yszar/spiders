# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
from .sql import WubaSql
from phone_number.items import WubaItem


class PhoneNumberPipeline(object):
    def process_item(self, item, spider):
        return item


class WubaPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, WubaItem):
            phone_num = item['phone_num']
            ret = WubaSql.select_name(phone_num)
            if ret[0] == 1:
                return print('已经存在')
            else:
                province = item['province']  # 省
                city = item['city']  # 市
                phone_num = item['phone_num']  # 电话号码
                name = item['name']  # 姓名
                title = item['title']  # 标题
                infoid = item['infoid']  # infoID
                date = item['date']
                source = item['source']
                WubaSql.insert_ftx(province, city, name, title, infoid,
                                   phone_num, date, source)
                return item
