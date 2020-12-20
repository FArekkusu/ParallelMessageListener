import aiosqlite

DATABASE = "logs.db"
TABLE = "actions"

CREATE = f"""
CREATE TABLE IF NOT EXISTS {TABLE} (
    ip_address TEXT,
    action TEXT,
    timestamp TEXT
);
"""
DROP = f"DROP TABLE IF EXISTS {TABLE}"
SELECT = f"SELECT * FROM {TABLE}"
INSERT = f"INSERT INTO {TABLE} (ip_address, action, timestamp) VALUES (?, ?, ?)"


async def create():
    async with aiosqlite.connect("logs.db") as db:
        await db.execute(CREATE)
        await db.commit()


async def drop():
    async with aiosqlite.connect("logs.db") as db:
        await db.execute(DROP)
        await db.commit()


async def select():
    async with aiosqlite.connect("logs.db") as db:
        async with db.execute(SELECT) as cursor:
            return await cursor.fetchall()


async def insert(ip_address, action, timestamp):
    async with aiosqlite.connect("logs.db") as db:
        await db.execute(INSERT, (ip_address, action, timestamp))
        await db.commit()