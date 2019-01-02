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
MYSQL_DB = 'phone_number'

conn = pymysql.connect(host=MYSQL_HOSTS, user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                       db=MYSQL_DB, port=MYSQL_PORT, charset='utf8')
cursor = conn.cursor()


class WubaSql:

    @classmethod
    def insert_ftx(cls, province, city, title, name, infoid, phone_num, date, source):
        sql = "INSERT INTO wuba (province, city, title, name, infoid, phone_num, date, source) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (province, city, title, name, infoid, phone_num, date, source))
        conn.commit()

    @classmethod
    def select_name(cls, phone_num):
        sql = "SELECT EXISTS(SELECT 1 FROM wuba WHERE phone_num=%s)"
        cursor.execute(sql, phone_num)
        return cursor.fetchall()[0]
