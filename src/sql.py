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


# Пример использования
"""
async def main():
    db = AsyncSQL('database.db')
    
    await db.connect()  # Открываем соединение
    await db.execute('INSERT INTO users (name, class, access_level, tg_id) VALUES (?, ?, ?, ?)', ('Камоза Оксана Евгеньевна', 43, 1, 1435393428))
    
    users = await db.fetchall('SELECT * FROM users')
    print(users)
    
    await db.close()  # Закрываем соединение

# Для запуска асинхронной функции
import asyncio
asyncio.run(main())
"""