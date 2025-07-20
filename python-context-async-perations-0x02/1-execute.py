import sqlite3


class ExecuteQuery:

    def __init__(self, age: int):
        self.age = age
        self.query = "SELECT * FROM users WHERE age > ?"
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect("users.db")
        cursor = self.connection.cursor()
        cursor.execute(self.query, (self.age,))
        return cursor.fetchall()

    def __exit__(self, type, value, traceback):
        self.connection.close()


with ExecuteQuery(25) as cursor:
    for row in cursor:
        print(row)
