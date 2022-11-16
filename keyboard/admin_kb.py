from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button1 = KeyboardButton('Еда')
button2 = KeyboardButton('Напитки')
button3 = KeyboardButton('Акции')

kb_admin = ReplyKeyboardMarkup()
kb_admin.row(button1, button2, button3)

# Кнопка отмены
kb_admin_cancel = ReplyKeyboardMarkup()
b = KeyboardButton('Отмена')
kb_admin_cancel.add(b)
