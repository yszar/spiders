from .sql import Sql
from wdzj.items import WdzjItem


class WdzjPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, WdzjItem):
            name = item['name']
            ret = Sql.select_name(name)
            if ret[0] == 1:
                print('已经存在')
                pass
            else:
                date = item['date']
                province = item['province']
                city = item['city']
                name = item['name']
                reference_rate = item['reference_rate']
                investment_period = item['investment_period']
                recommend = item['recommend']
                general = item['general']
                not_recommended = item['not_recommended']
                favorable_rate = item['favorable_rate']
                followers = item['followers']
                Turnover = item['Turnover']
                investors = item['investors']
                borrowers = item['borrowers']
                update_time = item['update_time']
                Unpaid = item['Unpaid']
                per_capita_investment = item['per_capita_investment']
                per_capita_borrowing = item['per_capita_borrowing']
                borrowing_number = item['borrowing_number']
                uncollected_money = item['uncollected_money']
                unpaid_people = item['unpaid_people']
                score = item['score']
                rating = item['rating']
                rating_ranking = item['rating_ranking']
                Sql.insert_ftx(date, province, city, name, reference_rate,
                               investment_period,
                               recommend, general, not_recommended,
                               favorable_rate,
                               followers, Turnover, investors, borrowers,
                               update_time,
                               Unpaid, per_capita_investment,
                               per_capita_borrowing,
                               borrowing_number, uncollected_money,
                               unpaid_people, score,
                               rating, rating_ranking)
                return item
