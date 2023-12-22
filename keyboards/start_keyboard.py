from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def start_keyboard():
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text='Просмотр задач', callback_data='view_task'),
        InlineKeyboardButton(text='Добавить задачу', callback_data='add_task'),

    )
    return kb.as_markup()