from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="➕ Добавить блюдо", callback_data="➕ Добавить блюдо")],
        [KeyboardButton(text="ℹ️ Help", callback_data="ℹ️ Help")],
        [KeyboardButton(text="Составить меню", callback_data="Составить меню")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard
