from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def register():
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text='Регистрация', callback_data='register'),
        InlineKeyboardButton(text='Отмена', callback_data='cancel_register'),
    )
    return kb.as_markup()
