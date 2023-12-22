from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class TasksList(CallbackData, prefix='tasks_list'):
    action: str
    value: int


def tasks_list(data: list):
    kb = InlineKeyboardBuilder()
    [kb.button(text=i[1], callback_data=TasksList(action='tasks_list', value=i[0])) for i in data]
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text='Добавить список задач',
                                callback_data=TasksList(action='create_list', value=0).pack()),
           InlineKeyboardButton(text='Удалить список задач',
                                callback_data=TasksList(action='delete_list', value=0).pack())
           )

    return kb.as_markup()


def start_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text='Посмотреть список задач', callback_data='view_tasks')
    kb.button(text='Добавить задачу', callback_data='add_task')

    return kb.as_markup()
