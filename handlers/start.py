# handlers/start.py
from aiogram import types, Dispatcher
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз по теме 'Разработка ИИ'!", reply_markup=builder.as_markup(resize_keyboard=True))

def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))