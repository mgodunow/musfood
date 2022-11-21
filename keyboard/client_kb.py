from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

# Клавиатура для start
button1 = KeyboardButton('Меню')
button2 = KeyboardButton('О нас')
button3 = KeyboardButton('Доставка')
button4 = KeyboardButton('Наши акции')

kb_client_start = ReplyKeyboardMarkup()
kb_client_start.add(button1).add(button2).add(button3).row(button4)

# Клавиатура для меню
menu_btn1 = KeyboardButton('Еда')
menu_btn2 = KeyboardButton('Напитки')

kb_client_menu = ReplyKeyboardMarkup()
kb_client_menu.row(menu_btn1, menu_btn2)