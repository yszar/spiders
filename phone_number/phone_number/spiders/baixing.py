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

    # p_dict = {'江苏': 'http://jiangsu.baixing.com/zhengzu/',
    #           '浙江': 'http://zhejiang.baixing.com/zhengzu/',
    #           '福建': 'http://fujian.baixing.com/zhengzu/',
    #           '山东': 'http://shandong.baixing.com/zhengzu/',
    #           '江西': 'http://jiangxi.baixing.com/zhengzu/',
    #           '安徽': 'http://anhui.baixing.com/zhengzu/',
    #           '广东': 'http://guangdong.baixing.com/zhengzu/',
    #           '海南': 'http://hannan.baixing.com/zhengzu/',
    #           '广西': 'http://guangxi.baixing.com/zhengzu/',
    #           '湖北': 'http://hubei.baixing.com/zhengzu/',
    #           '湖南': 'http://hunan.baixing.com/zhengzu/',
    #           '河南': 'http://henan.baixing.com/zhengzu/',
    #           '内蒙古': 'http://neimenggu.baixing.com/zhengzu/',
    #           '河北': 'http://hebei.baixing.com/zhengzu/',
    #           '山西': 'http://shanxi.baixing.com/zhengzu/',
    #           '辽宁': 'http://liaoning.baixing.com/zhengzu/',
    #           '吉林': 'http://jilinn.baixing.com/zhengzu/',
    #           '黑龙江': 'http://heilongjiang.baixing.com/zhengzu/',
    #           '四川': 'http://sichuan.baixing.com/zhengzu/',
    #           '西藏': 'http://xizang.baixing.com/zhengzu/',
    #           '云南': 'http://yunnan.baixing.com/zhengzu/',
    #           '贵州': 'http://guizhou.baixing.com/zhengzu/',
    #           '陕西': 'http://shaanxi.baixing.com/zhengzu/',
    #           '新疆': 'http://xinjiang.baixing.com/zhengzu/',
    #           '青海': 'http://qinghai.baixing.com/zhengzu/',
    #           '宁夏': 'http://ningxia.baixing.com/zhengzu/',
    #           '甘肃': 'http://gansu.baixing.com/zhengzu/',
    #           '上海': 'http://shanghai.baixing.com/zhengzu/',
    #           '北京': 'http://beijing.baixing.com/zhengzu/',
    #           '天津': 'http://tianjin.baixing.com/zhengzu/',
    #           '重庆': 'http://chongqing.baixing.com/zhengzu/'}
    p_t = None

    def __init__(self, p=None, *args, **kwargs):
        super(BaixingSpider, self).__init__(*args)
        if p is not None:
            self.p_t = p

    def parse(self, response):
        if 'spider_1' in response.url:
            yield scrapy.Request(url=response.meta['redirect_urls'][0],
                                 dont_filter=True, callback=self.parse,
                                 meta=response.meta)
        if self.p_t is None:
            municipality = response.xpath(
                '//ul[@class="wrapper"]/li/h4[text()="直辖市"]/following-sibling::ul/li')
            all_p = response.xpath('//div[@class="city-sec"]')

            for m in municipality:
                province = m.xpath('./a/text()').get()
                city = province
                url = response.urljoin(
                    m.xpath('./a/@href').get()) + 'zhengzu/?grfy=1'
                yield scrapy.Request(url=url, callback=self.parse_city,
                                     dont_filter=True,
                                     meta={'info': (province, city)})
            for p in all_p:
                province = p.xpath('./h5/a/text()').get()
                p_c = p.xpath('./ul/li[@class="city-item city-county-item"]')
                for c in p_c:
                    city = c.xpath('./a/text()').get()
                    url = response.urljoin(
                        c.xpath('./a/@href').get()) + 'zhengzu/?grfy=1'
                    yield scrapy.Request(url=url, callback=self.parse_city,
                                         dont_filter=True,
                                         meta={'info': (province, city)})
        else:
            pt = self.p_t
            for p in pt:
                if p in '北京上海天津重庆':
                    p_c = response.xpath('//a[text()={}]'.format(p))
                    province = p
                    city = p
                    url = response.urljoin(
                        p_c.xpath('./@href').get()) + 'zhengzu/?grfy=1'
                    yield scrapy.Request(url=url, callback=self.parse_city,
                                         dont_filter=True,
                                         meta={'info': (province, city)})
                else:
                    p_c = response.xpath(
                        '//a[text()={}]/following-sibling::ul/li'.format(p))
                    province = p
                    for c in p_c:
                        city = c.xpath('./a/text()').get()
                        url = response.urljoin(
                            c.xpath('./a/@href').get()) + 'zhengzu/?grfy=1'
                        yield scrapy.Request(url=url, callback=self.parse_city,
                                             dont_filter=True,
                                             meta={'info': (province, city)})

    def parse_city(self, response):
        if 'spider_1' in response.url:
            yield scrapy.Request(url=response.meta['redirect_urls'][0],
                                 dont_filter=True, callback=self.parse_city,
                                 meta=response.meta)
        province, city = response.meta.get('info')
        all_title = response.xpath(
            '//div[@class="media-body"]/div[@class="media-body-title"]/a[@class="ad-title"]')
        for t in all_title:
            title = t.xpath('./text()').get()
            url = t.xpath('./@href').get()
            yield scrapy.Request(url=url, callback=self.parse_title,
                                 dont_filter=True,
                                 meta={'info': (province, city, title)})

        next_url = response.xpath(
            '//ul[@class="list-pagination"]/li/a[text()="下一页"]/@href').get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),
                                 callback=self.parse_city,
                                 dont_filter=True,
                                 meta={'info': (province, city)})

    def parse_title(self, response):
        if 'spider_1' in response.url:
            yield scrapy.Request(url=response.meta['redirect_urls'][0],
                                 dont_filter=True, callback=self.parse_title,
                                 meta=response.meta)
        province, city, title = response.meta.get('info')
        date = response.xpath(
            '//div[@class="viewad-actions"]/span[@data-toggle="tooltip"]/text()').get()
        try:
            phone = response.xpath(
                '//li[@class="contact-btn-box"]//a[@class="contact-no"]/text()').get()
            num = response.xpath(
                '//li[@class="contact-btn-box"]//a[@class="show-contact"]/@data-contact').get()
            phone_num = phone[:7] + num
        except TypeError:
            phone_num = response.url
        name = response.xpath('//a[@class="poster-name"]/text()').get()
        infoid = ''
        source = '百姓'

        item = WubaItem(
            province=province,
            city=city,  # 省
            title=title,
            phone_num=phone_num,  # 电话号码
            name=name,  # 姓名
            infoid=infoid,
            date=date,
            source=source
        )

        yield item
