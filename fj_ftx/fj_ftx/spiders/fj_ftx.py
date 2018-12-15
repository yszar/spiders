import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from fj_ftx.items import FjFtxItem


class FangTianXia(scrapy.Spider):
    name = 'fj_ftx'
    allowed_domains = ['fang.com']
    start_urls = [
        'http://www.fang.com/SoufunFamily.htm',
    ]

    # def start_requests(self):
    #     for i in range(1, 11):
    #         url = self.bash_url + str(i)
    #         yield Request(url, self.parse)

    def parse(self, response):
        # print(response.text)
        soup = BeautifulSoup(response.text, 'html5lib')
        # 所有省份div
        div = soup.find('div', id='c02')
        for i in range(1, 31):
            if i < 10:
                i = '0' + str(i)
            sffamily = 'sffamily_B03_' + str(i)
            sffamily_html = div.find('tr', id=sffamily)
            province = sffamily_html.find('strong').string
            citys = sffamily_html.find_all('a')
            for x in citys:
                city = x.string
                city_url = x.get('href')
                city_abbrev = re.search(r'http://(\w+)', city_url).group(1)
                if city_abbrev == 'bj':
                    newhouse_url = ' http://newhouse.fang.com/house/s/'
                    esf_url = ' http://esf.fang.com/'
                else:
                    newhouse_url = 'http://' + (
                            city_abbrev + '.newhouse.fang.com/house/s/')
                    esf_url = 'http://' + city_abbrev + '.esf.fang.com'
                yield scrapy.Request(url=newhouse_url,
                                     callback=self.parse_newhouse,
                                     meta={'info': (province, city)})

                # yield scrapy.Request(url=esf_url,
                #                      callback=self.parse_esf,
                #                      meta={'info': (province, city)})

    def parse_newhouse(self, response):
        province, city = response.meta.get('info')
        soup = BeautifulSoup(response.text, 'html5lib')
        max_url = soup.find('a', class_='last')
        if max_url == None:
            max_num = 1
        else:
            max_url = max_url.get('href')
            max_num = re.search(r'/house/s/b9(\d+)/', max_url).group(1)
        for i in range(1, int(max_num) + 1):
            temp = soup.find_all('div', class_='nlcd_name')
            for x in range(0, temp.__len__()):
                url = 'http:' + temp[x].find('a').get('href')
                # urls = temp.find_all('a')
                yield scrapy.Request(url=url,
                                     callback=self.parse_house,
                                     meta={'info': (province, city)})

    def parse_house(self, response):
        province, city = response.meta.get('info')
        soup = BeautifulSoup(response.text, 'html5lib')
        county = re.search(r'>(\w+)楼盘<',
                           str(soup.find('div', class_='br_left'))).group(1)
        if county == None:
            county = re.search(r'>(\w+)新房<',
                               str(soup.find('div', class_='br_left'))).group(1)
        community = soup.find('div', class_='tit').find('strong').string
        total_score = re.search(r' (\d\.\d+)',
                                str(soup.find('div', class_='tit'))).group(1)
        address = soup.find('span', style='color:#333;').string
        average_price = soup.find('span', class_='prib cn_ff').string
        recent_opening_temp = soup.find('a', class_='kaipan')
        if recent_opening_temp == None:
            recent_opening = '暂无资料'
        else:
            recent_opening = recent_opening_temp.string

        # 未完成
        # community_label_len = soup.find('div', class_='biaoqian1').find_all(
        #     'a').__len__()
        # community_label = []
        # for a in range(community_label_len):
        #     community_label.append(
        #         soup.find('div', class_='biaoqian1').find_all('a')[a].string)
        all_dl = soup.find('div', class_='rn')
        if all_dl != None:
            all_dl = all_dl.find_all('dl')
            for i in range(all_dl.__len__()):
                house_type = re.search(r'alt="(.*?)\d', str(all_dl[i])).group(1)
                if house_type is None and r'开间' in str(all_dl[i]):
                    house_type = re.search(r'alt="(.*?)开间',
                                           str(all_dl[i])).group(1)
                if r'开间' in str(all_dl[i]):
                    pattern = '开间'
                else:
                    pattern = re.search(r'(\d室\S+)\t', str(all_dl[i])).group(1)
                area = re.search(r'\s(\d+)㎡', str(all_dl[i])).group(1)
                if r'售完' in str(all_dl[i]):
                    total_price = '售完'
                elif r'待售' in str(all_dl[i]):
                    total_price = '待售'
                else:
                    total_price_t = all_dl[i].find('div', class_='onxf').find(
                        'span').string
                    total_price = re.search(r'：(.*)万', total_price_t).group(1)
                if total_price == '售完' or total_price == '待售':
                    household_rating = '无'
                    # household_label = '无'
                else:
                    household_rating = all_dl[i].find('span',
                                                      class_='f18 red01')
                    if household_rating is None:
                        household_rating = '暂无'
                    else:
                        household_rating = household_rating.string
                    # household_label = []
                    # p_stag = all_dl[i].find('p', class_='stag mt10')
                    # if p_stag is not None:
                    #     for b in range(p_stag.find_all('a').__len__()):
                    #         household_label.append(
                    #             all_dl[i].find('p',
                    #                            class_='stag mt10').find_all(
                    #                 'a')[b].string)
                    # else:
                    #     household_label = '暂无'

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

        else:
            house_type = pattern = area = total_price = '无'
            household_rating = '无'
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
