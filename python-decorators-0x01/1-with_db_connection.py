import sqlite3
import functools


def with_db_connection(func):
    def wrapper_db_connection(*args, **kwargs):
        with sqlite3.connect("users.db") as connection:
            kwargs["conn"] = connection
            return func(*args, **kwargs)

    return wrapper_db_connection


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


#### Fetch user by ID with automatic connection handling

user = get_user_by_id(user_id=1)
