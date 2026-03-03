from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database.database import database
import random

create_menu_router = Router()


@create_menu_router.message(Command("create_menu"))
@create_menu_router.message(F.text == "Составить меню")
async def create_menu(message: Message, state: FSMContext) -> None:
    titles = ['🍳 Завтрак', '🍲 Обед', '🍽 Ужин']
    shopping_list = {} # список покупок
    ingredients_raw = []  # список ингридиентов
    reply = "📅 **Меню на неделю:**\n\n" #меню на неделю + список покупок
    weekdays = ['понедельник', 'вторник',
                'среда', 'четверг', 'пятница',
                'суббота', 'воскресенье']
    tables = ['breakfast', 'lunch', 'dinner'] #таблицы с блюдами
    breakfast_max_id = await database.get_max_id("breakfast") #максимальный id из таблицы breakfast
    lunch_max_id = await database.get_max_id("lunch") #максимальный id из таблицы lunch
    dinner_max_id = await database.get_max_id("dinner") #максимальный id из таблицы dinner
    max_ids = [breakfast_max_id, lunch_max_id, dinner_max_id] # список максимальных id

    for weekday in weekdays:  # каждый день недели - новая итерация
        reply += (f"{weekday}:\n")  # добавляем день недли в ответ
        for table, title, max_id in zip(tables, titles, max_ids):  # берём элементы с интексами 0-3 с помощью zip
            random_id = random.randint(1, int(max_id))  # случайный индекс из таблицы table
            data = await database.get_meal(table, random_id)  # случайный элемент из таблицы tabl
            if data[2]:  # если ингредиенты есть
                ingredients_raw.append(data[2])  # добавляем в строчку с ингридиентами
            reply += f"    {title}: {data[1]}\n"  # добавляем название блюда в ответ
        # --- Обработка ингредиентов ---
    all_ingredients = ", ".join(ingredients_raw)  # объединяем все ингредиенты в одну строку
    products = all_ingredients.split(", ")  # разбиваем на отдельные компоненты

    for product in products:
        product = product.strip()  # Убираем лишние пробелы

        # Пропускаем пустые строки
        if not product or '-' not in product:
            continue

        try:
            parts = product.split('-')  # разделяем название и вес
            if len(parts) != 2:  # защита от битых ингридиентов Суп-пюре - 500г
                continue
            name_of_product = parts[0].strip()  # убираем пробелы вокруг имени
            weight_str = parts[1].strip().replace("г", '')  # Убираем 'г' и пробелы
            weight_of_product = int(weight_str)
            # Суммируем вес
            if name_of_product not in shopping_list:  # если имя продукта нет в словаре
                shopping_list[name_of_product] = weight_of_product  # создаем новую пару
            else:
                shopping_list[name_of_product] += weight_of_product  # иначе добавляем вес к существующей паре

        except (ValueError, IndexError) as e:
            print(
                f"⚠️ Пропущен ингредиент: {product} (Ошибка: {e})")  # если вес не число или другая ошибка - пропускаем ингредиент
            continue

    # Формируем красивый список покупок
    shopping_list_text = "\n🛒 **Список покупок:**\n\n"
    for item, weight in sorted(shopping_list.items()):
        shopping_list_text += f"{item} - {weight}г\n"
    reply += shopping_list_text
    await message.answer(reply, parse_mode="Markdown")
