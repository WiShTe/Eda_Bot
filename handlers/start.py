from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from keyboards.main_menu import main_menu

from db.database import database

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Обработчик команды /start"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name

    # Проверяем, есть ли пользователь в базе
    existing_user = await database.get_user(user_id)

    if existing_user:
        await message.answer(
            f"👋 С возвращением, {first_name}, составим меню?\n"
        )
    else:
        # Добавляем нового пользователя
        await database.add_user(user_id, username, first_name)
        await message.answer(
            f"🎉 Добро пожаловать, {first_name}!\n"
            f"Вы успешно зарегистрированы в системе.",
        reply_markup = main_menu(message.from_user.id))
