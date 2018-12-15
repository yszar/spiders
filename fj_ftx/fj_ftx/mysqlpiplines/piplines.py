from .sql import Sql
from fj_ftx.items import FjFtxItem


class FtxPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, FjFtxItem):
            house_type = item['house_type']
            ret = Sql.select_name(house_type)
            if ret[0] == 1:
                print('已经存在')
                pass
            else:
                province = item['province']
                city = item['city']
                county = item['county']
                community = item['community']
                address = item['address']
                average_price = item['average_price']
                recent_opening = item['recent_opening']
                total_score = item['total_score']
                # community_label = item['community_label']
                house_type = item['house_type']
                pattern = item['pattern']
                area = item['area']
                total_price = item['total_price']
                household_rating = item['household_rating']
                # household_label = item['household_label']
                Sql.insert_ftx(province, city, county, community, address,
                               average_price, recent_opening, total_score,
                               house_type, pattern, area, total_price,
                               household_rating)
                return item
