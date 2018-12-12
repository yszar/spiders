import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from fj_ftx.items import FjFtxItem


class lzxq_ftx(scrapy.Spider):
    name = 'fj_ftx'
    allowed_domains = ['fang.com']
    bash_url = 'http://lz.newhouse.fang.com/house/s/b9'

    def start_requests(self):
        for i in range(1, 11):
            url = self.bash_url + str(i)
            yield Request(url, self.parse())

    def parse(self, response):
        print(response.text)
