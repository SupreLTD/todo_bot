from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class TasksView(CallbackData, prefix='tasks'):
    action: str
    value: Optional[int] = None


add_task = InlineKeyboardButton(text='✍️ Добавить задачу',
                                callback_data=TasksView(action='create_list', value=0).pack())
view_tasks = InlineKeyboardButton(text='📜 Посмотреть список задач', callback_data=TasksView(action='tasks').pack())
to_home = InlineKeyboardButton(text='🗄 Вернуться в главное меню', callback_data=TasksView(action='home').pack())

def tasks_keyboard(data: list):
    kb = InlineKeyboardBuilder()
    [kb.button(text='📝 '+i[1], callback_data=TasksView(action='task', value=i[0])) for i in data]
    kb.adjust(2)
    kb.row(add_task)

    return kb.as_markup()


def done_tasks_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text='⭕️ Удалить выполненные задания', callback_data=TasksView(action='delete_task'))
    kb.row(to_home)
    return kb.as_markup()


def start_keyboard():
    kb = InlineKeyboardBuilder()
    kb.row(view_tasks)
    kb.row(add_task)

    return kb.as_markup()


def edit_task(task_id: int):
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='✅ Задача выполнена', callback_data=TasksView(action='done', value=task_id).pack()))
    kb.row(view_tasks)
    return kb.as_markup()


def access_del_done_task():
    kb = InlineKeyboardBuilder()
    kb.button(text='✅ Да', callback_data=TasksView(action='yes'))
    kb.button(text='❌ Нет', callback_data=TasksView(action='no'))
    return kb.as_markup()
