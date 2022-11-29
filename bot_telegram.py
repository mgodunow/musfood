from aiogram.utils import executor
from bot_create import dp
from handlers import client, admin
from sqlite_db import sqlite_db


async def on_startup(_):
    print('Bot is online')
    sqlite_db.sql_start()

admin.register_admin_handers(dp)
client.register_client_handers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
