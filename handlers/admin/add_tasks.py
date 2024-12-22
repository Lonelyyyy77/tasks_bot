import sqlite3

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tasks_bot.database.db import DB_NAME
from tasks_bot.states.admin.add_task import AddTask

router = Router()


@router.callback_query(lambda c: c.data == 'add_task')
async def process_add_task(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введите название задачи")
    await state.set_state(AddTask.waiting_for_task_title)
    await callback_query.answer()  # Закрывает уведомление кнопки


@router.message(AddTask.waiting_for_task_title)
async def add_task_title(message: Message, state: FSMContext):
    title = message.text
    await state.update_data(title=title)

    await message.reply("Введите описание задачи:")
    await state.set_state(AddTask.waiting_for_task_description)


@router.message(AddTask.waiting_for_task_description)
async def add_task_description(message: Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)

    await message.reply("Введите цену задачи:")
    await state.set_state(AddTask.waiting_for_task_price)


@router.message(AddTask.waiting_for_task_price)
async def add_task_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
    except ValueError:
        await message.reply("Цена должна быть числом. Попробуйте снова.")
        return

    # Получение данных из состояния
    user_data = await state.get_data()
    title = user_data['title']
    description = user_data['description']

    # Сохранение задачи в базу данных
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description, price) VALUES (?, ?, ?)",
        (title, description, price)
    )
    conn.commit()
    conn.close()

    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Добавить еще', callback_data='add_task'))

    await state.clear()
    await message.reply("Задача успешно добавлена!", reply_markup=kb.as_markup())
