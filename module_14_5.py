from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import crud_functions as crud

db = crud.get_all_products()

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True,
                         keyboard=[
                             [KeyboardButton('🖨 Рассчитать'),
                              KeyboardButton('🖥 Информация')
                              ],
                             [KeyboardButton('💰 Купить')],
                             [KeyboardButton('📃 Регистрация')]
                         ])

kb1 = InlineKeyboardMarkup()
but = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
but2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formula')
kb1.add(but, but2)

kb2 = InlineKeyboardMarkup()
but = InlineKeyboardButton(text='Product1', callback_data='product_buying')
but2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
but3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
but4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kb2.add(but, but2, but3, but4)

pics = {1: 'https://disk.yandex.ru/i/52iZOXbJHqKLJQ',
        2: 'https://disk.yandex.ru/i/a2P-2NZ_zDLgFw',
        3: 'https://disk.yandex.ru/i/wz21c8qk1IMFqA',
        4: 'https://disk.yandex.ru/i/bPI8Tjptg4swgA'
        }


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start_command(message):
    await message.answer(f'Напишите фразу "Рассчитать" для начала расчета нормы калорий.',
                         reply_markup=kb)


@dp.message_handler(text='🖨 Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb1)


@dp.callback_query_handler(text='formula')
async def get_formulas(call):
    await call.message.answer(f'Ддля мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                              f'\nДля женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()


@dp.message_handler(text='🖥 Информация')
async def info(message):
    await message.answer('Программа для расчета нормы калорий')


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(text='💰 Купить')
async def get_buying_list(message):
    for product in db:
        name = product[1]
        description = product[2]
        price = product[3]
        await message.answer(f'Название: {name} | '
                             f'Описание: {description} | '
                             f'Цена: {price}')

        await message.answer_photo(photo=pics[product[0]])
    await message.answer(f'Выберите продукт для покупки:', reply_markup=kb2)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(f'Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    msj = 10 * weight + 6.25 * growth - 5 * age + 5
    msjm = msj + 5
    msjw = msj - 161
    await message.answer(f'Ваша норма для мужчин: {msjm} ккал в день. '
                         f'\nВаша норма для женщин: {msjw} ккал в день.')
    await state.finish()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(text='📃 Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if not crud.is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя.')
        return


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    username = data['username']
    email = data['email']
    age = data['age']
    crud.add_user(username, email, age)
    await message.answer('Вы успешно зарегистрированы!')
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer(f'Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
