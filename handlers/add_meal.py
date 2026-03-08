from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states import Add_meal

from database.database import database

from keyboards.time_of_meal_kb import time_of_meal_kb
from keyboards.confirmation import confirmation_kb
from keyboards.get_finish_ingredients_kb import get_finish_ingredients_kb
from keyboards.main_menu import main_menu

add_meal_router = Router()


@add_meal_router.message(Command("add_meal"))
@add_meal_router.message(F.text == "➕ Добавить блюдо")
async def cmd_help(message: Message, state: FSMContext) -> None:
    await state.set_state(Add_meal.name)  # устанавливаю состояние ввода имени блюда
    await message.answer(
        "Введите название блюда"
    )


# Добавление названия блюда в бд
@add_meal_router.message(Add_meal.name)  # если установлено состояние Add_meal.name
async def process_meal_name(message: Message, state: FSMContext):  # создаём функцию с аргументами(сообщение, State)
    meal_name = message.text  # получаем название блюда

    await state.update_data(name=meal_name)  # сохраняем данные в FSM

    print(f"User {message.from_user.username}: {meal_name}")  # вывод в консоль для отладки

    # проверка сохраненных данных (получаем весь словарь)
    data = await state.get_data()  # получаем словарь
    print(f"Data in state: {data}")  # выводим данные для отладки

    await state.set_state(Add_meal.inrdients)  # устанавливаем состояние ввода ингридиентов

    await message.answer(
        "🥘 Введите ингредиент в формате: \n"
        "🥕 Морковь - 100г\n\n"
        "Вводите по одному. Когда закончите, нажмите кнопку ниже:",
        reply_markup=get_finish_ingredients_kb())


@add_meal_router.message(Add_meal.name)
async def process_meal_name(message: Message, state: FSMContext):
    meal_name = message.text.strip()
    await state.update_data(name=meal_name)

    print(f"User {message.from_user.username}: Блюдо - {meal_name}")

    await state.set_state(Add_meal.inrdients)


@add_meal_router.message(Add_meal.inrdients, F.text)
async def process_ingredient(message: Message, state: FSMContext):
    new_ingredient = message.text.strip()

    # Получаем текущий список
    data = await state.get_data()
    ingredients = data.get("ingredients", [])

    # Добавляем новый
    ingredients.append(new_ingredient)
    await state.update_data(ingredients=ingredients)

    print(f"User {message.from_user.username}: Ингредиент - {new_ingredient}")
    print(f"Всего ингредиентов: {len(ingredients)}")

    await message.answer(
        f"✅ Добавлено: {new_ingredient}\n"
        f" Всего: {len(ingredients)}\n\n"
        "Введите следующий или нажмите «ЗАВЕРШИТЬ ВВОД»",
        reply_markup=get_finish_ingredients_kb()
    )
    # Состояние НЕ меняем, остаёмся в Add_meal.inrdients


# ──────────────────────────────
# 5. ЗАВЕРШЕНИЕ ВВОДА ИНГРЕДИЕНТОВ (CALLBACK)
# ──────────────────────────────
@add_meal_router.callback_query(F.data == "finish_ingredients")
async def finish_ingredients(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    ingredients = data.get("ingredients", [])

    if not ingredients:
        await callback.answer("⚠️ Вы не ввели ни одного ингредиента!", show_alert=True)
        return

    await state.set_state(Add_meal.reciept)

    ing_list = "\n".join(f"• {ing}" for ing in ingredients)
    await callback.message.edit_text(
        f"✅ Ингредиенты приняты ({len(ingredients)}):\n\n{ing_list}\n\n"
        "📝 Теперь введите рецепт приготовления:"
    )
    await callback.answer()


# Добавление рецепта блюда в бд по аналогии с именем(@add_meal_router.message(Add_meal.name)
@add_meal_router.message(Add_meal.reciept)
async def process_meal_reciept(message: Message, state: FSMContext):
    receipt = message.text

    await state.update_data(receipt=receipt)

    print(f"User {message.from_user.username}: {receipt}")

    data = await state.get_data()
    print(f"Data in state: {data}")

    await state.set_state(Add_meal.time_of_meal)

    await message.answer(
        F'Введите завтрак/обед/ужин?',
        reply_markup=time_of_meal_kb(message.from_user.id),
    )


@add_meal_router.message(Add_meal.time_of_meal)
async def process_time_of_meal(message: Message, state: FSMContext):
    time_of_meal = message.text

    await state.update_data(time_of_meal=time_of_meal)

    print(f"User {message.from_user.username}: {time_of_meal}")

    data = await state.get_data()
    print(f"Data in state: {data["name"], data["ingredients"], data["receipt"], data["time_of_meal"]}")
    await message.answer(
        f'Добавить в базу данных: \nБлюдо - {str(data["name"])}\n'
        f'Ингриденты: {", ".join(data["ingredients"])}\n'
        f'Рецепт - {str(data["receipt"])}\n'
        f'На {str(data["time_of_meal"])[2:]}',
        reply_markup=confirmation_kb(message.from_user.id)
    )
    await state.set_state(Add_meal.confirmation)


@add_meal_router.message(Add_meal.confirmation)
async def process_time_of_meal(message: Message, state: FSMContext):
    confirmation = message.text
    table = ""
    await state.update_data(confirmation=confirmation)
    print(f"User {message.from_user.username}: {confirmation}")
    data = await state.get_data()
    if data['time_of_meal'] == "🍳 Завтрак":
        table = "breakfast"
    elif data['time_of_meal'] == "🍲 Обед":
        table = "lunch"
    elif data['time_of_meal'] == "🍽 Ужин":
        table = "dinner"
    if data['confirmation'] == "✅":
        await database.add_meal(table, data)
        await state.clear()
        await message.answer('блюдо успешно добавленно в базу данных!', reply_markup=main_menu(message.from_user.id))
    else:
        await state.clear()
        await message.answer('Повторите ввод', reply_markup=main_menu(message.from_user.id))
