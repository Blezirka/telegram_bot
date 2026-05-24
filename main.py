import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database import init_db
from handlers import all_handlers_router

async def main() -> None:
    # 1. Инициализируем БД
    await init_db()
    
    # 2. Создаем экземпляры Бота и Диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # 3. Подключаем роутер со всеми хэндлерами проекта
    dp.include_router(all_handlers_router)
    
    # 4. Запускаем polling
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())