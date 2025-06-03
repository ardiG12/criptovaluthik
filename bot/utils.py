from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kbs = [
    [
        KeyboardButton(text="ДАА"), KeyboardButton(text="ЕСТЕСВЕННО")
    ]
]

keyboard = ReplyKeyboardMarkup(keyboard=kbs, resize_keyboard=True)
