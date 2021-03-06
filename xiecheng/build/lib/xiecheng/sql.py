import pymysql
# import requests

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


class XieChengSql:

    @classmethod
    def insert_ftx(cls, hotel_name, city, address, star):
        sql = "INSERT INTO xiecheng (hotel_name, city, address, star) VALUES(%s,%s,%s,%s)"
        cursor.execute(sql, (hotel_name, city, address, star))
        conn.commit()

    @classmethod
    def select_name(cls, hotel_name):
        sql = "SELECT EXISTS(SELECT 1 FROM xiecheng WHERE hotel_name=%s)"
        cursor.execute(sql, hotel_name)
        return cursor.fetchall()[0]
