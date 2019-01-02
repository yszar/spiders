# -*- coding: utf-8 -*-
import scrapy
from phone_number.items import PhoneNumberItem


class GanjiSpider(scrapy.Spider):
    name = 'ganji'
    allowed_domains = ['ganji.com']
    start_urls = ['http://www.ganji.com/index.htm']

    def parse(self, response):
        all_city = response.xpath('//div[@class="all-city"]//a')
        for city_a in all_city:
            city_url = city_a.xpath('./@href').extract()[0]+'zufang/0/'
            city_name = city_a.xpath('./text()').extract()[0]
            yield scrapy.Request(url=city_url,
                                 callback=self.parse_city,
                                 meta={'info': city_name})

    def parse_city(self, response):
        city_name = response.meta.get('info')

        a = 1
