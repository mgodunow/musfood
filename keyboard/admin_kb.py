from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button1 = KeyboardButton('Добавить')
button2 = KeyboardButton('Еда')
button3 = KeyboardButton('Напитки')
button4 = KeyboardButton('Акции')

kb_admin = ReplyKeyboardMarkup()
kb_admin.row(button1, button2, button3, button4)

# Для хендлера выбора типа товара
kb_admin_f_or_d = ReplyKeyboardMarkup()
b1 = KeyboardButton('Еда')
b2 = KeyboardButton('Напиток')

kb_admin_f_or_d.row(b1, b2)

# Кнопка отмены
kb_admin_cancel = ReplyKeyboardMarkup()
b = KeyboardButton('Отмена')
kb_admin_cancel.add(b)
