import sqlite3

from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tasks_bot.database.db import DB_NAME

router = Router()


@router.callback_query(lambda c: c.data == 'tasks')
async def show_tasks(callback_query: CallbackQuery):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Получаем все задачи
    cursor.execute("SELECT id, title, description, price, status FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()
    conn.close()

    if tasks:
        # Формируем текст всех задач
        tasks_text = "<b>Список задач:</b>\n\n"
        keyboard = InlineKeyboardBuilder()

        for task in tasks:
            task_id, title, description, price, status = task

            status_text = "✅ выполнено" if status == "выполнено" else "❌ не выполнено"

            tasks_text += (
                f"🆔 <b>ID:</b> {task_id}\n"
                f"📌 <b>Название:</b> {title}\n"
                f"📝 <b>Описание:</b> {description}\n"
                f"💰 <b>Цена:</b> {price} гривен\n"
                f"📋 <b>Статус:</b> {status_text}\n\n"
            )

            # Добавляем кнопку для изменения статуса каждой задачи
            keyboard.row(
                InlineKeyboardButton(
                    text=f"Отметить {task_id} как выполненную",
                    callback_data=f"complete_{task_id}"
                )
            )

        # Отправляем одно сообщение с кнопками
        await callback_query.message.answer(
            tasks_text,
            reply_markup=keyboard.as_markup(),
            parse_mode="HTML"
        )
    else:
        await callback_query.message.answer("Нет доступных задач.")

    await callback_query.answer()


@router.callback_query(lambda c: c.data.startswith("complete_"))
async def mark_task_completed(callback_query: CallbackQuery):
    # Извлекаем ID задачи из callback_data
    task_id = callback_query.data.split("_")[1]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Получаем текущие данные задачи
    cursor.execute("SELECT title, description, price, status FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()

    if not task:
        await callback_query.answer("Задача не найдена.", show_alert=True)
        return

    title, description, price, status = task

    # Если задача уже выполнена, уведомляем пользователя
    if status == "выполнено":
        await callback_query.answer("Задача уже отмечена как выполненная.", show_alert=True)
        return

    # Обновляем статус задачи на "выполнено"
    cursor.execute("UPDATE tasks SET status = 'выполнено' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    # Обновляем текст сообщения
    updated_text = (
        f"🆔 <b>ID:</b> {task_id}\n"
        f"📌 <b>Название:</b> {title}\n"
        f"📝 <b>Описание:</b> {description}\n"
        f"💰 <b>Цена:</b> {price} руб.\n"
        f"📋 <b>Статус:</b> выполнено ✅\n"
    )

    await callback_query.message.edit_text(updated_text, parse_mode="HTML")
    await callback_query.answer("Задача отмечена как выполненная!")
