import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from dotenv import load_dotenv
from datetime import datetime
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import psycopg2
from os import getenv, path

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
PASSWORD = getenv("PASSWORD")

connect = psycopg2.connect(
    dbname=getenv("DB_NAME"),
    user=getenv("USER"),
    password=getenv("PASSWORD"),
    host=getenv("HOST"),
    port=getenv("PORT")
)
cursor = connect.cursor()

kbs = [
    [
        InlineKeyboardButton(text="🇺🇿 uz", callback_data="uz"),
        InlineKeyboardButton(text="🇷🇺 ru", callback_data="ru"),
        InlineKeyboardButton(text="🇺🇸 en", callback_data="en"),

    ]
]
uz_ru_en_kbs = InlineKeyboardMarkup(inline_keyboard=kbs)

dp = Dispatcher()


def save_user(chat_id: int, lang: str):
    with connect:
        with connect.cursor():
            query = """INSERT INTO users (chat_id,lang) VALUES(%s, %s);"""
            cursor.execute(query, (chat_id, lang))


def update_data(chat_id: int, lang: str):
    with connect:
        with connect.cursor():
            query = """UPDATE users SET lang = %s WHERE chat_id = %s;"""
            cursor.execute(query, (lang, chat_id))


def delete_user(chat_id: int):
    with connect:
        with connect.cursor() as cur:
            query = "DELETE FROM users WHERE chat_id = %s;"
            cur.execute(query, (chat_id,))
        connect.commit()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Здраствуйте , {html.bold(message.from_user.full_name)}! "
                         f"Выберите язык: ", reply_markup=uz_ru_en_kbs)


@dp.message(Command("SetLanguage"))
async def language_handler(message: Message):
    update_data(message.chat.id, message.lang)
    await message.answer(f"Смените язык: ", reply_markup=uz_ru_en_kbs)


@dp.callback_query()
async def callback_query_handler(call: CallbackQuery) -> None:
    lang = call.data
    chat_id = call.message.chat.id

    save_user(chat_id, lang)

    if lang == "uz":
        await call.message.answer("Ajoyib, siz o'zbek tilini tanladingiz!")
    elif lang == "ru":
        await call.message.answer("Отлично, вы выбрали русский язык!")
    elif lang == "en":
        await call.message.answer("Great, you have chosen the English language!")

    await call.answer()



# @dp.message()
# async def echo_handler(message: Message) -> None:
#
#     try:
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         await message.answer("Nice try!")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

