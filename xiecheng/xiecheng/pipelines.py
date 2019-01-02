# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .sql import XieChengSql
from xiecheng.items import XiechengItem


class XiechengPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, XiechengItem):
            hotel_id = item['hotel_id']
            ret = XieChengSql.select_name(hotel_id)
            if ret[0] == 1:
                return print('已经存在')
            else:
                hotel_id = item['hotel_id']
                hotel_name = item['hotel_name']
                # 酒店名称
                city = item['city']
                address = item['address']
                star = item['star']
                lat = item['lat']
                lon = item['lon']
                score = item['score']
                dpscore = item['dpscore']
                dpcount = item['dpcount']
                amount = item['amount']
                XieChengSql.insert_ftx(hotel_id, hotel_name, city, address,
                                       star, lat, lon, score, dpscore, dpcount,
                                       amount)
                return item
