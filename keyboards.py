from aiogram import types

# MAIN_MENU_SCREEN_BUTTONS = [[types.KeyboardButton(text='Меню')]]
# MAIN_MENU_SCREEN_KEYBOARD = types.ReplyKeyboardMarkup(keyboard=MAIN_MENU_SCREEN_BUTTONS, resize_keyboard=True)

MAIN_MENU_BUTTONS = [
    [types.InlineKeyboardButton(text="Обо мне", callback_data='about_me')],
    [
        types.InlineKeyboardButton(text="Имя", callback_data='name'),
        types.InlineKeyboardButton(text="Портфолио", callback_data='portfolio')
    ],
    [types.InlineKeyboardButton(text="О тебе", callback_data='about_you')],
    [types.InlineKeyboardButton(text="Хочу котика", callback_data='send_cat')]
]
MAIN_MENU_KEYBOARD = types.InlineKeyboardMarkup(inline_keyboard=MAIN_MENU_BUTTONS)

BACK_TO_MENU_BUTTON = [[types.InlineKeyboardButton(text="Вернуться", callback_data='menu')]]
BACK_TO_MENU_KEYBOARD = types.InlineKeyboardMarkup(inline_keyboard=BACK_TO_MENU_BUTTON)

BACK_TO_ADMIN_BUTTON = [[types.InlineKeyboardButton(text="Вернуться", callback_data='admin')]]
BACK_TO_ADMIN_KEYBOARD = types.InlineKeyboardMarkup(inline_keyboard=BACK_TO_ADMIN_BUTTON)

ADMIN_MENU_BUTTONS = [
    [
        types.InlineKeyboardButton(text='Рассылка', callback_data='admin_newsletter'),
        types.InlineKeyboardButton(text='Статистика', callback_data='admin_statistic')
    ]
]
ADMIN_MENU_KEYBOARD = types.InlineKeyboardMarkup(inline_keyboard=ADMIN_MENU_BUTTONS)


def get_main_reply_keyboard(user_id: int, admin_list: list) -> types.ReplyKeyboardMarkup:
    # Базовая кнопка, которая есть у всех

    buttons = [types.KeyboardButton(text='Меню')]

    # Если зашел админ, добавляем ему вторую кнопку в тот же ряд
    if user_id in admin_list:
        buttons.append(types.KeyboardButton(text='Админ меню'))

    # Собираем клавиатуру (обрати внимание на структуру списка [[...]])
    return types.ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)


def get_pagination_keyboard(page: int, total_pages: int, prefix: str) -> types.InlineKeyboardMarkup:
    buttons = []
    if page > 0:
        buttons.append(types.InlineKeyboardButton(text="⬅️ Назад", callback_data=f"{prefix}:{page - 1}"))

    if page < total_pages - 1:
        buttons.append(types.InlineKeyboardButton(text="Вперед ➡️", callback_data=f"{prefix}:{page + 1}"))

    if prefix == "user_page":
        back_cb = "menu"
        back_text = "Вернуться в меню"
    elif prefix == "news_page":
        back_cb = "admin"
        back_text = "Вернуться"
    else:
        back_cb = "close_archive"
        back_text = "Закрыть"

    close_button = [[types.InlineKeyboardButton(text=back_text, callback_data=back_cb)]]
    return types.InlineKeyboardMarkup(inline_keyboard=[buttons, *close_button])