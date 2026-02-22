from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from states import Add_meal


add_meal_router = Router()


@add_meal_router.message(Command("add_meal"))
@add_meal_router.message(F.text == "➕ Добавить блюдо")
async def cmd_help(message: Message, state: FSMContext) -> None:
    await state.set_state(Add_meal.name) #устанавливаю состояние ввода имени блюда
    await message.answer(
        "Введите название блюда"
    )

#Добавление названия блюда в бд
@add_meal_router.message(Add_meal.name) #если установлено состояние Add_meal.name
async def process_meal_name(message: Message, state: FSMContext): #создаём функцию с аргументами(сообщение, State)
    meal_name = message.text #получаем название блюда

    await state.update_data(name=meal_name) #сохраняем данные в FSM

    print(f"User {message.from_user.username}: {meal_name}") #вывод в консоль для отладки

    # Проверка сохраненных данных (получаем весь словарь)
    data = await state.get_data() #получаем словарь
    print(f"Data in state: {data}") # выводим данные для отладки

    await state.set_state(Add_meal.inrdients) #устанавливаем состояние ввода ингридиентов

    await message.answer(
        "Введите название ингридиента"
    )

#Добавление ингридиентов  в бд по аналогии с именем(@add_meal_router.message(Add_meal.name)
@add_meal_router.message(Add_meal.inrdients)
async def process_meal_inrdents(message: Message, state: FSMContext):
    inridient_name = message.text

    await state.update_data(inridient_name=inridient_name)

    print(f"User {message.from_user.username}: {inridient_name}")

    data = await state.get_data()
    print(f"Data in state: {data}")

    await state.set_state(Add_meal.reciept)

    await message.answer(
        "Введите Рецепт"
    )

#Добавление рецепта блюда в бд по аналогии с именем(@add_meal_router.message(Add_meal.name)
@add_meal_router.message(Add_meal.reciept)
async def process_meal_reciept(message: Message, state: FSMContext):
    reciept = message.text

    await state.update_data(reciept=reciept)

    print(f"User {message.from_user.username}: {reciept}")

    data = await state.get_data()
    print(f"Data in state: {data}")

    await state.set_state(Add_meal.time_of_meal)

    await message.answer(
        "Введите завтрак/обед/ужин?"
    )

@add_meal_router.message(Add_meal.time_of_meal)
async def process_time_of_meal(message: Message, state: FSMContext):
    time_of_meal = message.text

    await state.update_data(time_of_meal=time_of_meal)

    print(f"User {message.from_user.username}: {time_of_meal}")

    data = await state.get_data()
    print(f"Data in state: {data}")

    await message.answer(
        F'Вы ввели {data}'
    )