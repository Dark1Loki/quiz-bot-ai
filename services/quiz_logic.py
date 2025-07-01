# services/quiz_logic.py
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.db import get_state
from data.questions import quiz_data

def generate_options_keyboard(answer_options):
    builder = InlineKeyboardBuilder()
    for idx, option in enumerate(answer_options):
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=str(idx)
        ))
    builder.adjust(1)
    return builder.as_markup()

async def get_question(message_obj, user_id):
    current_question_index, _ = await get_state(user_id)
    question = quiz_data[current_question_index]
    kb = generate_options_keyboard(question['options'])

    # Если это callback, получаем объект .message
    if isinstance(message_obj, types.CallbackQuery):
        message_obj = message_obj.message

    await message_obj.answer(question['question'], reply_markup=kb)