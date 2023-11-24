from typing import Union
from aiogram import types, Dispatcher, F
from bot.handlers.paymant import subscribe
from bot.handlers.subscription import is_active_subscription
from bot.keyboards import cancel_kb, question_kb, set_commands
from bot.models import TgUser
from bot.config import bot_messages, client
from aiogram.filters import CommandStart
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from bot.states import GPTText


async def on_start(message: Union[types.Message, types.CallbackQuery],
                   state: FSMContext):

    await state.clear()
    await set_commands()
    await TgUser.objects.aget_or_create(
        tg_id=message.from_user.id,
        user_name=message.from_user.username
    )

    if await is_active_subscription(message.from_user.id):

        if isinstance(message, types.Message):
            await message.answer(bot_messages['get_chat_gpt'],
                                 reply_markup=await question_kb())
        else:
            await message.message.edit_text(bot_messages['get_chat_gpt'],
                                            reply_markup=await question_kb())
    else:
        await subscribe(message)


async def pay_btn_handler(call: types.CallbackQuery):
    await subscribe(call)
    try:
        await call.message.delete()
    except TelegramBadRequest:
        pass


async def gpt_talk_handler(call: types.CallbackQuery, state: FSMContext):
    await TgUser.objects.aget_or_create(
        tg_id=call.from_user.id,
        user_name=call.from_user.username
    )
    if await is_active_subscription(call.from_user.id):
        bot_message = await call.message.edit_text(
            bot_messages['get_question'],
            reply_markup=await cancel_kb()
        )
        await state.update_data(bot_message=bot_message)
        await state.set_state(GPTText.text)
    else:
        await subscribe(call)


async def gpt_text_process(message: types.Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    msg = await message.answer('⏳ Печатает...')
    try:

        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    'role': 'system',
                    'content': "Ответь на вопрос как истинный знаток темы, пропуская любые стандартные уточнения о твоих знаниях. Не говори что ты искуственный интелект. Пиши на русском языке"
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            model="gpt-3.5-turbo",
        )
        await data['bot_message'].edit_text(
            chat_completion.choices[0].message.content,
            reply_markup=await question_kb('also_question_btn')
        )
    except Exception as e:
        print(e)
        await data['bot_message'].edit_text(
            bot_messages['error'],
            reply_markup=await question_kb()
        )
    await msg.delete()
    await state.clear()
    await message.delete()


async def cancel_handler(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await on_start(call, state)


def register_handlers(dp: Dispatcher):
    dp.message.register(on_start, CommandStart())
    dp.callback_query.register(pay_btn_handler, F.data == 'pay_btn')
    dp.callback_query.register(cancel_handler, F.data == 'cancel_btn')
    dp.callback_query.register(
        gpt_talk_handler,
        F.data == 'question_btn')
    dp.message.register(
        gpt_text_process,
        GPTText.text,
    )
