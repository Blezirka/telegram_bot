import asyncio
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError
from contextlib import suppress

from config import IsAdmin, LIST_OF_COMMANDS
from states import AdminState
from keyboards import ADMIN_MENU_KEYBOARD, BACK_TO_ADMIN_KEYBOARD, get_pagination_keyboard
import database as db

# Создаем роутер для админских команд
admin_router = Router()


@admin_router.message(F.text == 'Админ меню', IsAdmin())
async def admin_reply_button_handler(message: types.Message, state: FSMContext) -> None:
    await state.set_state(state=None)
    await message.answer('Добро пожаловать в Админ-панель!', reply_markup=ADMIN_MENU_KEYBOARD)

@admin_router.message(Command('admin'), IsAdmin())
async def admin_command(message: types.Message, state: FSMContext) -> None:
    await state.set_state(state=None)
    await message.answer('Добро пожаловать в Админ-панель!', reply_markup=ADMIN_MENU_KEYBOARD)

@admin_router.callback_query(F.data == "admin", IsAdmin())
async def admin_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(state=None)
    with suppress(TelegramAPIError):
        await callback.message.edit_text('Добро пожаловать в Админ-панель!', reply_markup=ADMIN_MENU_KEYBOARD)
        return
    await callback.message.answer('Добро пожаловать в Админ-панель!', reply_markup=ADMIN_MENU_KEYBOARD)
@admin_router.callback_query(F.data == 'admin_statistic', IsAdmin())
async def admin_statistic(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(state=None)
    user_count = await db.get_user_count()
    await callback.message.edit_text(
        'Статистика\n\n'
        f'Количество пользователей: {user_count}',
        reply_markup=BACK_TO_ADMIN_KEYBOARD
    )

@admin_router.callback_query(F.data == 'admin_newsletter', IsAdmin())
async def admin_newsletter(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        'Рассылка\n\nВведите сообщение, которое будет отправлено пользователям',
        reply_markup=BACK_TO_ADMIN_KEYBOARD
    )
    await state.set_state(AdminState.newsletter)

@admin_router.message(AdminState.newsletter, ~F.text.in_(LIST_OF_COMMANDS))
async def admin_newsletter_step_2(message: types.Message, state: FSMContext):
    newsletter_text = message.text or message.caption  
    if not newsletter_text:
        await message.answer("Пожалуйста, введите текст.")
        return

    await db.save_newsletter_to_history(newsletter_text)
    all_ids = await db.get_all_users_id()
    success_sends = 0
    for user_id in all_ids:
        with suppress(TelegramAPIError):
            await message.send_copy(user_id[0])
            await asyncio.sleep(0.3)
            success_sends += 1
    await state.set_state(state=None)
    await message.answer(
        f'Успешно отправлена рассылка {success_sends}/{len(all_ids)}',
        reply_markup=BACK_TO_ADMIN_KEYBOARD
    )

@admin_router.message(Command('get_data'), IsAdmin())
async def get_data_command(message: types.Message, state: FSMContext) -> None: 
    await state.set_state(state=None)         
    history = await db.get_all_newsletters_history()
    if not history:
        await message.answer("В архиве еще нет сохраненных рассылок!")
        return
    page = 0
    total = len(history)
    text = f"📰 **Архив рассылок (Запись {page + 1} из {total})**:\n\n{history[page]}"
    await message.answer(text, parse_mode="Markdown", reply_markup=get_pagination_keyboard(page, total, "news_page"))

@admin_router.callback_query(F.data.startswith("news_page:"), IsAdmin())
async def process_newsletter_page(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(state=None)
    page = int(callback.data.split(":")[1])
    history = await db.get_all_newsletters_history()
    total = len(history)

    if not history:
        await callback.message.edit_text("Архив пуст.")
        return

    text = f"📰 **Архив рассылок (Запись {page + 1} из {total})**:\n\n{history[page]}"
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_pagination_keyboard(page, total, "news_page"))

@admin_router.callback_query(F.data == "close_archive")
async def close_archive_callback(callback: types.CallbackQuery) -> None:
    await callback.answer()
    await callback.message.delete()