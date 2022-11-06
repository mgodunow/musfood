from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

button1 = KeyboardButton('Добавить')
button2 = KeyboardButton('Удалить')

kb_admin = ReplyKeyboardMarkup()
kb_admin.row(button1).row(button2)

# Для хендлера выбора типа товара
kb_admin_f_or_d = ReplyKeyboardMarkup()
b1 = KeyboardButton('Еда')
b2 = KeyboardButton('Напиток')
b3 = KeyboardButton('По акции')
b4 = KeyboardButton('Отмена')

kb_admin_f_or_d.row(b1, b2, b3, b4)

# Кнопка отмены
kb_admin_cancel = ReplyKeyboardMarkup()
b = KeyboardButton('Отмена')
kb_admin_cancel.add(b)
