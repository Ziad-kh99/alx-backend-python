import aiosqlite
import asyncio


async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        cur = await db.cursor()
        await cur.execute("SELECT * FROM users")
        return await cur.fetchall()


async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        cur = await db.cursor()
        await cur.execute("SELECT * FROM users WHERE age > 40")
        return await cur.fetchall()


async def fetch_concurrently():

    users, older_users = await asyncio.gather(
        async_fetch_users(), async_fetch_older_users()
    )

    print(f"all users ------------> \n {users}")
    print(f"all users older than 40 ------------> \n {older_users}")


asyncio.run(fetch_concurrently())
