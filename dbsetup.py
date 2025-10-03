import sqlite3

class Database:
    _instance = None

    def __new__(cls, db_name="user.db"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = sqlite3.connect(db_name, check_same_thread=False, timeout=10)
            cls._instance.cursor = cls._instance.connection.cursor()
            cls._instance._create_table()
        return cls._instance

    def _create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS user
          (id INTEGER PRIMARY KEY AUTOINCREMENT,
          username TEXT UNIQUE,
          email TEXT UNIQUE,
          password TEXT)""")
        self.connection.commit()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
        Database._instance = None
