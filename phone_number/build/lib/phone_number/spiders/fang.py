# -*- coding: utf-8 -*-
import scrapy
import re


class FangSpider(scrapy.Spider):
    name = 'fang'
    allowed_domains = ['fang.com']
    start_urls = ['http://zu.fang.com/cities.aspx']
    custom_settings = {
        "COOKIES_ENABLED": False  # 覆盖掉settings.py里的相同设置，开启COOKIES
    }

    municipality_dict = {'北京': 'http://zu1.fang.com/house/a21/',
                         '上海': 'http://sh.zu.fang.com/house/a21/',
                         '天津': 'http://tj.zu.fang.com/house/a21/',
                         '重庆': 'http://cq.zu.fang.com/house/a21/'}
    p_c_dict = {}
    p_dict = {'安徽': 'f13', '福建': 'f13', '甘肃': 'f13', '广东': 'f13',
              '广西': 'f13', '贵州': 'f13', '海南': 'f13', '河北': 'f13',
              '河南': 'f13', '黑龙江': 'f13', '湖北': 'f13', '湖南': 'f13',
              '吉林': 'f13', '江苏': 'f13', '江西': 'f13', '辽宁': 'f13',
              '内蒙古': 'f13', '宁夏': 'f13', '青海': 'f13', '山东': 'f13',
              '山西': 'f13', '陕西': 'f13', '四川': 'f13', '西藏': 'f13',
              '新疆': 'f13', '云南': 'f13', '浙江': 'f13'}

    province_name = ()

    def __init__(self, p=None, *args, **kwargs):
        super(FangSpider, self).__init__(*args)
        self.province_name = p

    def parse(self, response):
        if self.province_name is None:
            all_li = response.xpath('//div[@id="c02"]//li')
            for li in all_li:
                province = li.xpath('.//strong/text()').get()
                if province is None:
                    for a in li.xpath('.//a[@spell]'):
                        province = a.xpath('./text()').get()
                        city = province
                        if province == '北京':
                            url = 'http://zu.fang.com/house/a21/'
                        else:
                            pass
                a = 1
        # for i in range(2, 29):
        #     one_p = response.xpath('//div[@id="c02"]/ul/li[{}]'.format(i))
        #     one_p.xpath('./a')
        #     p_name = response.xpath('//div[@id="c02"]/ul/li[{}]/strong/text()'.format(i)).get()
        #     for a in one_p.xpath('./a'):
        #         self.p_c_dict[a.root.text] = 'http:' + a.attrib[
        #             'href'] + 'house/a21/'
        #     self.p_dict[p_name] = self.p_c_dict
        #     self.p_c_dict = {}

        pass

        p_v = ['f13', 'f13', 'f13', 'f13', 'f13', 'f13', 'f13', 'f13', 'f13',
               'f13', 'f13', 'f13', 'f13', 'f13', 'f13', 'f13', 'f13', 'f13',
               'f13', 'f13', 'f13', 'f13', 'f13', 'f13', 'f13', 'f13', 'f13']
        p_k = ['安徽', '福建', '甘肃', '广东', '广西', '贵州', '海南', '河北', '河南', '黑龙江',
               '湖北', '湖南', '吉林', '江苏', '江西', '辽宁', '内蒙古', '宁夏', '青海', '山东',
               '山西', '陕西', '四川', '西藏', '新疆', '云南', '浙江']



        c_list = response.xpath('//div[@id="c02"]//li/a/text()').extract()
        cu_list = response.xpath('//div[@id="c02"]//li/a/@href').extract()
        city_urls = []
        for c in cu_list:
            city_urls.append('http:' + c)
        city_dict = dict(zip(c_list, city_urls))
        c_url = 0

        pass
