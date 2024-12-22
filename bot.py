import asyncio
import logging

from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.user.view_tasks import router as user_router
from handlers.admin.admin_panel import router as admin_panel_router
from handlers.admin.add_tasks import router as admin_add_tasks_router

from tasks_bot.database.admin.admin import add_admin
from tasks_bot.database.db import create_tables

TOKEN = "7772152147:AAHmceBDqzK8iaAw0eaq_gOAOFjlfklhhyY"
router = Router()

logging.basicConfig(level=logging.INFO)

@router.message(CommandStart())
async def start_handler(message: Message):
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='Посмотреть', callback_data='tasks'))

    await message.answer("Чтобы посмотреть таски нажми на кнопку ниже:", reply_markup=kb.as_markup())


async def main():
    # add_admin(6588562022)
    # add_admin(1001605513)

    create_tables()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(router)
    dp.include_router(user_router)
    dp.include_router(admin_panel_router)
    dp.include_router(admin_add_tasks_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
