import unittest
from unittest.mock import AsyncMock, patch
from telegram import Update, Message, Chat
from typing import Dict
from datetime import datetime
from bot.responses import start, help


class TestResponses(unittest.TestCase):
    def setUp(self) -> None:
        chat = Chat(
            id=12345, type="private", first_name="TestUser"
        )  # Create a Chat object with first_name
        self.update: Update = Update(
            update_id=1,
            message=Message(
                message_id=1,
                date=datetime.now(),
                chat=chat,
                text="Test",
            ),
        )
        self.context: AsyncMock = AsyncMock()

    @patch(
        "responses.messages",
        {
            "start_user": "Welcome, {}!",
            "help": "Help message for {}, {}",
            "response": "{}: {}",
            "no_tagged_question": "No tagged question.",
            "respond_to_question": "Responding to question: {}",
        },
    )
    @patch("responses.store_message_to_db")
    async def test_start(
        self, mock_messages: Dict[str, str], mock_store_message_to_db: AsyncMock
    ) -> None:
        self.context.bot.send_message = AsyncMock()

        await start(self.update, self.context)

        self.context.bot.send_message.assert_awaited_once_with(
            chat_id=12345, text="Welcome, TestUser!"
        )

    @patch("responses.store_message_to_db")
    @patch(
        "responses.messages",
        {
            "start_user": "Welcome, {}!",
            "help": "Help message for {}, {}",
            "response": "{}: {}",
            "no_tagged_question": "No tagged question.",
            "respond_to_question": "Responding to question: {}",
        },
    )
    async def test_help(
        self, mock_messages: Dict[str, str], mock_store_message_to_db: AsyncMock
    ) -> None:
        self.context.bot.send_message = AsyncMock()

        await help(self.update, self.context)

        self.context.bot.send_message.assert_awaited_once_with(
            chat_id=12345, text="Help message for TestUser, "
        )
