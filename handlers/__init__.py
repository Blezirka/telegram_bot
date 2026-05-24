from aiogram import Router
from .admin import admin_router
from .user import user_router

# Создаем общий роутер для всей папки handlers
all_handlers_router = Router()

# Включаем в него логику из отдельных файлов
all_handlers_router.include_router(admin_router)
all_handlers_router.include_router(user_router)