from aiogram import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from keyboard.client_kb import kb_client_start, kb_client_menu
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from sqlite_db.sqlite_db import *
from bot_create import bot


async def start(message: types.Message):
    await message.reply('Здравствуйте! Хотите что-нибудь заказать?', reply_markup=kb_client_start)


async def delivery(message: types.Message):
    await message.reply('Доставим бесплатно от 2.5 тысяч рублей! Среднее время доставки 26 минут')


async def about(message: types.Message):
    await message.reply('Открыты с 2004 года\n241870 гостей уже попробовали нашу еду'
                        '\n78000 пицц приготовлено в 2021 году')


async def menu(message: types.Message):
    await message.reply('Что желаете заказать?', reply_markup=kb_client_menu)


async def sale_list(message: types.Message):
    sales = await read_sale()
    for sale in sales:
        await bot.send_photo(message.from_user.id, sale[0], f'{sale[1]}\n{sale[2]}')


class FSMmenu(StatesGroup):
    tip = State()
    cls = State()


async def start_menu(message: types.Message):
    await FSMmenu.tip.set()
    await message.reply('Еда или напитки?', reply_markup=ReplyKeyboardMarkup().add(KeyboardButton('Еда'))
                        .add(KeyboardButton('Напитки')))


async def load_tip(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tip'] = message.text
    cls_list = []
    if data['tip'] == 'Еда':
        cls_list = await read_menu_class()
    elif data['tip'] == 'Напитки':
        cls_list =  await read_drinks_class()
    else:
        await message.reply('Неправильный тип позиций')
        await state.finish()
    classes = ReplyKeyboardMarkup()
    for cls in cls_list:
        button = KeyboardButton(cls[0])
        classes.row(button)
    await message.reply('Выберите что0-нибудь :)', reply_markup=classes)
    await FSMmenu.next()


async def load_cls(message: types.Message, state: FSMContext):
    cls = message.text
    read = []
    async with state.proxy() as data:
        data['cls'] = message.text
        if data['tip'] == 'Еда':
            read = await read_menu_list(data['cls'])
        elif data['tip'] == 'Напиток':
            read = await read_drinks_list(data['cls'])
    for rec in read:
        await bot.send_photo(message.from_user.id, rec[3], f'{rec[0]}\n{rec[1]}\n{rec[2]}\n'
                                                           f'Цена:{rec[4]}\nИнгридиенты:{rec[5]}')
        await bot.send_message(message.from_user.id, text='***', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(f'В корзину {rec[2]}', callback_data=f'in_basket {rec[2]}')
        ))
    await state.finish()


def register_client_handers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(delivery, commands=['Доставка'])
    dp.register_message_handler(delivery, Text(equals='Доставка', ignore_case=True))
    dp.register_message_handler(about, commands=['О нас'])
    dp.register_message_handler(about, Text(equals='О нас', ignore_case=True))
    dp.register_message_handler(sale_list, commands='Наши акции')
    dp.register_message_handler(sale_list, Text(equals='Наши акции', ignore_case=True))
    dp.register_message_handler(start_menu, commands='Меню')
    dp.register_message_handler(start_menu, Text(equals='Меню', ignore_case=True), state=None)
    dp.register_message_handler(load_tip, state=FSMmenu.tip)
    dp.register_message_handler(load_cls, state=FSMmenu.cls)