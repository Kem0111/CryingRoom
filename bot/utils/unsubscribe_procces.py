
from datetime import datetime
from aiogram import Bot

from django.utils.timezone import make_aware
from bot.keyboards import pay_kb
from bot.models import Subscription
from asgiref.sync import sync_to_async
from package.settings import CHANEL_ID
from bot.config import bot_messages


async def check_subscriptions_and_remove(bot: Bot):
    current_time = make_aware(datetime.now())
    expired_subscriptions = Subscription.objects.filter(
        expiration_date__lt=current_time, is_active=True
    )

    async for subscription in expired_subscriptions:
        try:
            await bot.ban_chat_member(chat_id=CHANEL_ID,
                                      user_id=subscription.user_id)
            subscription.is_active = False
            await sync_to_async(subscription.save)()
            await bot.send_message(chat_id=subscription.user_id,
                                   text=bot_messages['stop_subscribe'],
                                   reply_markup=await pay_kb())

            print(f"User {subscription.user_id} has been removed from the channel due to expired subscription.")
        except Exception as e:
            print(f"Failed to remove user {subscription.user}: {e}")
