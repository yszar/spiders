import re
import scrapy
# from bs4 import BeautifulSoup
# from scrapy.http import Request
from fj_ftx.items import FjFtxItem
import sys

sys.setrecursionlimit(1000000)


# 爬虫主程序
class FangTianXia(scrapy.Spider):
    # 爬虫项目名
    name = 'fj_ftx'
    # 网址
    allowed_domains = ['fang.com']
    # 开始网址
    start_urls = [
        'http://www.fang.com/SoufunFamily.htm',
    ]

    # def start_requests(self):
    #     for i in range(1, 11):
    #         url = self.bash_url + str(i)
    #         yield Request(url, self.parse)

    # 查找所有url
    def parse(self, response):
        # print(response.text)
        # 所有省份div
        trs = response.xpath('// div[ @ id = "c02"]// tr')
        # 迭代所有省份
        for tr in trs:
            tds = tr.xpath('.//td[not(@class)]')
            province_text = tds[0].xpath(".//text()").get()
            province_text = re.sub(r"\s", "", province_text)
            if province_text:
                province = province_text
            city_td = tds[1]
            city_links = city_td.xpath(".//a")
            for city_link in city_links:
                city = city_link.xpath(".//text()").get()
                city_url = city_link.xpath(".//@href").get()
                url_module = city_url.split("//")
                scheme = url_module[0]  # http:
                domain = url_module[1]  # cq.fang.com/
                city_abbrev = re.search(r'(\w+).', domain).group(1)
                bashurl = '.newhouse.fang.com/house/s/'
                if 'bj' in domain:
                    newhouse_url = 'http://newhouse.fang.com/house/s/'
                    esf_url = 'http://esf.fang.com/'
                else:
                    # 新房url
                    newhouse_url = scheme + '//' + city_abbrev + bashurl
                    # 二手房url
                    esf_url = scheme + '//' + city_abbrev + '.esf.fang.com'

                yield scrapy.Request(url=newhouse_url,
                                     callback=self.parse_newhouse,
                                     meta={'info': (province, city)})

                # yield scrapy.Request(url=esf_url,
                #                      callback=self.parse_esf,
                #                      meta={'info': (province, city)})

    def parse_newhouse(self, response):
        province, city = response.meta.get('info')
        # soup = BeautifulSoup(response.text, 'html5lib')
        # 查找所有新房共多少页
        a_url = response.xpath('//div/ul/li[@class="fr"]/a')

        if a_url:
            max_page = max(
                list(map(int, re.findall(r'/house/s/b9(\d+)', str(a_url)))))
            for url_num in range(max_page):
                url = response.url + 'b9' + str(url_num + 1) + '/'
                yield scrapy.Request(url=url,
                                     callback=self.parse_house,
                                     meta={'info': (province, city)})
        else:
            url = response.url
            yield scrapy.Request(url=url,
                                 callback=self.parse_house,
                                 meta={'info': (province, city)})

    def parse_house(self, response):
        province, city = response.meta.get('info')
        # soup = BeautifulSoup(response.text, 'html5lib')
        all_a = response.xpath('//div[@class="nlcd_name"]/a')
        for url in all_a:
            url_text = 'http:' + url.xpath('.//@href').get()
        yield scrapy.Request(url=url_text,
                             callback=self.get_all_value,
                             meta={'info': (province, city)})

    def get_all_value(self, response):
        province, city = response.meta.get('info')
        county_t = response.xpath(
            '//*[@class="tf f12"]/li[3]/a/attribute::title').get()
        county = re.search(r'(\w+)新', county_t).group(1)
        community_div = response.xpath('//div[@class="tit"]')
        community = community_div.xpath('./h1/strong/text()').get()
        total_score_t = community_div.xpath('./a/text()').get()
        if total_score_t is None:
            total_score = '无'
        else:
            total_score = re.search(r' (\d\.\d+)', total_score_t).group(1)
        address_t = response.xpath('//div[@class="inf_left fl"]')[1]
        address = address_t.xpath('./span/text()').get()
        average_price = response.xpath('//div[@class="inf_left fl"]')[1].xpath(
            './span/text()').get()
        recent_opening_temp = response.xpath('//div[@class="inf_left fl"]')[
            2].xpath(
            './span/text()').get()
        if recent_opening_temp is not None:
            recent_opening = re.search(r'(\d+年\d+月\d+日)',
                                       recent_opening_temp).group(1)
        else:
            recent_opening = '暂无资料'

        # 未完成
        # community_label_len = soup.find('div', class_='biaoqian1').find_all(
        #     'a').__len__()
        # community_label = []
        # for a in range(community_label_len):
        #     community_label.append(
        #         soup.find('div', class_='biaoqian1').find_all('a')[a].string)
        all_rn = response.xpath('//div[@class="rn"]')
        if all_rn:
            all_dl = all_rn.xpath('./dl')
            for dl in all_dl:
                dl_alt = dl.xpath('./dd/h2/a/attribute::alt').get()
                house_type = re.search(r'(.*)\d室', dl_alt).group(1)
                pattern = re.search(r'(\d室\S+)\t', dl_alt).group(1)
                area = re.search(r'\s(\d+)㎡', dl_alt).group(1)
                total_price_t = dl.xpath(
                    './/div[@class="onxf"]/span/text()').get()
                if total_price_t is None:
                    total_price = '无'
                else:
                    total_price = re.search(r'：(.*)万', total_price_t).group(1)
                household_rating = dl.xpath(
                    './/span[@class="f18 red01"]/text()').get()
                if household_rating is None:
                    household_rating = '暂无'
        else:
            house_type = pattern = area = total_price = household_rating = '无'

        item = FjFtxItem()
        item['province'] = province
        item['city'] = city
        item['county'] = county
        item['community'] = community
        item['address'] = address
        item['average_price'] = average_price
        item['recent_opening'] = recent_opening
        item['total_score'] = total_score
        # item['community_label'] = community_label
        item['house_type'] = house_type
        item['pattern'] = pattern
        item['area'] = area
        item['total_price'] = total_price
        item['household_rating'] = household_rating
        # item['household_label'] = household_label
        yield item
        # bashurl = response.url[]
        # yield Request(url, callback=self.get_name)
