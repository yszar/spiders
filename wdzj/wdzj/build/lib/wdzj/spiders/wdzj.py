import re
import scrapy
from wdzj.items import WdzjItem


# import sys
#
# sys.setrecursionlimit(1000000)

class Wdzj(scrapy.Spider):
    name = 'wdzj'
    allowed_domains = ['wdzj.com']
    start_urls = [
        # 'https://www.wdzj.com/dangan/zhlc/',
        'https://www.wdzj.com/dangan/search?filter=e1&show=1&sort=3&currentPage=1',
    ]

    def parse(self, response):
        max_page = response.xpath('//div[@class="pageList"]/span/text()').get()
        max_num = int(re.search(r'/(\d+)页', max_page).group(1))
        for num in range(1, max_num + 1):
            url = (
                      'https://www.wdzj.com/'
                      'dangan/search?filter=e1&show=1'
                      '&sort=3&currentPage=%s') % str(num)
            yield scrapy.Request(url=url,
                                 callback=self.parse_pages)

    def parse_pages(self, response):
        li = response.xpath('//ul[@class="terraceList"]/li')
        for a in li:
            href = a.xpath('./div[@class="itemTitle"]/h2/a/@href').get()
            url = 'https://www.wdzj.com%s' % href
            name = a.xpath('./div[@class="itemTitle"]/h2/a/text()').get()
            yield scrapy.Request(url=url,
                                 callback=self.parse_info,
                                 meta={'info': name})
        # next_url = response.xpath('//div[@class="pageList"]/a/text()').get()

    def parse_info(self, response):
        name = response.meta.get('info')
        pt_info = response.xpath('//div[@class="pt-info"]/div').extract()[0:-2]
        data_location = response.xpath('//div[@class="pt-info"]/span')
        date = re.sub(r'(\d{4})-(\d{2})-(\d{2}).*', r'\1年\2月\3日',
                      data_location[0].xpath('./text()').get())
        location = data_location[1].xpath('./em/text()').get().split(" · ")
        if location[0] in '北京上海天津重庆':
            province = '直辖市'
            city = location[0]
        else:
            province = location[0]
            city = location[1]
        rating = rating_ranking = '无'
        for boxs in pt_info:
            if '综合评级' in boxs:
                rating = re.search(r'\((.*)\)', boxs).group(1)
                rating_ranking = re.search(r'<b>(\d+)</b>', boxs).group(1)
            elif '参考收益' in boxs:
                reference_rate = re.search(r'data">(.*)</b>', boxs).group(
                    1) + '%'
            elif '投资期限' in boxs:
                investment_period = re.search(r'data">(.*)</b>', boxs).group(
                    1) + '月'
            elif '点评' in boxs:
                score = re.search(r'<b>\s+(\S+)\s+</b>', boxs).group(1)

        lba = response.xpath('//div[@class="lba"]/a')
        if lba.__len__() != 0:
            recommend = re.search(r'\((.*)\)',
                                  lba[1].xpath('./text()').get()).group(1)
            general = re.search(r'\((.*)\)',
                                lba[2].xpath('./text()').get()).group(1)
            not_recommended = re.search(r'\((.*)\)',
                                        lba[3].xpath('./text()').get()).group(1)
            favorable_rate = round(int(recommend) / (
                    int(recommend) + int(general) + int(not_recommended)) * 100,
                                   2)
        else:
            recommend = general = not_recommended = 0
            favorable_rate = '0%'
        followers = response.xpath(
            '//div[@class="ty-box"]/span/em/text()').get()
        # pt_30xq = response.xpath('//div[@class="pt-30xq"]/ul/li')
        nav_data = response.xpath('//div[@class="common-header-nav"]')
        nav_data_str = nav_data.xpath('string(.)')
        if '数据' not in nav_data_str.get():
            item = WdzjItem()
            item['date'] = date
            # 省+
            item['province'] = province
            # 市+
            item['city'] = city
            # 平台名称+
            item['name'] = name
            # 参考利率+
            item['reference_rate'] = reference_rate
            # 投资期限+
            item['investment_period'] = investment_period
            # 推荐数+
            item['recommend'] = recommend
            # 一般数+
            item['general'] = general
            # 不推荐+
            item['not_recommended'] = not_recommended
            # 好评率+
            item['favorable_rate'] = favorable_rate
            # 关注数+
            item['followers'] = followers
            # 成交金额
            item['Turnover'] = 0
            # 投资人数
            item['investors'] = 0
            # 30天借款人数
            item['borrowers'] = 0
            # 更新时间
            item['update_time'] = '无'
            # 待还金额
            item['Unpaid'] = 0
            # 人均投资万
            item['per_capita_investment'] = 0
            # 人均借款万
            item['per_capita_borrowing'] = 0
            # 借款标数
            item['borrowing_number'] = 0
            # 待收投资人数
            item['uncollected_money'] = 0
            # 待还款人数
            item['unpaid_people'] = 0
            # 评分+
            item['score'] = score
            # 评级+
            item['rating'] = rating
            # 评级排名+
            item['rating_ranking'] = rating_ranking
            yield item
        else:
            next_url = 'https://' + nav_data.xpath(
                '//a[2]/@href').get()
            yield scrapy.Request(url=next_url,
                                 callback=self.parse_data,
                                 meta={'info': (
                                     date, province, city, name, reference_rate,
                                     investment_period, recommend, general,
                                     not_recommended, favorable_rate, followers,
                                     score, rating, rating_ranking)})

    def parse_data(self, response):
        date, province, city, name, reference_rate, investment_period, \
        recommend, general, not_recommended, favorable_rate, followers, \
        score, rating, rating_ranking = response.meta.get('info')

        update_time_text = response.xpath(
            '//div[@class="detail-tit"]/em/text()').get()
        update_time = re.sub(r'.*(\d{4})-(\d{2})-(\d{2})', r'\1年\2月\3日',
                             update_time_text)
        a = 1
