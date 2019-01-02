import pymysql
import requests

# from fj_ftx import settings
#
# MYSQL_HOSTS = settings.MYSQL_HOSTS
# MYSQL_USER = settings.MYSQL_USER
# MYSQL_PASSWORD = settings.MYSQL_PASSWORD
# MYSQL_PORT = settings.MYSQL_PORT
# MYSQL_DB = settings.MYSQL_DB
MYSQL_HOSTS = 'cdb-4sj903z8.bj.tencentcdb.com'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'andylau1987212'
MYSQL_PORT = 10012
MYSQL_DB = 'spiders'

conn = pymysql.connect(host=MYSQL_HOSTS, user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                       db=MYSQL_DB, port=MYSQL_PORT, charset='utf8')
cursor = conn.cursor()


class GetIP(object):

    def delete_ip(self, url):
        # 从数据库中删除无效的ip
        delete_sql = "delete from ip where url='{0}'".format(url)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    # def get_ip(self):
    #     # 获取所有结果
    #     sql = "SELECT url FROM ip ORDER BY RAND() LIMIT 1"
    #     cursor.execute(sql)
    #     results = cursor.fetchall()
    #     return list(results)

    # def get_random_ip(self):
    #     # 从数据库中随机获取一个可用的ip
    #     random_sql = random.choice(self.get_ip())
    #
    #     result = cursor.execute(random_sql)
    #     for ip_info in cursor.fetchall():
    #         ip = ip_info[0]
    #         port = ip_info[1]
    #         ip_type = ip_info[2]
    #
    #         judge_re = self.judge_ip(ip, port, ip_type)
    #         if judge_re:
    #             return "{2}://{0}:{1}".format(ip, port,
    #                                           str(ip_type).lower())
    #         else:
    #             return self.get_random_ip()
    def judge_ip(self, url):
        # url = url.lower()
        # 判断ip是否可用，如果通过代理ip访问百度，返回code200则说明可用
        # 若不可用则从数据库中删除
        try:
            # 设置代理链接百度  如果状态码为200 则表示该代理可以使用 然后交给流水线处理
            testurl = {url.split(':')[0]: url}
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
        cursor.execute(sql)
        results_t = cursor.fetchall()
        results = results_t[0][0].lower()
        ip_re = self.judge_ip(results)
        if ip_re:
            # return Sql.get_ip()[0][0]
            return results
        else:
            return self.effective_ip()

        # print('begin judging ---->', random_url)
        # http_url = "https://www.baidu.com"
        # proxy_url = random_url
        # try:
        #     proxy_dict = {
        #         "http": proxy_url,
        #     }
        #     response = requests.get(http_url, proxies=proxy_dict)
        # except Exception as e:
        #     print
        #     "invalid ip and port,cannot connect baidu"
        #     self.delete_ip(ip)
        #     return False
        # else:
        #     code = response.status_code
        #     if code >= 200 and code < 300:
        #         print
        #         "effective ip"
        #         return True
        #     else:
        #         print
        #         "invalid ip and port,code is " + code
        #         self.delete_ip(ip)
        #         return False


if __name__ == "__main__":
    getip = GetIP()
    getip.effective_ip()
