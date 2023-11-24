import asyncio
import os

import django
from bot.config import dp, bot, scheduler


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "package.settings")
django.setup()


async def main():
    from bot.handlers import subscription, paymant, start_segregation
    from bot.utils.unsubscribe_procces import check_subscriptions_and_remove

    allowed_updates = [
        "message",
        "edited_message",
        "channel_post",
        "edited_channel_post",
        "inline_query",
        "chosen_inline_result",
        "callback_query",
        "shipping_query",
        "pre_checkout_query",
        "poll",
        "poll_answer",
        "my_chat_member",
        "chat_member",
        "chat_join_request",
    ]
    start_segregation.register_handlers(dp)
    subscription.register_handlers(dp)
    paymant.register_handlers(dp)
    try:
        scheduler.add_job(
            check_subscriptions_and_remove,
            "cron",
            hour=8,
            minute=0,
            args=(bot,)
        )
        scheduler.start()

        await dp.start_polling(
            bot,
            allowed_updates=allowed_updates
        )
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
