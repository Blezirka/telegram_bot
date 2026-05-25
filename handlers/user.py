from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config import LIST_OF_COMMANDS, PORTFOLIO_TEXT, admin_ids
from states import UserState
from keyboards import get_main_reply_keyboard, MAIN_MENU_KEYBOARD, BACK_TO_MENU_KEYBOARD
import database as db

user_router = Router()

@user_router.message(Command('start'))
async def start_command(message: types.Message, state: FSMContext) -> None:
    await state.set_state(state=None)
    await db.add_user(
        user_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username
    )

    # Генерируем клавиатуру персонально для этого юзера:
    dynamic_reply_kb = get_main_reply_keyboard(message.from_user.id, admin_ids)

    await message.answer(
        f'Добрый день, {message.from_user.full_name}\n'
        f'Рад вас видеть, выберите Меню, чтобы узнать мои команды'
        ,reply_markup=dynamic_reply_kb
    ) 
    await message.answer('Привет! это мой бот-визитка', reply_markup=MAIN_MENU_KEYBOARD)

@user_router.callback_query(F.data == "menu")
async def menu_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(state=None)
    await callback.message.edit_text('Привет! это мой бот-визитка', reply_markup=MAIN_MENU_KEYBOARD)

@user_router.callback_query(F.data == "about_me")
async def about_me_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(state=None)
    await callback.message.edit_text(
        'Рад, что ты спросил\n'
        'Я на самом деле редко говорю о себе, но мама говорит, что я классный',
        reply_markup=BACK_TO_MENU_KEYBOARD
    )

@user_router.callback_query(F.data == "name")
async def name_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    user = callback.from_user
    await callback.answer()
    await state.set_state(state=None)
    await callback.message.edit_text(
        f"Твоё имя: {user.full_name} (можно обращаться {user.first_name})",
        reply_markup=BACK_TO_MENU_KEYBOARD
    )

@user_router.callback_query(F.data == "portfolio")
async def portfolio_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(state=None)
    await callback.message.edit_text(PORTFOLIO_TEXT, reply_markup=BACK_TO_MENU_KEYBOARD)

@user_router.callback_query(F.data == "about_you")
async def about_you_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    current_story = await db.get_user_story(callback.from_user.id)
    if not current_story:
        text = "Расскажи о себе в ответном сообщении! Я постараюсь всё запомнить."
        await callback.message.edit_text(text, reply_markup=BACK_TO_MENU_KEYBOARD)
    else:
        pages = [p.strip() for p in current_story.split('\n') if p.strip()]
        page = 0
        total = len(pages)
        text = f"👤 **Твоя история (Страница {page + 1} из {total})**:\n\n{pages[page]}\n\n*— Пиши сюда, чтобы добавить страницу!*"
        await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_pagination_keyboard(page, total, "user_page"))
        
    await state.set_state(UserState.waiting_for_about_you)

@user_router.callback_query(F.data.startswith("user_page:"))
async def process_user_story_page(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    page = int(callback.data.split(":")[1])
    current_story = await db.get_user_story(callback.from_user.id)
    pages = [p.strip() for p in current_story.split('\n') if p.strip()]
    total = len(pages)

    text = f"👤 **Твоя история (Страница {page + 1} из {total})**:\n\n{pages[page]}\n\n*— Пиши сюда, чтобы добавить страницу!*"
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_pagination_keyboard(page, total, "user_page"))
    await state.set_state(UserState.waiting_for_about_you)

@user_router.message(UserState.waiting_for_about_you, ~F.text.in_(LIST_OF_COMMANDS))
async def about_you_step_2(message: types.Message, state: FSMContext):
    current_story = await db.get_user_story(message.from_user.id)
    updated_story = f"{current_story}\n{message.text}" if current_story else message.text
        
    await db.update_user_story(message.from_user.id, updated_story)
    
    pages = [p.strip() for p in updated_story.split('\n') if p.strip()]
    total = len(pages)
    page = total - 1
    
    text = f"✅ **Запомнил новую страницу! ({page + 1} из {total})**:\n\n{pages[page]}"
    await message.answer(text, parse_mode="Markdown", reply_markup=get_pagination_keyboard(page, total, "user_page"))

@user_router.message(F.text == 'Меню')
async def menu_handler(message: types.Message, state: FSMContext) -> None:
    await state.set_state(state=None)
    await message.answer(
        'Мои команды\n\n'
        'Привет - я тебе отвечу привет!\n'
        'Морс - я расскажу о том, какой вкусный облепиховый морс'
    )
    await message.answer('Привет! это мой бот-визитка', reply_markup=MAIN_MENU_KEYBOARD)

@user_router.message(F.text == 'Привет')
async def hello_handler(message: types.Message) -> None:
    await message.answer('Привет! Как у тебя дела?')

@user_router.message(F.text == 'Морс')
async def morse_handler(message: types.Message) -> None:
    await message.answer('Ты не представляешь какой вкусный морс я сегодня пил. Мне кажется, он вызывает зависимость')