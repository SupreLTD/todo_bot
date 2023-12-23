from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.db_client import db
from keyboards.tasks_keyboard import TasksView, tasks_keyboard

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
        await call.message.answer(task)


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
