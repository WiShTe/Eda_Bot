from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message


help_router = Router()


@help_router.message(Command("help"))
@help_router.message(F.text == "ℹ️ Help")
async def cmd_help(message: Message) -> None:
    """Reply with a help message."""
    await message.answer(
        "Этот бот отравит вам меню на 7 дней, список покупок + рецепты: 21 блюдо, фрукты, овощи, вкусности к чаю."
        "\n \nОтправьте <em>/start</em> для начала работы"
    )