import asyncio
import logging
import sys
from os import getenv

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()


class KBS(CallbackData, prefix="simple"):
    action: str


@dp.message(CommandStart())
async def start(message: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Нажми 1", callback_data=KBS(action="b1").pack()),
             InlineKeyboardButton(text="Нажми 2", callback_data=KBS(action="b2").pack())]
        ]
    )
    await message.answer("Привет! Нажми кнопку ниже:", reply_markup=kb)


@dp.callback_query(KBS.filter())
async def b1(callback: CallbackQuery, callback_data: KBS):  # Получаем распарсенный callback_data
    if callback_data.action == "b1":
        await callback.answer("Ты нажал на кнопку 1")
    elif callback_data.action == "b2":
        await callback.answer("Ты нажал на кнопку 2")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
