from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from bot_create import bot


ID = None


class FSMAdmin(StatesGroup):
    cls = State()
    name = State()
    photo = State()
    price = State()
    ingredients = State()


async def moder(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что желаете?')
    await message.delete()


async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.cls.set()
        await message.reply('Какую еду вы собираетесь добавить в меню?:')


async def load_cls(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['cls'] = message.text
        await FSMAdmin.next()
        await message.reply('Введите название продукта:')


async def load_name(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь загрузите фотографию:')


async def load_photo(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Введите цену:')


async def load_price(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = message.text
        await FSMAdmin.next()
        await message.reply('Введите ингридиенты:')


async def load_ingridients(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['ingridients'] = message.text

        await state.finish()
        await message.reply('Позиция успешно добавлена')


async def cancel_fsm(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Отменено')


def register_admin_handers(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands='Добавить', state=None)
    dp.register_message_handler(load_cls, state=FSMAdmin.cls)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(load_ingridients, state=FSMAdmin.ingredients)
    dp.register_message_handler(cancel_fsm, commands='отмена', state='*')
    dp.register_message_handler(cancel_fsm, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(moder, commands='mod')
    dp.register_message_handler(moder, Text(equals='mod', ignore_case=True))
