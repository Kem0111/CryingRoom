from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from bot.config import bot_messages, bot


async def set_commands():
    commands = [
        BotCommand(command="/start", description="Обновить"),
    ]

    await bot.set_my_commands(commands=commands)


async def question_kb(btn_name='question_btn'):
    kb = [
        [
            InlineKeyboardButton(
                text=bot_messages[btn_name],
                callback_data='question_btn'
            )
        ],
        [
            InlineKeyboardButton(
                text=bot_messages['get_chanel'],
                url='https://t.me/+GvJgwDw6MOdjYzEy'
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


async def pay_kb():
    kb = [[
        InlineKeyboardButton(
            text=bot_messages['pay_btn'],
            callback_data='pay_btn'
        )
    ]]
    return InlineKeyboardMarkup(inline_keyboard=kb)


async def cancel_kb():
    kb = [[
        InlineKeyboardButton(
            text=bot_messages['cancel_btn'],
            callback_data='cancel_btn'
        )
    ]]
    return InlineKeyboardMarkup(inline_keyboard=kb)
