import time
import sqlite3
import functools

connection_module = __import__("1-with_db_connection")
with_db_connection = connection_module.with_db_connection


#### paste your with_db_decorator here
def retry_on_failure(retries=3, delay=2):
    def retry_on_failure_real(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            last_exception = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    time.sleep(delay)
                    last_exception = e
            raise last_exception

        return wrapper

    return retry_on_failure_real


@retry_on_failure(retries=3, delay=1)
@with_db_connection
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)
