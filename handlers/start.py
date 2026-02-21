from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from keyboards.main_menu import main_menu

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Обработка команды start"""
    await message.answer(
        "Привет, составим меню?",
        reply_markup=main_menu(message.from_user.id),
    )