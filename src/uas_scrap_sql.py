import mysql.connector


class DBUASScrap:
    host = "192.168.1.51"
    user = "lam"
    password = "ldl",
    database = "uas_scrap"

    def __init__(self) -> None:
        self.conn = mysql.connector.connect(
            host="192.168.1.51",
            user="lam",
            password="ldl",
            database="uas_scrap"
        )
        super().__init__()

    def insert_category(self, category):
        cursor = self.conn.cursor()
        sql = "INSERT INTO UnityAssetCategory (name, slug, idCategory) VALUES (%s, %s, %s)"
        val = (category[1], category[2], category[0])
        cursor.execute(sql, val)

        return cursor.lastrowid

    def insert_asset(self, asset, publisher_id, rating_id, category_id):
        cursor = self.conn.cursor()
        sql = "INSERT INTO " \
              "Asset (idAsset, name, mainImage, price, originPrice, idRating, idPublisher, idCategory)" \
              " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (asset["idAsset"], asset["name"], asset["mainImage"],
               asset["price"], asset["originPrice"], rating_id, publisher_id, category_id)

        cursor.execute(sql, val)

        return cursor.lastrowid

    def insert_publisher(self, publisher):
        cursor = self.conn.cursor()
        sql = "INSERT INTO Publisher (idPublisher, name) VALUES (%s, %s)"
        val = (publisher["publisherId"], publisher["publisherName"])
        cursor.execute(sql, val)

        return cursor.lastrowid

    def insert_rating(self, rating):
        cursor = self.conn.cursor()
        sql = "INSERT INTO Rating (rating, count) VALUES (%s, %s)"
        val = (rating["average"], rating["count"])
        cursor.execute(sql, val)

        return cursor.lastrowid

    def get_publisher(self, id_publisher):
        cursor = self.conn.cursor()
        sql = "SELECT * FROM Publisher WHERE idPublisher = {}".format(id_publisher)
        cursor.execute(sql)
        results = cursor.fetchall()

        return results

    def get_rating(self, id_asset):
        cursor = self.conn.cursor()
        sql = "SELECT * FROM Asset JOIN Rating ON Asset.idRating = Rating.id WHERE Asset.idAsset = {}".format(id_asset)
        cursor.execute(sql)
        results = cursor.fetchall()

        return results

    def get_count_categories(self):
        cursor = self.conn.cursor()
        sql = "SELECT COUNT(*) FROM UnityAssetCategory"
        cursor.execute(sql)
        results = cursor.fetchall()

        count = 0
        for r in results:
            count = r

        return count

    def delete_categories(self):
        cursor = self.conn.cursor()
        sql = "DELETE FROM UnityAssetCategory"
        cursor.execute(sql)

    def commit(self):
        self.conn.commit()
