from aiogram import Router,html
from aiogram.filters import CommandStart
from aiogram.types import Message

start_router = Router()

@start_router.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f"Привет {html.bold(message.from_user.first_name)}")