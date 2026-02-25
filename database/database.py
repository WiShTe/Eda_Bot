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
                VALUES ($1, $2, $3)
                ON CONFLICT (telegram_id) DO NOTHING
                """,
                telegram_id, username, first_name
            )


    async def add_meal(self, data: dict):
        """Добавляем блюдо в базу данных dishes"""
        try:
            async with self.pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO dishes (name, ingredients, receipt, time_of_meal)
                    VALUES ($1, $2, $3, $4)
                    """,
                    data['name'],  # $1
                    data['ingredients'],  # $2
                    data['receipt'],  # $3
                    data['time_of_meal']  # $4
                )
            return True  # Успех
        except Exception as e:
            print(f"❌ Ошибка при добавлении блюда: {e}")
            return False  # Ошибка

    async def get_meal(self, meal_id: int):
        """Получить блюдо из базы"""
        async with self.pool.acquire() as conn:
            meal = await conn.fetchrow(
                "SELECT * FROM dishes WHERE id = $1",
                 meal_id
            )
            return meal

    async def get_max_meal_id(self):
        """Получить максимальное id из таблицы dishes"""
        async with self.pool.acquire() as conn:
            id = await conn.fetchrow(
                "SELECT MAX(id) FROM dishes"
            )
            return id

    async def get_user(self, telegram_id: int):
        """Получить пользователя из базы"""
        async with self.pool.acquire() as conn:
            user = await conn.fetchrow(
                "SELECT * FROM users WHERE telegram_id = $1",
                telegram_id
            )
            return user


# Глобальный экземпляр
database = Database()