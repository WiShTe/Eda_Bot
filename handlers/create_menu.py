from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from database.database import database
import random

create_menu_router = Router()


@create_menu_router.message(Command("create_menu"))
@create_menu_router.message(F.text == "Составить меню")
async def create_menu(message: Message) -> None:
    reply = ""
    shopping_list = {} #словарь для списка покупок

    max_id_result = await database.get_max_meal_id() #получаем максимальный ID
    max_id = int(max_id_result[0]) #получаем максимальный ID
    ingredients_raw = [] #список ингридиентов

    for i in range(21):
        random_id = random.randint(1, max_id) #получаем случайное число от 1 до max id
        meal_data = await database.get_meal(random_id) #получаем случайное блюдо из БД

        #проверка, что данные получены
        if meal_data and len(meal_data) > 2:
            reply += f'{meal_data[1]}\n'  #название блюда
            if meal_data[2]:  #если ингредиенты есть
                ingredients_raw.append(meal_data[2]) #ингредиенты добавить ингридиенты в список

    # --- Обработка ингредиентов ---
    all_ingredients = ", ".join(ingredients_raw) #объединяем все ингредиенты в одну строку
    products = all_ingredients.split(", ") #разбиваем на отдельные компоненты

    for product in products:
        product = product.strip()  # Убираем лишние пробелы

        # Пропускаем пустые строки
        if not product or '-' not in product:
            continue

        try:
            parts = product.split('-') # разделяем название и вес
            if len(parts) != 2: #защита от битых ингридиентов Суп-пюре - 500г
                continue

            name_of_product = parts[0].strip()  #убираем пробелы вокруг имени
            weight_str = parts[1].strip().replace("г", '')  # Убираем 'г' и пробелы

            weight_of_product = int(weight_str)

            # Суммируем вес
            if name_of_product not in shopping_list: #если имя продукта нет в словаре
                shopping_list[name_of_product] = weight_of_product #создаем новую пару
            else:
                shopping_list[name_of_product] += weight_of_product #иначе добавляем вес к существующей паре

        except (ValueError, IndexError) as e:
            print(f"⚠️ Пропущен ингредиент: {product} (Ошибка: {e})") #если вес не число или другая ошибка - пропускаем ингредиент
            continue

    # Формируем красивый список покупок
    shopping_list_text = "🛒 **Список покупок:**\n\n"
    for item, weight in sorted(shopping_list.items()):
        shopping_list_text += f"{item} - {weight}г\n"

    await message.answer(
        f"📅 **Меню на неделю:**\n\n{reply}\n{shopping_list_text}",
        parse_mode="Markdown"
    )