import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.pool = None

    async def create_pool(self):
        """Создание пула соединений"""
        self.pool = await asyncpg.create_pool(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME')
        )
        print("✅ Пул соединений создан")

    async def add_user(self, telegram_id: int, username: str, first_name: str):
        """Добавить пользователя в базу"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO users (telegram_id, username, first_name)
                VALUES ($1, $2, $3) ON CONFLICT (telegram_id) DO NOTHING
                """,
                telegram_id, username, first_name
            )

    async def add_meal(self,  table:str, data: dict):
        """Добавляем блюдо в базу данных dishes"""
        allowed_tables = ['breakfast', 'lunch', 'dinner']
        if table not in allowed_tables:
            raise ValueError(f"Таблица {table} не разрешена")
        try:
            async with self.pool.acquire() as conn:
                await conn.execute(
                    F'INSERT INTO {table} (name, ingredients, receipt) VALUES ($1, $2, $3)',
                    data['name'],  # $1
                    ', '.join(data['ingredients']),  # $2
                    data['receipt'],  # $3
                )
            return True  # Успех
        except Exception as e:
            print(f"❌ Ошибка при добавлении блюда: {e}")
            return False  # Ошибка

    async def get_meal(self, table: str, meal_id: int):
        """Получить блюдо из базы"""
        allowed_tables = ['breakfast', 'lunch', 'dinner']
        if table not in allowed_tables:
            raise ValueError(f"Таблица {table} не разрешена")
        async with self.pool.acquire() as conn:
            print(table, meal_id)
            meal = await conn.fetchrow(
                f"SELECT * FROM {table} WHERE id = $1",
                meal_id
            )
            return meal

    async def get_user(self, telegram_id: int):
        """Получить пользователя из базы"""
        async with self.pool.acquire() as conn:
            user = await conn.fetchrow(
                "SELECT * FROM users WHERE telegram_id = $1",
                telegram_id
            )
            return user

    async def get_max_id(self, table_name: str):
        allowed_tables = ['breakfast', 'lunch', 'dinner', 'dishes', 'users']
        if table_name not in allowed_tables:
            raise ValueError(f"Таблица {table_name} не разрешена")
        else:
            async with self.pool.acquire() as conn:
                query = f"SELECT MAX(id) FROM {table_name}"
                result = await conn.fetchval(query)
                return result


# Глобальный экземпляр
database = Database()
