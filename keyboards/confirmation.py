from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def confirmation_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="✅")],
        [KeyboardButton(text="❌")],

    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard