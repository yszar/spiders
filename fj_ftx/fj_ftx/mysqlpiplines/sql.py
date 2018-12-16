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
    def insert_ftx(cls, province, city, county, community, address,
                   average_price, recent_opening, total_score,
                   house_type, pattern, area, total_price, household_rating):
        sql = "INSERT INTO fangtianxia (province, city, county, community, address,average_price, recent_opening, total_score,house_type, pattern, area, total_price, household_rating) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (
            province, city, county, community, address, average_price,
            recent_opening, total_score, house_type,
            pattern, area,
            total_price, household_rating))
        conn.commit()

    @classmethod
    def select_name(cls, house_type):
        sql = "SELECT EXISTS(SELECT 1 FROM fangtianxia WHERE house_type=%s)"
        cursor.execute(sql, house_type)
        return cursor.fetchall()[0]
