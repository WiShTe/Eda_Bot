from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def time_of_meal_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="🍳 Завтрак")],
        [KeyboardButton(text="🍲 Обед")],
        [KeyboardButton(text="🍽 Ужин")],

    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard