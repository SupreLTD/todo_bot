from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.db_client import db
from keyboards.register_keyboard import register
from keyboards.tasks_keyboard import TasksView, tasks_keyboard, edit_task, done_tasks_keyboard, start_keyboard, \
    access_del_done_task, to_home

router = Router()


class CreateTask(StatesGroup):
    description = State()
    task = State()


@router.callback_query(TasksView.filter())
async def task_list_view(call: CallbackQuery, callback_data: TasksView, state: FSMContext):
    if callback_data.action == 'tasks':
        tasks = await db.get_tasks(call.from_user.id)
        await call.message.answer('Выберите задачу', reply_markup=tasks_keyboard(tasks))
    elif callback_data.action == 'create_list':
        await call.message.answer('Введите заголовок задачи, не более 20 символов')
        await state.set_state(CreateTask.description)
    elif callback_data.action == 'task':
        task = await db.get_task(callback_data.value)
        await call.message.answer(task, reply_markup=edit_task(callback_data.value))
    elif callback_data.action == 'done':
        await db.done_task(callback_data.value)
        await call.answer('Задание выполнено!', show_alert=True)
        tasks = await db.get_tasks(call.from_user.id)
        await call.message.answer('Выберите задачу', reply_markup=tasks_keyboard(tasks))
    elif callback_data.action == 'home':
        await call.message.answer('Вы вернулись в главное меню', reply_markup=start_keyboard())
    elif callback_data.action == 'delete_task':
        await call.message.answer('Вы уверены?', reply_markup=access_del_done_task())
    elif callback_data.action == 'yes':
        await db.delete_done_task(call.from_user.id)
        await call.message.answer('Выполненные задачи удалены', reply_markup=start_keyboard())
    elif callback_data.action == 'no':
        tasks = await db.get_done_tasks(call.from_user.id)
        answer = '\n\n'.join([f'📍 {n}. {i.get("task")}' for n, i in enumerate(tasks)])
        await call.message.answer(answer, parse_mode='html', reply_markup=done_tasks_keyboard())
        # await call.message.answer('Действие отклонено', reply_markup=start_keyboard())


@router.message(CreateTask.description)
async def set_task(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Введите задачу')
    await state.set_state(CreateTask.task)


@router.message(CreateTask.task)
async def create_task(message: Message, state: FSMContext):
    fsm_data = await state.get_data()
    await db.create_task(fsm_data['description'], message.text, message.from_user.id)
    await message.answer('Задача успешно добавлена!',
                         reply_markup=tasks_keyboard(await db.get_tasks(message.from_user.id)))
    await state.clear()


@router.message(Command(commands=['done_tasks']))
async def view_done_tasks(message: Message):
    if not db.check_user(message.from_user.id):
        await message.delete()
        await message.answer('Пройдите регистрацию', reply_markup=register())
    else:
        tasks = await db.get_done_tasks(message.from_user.id)
        answer = '\n\n'.join(
            [f'📍 {n}. {i.get("task")}' for n, i in enumerate(tasks, start=1)]) if tasks else 'Выполненных заданий нет'
        await message.delete()
        builder = InlineKeyboardBuilder()
        builder.row(to_home)
        await message.answer(answer, parse_mode='html', reply_markup=done_tasks_keyboard()) \
            if tasks else await message.answer(answer, reply_markup=builder.as_markup())
