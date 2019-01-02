# -*- coding: utf-8 -*-
import scrapy
import re
import json
import math
from scrapy.selector import Selector
# from scrapy_splash import SplashRequest
from xiecheng.items import XiechengItem


class HotelSpider(scrapy.Spider):
    name = 'hotel'
    allowed_domains = ['ctrip.com']
    start_urls = ['http://hotels.ctrip.com/domestic-city-hotel.html']

    def parse(self, response):
        # if response.status == 502:
        #     yield scrapy.Request(url=response.url,
        #                          dont_filter=True, callback=self.parse,
        #                          meta=response.meta)
        all_city = response.xpath('//li[@id="base_bd"]/dl/dd/a')
        for city_a in all_city:
            city = city_a.xpath('./text()').get()
            city_info = city_a.xpath('./@href').get().split('/')[2]
            city_py = re.search(r'\D+', city_info).group(0)
            city_id = re.search(r'\d+', city_info).group(0)
            url = 'http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx'
            yield scrapy.FormRequest(url=url,
                                     formdata={'IsOnlyAirHotel': 'F',
                                               'cityId': city_id,
                                               'cityPY': city_py},
                                     callback=self.parse_city,
                                     meta={'info': (city)})

    def parse_city(self, response):
        city = response.meta.get('info')
        hotel_json = json.loads(response.body)
        hotelAmount = hotel_json['hotelAmount']
        page_num = math.ceil(hotelAmount / 25)
        hotel_25 = json.loads(response.body)['hotelPositionJSON']
        amount_dict = json.loads(response.body)['HotelMaiDianData']['value'][
            'htllist']
        for i, h in enumerate(hotel_25):
            hotel_id = h['id']
            hotel_name = h['name']
            address = h['address']
            try:
                star = h['star'][-1]
            except IndexError:
                star = '0'
            lat = h['lat']
            lon = h['lon']
            score = h['score']
            dpscore = h['dpscore']
            dpcount = h['dpcount']
            amount = json.loads(amount_dict)[i]['amount']

            item = XiechengItem(
                hotel_id=hotel_id,
                hotel_name=hotel_name,
                address=address,
                city=city,
                star=star,
                lat=lat,
                lon=lon,
                score=score,
                dpscore=dpscore,
                dpcount=dpcount,
                amount=amount
            )

            yield item
        form_data = str(response.request.body, encoding="utf-8").split('&')
        for p in range(2, page_num + 1):
            yield scrapy.FormRequest(url=response.url,
                                     formdata={'IsOnlyAirHotel': 'F',
                                               'cityId':
                                                   form_data[1].split('=')[1],
                                               'cityPY':
                                                   form_data[2].split('=')[1],
                                               'page': p},
                                     callback=self.parse_city,
                                     meta={'info': (city)})
