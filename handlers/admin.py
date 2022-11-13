from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from bot_create import bot
from sqlite_db.sqlite_db import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from keyboard.admin_kb import kb_admin, kb_admin_f_or_d, kb_admin_cancel

ID = None


# Проверка на администратора
async def moderator(message: types.Message):
    global ID
    ID = message.from_user.id
    if message.from_user.id == ID:
        await bot.send_message(message.from_user.id, 'Что желаете? Добавить - добавление еды и напитков\n'
                                                     'Акции - удаление и добавление акций', reply_markup=kb_admin)


# Отмена машины состояний
async def cancel_fsm(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Отменено')


# Машина состояний для акций
class FSMAdminSale(StatesGroup):
    photo = State()
    name = State()
    description = State()


async def sale_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdminSale.photo.set()
        await message.reply('Отправьте картинку для акции')


async def load_sale_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdminSale.next()
        await message.reply('Введите название для акции')


async def load_sale_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdminSale.next()
        await message.reply('Введите описание акции')


async def load_sale_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['desc'] = message.text
        await sale_add_position(state)
        await state.finish()
        await message.reply('Акция успешно добавлена')


# Машина состояний для напитков и еды
class FSMAdmin(StatesGroup):
    tip = State()
    cls = State()
    name = State()
    photo = State()
    price = State()
    ingredients = State()


async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.tip.set()
        # Также здесь должна выпадать клавиатура
        await message.reply('Еду или напиток вы собираетесь добавить в меню?:', reply_markup=kb_admin_f_or_d)


async def load_type(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['type'] = message.text
        await FSMAdmin.next()
        await message.reply('Введите класс продукта, который хотите добавить (например: пицца)',
                            reply_markup=kb_admin_cancel)


async def load_cls(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['cls'] = message.text
        await FSMAdmin.next()
        await message.reply('Введите название продукта:', reply_markup=kb_admin_cancel)


async def load_name(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь загрузите фотографию:', reply_markup=kb_admin_cancel)


async def load_photo(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Введите цену:', reply_markup=kb_admin_cancel)


async def load_price(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = message.text
        await FSMAdmin.next()
        await message.reply('Введите ингридиенты:', reply_markup=kb_admin_cancel)


async def load_ingridients(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['ingridients'] = message.text
        if data['type'] != 'Еда' and data['type'] != 'Напиток':
            await message.reply('Неправильный тип позиции')
        elif data['type'] == 'Напиток':
            await drinks_add_position(state)
            await message.reply('Позиция успешно добавлена')
        else:
            await menu_add_position(state)
            await message.reply('Позиция успешно добавлена')
        await state.finish()


async def del_callback_run_menu(callback_query: types.CallbackQuery):
    await delete_command_menu(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена', show_alert=True)


async def delete_food(message: types.Message):
    if message.from_user.id == ID:
        read = await read_menu()
        for rec in read:
            await bot.send_photo(message.from_user.id, rec[3], f'Тип:{rec[0]}\nКласс:{rec[1]}\nНазвание:{rec[2]}\n'
                                                               f'Цена:{rec[4]}\nИнгридиенты:{rec[5]}')
            await bot.send_message(message.from_user.id, text='***', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(f'Удалить {rec[2]}', callback_data=f'del {rec[2]}')
            ))


async def del_callback_run_drinks(callback_query: types.CallbackQuery):
    await delete_command_drinks(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена', show_alert=True)


async def delete_drinks(message: types.Message):
    if message.from_user.id == ID:
        read = await read_drinks()
        for rec in read:
            await bot.send_photo(message.from_user.id, rec[3], f'Тип:{rec[0]}\nКласс:{rec[1]}\nНазвание:{rec[2]}\n'
                                                               f'Цена:{rec[4]}\nИнгридиенты:{rec[5]}')
            await bot.send_message(message.from_user.id, text='***', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(f'Удалить {rec[2]}', callback_data=f'del {rec[2]}')
            ))


# Отображаем акции с кнопками удаления под каждой
async def del_callback_run_sale(callback_query: types.CallbackQuery):
    await delete_command_sale(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена', show_alert=True)


async def sale_list(message: types.Message):
    if message.from_user.id == ID:
        read = await read_sale()
        for rec in read:
            await bot.send_photo(message.from_user.id, rec[0], f'Название:{rec[1]}\nОписание:{rec[2]}')
            await bot.send_message(message.from_user.id, text='***', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(f'Удалить {rec[1]}', callback_data=f'del {rec[1]}')
            ))
        await message.reply('Хотите добавить акцию?',
                            reply_markup=ReplyKeyboardMarkup().add(KeyboardButton('Добавить акцию')))


def register_admin_handers(dp: Dispatcher):
    dp.register_message_handler(moderator, commands='mod')
    dp.register_message_handler(moderator, Text(equals='mod', ignore_case=True))
    dp.register_message_handler(cancel_fsm, commands='Отмена', state='*')
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена', ignore_case=True), state='*')
    dp.register_message_handler(sale_start, commands='Добавить акцию')
    dp.register_message_handler(sale_start, Text(equals='Добавить акцию', ignore_case=True))
    dp.register_message_handler(load_sale_photo, content_types=['photo'], state=FSMAdminSale.photo)
    dp.register_message_handler(load_sale_name, state=FSMAdminSale.name)
    dp.register_message_handler(load_sale_description, state=FSMAdminSale.description)
    dp.register_message_handler(cm_start, commands='Добавить', state=None)
    dp.register_message_handler(cm_start, Text(equals='Добавить', ignore_case=True))
    dp.register_message_handler(load_type, state=FSMAdmin.tip)
    dp.register_message_handler(load_cls, state=FSMAdmin.cls)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(load_ingridients, state=FSMAdmin.ingredients)
    dp.register_callback_query_handler(del_callback_run_drinks, lambda x: x.data and x.data.startswith('del '))
    dp.register_callback_query_handler(del_callback_run_menu, lambda x: x.data and x.data.startswith('del '))
    dp.register_callback_query_handler(del_callback_run_sale, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(delete_food, commands='Еда')
    dp.register_message_handler(delete_food, Text(equals='Еда', ignore_case=True))
    dp.register_message_handler(delete_drinks, commands='Напитки')
    dp.register_message_handler(delete_drinks, Text(equals='Напитки', ignore_case=True))
    dp.register_message_handler(sale_list, commands='Акции')
    dp.register_message_handler(sale_list, Text(equals='Акции', ignore_case=True))
