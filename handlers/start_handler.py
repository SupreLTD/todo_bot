from aiogram import Router, types
from aiogram.filters.command import CommandStart


router = Router()

@router.message(CommandStart)
async def start(message: types.Message):
    await message.answer(f'Hello, {message.from_user.username}')