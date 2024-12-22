from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton
import sqlite3

from aiogram.utils.keyboard import InlineKeyboardBuilder

from tasks_bot.database.db import DB_NAME

router = Router()

@router.message(Command('admin'))
async def admin_panel(message: Message):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT telegram_id FROM admin_id WHERE telegram_id = ?", (message.from_user.id,))
    is_admin = cursor.fetchone()
    conn.close()

    if is_admin:
        keyboard = InlineKeyboardBuilder()
        keyboard.row(InlineKeyboardButton(text="Добавить таск", callback_data="add_task"))

        await message.reply("Админ панель:", reply_markup=keyboard.as_markup())
    else:
        await message.reply("У вас нет доступа к админ панели.")