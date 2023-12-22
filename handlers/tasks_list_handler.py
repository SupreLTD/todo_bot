from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from db_client import Database
from keyboards.start_keyboard import TasksList, tasks_list

db = Database()
router = Router()


class CreateTask(StatesGroup):
    name = State()


@router.callback_query(TasksList.filter())
async def task_list_view(call: CallbackQuery, callback_data: TasksList, state: FSMContext):
    if callback_data.action == 'tasks_list':
        tasks = await db.get_tasks(callback_data.value)
        answer = ...
        await call.message.answer(str(tasks))
    elif callback_data.action == 'create_list':
        await call.message.answer('Введите название списка, не более 20 символов')
        await state.set_state(CreateTask.name)


@router.message(CreateTask.name)
async def create_tasks_list(message: Message, state: FSMContext):
    if len(message.text) <= 20:
        await db.create_tasks_list(message.text, message.from_user.id)
        await message.answer('Задача добавлена!', reply_markup=tasks_list(
            await db.get_tasks_list(message.from_user.id)))
        await state.clear()
    else:
        await message.answer("Вы привысили длину!!")


