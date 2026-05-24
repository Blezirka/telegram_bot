import aiosqlite
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

DB_NAME = os.path.join(CURRENT_DIR, 'db')

async def init_db():
    async with aiosqlite.connect(DB_NAME) as connect:
        async with connect.cursor() as cursor:
            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    full_name TEXT,
                    username TEXT,
                    about_you TEXT DEFAULT ''
                )
            ''')
            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS newsletter_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT
                )
            ''')
            await connect.commit()

async def get_user_count():
    async with aiosqlite.connect(DB_NAME) as connect:
        async with connect.cursor() as cursor:
            res = await cursor.execute('SELECT COUNT(*) FROM users')
            row = await res.fetchone()
            return row[0] if row else 0

async def add_user(user_id: int, full_name: str, username: str) -> None:
    async with aiosqlite.connect(DB_NAME) as connect:
        async with connect.cursor() as cursor:
            check_user = await cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            if await check_user.fetchone() is None:
                await cursor.execute(
                    'INSERT INTO users (user_id, full_name, username) VALUES (?, ?, ?)',
                    (user_id, full_name, username)
                )
                await connect.commit()

async def get_all_users_id():
    async with aiosqlite.connect(DB_NAME) as connect:
        async with connect.cursor() as cursor:
            res = await cursor.execute('SELECT user_id FROM users')
            return await res.fetchall()

async def update_user_story(user_id: int, story: str) -> None:
    async with aiosqlite.connect(DB_NAME) as connect:
        async with connect.cursor() as cursor:
            await cursor.execute('UPDATE users SET about_you = ? WHERE user_id = ?', (story, user_id))
            await connect.commit()

async def get_user_story(user_id: int) -> str:
    async with aiosqlite.connect(DB_NAME) as connect:
        async with connect.cursor() as cursor:
            res = await cursor.execute('SELECT about_you FROM users WHERE user_id = ?', (user_id,))
            row = await res.fetchone()
            return row[0] if row and row[0] else ""

async def save_newsletter_to_history(text: str) -> None:
    async with aiosqlite.connect(DB_NAME) as connect:
        async with connect.cursor() as cursor:
            await cursor.execute('INSERT INTO newsletter_history (text) VALUES (?)', (text,))
            await connect.commit()

async def get_all_newsletters_history() -> list:
    async with aiosqlite.connect(DB_NAME) as connect:
        async with connect.cursor() as cursor:
            res = await cursor.execute('SELECT text FROM newsletter_history ORDER BY id ASC')
            rows = await res.fetchall()
            return [row[0] for row in rows]