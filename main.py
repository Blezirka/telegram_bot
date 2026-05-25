import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN, admin_ids
from database import init_db
from handlers import all_handlers_router
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat


async def set_bot_commands(bot: Bot):
    # 1. Команды по умолчанию (для всех обычных пользователей)
    user_commands = [
        BotCommand(command="start", description="Запустить бота / Вернуться в меню")
    ]
    await bot.set_my_commands(commands=user_commands, scope=BotCommandScopeDefault())
    
    # 2. Команды для каждого админа из списка ADMIN_IDS
    admin_commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="admin", description="Открыть админ-панель"),
        BotCommand(command="get_data", description="Архив рассылок")
    ]
    for admin_id in admin_ids:
        try:
            await bot.set_my_commands(
                commands=admin_commands, 
                scope=BotCommandScopeChat(chat_id=admin_id)
            )
        except Exception as e:
            print(f"Не удалось установить команды для админа {admin_id}: {e}")


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