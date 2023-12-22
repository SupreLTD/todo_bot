from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from phonenumbers import parse, is_valid_number

from keyboards.start_keyboard import tasks_list
from keyboards.register_keyboard import register
from db_client import Database

router = Router()
db = Database()


class Register(StatesGroup):
    get_name = State()
    get_phone = State()


@router.message(Command(commands=['start']))
async def start(message: types.Message):
    if await db.check_user(message.from_user.id):
        await message.answer(f'Привет, {message.from_user.username}\nСписки задач: ', reply_markup=tasks_list(
            await db.get_tasks_list(message.from_user.id)
        ))
    else:
        await message.answer('Пройдите регистрацию', reply_markup=register())


@router.callback_query(F.data == 'register')
async def get_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите ваше имя')
    await call.message.delete()
    await state.set_state(Register.get_name)


@router.message(Register.get_name)
async def get_phone(message: types.Message, state: FSMContext):
    if len(message.text) > 0:
        await state.update_data(name=message.text)
        await message.answer('Введите ваш номер телефона в международном формате')
        await state.set_state(Register.get_phone)
    else:
        await message.answer('Введите корректные данные')
    await message.delete()


@router.message(Register.get_phone)
async def register_user(message: types.Message, state: FSMContext):
    try:
        if is_valid_number(parse(message.text, None)):
            fsm_data = await state.get_data()
            name = fsm_data['name']
            await db.register_user([message.from_user.id, name, message.text])
            await message.answer('Регистрация прошла успешно!', reply_markup=tasks_list(
                await db.get_tasks_list(message.from_user.id)))  # клавиатура логики
            await state.clear()
        else:
            await message.answer('Номер телефона не корректный!')
        await message.delete()
    except Exception as e:
        print(message.text)
        print(e)
        await message.answer('Номер телефона не корректный!')
        await message.delete()
