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
        
        CREATE TABLE IF NOT EXISTS tasks(
        id SERIAL PRIMARY KEY ,
        description varchar(20),
        task TEXT,
        completed BOOLEAN DEFAULT FALSE,
        list_id INTEGER REFERENCES users(id) ON DELETE CASCADE 
        )
        """)

    async def check_user(self, user_id: int) -> bool:
        query = """SELECT EXISTS (SELECT 1 FROM users WHERE user_id = $1)"""
        result = await self.get_data_value(query, [user_id])
        return result

    async def register_user(self, data: list) -> None:
        query = """INSERT INTO users(user_id, name, phone) VALUES ($1, $2, $3)"""
        await self.query_update(query, data)

    async def get_task(self, task_id: int) -> list:
        query = """SELECT task FROM tasks WHERE id = $1"""
        result = await self.get_data_value(query, [task_id])
        return result

    async def get_tasks(self, user_id: int) -> list:
        query = """SELECT tasks.id, tasks.description FROM tasks JOIN users u on tasks.user_id = u.id 
                                                                    WHERE u.user_id = $1 AND tasks.completed is false"""
        return await self.get_all_data(query, [user_id])

    async def create_task(self, description: str, task: str, user_id: int) -> None:
        query = """INSERT INTO tasks(description, task, user_id) 
                            VALUES ($1, $2, (SELECT id FROM users WHERE user_id = $3))"""
        await self.query_update(query, [description, task, user_id])


db = Database()

