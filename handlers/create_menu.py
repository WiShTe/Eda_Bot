from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from database.database import database
import random

create_menu_router = Router()


@create_menu_router.message(Command("create_menu"))
@create_menu_router.message(F.text == "Составить меню")
async def create_menu(message: Message) -> None:
    reply = str()  # строка ответа
    max_id = await database.get_max_meal_id()  # получение максимального id из базы данных
    max_id = int(max_id[0])  # получение максимального id из базы данных
    for i in range(21):
        random_id = random.randint(1, max_id)  # получаем случайное число от 1 до максимального индекса
        data = await database.get_meal(random_id)  # получаем из базы данных блюдо со случайным id
        reply += (F'{data[1]} \n')  # добавляем в ответ название блюда
    """Хендлер создания меню на неделю"""
    await message.answer(
        F'{reply}' # отправляем ответ пользователю
    )
