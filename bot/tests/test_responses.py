import asyncio
import unittest
from unittest.mock import AsyncMock, patch
from telegram import Update, Message, Chat, User
from telegram.ext import ContextTypes

import responses  # Your responses module


class TestResponses(unittest.TestCase):
    def setUp(self):
        self.update = Update(
            update_id=1,
            message=Message(
                message_id=1,
                date=None,
                chat=Chat(id=12345, type="private"),
                text="Test",
            ),
        )
        self.context = AsyncMock()

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
    async def test_start(self, mock_messages, mock_store_message_to_db):
        self.update.effective_chat.first_name = "TestUser"
        self.context.bot.send_message = AsyncMock()

        await responses.start(self.update, self.context)

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
    async def test_help(self, mock_messages, mock_store_message_to_db):
        self.update.effective_chat.first_name = "TestUser"
        self.context.bot.send_message = AsyncMock()

        await responses.help(self.update, self.context)

        self.context.bot.send_message.assert_awaited_once_with(
            chat_id=12345, text="Help message for TestUser, "
        )

    def test_handle_message(self):
        # More complex due to different branches in the function
        # You'll need to test different message types and contents
        pass
