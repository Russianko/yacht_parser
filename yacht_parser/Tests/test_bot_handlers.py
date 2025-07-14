import pytest
from telegram import InlineKeyboardMarkup, Update, InlineKeyboardButton, User, Message, Chat
from telegram.ext import CallbackContext, ContextTypes
from yacht_parser.Bot import handlers
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock


class DummyBot:
    async def send_message(self, chat_id, text,reply_markup=None):
        self.chat_id = chat_id
        self.text = text
        self.reply_markup = reply_markup


@pytest.mark.asyncio
async def test_start_command():
    message = AsyncMock()
    message.text ="/start"
    message.chat = SimpleNamespace(id=123)
    message.reply_text = AsyncMock()

    update = SimpleNamespace(message=message)
    context = MagicMock()

    await handlers.start(update, context)

    message.reply_text.assert_called_once()
    args, kwargs = message.reply_text.call_args
    assert "начать" in args[0].lower()


@pytest.mark.asyncio
async def test_begin_search():
    update = SimpleNamespace()
    update.callback_query = SimpleNamespace()
    update.callback_query.answer = AsyncMock()
    update.callback_query.message = SimpleNamespace()
    update.callback_query.message.reply_text = AsyncMock()

    context = SimpleNamespace()
    context.user_data = {}
    await handlers.begin_search(update, context)
    args, kwargs = update.callback_query.message.reply_text.call_args
    assert "бренд яхты" in args[0]



