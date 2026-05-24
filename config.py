import os
from dotenv import load_dotenv
from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
admin_ids = [int(x.strip()) for x in os.getenv('ADMIN_IDS', '').split(',') if x.strip()]

LIST_OF_COMMANDS = ['Меню', '/admin', '/start', '/get_data']

class IsAdmin(BaseFilter):
    async def __call__(self, obj: TelegramObject) -> bool:
        return obj.from_user.id in admin_ids

def load_portfolio_text():
    try:
        with open('portfolio.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Портфолио временно недоступно."

PORTFOLIO_TEXT = load_portfolio_text()