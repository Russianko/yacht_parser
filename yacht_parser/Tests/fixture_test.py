import pytest
from unittest.mock import AsyncMock, MagicMock
from types import SimpleNamespace
from yacht_parser.Bot import handlers
from unittest.mock import patch


# Фикстуры

@pytest.fixture
def dummy_context():
    context = SimpleNamespace()
    context.user_data = {}
    context.bot = MagicMock()
    return context

@pytest.fixture
def dummy_update_with_message():
    message = AsyncMock()
    message.text = '/start'
    message.chat = SimpleNamespace(id=123)
    message.reply_text = AsyncMock()
    return SimpleNamespace(message=message)


@pytest.fixture
def dummy_update_with_callback():
    callback = SimpleNamespace()
    callback_query.answer = AsyncMock()
    callback_query.message = SimpleNamespace()
    callback_query.message.reply_text = AsyncMock()
    return SimpleNamespace(callback_query=callback_query)


@pytest.fixture
def dummy_context_with_user_data():
    context = SimpleNamespace()
    context.user_data = {}
    return context


@pytest.fixture
def dummy_update_with_brand_callback():
    callback_query = SimpleNamespace()
    callback_query.data = "brand_Bavaria"
    callback_query.answer = AsyncMock()
    callback_query.edit_message_text = AsyncMock()
    callback_query.message = SimpleNamespace()
    callback_query.message.reply_text = AsyncMock()
    return SimpleNamespace(callback_query=callback_query)


@pytest.fixture
def dummy_update_with_price_callback():
    callback_query = SimpleNamespace()
    callback_query.data = "price_50000"
    callback_query.answer = AsyncMock()
    callback_query.edit_message_text = AsyncMock()
    callback_query.message = SimpleNamespace()
    callback_query.message.reply_text = AsyncMock()
    return SimpleNamespace(callback_query=callback_query)


@pytest.mark.asyncio
async def test_start_command():
    message = AsyncMock()
    message.text = '/start'
    message.chat = SimpleNamespace(id=123)
    message.reply_text = AsyncMock()

    update = SimpleNamespace(message=message)
    context = MagicMock()

    await handlers.start(update, context)

    message.reply_text.assert_called_once()
    args, kwargs = message.reply_text.call_args
    assert "начать" in args[0].lower()


@pytest.mark.asyncio
async def test_brand_callback_handler(dummy_update_with_brand_callback, dummy_context_with_user_data):
    await handlers.brand_callback_handler(dummy_update_with_brand_callback, dummy_context_with_user_data)

    #проверяем что сообщение редактируется и появляется кнопка выбора типа лодки
    dummy_update_with_brand_callback.callback_query.answer.assert_called_once()
    dummy_update_with_brand_callback.callback_query.message.reply_text.assert_called_once()

    args, kwargs = dummy_update_with_brand_callback.callback_query.message.reply_text.call_args

    assert "выберите бренд" in args[0].lower()
    assert "выберите" in args[0].lower()



@pytest.mark.asyncio
@patch('yacht_parser.Bot.handlers.get_links_by_producer')
@patch('yacht_parser.Bot.handlers.parse_yacht')
@patch('yacht_parser.Bot.handlers.sqlite3.connect')

async def test_price_callback_handler(mock_connect, mock_parse_yacht, mock_get_links_by_producer, dummy_update_with_price_callback, dummy_context_with_user_data):
    dummy_context_with_user_data.user_data = {
        'brand': 'Bavaria',
        'type': 'Парусная',
        'budget': 50000
    }

    #настроаиваем мок на возврат одной сслыки
    mock_get_links_by_producer.return_value = ['http://example.com/yacht1']

    # Мокаем базу
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    mock_cursor.fetchall.return_value = [
        ('Bavaria 32', '€49,000', 49000, 'http://example.com/yacht1')
    ]

    await handlers.price_callback_handler(dummy_update_with_price_callback, dummy_context_with_user_data)

    #проверяем наличие результатов и кнопку нового поиска
    assert dummy_update_with_price_callback.callback_query.edit_message_text.called
    assert dummy_update_with_price_callback.callback_query.message.reply_text.call_count >= 2

    called_texts = [args[0] for args, _ in dummy_update_with_price_callback.callback_query.message.reply_text.call_args_list]
    assert any("bavaria" in text.lower() for text in called_texts)
    assert any("начать новый поиск" in text.lower() for text in called_texts)

