# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .sql import Sql
from xicidaili.items import XicidailiItem

class XicidailiPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, XicidailiItem):
            url = item['url']
            ret = Sql.select_name(url)
            if ret[0] == 1:
                print('已经存在')
                pass
            else:
                url = item['url']
                Sql.insert_ftx(url)
                return item

