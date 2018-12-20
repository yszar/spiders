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
    def insert_ftx(cls, date, province, city, name, reference_rate,
                   investment_period,
                   recommend, general, not_recommended, favorable_rate,
                   followers, Turnover, investors, borrowers, update_time,
                   Unpaid, per_capita_investment, per_capita_borrowing,
                   borrowing_number, uncollected_money, unpaid_people, score,
                   rating, rating_ranking):
        sql = "INSERT INTO wdzj (date, province, city, name,reference_rate, " \
              "investment_period,recommend, general,not_recommended, " \
              "favorable_rate,followers, Turnover,investors, borrowers, " \
              "update_time,Unpaid,per_capita_investment, " \
              "per_capita_borrowing,borrowing_number, uncollected_money, " \
              "unpaid_people,score,rating, rating_ranking) VALUES(%(date)s," \
              "%(province)s, %(city)s, %(name)s, %(reference_rate)s, " \
              "%(investment_period)s, %(recommend)s, %(general)s," \
              "%(not_recommended)s, %(favorable_rate)s, %(followers)s," \
              "%(Turnover)s, %(investors)s, %(borrowers)s, %(update_time)s," \
              "%(Unpaid)s, %(per_capita_investment)s," \
              "%(per_capita_borrowing)s, %(borrowing_number)s," \
              "%(uncollected_money)s, %(unpaid_people)s, %(score)s," \
              "%(rating)s, %(rating_ranking)s)"
        value = {
            'date': date,
            'province': province,
            'city': city,
            'name': name,
            'reference_rate': reference_rate,
            'investment_period': investment_period,
            'recommend': recommend,
            'general': general,
            'not_recommended': not_recommended,
            'favorable_rate': favorable_rate,
            'followers': followers,
            'Turnover': Turnover,
            'investors': investors,
            'borrowers': borrowers,
            'update_time': update_time,
            'Unpaid': Unpaid,
            'per_capita_investment': per_capita_investment,
            'per_capita_borrowing': per_capita_borrowing,
            'borrowing_number': borrowing_number,
            'uncollected_money': uncollected_money,
            'unpaid_people': unpaid_people,
            'score': score,
            'rating': rating,
            'rating_ranking': rating_ranking
        }
        cursor.execute(sql, value)
        conn.commit()

    @classmethod
    def select_name(cls, name):
        sql = "SELECT EXISTS(SELECT 1 FROM wdzj WHERE name=%(name)s)"
        value = {
            'name': name
        }
        cursor.execute(sql, value)
        return cursor.fetchall()[0]
