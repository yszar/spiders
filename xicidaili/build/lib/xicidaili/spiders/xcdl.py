# -*- coding: utf-8 -*-
import scrapy.http.request
import requests
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from xicidaili.items import XicidailiItem


class XcdlSpider(CrawlSpider):
    name = 'xcdl'
    allowed_domains = ['xicidaili.com']
    start_urls = ['https://www.xicidaili.com/nn/1']

    rules = (
        Rule(LinkExtractor(allow=r'^https://www.xicidaili.com/nn/[1-9]?$'),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # 提取出ip列表
        ip_list = response.xpath(
            '//table[@id="ip_list"]//tr[@class="odd" or @class=""]/td[2]/text()').extract()
        # 提取出端口列表
        port_list = response.xpath(
            '//table[@id="ip_list"]//tr[@class="odd" or @class=""]/td[3]/text()').extract()
        # 提取出协议类型列表
        type_list = response.xpath(
            '//table[@id="ip_list"]//tr[@class="odd" or @class=""]/td[6]/text()').extract()
        print(response.url)
        for (ip, port, type) in zip(ip_list, port_list, type_list):
            proxies = {type: ip + port}
            try:
                # 设置代理链接百度  如果状态码为200 则表示该代理可以使用 然后交给流水线处理
                if requests.get('http://www.baidu.com', proxies=proxies,
                                timeout=2).status_code == 200:
                    print('success %s' % ip)
                    item = XicidailiItem()
                    item['url'] = type + '://' + ip + ':' + port
                    yield item
            except:
                print('fail %s' % ip)
