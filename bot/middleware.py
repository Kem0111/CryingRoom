from __future__ import annotations

from aiogram.dispatcher.flags import get_flag
from aiogram.utils.chat_action import ChatActionSender
from typing import Any, Awaitable, Callable, Dict
from aiogram.types import Message
from aiogram import BaseMiddleware


class ChatActionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        long_operation_type = get_flag(data, "long_operation")

        # Если такого флага на хэндлере нет
        if not long_operation_type:

            return await handler(event, data)

        async with ChatActionSender(
                bot=event.bot,
                action=long_operation_type,
                chat_id=event.chat.id,
                interval=30.0,
                initial_sleep=2
        ):
            return await handler(event, data)
