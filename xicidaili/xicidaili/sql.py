import pymysql

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


class Sql:

    @classmethod
    def insert_ftx(cls, url):
        sql = "INSERT INTO ip (url) VALUES(%s)"
        cursor.execute(sql, url)
        conn.commit()

    @classmethod
    def select_name(cls, url):
        sql = "SELECT EXISTS(SELECT 1 FROM ip WHERE url=%s)"
        cursor.execute(sql, url)
        return cursor.fetchall()[0]
