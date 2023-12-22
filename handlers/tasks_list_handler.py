from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from db_client import Database
from keyboards.start_keyboard import TasksList

db = Database()
router = Router()


@router.callback_query(TasksList.filter())
async def task_list_view(call: CallbackQuery, callback_data: TasksList):
    tasks = await db.get_tasks(callback_data.value)
    await call.message.answer(str(tasks))
