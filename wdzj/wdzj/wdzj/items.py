# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WdzjItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 上线日期+
    date = scrapy.Field()
    # 省+
    province = scrapy.Field()
    # 市+
    city = scrapy.Field()
    # 平台名称+
    name = scrapy.Field()
    # 参考利率+
    reference_rate = scrapy.Field()
    # 投资期限+
    investment_period = scrapy.Field()
    # 推荐数+
    recommend = scrapy.Field()
    # 一般数+
    general = scrapy.Field()
    # 不推荐+
    not_recommended = scrapy.Field()
    # 好评率+
    favorable_rate = scrapy.Field()
    # 关注数+
    followers = scrapy.Field()
    # 成交金额
    Turnover = scrapy.Field()
    # 投资人数
    investors = scrapy.Field()
    # 30天借款人数
    borrowers = scrapy.Field()
    # 更新时间
    update_time = scrapy.Field()
    # 待还金额
    Unpaid = scrapy.Field()
    # 人均投资万
    per_capita_investment = scrapy.Field()
    # 人均借款万
    per_capita_borrowing = scrapy.Field()
    # 借款标数
    borrowing_number = scrapy.Field()
    # 待收投资人数
    uncollected_money = scrapy.Field()
    # 待还款人数
    unpaid_people = scrapy.Field()
    # 评分+
    score = scrapy.Field()
    # 评级+
    rating = scrapy.Field()
    # 评级排名+
    rating_ranking = scrapy.Field()
