from bot.models import Subscription
from aiogram.types import ChatJoinRequest
from bot.config import bot_messages, bot
from aiogram import Dispatcher
from package.settings import CHANEL_ID


async def is_active_subscription(tg_id):

    subscription = await Subscription.objects.filter(user__pk=tg_id).afirst()
    return subscription.is_active if subscription else False


async def approve_request(chat_join: ChatJoinRequest):

    if await is_active_subscription(chat_join.from_user.id):
        print('new_user')
        await chat_join.approve()
        await bot.send_message(
            chat_id=CHANEL_ID,
            text=bot_messages['welocome'].format(
                chat_join.from_user.first_name
            ),
            parse_mode='HTML'
        )


def register_handlers(dp: Dispatcher):
    dp.chat_join_request.register(approve_request)
