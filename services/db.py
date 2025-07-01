# services/db.py
import aiosqlite

DB_NAME = 'quiz_bot.db'

async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS quiz_state (
                user_id INTEGER PRIMARY KEY,
                question_index INTEGER,
                correct_answers INTEGER
            )
        ''')
        await db.commit()

async def get_state(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index, correct_answers FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            if result:
                return result  # (question_index, correct_answers)
            return (0, 0)

async def update_state(user_id, question_index=None, correct_answers=None):
    async with aiosqlite.connect(DB_NAME) as db:
        current = await db.execute('SELECT question_index, correct_answers FROM quiz_state WHERE user_id = ?', (user_id,))
        result = await current.fetchone()

        # Начальные значения
        current_index = result[0] if result else 0
        current_correct = result[1] if result else 0

        # Обновляем, если передано новое значение
        question_index = question_index if question_index is not None else current_index
        correct_answers = correct_answers if correct_answers is not None else current_correct

        await db.execute('''
            INSERT OR REPLACE INTO quiz_state (user_id, question_index, correct_answers)
            VALUES (?, ?, ?)
        ''', (user_id, question_index, correct_answers))
        await db.commit()