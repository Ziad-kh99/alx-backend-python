import sqlite3
import functools

connection_module = __import__("1-with_db_connection")
with_db_connection = connection_module.with_db_connection


def transactional(func):
    def wrapper_trans(*args, **kwargs):
        func(*args, **kwargs)
        connection = kwargs.get("conn")
        connection.commit()
        return

    return wrapper_trans


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


#### Update user's email with automatic transaction handling

update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")
