import aiosqlite

class AsyncSQL:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    async def connect(self):
        if self.connection is None:
            self.connection = await aiosqlite.connect(self.db_name)

    async def close(self):
        if self.connection is not None:
            await self.connection.close()
            self.connection = None

    async def execute(self, query, params=None):
        await self.connect()
        async with self.connection.execute(query, params or []) as cursor:
            await self.connection.commit()
            return cursor

    async def fetchall(self, query, params=None):
        await self.connect()
        async with self.connection.execute(query, params or []) as cursor:
            return await cursor.fetchall()

    async def fetchone(self, query, params=None):
        await self.connect()
        async with self.connection.execute(query, params or []) as cursor:
            return await cursor.fetchone()
