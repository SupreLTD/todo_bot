import asyncio
import asyncpg

from config import env


class Database:
    DB = env("DB")

    async def get_data_value(self, query: str, data: tuple | str = None):
        conn = await asyncpg.connect(self.DB)
        if data:
            result = await conn.fetchval(query, data)
            await conn.close()
            return result
        else:
            result = await conn.fetchval(query)
            await conn.close()
            return result

    async def get_all_data(self, query: str, data: tuple | str = None) -> list:
        conn = await asyncpg.connect(self.DB)
        if data:
            result = await conn.fetch(query, data)
            await conn.close()
            return result
        else:
            result = await conn.fetch(query)
            await conn.close()
            return result

    async def query_update(self, query: str, data: list = None) -> None:
        conn = await asyncpg.connect(self.DB)
        if data:
            await conn.execute(query, *data)
            await conn.close()
        else:
            await conn.execute(query)
            await conn.close()

    async def create_user_table(self):
        await self.query_update("""
        CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY ,
        user_id varchar(20) unique ,
        name varchar(500),
        phone varchar(30)
        )
        """)

    async def create_tasks_table(self):
        await self.query_update("""
        CREATE TABLE IF NOT EXISTS tasks(
        id SERIAL PRIMARY KEY ,
        description varchar(100),
        task TEXT,
        completed BOOLEAN DEFAULT FALSE,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE 
        )
        """)

    async def check_user(self, user_id: str) -> bool:
        query = """SELECT EXISTS (SELECT 1 FROM users WHERE user_id = $1)"""
        result = await self.get_data_value(query, user_id)
        return result

    async def register_user(self, data: list) -> None:
        query = """INSERT INTO users(user_id, name, phone) VALUES ($1, $2, $3)"""
        await self.query_update(query, data)



# db = Database()
# asyncio.run(db.create_user_table())
# # asyncio.run(db.register_user(['5484545', 'Ivan', '+375255575577']))
# r = asyncio.run(db.check_user('5484545'))
# print(r)
