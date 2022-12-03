from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

# Клавиатура для start
button1 = KeyboardButton('Меню')
button2 = KeyboardButton('О нас')
button3 = KeyboardButton('Корзина')
button4 = KeyboardButton('Наши акции')

kb_client_start = ReplyKeyboardMarkup()
kb_client_start.add(button1).add(button2).add(button3).add(button4)

# Клавиатура для меню
menu_btn1 = KeyboardButton('Еда')
menu_btn2 = KeyboardButton('Напитки')

kb_client_menu = ReplyKeyboardMarkup()
kb_client_menu.row(menu_btn1, menu_btn2)

# Клавиатура для корзины
cart_kb = ReplyKeyboardMarkup()

cart_btn1 = KeyboardButton('Удалить из корзины ' + '\U00002716')
cart_btn2 = KeyboardButton('Оформить заказ ' + '\U0001F69B')
cart_btn3 = KeyboardButton('\U0001F3E0')

cart_kb.add(cart_btn1).add(cart_btn2).add(cart_btn3)
