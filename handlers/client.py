from aiogram import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from aiogram.types.message import ContentType
from keyboard.client_kb import kb_client_start, kb_client_menu, cart_kb
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from sqlite_db.sqlite_db import *
from bot_create import bot
import os


async def start(message: types.Message):
    await message.reply('Здравствуйте! Хотите что-нибудь заказать?', reply_markup=kb_client_start)


async def about(message: types.Message):
    await message.reply('Открыты с 2004 года\n241870 гостей уже попробовали нашу еду'
                        '\n78000 пицц приготовлено в 2021 году'
                        '\nДоставим бесплатно от 2.5 тысяч рублей! Среднее время доставки 26 минут', reply_markup=
                        ReplyKeyboardMarkup().add(KeyboardButton('\U0001F3E0')))


async def menu(message: types.Message):
    await message.reply('Что желаете заказать?', reply_markup=kb_client_menu)


async def sale_list(message: types.Message):
    sales = await read_sale()
    for sale in sales:
        await bot.send_photo(message.from_user.id, sale[0], f'{sale[1]}\n{sale[2]}')
    await bot.send_message(message.from_user.id, 'Наши действующие акции', reply_markup=ReplyKeyboardMarkup().
                           add(KeyboardButton('\U0001F3E0')))


class FSMmenu(StatesGroup):
    tip = State()
    cls = State()


async def start_menu(message: types.Message):
    await FSMmenu.tip.set()
    await message.reply('Еда или напитки?', reply_markup=ReplyKeyboardMarkup().add(KeyboardButton('Еда'))
                        .add(KeyboardButton('Напитки')).add(KeyboardButton('\U0001F3E0')))


async def main(message: types.Message):
    await message.reply('Вы на главной', reply_markup=kb_client_start)


async def load_tip(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tip'] = message.text
    cls_list = []
    if data['tip'] == '\U0001F3E0':
        await message.reply('Вы на главной', reply_markup=kb_client_start)
        await state.finish()
        return
    elif data['tip'] == 'Еда':
        cls_list = await read_menu_class()
    elif data['tip'] == 'Напитки':
        cls_list = await read_drinks_class()
    elif data['tip'].lower() == 'отмена':
        await state.finish()
        return
    else:
        await message.reply('Неправильный тип позиций')
        await state.finish()
        return
    classes = ReplyKeyboardMarkup()
    for cls in cls_list:
        button = KeyboardButton(cls[0])
        classes.row(button)
    await message.reply('Выберите что-нибудь :)', reply_markup=classes.add('\U0001F3E0'))
    await FSMmenu.next()


async def load_cls(message: types.Message, state: FSMContext):
    cls = message.text
    read = []
    async with state.proxy() as data:
        data['cls'] = message.text
        if data['cls'] == '\U0001F3E0':
            await state.finish()
            await message.reply('Вы на главной', reply_markup=kb_client_start)
        if data['tip'] == 'Еда':
            read = await read_menu_list(data['cls'])
        if data['tip'] == 'Напитки':
            read = await read_drinks_list(data['cls'])
    for rec in read:
        await bot.send_photo(message.from_user.id, rec[3], f'{rec[0]}\n{rec[1]}\n{rec[2]}\n'
                                                           f'Цена:{rec[4]}\nИнгридиенты:{rec[5]}')
        await bot.send_message(message.from_user.id, text='***', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(f'В корзину {rec[2]}', callback_data=f'in_cart {rec[2]}_{rec[4]}')
        ))
    await state.finish()


async def add_pos_to_cart(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    productnprice = callback_query.data.replace('in_cart ', '').split('_')
    await to_cart(user_id, productnprice[0], productnprice[1])
    await callback_query.answer(
        text=f'{callback_query.data.replace("in_cart", "").split("_")[0]} : добавлено в корзину')


async def cart(message: types.Message):
    products = await select_cart(message.from_user.id)
    cart = ''
    price = 0
    for product in products:
        cart += str(product[0] + f' {product[1]}' + '\n')
        price += int(product[1])
    if not cart:
        await message.reply('Ваша корзина пуста')
        return
    if price >= 2500:
        await bot.send_message(message.from_user.id, f'{cart}\nИтого:{price}', reply_markup=cart_kb)
    else:
        await bot.send_message(message.from_user.id, f'{cart}\nИтого с доставкой :{price + 500}', reply_markup=cart_kb)


class FSMcart(StatesGroup):
    products = State()
    del_product = State()


async def del_cart(message: types.Message):
    await FSMcart.products.set()
    products = await select_cart(message.from_user.id)
    kb_del_cart = ReplyKeyboardMarkup()
    for product in products:
        kb_del_cart_button = KeyboardButton(str(product[0]))
        kb_del_cart.row(kb_del_cart_button)
    await bot.send_message(message.from_user.id, 'Что хотите удалить?', reply_markup=kb_del_cart)
    await FSMcart.next()


async def del_product_cart(message: types.Message, state: FSMContext):
    await delete_user_cart(str(message.from_user.id), message.text)
    await bot.send_message(message.from_user.id, 'Позиция удалена', reply_markup=ReplyKeyboardMarkup().add(
        KeyboardButton('Корзина')
    ))
    await state.finish()


# class Buy(StatesGroup):
#     address = State()
#
#
# async def buy(message: types.Message):
#     await Buy.address.set()
#     await bot.send_message('Введите адрес доставки')
#
#
# async def load_address(message: types.Message, state: FSMContext):
#

async def process_buy(message: types.Message):
    payment_token = os.getenv('PAYMENT_TOKEN')
    products = await select_cart(message.from_user.id)
    if not products:
        await message.reply('Вы ничего не выбрали')
        return
    prices = []
    total_price = 0
    for product in products:
        total_price += int(product[1])
        price = types.LabeledPrice(label=product[0], amount=int(product[1]) * 100)
        prices.append(price)
    if total_price < 2500:
        prices.append(types.LabeledPrice(label='Доставка', amount=500 * 100))
    if payment_token.split(':')[1] == 'TEST':
        await bot.send_message(message.from_user.id, 'Платеж является тестовым.')
    await bot.send_invoice(
        message.from_user.id,
        title='Оплата заказа',
        description='Оплата доставки и заказа',
        provider_token=payment_token,
        currency='rub',
        need_shipping_address=True,
        prices=prices,
        payload='test-invoice-payload',
        is_flexible=False,
    )


async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


async def successful_payment(message: types.Message):
    await delete_cart(message.from_user.id)
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f'{k} {v}')

    await bot.send_message(message.from_user.id, f'Платеж на сумму {message.successful_payment.total_amount // 100}'
                                                 f'{message.successful_payment.currency} успешно прошел')


async def command_handler(message: types.Message):
    await message.reply('Такой команды нет ' + '\U0001f60C')


def register_client_handers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(about, commands=['О нас'])
    dp.register_message_handler(about, Text(equals='О нас', ignore_case=True))
    dp.register_message_handler(sale_list, commands='Наши акции')
    dp.register_message_handler(sale_list, Text(equals='Наши акции', ignore_case=True))
    dp.register_message_handler(start_menu, commands='Меню')
    dp.register_message_handler(start_menu, Text(equals='Меню', ignore_case=True), state=None)
    dp.register_message_handler(load_tip, state=FSMmenu.tip)
    dp.register_message_handler(load_cls, state=FSMmenu.cls)
    dp.register_message_handler(cart, commands=['Корзина'])
    dp.register_message_handler(cart, Text(equals='Корзина', ignore_case=True))
    dp.register_callback_query_handler(add_pos_to_cart, lambda x: x.data and x.data.startswith('in_cart'))
    dp.register_message_handler(del_cart, commands=['Удалить из корзины' + '\U00002716'], state=None)
    dp.register_message_handler(del_cart, Text(equals='Удалить из корзины ' + '\U00002716', ignore_case=True))
    dp.register_message_handler(del_product_cart, state=FSMcart.del_product)
    dp.register_message_handler(main, commands='\U0001F3E0')
    dp.register_message_handler(main, Text(equals='\U0001F3E0', ignore_case=True))
    dp.register_message_handler(process_buy, commands=['Оформить зака ' + '\U0001F69B'])
    dp.register_message_handler(process_buy, Text(equals='Оформить заказ ' + '\U0001F69B', ignore_case=True))
    dp.register_pre_checkout_query_handler(pre_checkout_query, lambda query: True)
    dp.register_message_handler(successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)
    dp.register_message_handler(command_handler, commands=None)
