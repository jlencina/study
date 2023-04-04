import pymongo

class get_data_robots:
    def __init__(self, ies_name, course_name, uf_name, local_name, price, full_price):
        self.ies_name = ies_name,
        self.course_name = course_name,
        self.uf_name = uf_name,
        self.local_name = local_name,
        self.price = price,
        self.full_price = full_price

    def insert_scrap_data(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["database_main"]
        robots_data = db["robots"]

        datas = {
            "ies_name": self.ies_name ,
            "course": self.course_name,
            "uf_name": self.uf_name, 
            "local_namee": self.local_name, 
            "price": self.price,
            "full_price": self.full_price
        }

        x = robots_data.insert_one(datas)
        if x == True:
            print("Deu bom")