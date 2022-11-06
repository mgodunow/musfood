from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from bot_create import bot
from sqlite_db.sqlite_db import menu_add_position, read2, delete_command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboard.admin_kb import kb_admin, kb_admin_f_or_d, kb_admin_cancel

ID = None


class FSMAdmin(StatesGroup):
    tip = State()
    cls = State()
    name = State()
    photo = State()
    price = State()
    ingredients = State()


async def moderator(message: types.Message):
    global ID
    ID = message.from_user.id
    if message.from_user.id == ID:
        mod_kb = InlineKeyboardMarkup()
        mod_kb.add(InlineKeyboardButton('Удалить', callback_data='/Удалить'))
        await bot.send_message(message.from_user.id, 'Что желаете?', reply_markup=kb_admin)


async def cancel_fsm(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Отменено')


async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.tip.set()
        # Также здесь должна выпадать клавиатура
        await message.reply('Еду или напиток вы собираетесь добавить в меню?:', reply_markup=kb_admin_f_or_d)


async def load_tip(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['tip'] = message.text
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

        await menu_add_position(state)
        await state.finish()
        await message.reply('Позиция успешно добавлена')


async def del_callback_run(callback_query: types.CallbackQuery):
    await delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена', show_alert=True)


async def delete_food(message: types.Message):
    if message.from_user.id == ID:
        read = await read2()
        for rec in read:
            await bot.send_photo(message.from_user.id, rec[3], f'Тип:{rec[0]}\nКласс:{rec[1]}\nНазвание:{rec[2]}\n'
                                                               f'Цена:{rec[4]}\nИнгридиенты:{rec[5]}')
            await bot.send_message(message.from_user.id, text='***', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(f'Удалить {rec[2]}', callback_data=f'del {rec[2]}')
            ))


def register_admin_handers(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands='Добавить', state=None)
    dp.register_message_handler(cm_start, Text(equals='Добавить', ignore_case=True))
    dp.register_message_handler(cancel_fsm, commands='Отмена', state='*')
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_tip, state=FSMAdmin.tip)
    dp.register_message_handler(load_cls, state=FSMAdmin.cls)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(load_ingridients, state=FSMAdmin.ingredients)
    dp.register_message_handler(moderator, commands='mod')
    dp.register_message_handler(moderator, Text(equals='mod', ignore_case=True))
    dp.register_message_handler(moderator, Text(equals='Назад', ignore_case=True))
    dp.register_message_handler(delete_food, commands='Удалить')
    dp.register_message_handler(delete_food, Text(equals='Удалить', ignore_case=True))
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
