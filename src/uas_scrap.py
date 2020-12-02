from bs4 import BeautifulSoup
import requests
import re
import json
from src.uas_scrap_sql import DBUASScrap


class UASScrap:
    ASSETS_LIST_URL = "https://assetstore.unity.com/?orderBy=1&page={}&rows=48";

    def __init__(self) -> None:
        self.index_pagination = 0
        self.db_conn = DBUASScrap()
        super().__init__()

    @staticmethod
    def get_asset_list_url(index_pagination):
        return UASScrap.ASSETS_LIST_URL.format(index_pagination)

    def add_categories(self, menu):
        count = self.db_conn.get_count_categories()

        if count == 0 or len(menu) != count:
            self.db_conn.delete_categories()
            for m in menu:
                self.db_conn.insert_category(m)
            self.db_conn.commit()

    def get_or_add_publisher(self, publisher):
        res = self.db_conn.get_publisher(publisher["publisherId"])

        if len(res) == 0:
            last_id = self.db_conn.insert_publisher(publisher)
            self.db_conn.commit()
            return last_id
        else:
            return res[0][0]

    def add_rating(self, rating):
        last_id = self.db_conn.insert_rating(rating)
        self.db_conn.commit()
        return last_id

    def get_or_add_asset(self, asset, id_publisher, id_rating, id_category):
        last_id = self.db_conn.insert_asset(asset, id_publisher, id_rating, id_category)
        self.db_conn.commit()
        return last_id

    def get_categories(self, categories, menu):
        for c in categories:
            t = (c['id'], c['name'], c['slug'])
            menu.append(t)

            if 'subs' in c:
                self.get_categories(c['subs'], menu)

    def get_asset_list(self):
        session = requests.Session()
        request = session.get(self.get_asset_list_url(self.index_pagination))
        soup = BeautifulSoup(request.text, 'html.parser')
        print(session.cookies.get_dict())

        sjson = ""
        for script in soup.find_all("script"):
            if "DOMContentLoaded" in str(script):
                regex = "ReactDOMrender\\(({.*}),document.getElementById"
                res = re.search(regex, str(script))
                sjson = json.loads(res.group(1))

        json_product = sjson["data"]["ENTITY"]["ProductQ"]

        print(len(json_product))
        for key in json_product:
            print(json_product[key])
            publisher = {
                "publisherId": json_product[key]["publisherId"],
                "publisherName": json_product[key]["publisherName"]
            }
            rating = {
                "average": json_product[key]["rating"]["average"],
                "count": json_product[key]["rating"]["count"]
            }
            last_id_publisher = self.get_or_add_publisher(publisher)
            last_id_rating = self.add_rating(rating)

            asset = {
                "idAsset": json_product[key]["id"], "name": json_product[key]["name"],
                "mainImage": json_product[key]["mainImage"], "price": json_product[key]["price"]["price"],
                "originPrice": json_product[key]["price"]["originPrice"]
            }

            self.get_or_add_asset(asset, last_id_publisher, last_id_rating, 0)

        menu = []
        self.get_categories(sjson["data"]["filter"]["defaults"]['category']['options'], menu)
        self.add_categories(menu)


def main():
    scrap = UASScrap()
    scrap.get_asset_list()


if __name__ == '__main__':
    main()
