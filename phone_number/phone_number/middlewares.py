# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import pymysql
import requests
from scrapy import signals
import random
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware

class UserAgentDownloadMiddleware(object):
    USER_AGENTS = [
        # "58tongcheng/8.14.1 (iPhone; iOS 12.1.2; Scale/2.00)",
        # "58tongcheng/8.14.1 (iPhone; iOS 11.4.1; Scale/2.00)",
        # "58tongcheng/8.14.1 (iPhone; iOS 10.1; Scale/2.00)",
        # "58tongcheng/8.14.1 (iPhone; iOS 11.2; Scale/2.00)",
        # "58tongcheng/8.14.1 (iPhone; iOS 11.0.2; Scale/2.00)",
        # "58tongcheng/8.14.1 (iPhone; iOS 10.1.1; Scale/2.00)"
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"
    ]

    def process_request(self,request,spider):
        user_agent = random.choice(self.USER_AGENTS)
        request.headers['User-Agent'] = user_agent


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        # 代理服务器
        # proxyServer = "http://transfer.mogumiao.com:9001"
        appkey = "SFNjaENsekF0UXowS0pWNjowVVFjTWpzQVZxY25zMGNj"
        # appkey为你订单的key
        proxyAuth = "Basic " + appkey
        if request.url.startswith("http://"):
            request.meta['proxy'] = "http://transfer.mogumiao.com:9001"  # http代理
        elif request.url.startswith("https://"):
            request.meta['proxy'] = "https://transfer.mogumiao.com:9001"
        # request.meta["proxy"] = proxyServer
        request.headers["Authorization"] = proxyAuth


class RandomProxyMiddleware(object):
    MYSQL_HOSTS = 'cdb-4sj903z8.bj.tencentcdb.com'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'andylau1987212'
    MYSQL_PORT = 10012
    MYSQL_DB = 'spiders'

    conn = pymysql.connect(host=MYSQL_HOSTS, user=MYSQL_USER,
                           passwd=MYSQL_PASSWORD,
                           db=MYSQL_DB, port=MYSQL_PORT, charset='utf8')
    cursor = conn.cursor()

    def delete_ip(self, url):
        # 从数据库中删除无效的ip
        delete_sql = "delete from ip where url='{0}'".format(url)
        self.cursor.execute(delete_sql)
        self.conn.commit()
        return True

    def judge_ip(self, url):
        # url = url.lower()
        # 判断ip是否可用，如果通过代理ip访问百度，返回code200则说明可用
        # 若不可用则从数据库中删除
        try:
            # 设置代理链接百度  如果状态码为200 则表示该代理可以使用 然后交给流水线处理
            testurl = {'http': url}
            resp = requests.get('http://www.baidu.com', proxies=testurl,
                                timeout=1)
        except Exception as e:
            print('fail %s' % url)
            self.delete_ip(url)
            return False
        else:
            code = resp.status_code
            if code >= 200 and code < 300:
                print('success %s' % url)
                return True
            else:
                print('fail %s' % url)
                self.delete_ip(url)
                return False

    def effective_ip(self):
        sql = "SELECT url FROM ip ORDER BY RAND() LIMIT 1"
        self.cursor.execute(sql)
        results_t = self.cursor.fetchall()
        results = results_t[0][0].lower()
        ip_re = self.judge_ip(results)
        if ip_re:
            # return Sql.get_ip()[0][0]
            return results
        else:
            return self.effective_ip()
    # 动态设置ip代理
    def process_request(self, request, spider):
        proxy_ip = self.effective_ip()
        print('using ip proxy:', proxy_ip)
        request.meta["proxy"] = proxy_ip


class PhoneNumberRedirectMiddleware(RedirectMiddleware):
    def process_response(self, request, response, spider):
        if response.status == 301 or response.status == 302:
            return request

class PhoneNumberSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class PhoneNumberDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
