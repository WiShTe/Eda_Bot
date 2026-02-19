from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

# Reply Keyboard старотового меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Составить меню на неделю🍽"),
            KeyboardButton(text="ℹ️ Help"),
        ]
    ],
    resize_keyboard=True,
)