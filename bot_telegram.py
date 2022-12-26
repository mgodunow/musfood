from aiogram.utils import executor
import config
from bot_create import dp, bot
from handlers import client, admin
from sqlite_db import sqlite_db
import os


async def on_startup(dp):
    sqlite_db.sql_start()
    await bot.set_webhook(config.URL_APP)


async def on_shutdown(dp):
   await bot.delete_webhook()

admin.register_admin_handers(dp)
client.register_client_handers(dp)

executor.start_webhook(
    dispatcher=dp,
    webhook_path='',
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    skip_updates=True,
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 5000))
)
