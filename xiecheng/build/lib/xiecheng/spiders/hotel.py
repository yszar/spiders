# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy_splash import SplashRequest
from xiecheng.items import XiechengItem


class HotelSpider(scrapy.Spider):
    name = 'hotel'
    allowed_domains = ['ctrip.com']
    start_urls = ['http://hotels.ctrip.com/domestic-city-hotel.html']

    def parse(self, response):
        if response.status == 502:
            yield scrapy.Request(url=response.url,
                                 dont_filter=True, callback=self.parse,
                                 meta=response.meta)
        all_city = response.xpath('//li[@id="base_bd"]/dl/dd/a')
        for city_a in all_city:
            city = city_a.xpath('./text()').get()
            url = response.urljoin(city_a.xpath('./@href').get())
            yield scrapy.Request(url=url, callback=self.parse_city,
                                 dont_filter=True,
                                 meta={'info': (city)})

    def parse_city(self, response):
        if response.status == 502:
            yield scrapy.Request(url=response.url,
                                 dont_filter=True, callback=self.parse_city,
                                 meta=response.meta)
        city = response.meta.get('info')
        all_hotel = response.xpath(
            '//div[@id="hotel_list"]//ul[@class="hotel_item"]')
        for hotel in all_hotel:
            hotel_name = hotel.xpath(
                './/h2[@class="hotel_name"]/a/@title').get()
            address_text = hotel.xpath(
                './/p[@class="hotel_item_htladdress"]').get()
            if '】' in address_text:
                address = re.search(r'】(.*)。', address_text).group(1)
            else:
                address = hotel.xpath(
                './/p[@class="hotel_item_htladdress"]/text()').get()
            star_text = hotel.xpath(
                './/span[starts-with(@class,"hotel_diamond")]/@class').get()
            if star_text is not None:
                star = star_text[-1]
            else:
                star = '0'

            item = XiechengItem(
                hotel_name=hotel_name,
                city=city,
                address=address,
                star=star
            )
            yield item

        pages = response.xpath(
            '//div[@class="c_page_list layoutfix"]/a[@rel="nofollow"]/text()').get()
        if pages:
            for n in range(1, int(pages)+1):
                url = response.url+'/p'+str(n)
                yield scrapy.Request(url=url, callback=self.parse,
                                     dont_filter=True,
                                     meta={'info': (city)})


