# -*- coding: utf-8 -*-
import scrapy
from phone_number.items import WubaItem


class BaixingSpider(scrapy.Spider):
    name = 'baixing'
    allowed_domains = ['baixing.com']
    # allowed_domains = ['httpbin.org']
    custom_settings = {
        "COOKIES_ENABLED": False  # 覆盖掉settings.py里的相同设置，开启COOKIES
    }
    # start_urls = [
    #     'https://httpbin.org/get'
    # ]
    start_urls = ['http://www.baixing.com/?changeLocation=yes&return=%2F']

    def parse(self, response):
        if 'spider_1' in response.url:
            yield scrapy.Request(url=response.meta['redirect_urls'][0],
                                 dont_filter=True, callback=self.parse,
                                 meta=response.meta)
        # if self.p_t is None:
        municipality = response.xpath(
            '//ul[@class="wrapper"]/li/h4[text()="直辖市"]/following-sibling::ul/li/a')
        all_city = response.xpath('//div[@class="city-sec"]/ul/li/a') + municipality

        # for m in municipality:
        #     city = m.xpath('./a/text()').get()
        #     # city = province
        #     url = response.urljoin(
        #         m.xpath('./a/@href').get()) + 'zhengzu/?grfy=1'
        #     yield scrapy.Request(url=url, callback=self.parse_city,
        #                          dont_filter=True,
        #                          meta={'info': (province, city)})
        for c in all_city:
            # province = p.xpath('./h5/a/text()').get()
            # p_c = p.xpath('./ul/li[@class="city-item city-county-item"]')
            # for c in p_c:
            city = c.xpath('./text()').get()
            url = response.urljoin(
                c.xpath('./@href').get()) + 'zhengzu/?grfy=1'
            yield scrapy.Request(url=url, callback=self.parse_city,
                                 dont_filter=True,
                                 meta={'info': city})
        # else:
        #     pt = self.p_t
        #     for p in pt:
        #         if p in '北京上海天津重庆':
        #             p_c = response.xpath('//a[text()={}]'.format(p))
        #             province = p
        #             city = p
        #             url = response.urljoin(
        #                 p_c.xpath('./@href').get()) + 'zhengzu/?grfy=1'
        #             yield scrapy.Request(url=url, callback=self.parse_city,
        #                                  dont_filter=True,
        #                                  meta={'info': (province, city)})
        #         else:
        #             p_c = response.xpath(
        #                 '//a[text()={}]/following-sibling::ul/li'.format(p))
        #             province = p
        #             for c in p_c:
        #                 city = c.xpath('./a/text()').get()
        #                 url = response.urljoin(
        #                     c.xpath('./a/@href').get()) + 'zhengzu/?grfy=1'
        #                 yield scrapy.Request(url=url, callback=self.parse_city,
        #                                      dont_filter=True,
        #                                      meta={'info': (province, city)})

    def parse_city(self, response):
        if 'spider_1' in response.url:
            return scrapy.Request(url=response.meta['redirect_urls'][0],
                                 dont_filter=True, callback=self.parse_city,
                                 meta=response.meta)
        city = response.meta.get('info')
        all_title = response.xpath(
            '//div[@class="media-body"]/div[@class="media-body-title"]/a[@class="ad-title"]')
        for t in all_title:
            title = t.xpath('./text()').get()
            url = t.xpath('./@href').get()
            yield scrapy.Request(url=url, callback=self.parse_title,
                                 dont_filter=True,
                                 meta={'info': (city, title)})

        next_url = response.xpath(
            '//ul[@class="list-pagination"]/li/a[text()="下一页"]/@href').get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),
                                 callback=self.parse_city,
                                 dont_filter=True,
                                 meta={'info': city})

    def parse_title(self, response):
        if 'spider_1' in response.url:
            return scrapy.Request(url=response.meta['redirect_urls'][0],
                                 dont_filter=True, callback=self.parse_title,
                                 meta=response.meta)
        city, title = response.meta.get('info')
        try:
            community = response.xpath('//span[@class="meta-小区名"]/text()').get()
        except:
            community = ' '
        # if community is None:
        #     a = 1
        date = response.xpath(
            '//div[@class="viewad-actions"]/span[@data-toggle="tooltip"]/text()').get()
        try:
            phone = response.xpath(
                '//li[@class="contact-btn-box"]//a[@class="contact-no"]/text()').get()
            num = response.xpath(
                '//li[@class="contact-btn-box"]//a[@class="show-contact"]/@data-contact').get()
            phone_num = phone[:7] + num
        except TypeError:
            phone_num = response.xpath(
                '//li[@class="chat-btn-box"]//div[@class="detail"]/text()').get()
            if phone_num is None:
                phone_num = response.url
        name = response.xpath('//a[@class="poster-name"]/text()').get()

        item = WubaItem(
            city=city,  # 省
            community=community,
            title=title,
            name=name,  # 姓名
            phone_num=phone_num,  # 电话号码
            date=date
        )

        yield item
