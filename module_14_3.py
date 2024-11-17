import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

logging.basicConfig(level=logging.INFO)# настройка logov

api = '7707234672:AAF-oM2PH-ddxA2_kHagE_X3MucBrGCb8CE'
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

# В главную (обычную) клавиатуру меню добавьте кнопку "Купить".

kb_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Расчитать'),
            KeyboardButton(text='Информация')
        ],
        [
            KeyboardButton(text='Купить')
        ]
    ], resize_keyboard=True # активировать автоматическое изменение размера клавиатуры
)

kb_calculate = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
        [InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
    ]
)

#Создайте Inline меню из 4 кнопок с надписями
# "Product1", "Product2", "Product3", "Product4". У всех кнопок назначьте callback_data="product_buying"

kb_product = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Продукт 1', callback_data='product_buying'),
         InlineKeyboardButton(text='Продукт 2', callback_data='product_buying'),
         InlineKeyboardButton(text='Продукт 3', callback_data='product_buying'),
         InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
         ]
    ],resize_keyboard=True
)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


#Message хэндлер, который реагирует на текст "Купить" и оборачивает функцию get_buying_list(message).
#Функция get_buying_list должна выводить надписи
# 'Название: Product<number> | Описание: описание <number> | Цена: <number * 100>' 4 раза.
# После каждой надписи выводите картинки к продуктам.
# В конце выведите ранее созданное Inline меню с надписью "Выберите продукт для покупки:".

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    number = 1
    await message.answer(f'Название: Продукт {number} | Описание: описание {number} '
                                       f'| Цена: {number * 100}')
    with open('prod_1.jpg', 'rb') as img:
       await message.answer_photo(img)
    number += 1
    await message.answer(f'Название: Продукт {number} | Описание: описание {number} '
                         f'| Цена: {number * 100}')
    with open('prod_2.jpg', 'rb') as img:
        await message.answer_photo(img)
    number += 1
    await message.answer(f'Название: Продукт {number} | Описание: описание {number} '
                         f'| Цена: {number * 100}')
    with open('prod_3.jpg', 'rb') as img:
        await message.answer_photo(img)
    number += 1
    await message.answer(f'Название: Продукт {number} | Описание: описание {number} '
                         f'| Цена: {number * 100}')
    with open('prod_4.jpg', 'rb') as img:
        await message.answer_photo(img)
    await message.answer(f'Выберите продукт для покупки:',reply_markup=kb_product)


#Callback хэндлер, который реагирует на текст "product_buying"
# и оборачивает функцию send_confirm_message(call).
# Функция send_confirm_message, присылает сообщение "Вы успешно приобрели продукт!"

@dp.callback_query_handler(text='product_buying')
async def get_formulas(call):
    await call.message.answer('Вы успешно приобрели продукт!')

@dp.message_handler(commands='start')
async def start_message(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb_start)

@dp.message_handler(text='Расчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_calculate)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('BMR=10×масса тела (кг)+6,25×рост (см)−5×возраст (годы)+5')

@dp.message_handler(text = 'Информация')
async def info_message(message):
    await message.answer('Я бот, помогающий твоему здоровью!')

@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer(f"Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer(f"Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def set_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    bmr = int(data['weight']) * 10 + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f"Ваша норма калорий: {bmr}")
    await state.finish()

@dp.message_handler()
async def start_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)