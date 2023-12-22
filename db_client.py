import asyncio
import asyncpg

from config import env


class Database:
    DB = env("DB")

    async def get_data_value(self, query: str, data: list = None):
        conn = await asyncpg.connect(self.DB)
        if data:
            result = await conn.fetchval(query, *data)
            await conn.close()
            return result
        else:
            result = await conn.fetchval(query)
            await conn.close()
            return result

    async def get_all_data(self, query: str, data: list = None) -> list:
        conn = await asyncpg.connect(self.DB)
        if data:
            result = await conn.fetch(query, *data)
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
        user_id INTEGER unique ,
        name varchar(500),
        phone varchar(30)
        )
        """)

    async def create_tasks_table(self):
        await self.query_update("""
        CREATE TABLE IF NOT EXISTS task_lists(
        id SERIAL PRIMARY KEY ,
        name varchar(100),
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
        );
        
        CREATE TABLE IF NOT EXISTS tasks(
        id SERIAL PRIMARY KEY ,
        description varchar(100),
        task TEXT,
        completed BOOLEAN DEFAULT FALSE,
        list_id INTEGER REFERENCES task_lists(id) ON DELETE CASCADE 
        )
        """)

    async def check_user(self, user_id: int) -> bool:
        query = """SELECT EXISTS (SELECT 1 FROM users WHERE user_id = $1)"""
        result = await self.get_data_value(query, [user_id])
        return result

    async def register_user(self, data: list) -> None:
        query = """INSERT INTO users(user_id, name, phone) VALUES ($1, $2, $3)"""
        await self.query_update(query, data)

    async def get_tasks_list(self, user_id: int):
        query = """SELECT task_lists.id, task_lists.name FROM task_lists JOIN users ON task_lists.user_id = users.id 
                                                        WHERE users.user_id = $1"""
        result = await self.get_all_data(query, [user_id])
        return result

    async def get_tasks(self, tasks_list_id: int):
        query = """SELECT * FROM tasks JOIN task_lists tl on tl.id = tasks.list_id WHERE tl.id = $1"""
        return await self.get_all_data(query, [tasks_list_id])

# db = Database()
# asyncio.run(db.create_user_table())
# # asyncio.run(db.register_user(['5484545', 'Ivan', '+375255575577']))
# r = asyncio.run(db.check_user('5484545'))
# print(r)
