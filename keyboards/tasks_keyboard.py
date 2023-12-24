from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class TasksView(CallbackData, prefix='tasks'):
    action: str
    value: Optional[int] = None


add_task = InlineKeyboardButton(text='Добавить задачу',
                                callback_data=TasksView(action='create_list', value=0).pack())


def tasks_keyboard(data: list):
    kb = InlineKeyboardBuilder()
    [kb.button(text=i[1], callback_data=TasksView(action='task', value=i[0])) for i in data]
    kb.adjust(2)
    kb.row(add_task)

    return kb.as_markup()


def start_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text='Посмотреть список задач', callback_data=TasksView(action='tasks'))
    kb.row(add_task)

    return kb.as_markup()


def edit_task(task_id: int):
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='Задача выполнена', callback_data=TasksView(action='done', value=task_id).pack()),
           InlineKeyboardButton

           )
