from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_finish_ingredients_kb():
    kb = [[InlineKeyboardButton(text="✅ ЗАВЕРШИТЬ ВВОД", callback_data="finish_ingredients")]]
    return InlineKeyboardMarkup(inline_keyboard=kb)
