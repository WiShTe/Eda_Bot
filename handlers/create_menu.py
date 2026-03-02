from calendar import weekday

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database.database import database
from states import Create_menu
import random

create_menu_router = Router()

'''@create_menu_router.message(Command("create_menu"))
@create_menu_router.message(F.text == "Составить меню")
async def create_menu(message: Message, ) -> None:
    reply = str()  # строка ответа
    max_id = await database.get_max_meal_id()  # получение максимального id из базы данных
    max_id = int(max_id[0])  # получение максимального id из базы данных
    for i in range(21):
        random_id = random.randint(1, max_id)  # получаем случайное число от 1 до максимального индекса
        data = await database.get_meal(random_id)  # получаем из базы данных блюдо со случайным id
        reply += (F'{data[1]} \n')  # добавляем в ответ название блюда
    """Хендлер создания меню на неделю"""
    await message.answer(
        F'{reply}'  # отправляем ответ пользователю
    )'''


@create_menu_router.message(Command("create_menu"))
@create_menu_router.message(F.text == "Составить меню")
async def create_menu(message: Message, state: FSMContext) -> None:
    titles = ['🍳 Завтрак', '🍲 Обед', '🍽 Ужин']
    reply = "📅 **Меню на неделю:**\n\n"
    weekdays = ['понедельник', 'вторник',
                'среда', 'четверг', 'пятница',
                'суббота', 'воскресенье']
    tables = ['breakfast', 'lunch', 'dinner']
    breakfast_max_id = await database.get_max_id("breakfast")
    lunch_max_id = await database.get_max_id("lunch")
    dinner_max_id = await database.get_max_id("dinner")
    max_ids = [breakfast_max_id, lunch_max_id, dinner_max_id]

    for weekday in weekdays:
        reply += (f"{weekday}:\n")
        for table, title, max_id in zip(tables, titles, max_ids):
            print(max_id)
            random_id = random.randint(1, int(max_id))
            data = await database.get_meal(table, random_id)
            reply += f"    {title}: {data[1]}\n"

    await message.answer(reply, parse_mode="Markdown")
