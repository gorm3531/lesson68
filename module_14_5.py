from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *


api = '7705832901:AAFlAOrIVady3Xcx3X9VWeIqm2U7EFVIsKg'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb = ReplyKeyboardMarkup(resize_keyboard=True)
but = KeyboardButton(text='Рассчитать')
but2 = KeyboardButton(text='Информация')
but3 = KeyboardButton(text='Купить')
but4 = KeyboardButton(text='Регистрация')
kb.add(but)
kb.add(but2)
kb.add(but3)
kb.add(but4)


ikb = InlineKeyboardMarkup()
inl = InlineKeyboardMarkup()
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button1 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
button2 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button3 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button4 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button5 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
ikb.add(button)
ikb.add(button1)
inl.add(button2)
inl.add(button3)
inl.add(button4)
inl.add(button5)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

@dp.message_handler(commands=['start'])
async def start_(message):
    await message.answer('Привет, я бот помогающий твоему здоровью', reply_markup=kb)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()



@dp.message_handler(text= 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=ikb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(age= message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    formula = (10*int(data['weight']) + 6.25*int(data['growth']) - 5*int(data['age']) + 5)
    await message.answer(f"Ваша норма каллорий: {formula}")
    await state.finish()


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    base = get_all_products()
    for number in base:
        await message.answer(f'Название:Продукт {number[1]} / Описание: описание {number[2]} / Цена: {number[3]}')
        with open(f'{number[0]}.jpg', 'rb') as file:
            await message.answer_photo(file)
    await message.answer("Выберите продукт для покупки:", reply_markup=inl)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит): ')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    await state.update_data(users_name=message.text)
    data = await state.get_data(['users_name'])
    if is_included(data['users_name']):
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()
    else:
        await state.update_data(users_name=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(users_email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(users_age=message.text)
    data1 = await state.get_data(['users_name', 'users_email', 'users_age'])
    add_user(data1['users_name'], data1['users_email'], data1['users_age'])
    connection.commit()
    await message.answer('Регистрация прошла успешно')
    await state.finish()


@dp.message_handler()
async def hi(message: types.Message):
    await message.answer('Привет! Хочешь узнать свою норму калорий? Тогда напиши /start')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)