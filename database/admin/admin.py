import sqlite3

from tasks_bot.database.db import DB_NAME


def add_admin(telegram_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO admin_id (telegram_id) VALUES (?)", (telegram_id,))

    conn.commit()
    conn.close()
