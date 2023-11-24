from aiogram import types, Dispatcher, F
from bot.config import bot, bot_messages
from package.settings import UKASSA_TOKEN, SUBSCRIPTION_PRICE, CHANEL_LINK, CHANEL_ID
from bot.models import TgUser, Subscription
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from asgiref.sync import sync_to_async
from django.utils.timezone import now
from aiogram.exceptions import TelegramBadRequest


async def subscribe(message: types.Message):

    await bot.send_invoice(
        chat_id=message.from_user.id,
        title=bot_messages['invoice_title'],
        description=bot_messages['invoice_description'],
        payload='ukassa_pay',
        provider_token=UKASSA_TOKEN,
        currency='RUB',
        start_parameter='bot',
        prices=[types.LabeledPrice(
            label="Руб", amount=int(SUBSCRIPTION_PRICE * 100)
        )]
    )


async def process_pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def process_success_pay(message: types.Message):
    success_pay = message.successful_payment.invoice_payload

    if not success_pay.startswith('ukassa_pay'):
        await message.answer(
            bot_messages['not_confirm']
        )
        await message.delete()

    try:
        await bot.unban_chat_member(
            chat_id=CHANEL_ID,
            user_id=message.from_user.id)
    except TelegramBadRequest:
        pass
    user = await TgUser.objects.filter(pk=message.from_user.id).afirst()
    current_time = make_aware(datetime.now())

    subscription, created = await Subscription.objects.aget_or_create(
        user=user,
        defaults={
            'start_date': current_time,
            'expiration_date': current_time + timedelta(days=30),
            'is_active': True
        }
    )
    if not created:
        # Если подписка уже есть, обновляем даты
        if subscription.expiration_date > now():
            # Подписка еще активна, добавляем 30 дней к существующей дате окончания
            subscription.expiration_date += timedelta(days=30)
        else:
            # Подписка истекла, начинаем новый период от текущей даты
            subscription.start_date = current_time
            subscription.expiration_date = current_time + timedelta(days=30)

        subscription.is_active = True
        await sync_to_async(subscription.save)()

    await message.answer(text=bot_messages["succes_pay"].format(CHANEL_LINK))


def register_handlers(dp: Dispatcher):
    dp.pre_checkout_query.register(process_pre_checkout)
    dp.message.register(
        process_success_pay,
        F.content_type == types.ContentType.SUCCESSFUL_PAYMENT
    )
