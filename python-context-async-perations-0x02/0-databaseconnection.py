import sqlite3


class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect("users.db")
        return self.connection

    def __exit__(self, type, value, traceback):
        self.connection.close()


with DatabaseConnection() as DC:
    cursor = DC.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
