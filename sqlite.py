import sqlite3


class SqlLite:
    def Connect(self):
        conn = sqlite3.connect('database.db')
        print("Opened database successfully")
        return conn

    def CreateUserTable(self):
        conn = self.Connect()
        conn.execute(
            'CREATE TABLE users (name TEXT, email TEXT, password TEXT)')
        print("Table created successfully")