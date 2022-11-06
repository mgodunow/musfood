from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

button1 = KeyboardButton('Меню')
button2 = KeyboardButton('О нас')
button3 = KeyboardButton('Доставка')

kb_client = ReplyKeyboardMarkup()
kb_client.add(button1).add(button2).add(button3)