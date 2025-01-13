from tinydb import TinyDB, Query

class Database:
    def __init__(self, path: str):
        self.db = TinyDB(path)

    def insert(self, table: str, data: dict):
        self.db.table(table).insert(data)

    def get_all(self, table: str):
        return self.db.table(table).all()
