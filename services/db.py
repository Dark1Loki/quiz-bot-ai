# services/db.py
import aiosqlite

DB_NAME = 'quiz_bot.db'

async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS quiz_state (
                user_id INTEGER PRIMARY KEY,
                q_idx INTEGER,
                ok_count INTEGER
            )
        ''')
        await db.commit()

async def get_state(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT q_idx, ok_count FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            if result:
                return result  # (q_idx, ok_count)
            return (0, 0)

async def update_state(user_id, q_idx=None, ok_count=None):
    async with aiosqlite.connect(DB_NAME) as db:
        current = await db.execute('SELECT q_idx, ok_count FROM quiz_state WHERE user_id = ?', (user_id,))
        result = await current.fetchone()

        step = result[0] if result else 0
        current_correct = result[1] if result else 0

        q_idx = q_idx if q_idx is not None else step
        ok_count = ok_count if ok_count is not None else current_correct

        await db.execute('''
            INSERT OR REPLACE INTO quiz_state (user_id, q_idx, ok_count)
            VALUES (?, ?, ?)
        ''', (user_id, q_idx, ok_count))
        await db.commit()