import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup, ReplyKeyboardMarkup, \
    KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()
dp = Dispatcher()
BOT_TOKEN = getenv("BOT_TOKEN")

kbs = [
    [
        KeyboardButton(text="ДАА"), KeyboardButton(text="ЕСТЕСВЕННО"),
    ],
    [KeyboardButton(text="нет")
     ]
]

keyboard = ReplyKeyboardMarkup(keyboard=kbs, resize_keyboard=True)


@dp.message(CommandStart())
async def callback_handler(message: Message):
    await message.answer("Вам нравится наш бот???", reply_markup=keyboard)


@dp.message()
async def message_handler(message: Message):
    if message.text == "ДАА":
        await message.answer("И Я ОБОЖАЮ НАШЕГО БОТА")
    elif message.text == "нет":
        await message.answer("Тогда иди нахуй")
    else:
        await message.answer("ЕСТЕСТВЕННО НАШ БОТ ЛУЧШИЙ")


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
