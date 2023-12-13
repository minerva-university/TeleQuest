import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Update, Message, Chat, Document, File
from db.tests.test_db_types import TestSerializedMessage
from typing import Dict
from datetime import datetime

import json

from bot.responses import start, help, history


class TestResponses(unittest.IsolatedAsyncioTestCase):
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
        "bot.responses.bot_messages",
        {
            "start_user": "Welcome, {}!",
            "help": "Help message for {}, {}",
            "response": "{}: {}",
            "no_tagged_question": "No tagged question.",
            "respond_to_question": "Responding to question: {}",
        },
    )
    @patch("bot.responses.store_message_to_db")
    async def test_start(self, mock_store_message_to_db: AsyncMock) -> None:
        self.context.bot.send_message = AsyncMock()

        await start(self.update, self.context)

        self.context.bot.send_message.assert_awaited_once_with(
            chat_id=12345,
            text="Welcome, TestUser!",
            parse_mode="markdown",
        )

    @patch("bot.responses.store_message_to_db")
    @patch(
        "bot.responses.bot_messages",
        {
            "start_user": "Welcome, {}!",
            "help": "Help message for {}, {}",
            "response": "{}: {}",
            "no_tagged_question": "No tagged question.",
            "respond_to_question": "Responding to question: {}",
        },
    )
    async def test_help(self, mock_store_message_to_db: AsyncMock) -> None:
        self.context.bot.send_message = AsyncMock()

        await help(self.update, self.context)

        self.context.bot.send_message.assert_awaited_once_with(
            chat_id=12345,
            text="Help message for TestUser, ",
            parse_mode="markdown",
        )

    @patch("bot.responses.store_message_to_db")
    @patch("bot.responses.handle_message")
    async def test_handle_edited_message(
        self, mock_handle_message: AsyncMock, mock_store_message_to_db: AsyncMock
    ) -> None:
        # Create a Chat object
        chat = Chat(id=12345, type="private", first_name="TestUser")

        # Create an edited Message object
        edited_message = Message(
            message_id=1,
            date=datetime.now(),
            chat=chat,
            text="Edited Test",
        )

        # Create an Update object with the edited message
        update = Update(
            update_id=1,
            edited_message=edited_message,
        )

        # Set up the context mock
        context: AsyncMock = AsyncMock()

        # Call the handle_message function with the edited message
        await mock_handle_message(update, context)

        # Assert that the handle_message function was called with the edited message
        mock_handle_message.assert_awaited_once_with(update, context)

        # Assert that the store_message_to_db function was called with the correct parameters
        mock_store_message_to_db.assert_awaited_once_with(
            chat_id=12345,
            msg=TestSerializedMessage(edited_message),
        )


class TestHistory(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        chat = Chat(
            id=12345, type="private", first_name="TestUser"
        )  # Create a Chat object with first_name
        self.history = {
            "name": "TestGroup",
            "type": "private_group",
            "id": 12349,
            "messages": [
                {
                    "id": 1,
                    "date": "2021-09-07T14:40:00",
                    "from": "TestUser Lastname",
                    "from_id": "user12345",
                    "text": "Test",
                    "text_entities": [{"type": "plain", "text": "Test"}],
                },
                {
                    "id": 2,
                    "date": "2021-09-07T14:40:00",
                    "from": "TestUser2 Lastname",
                    "from_id": "user12346",
                    "text": "Test 2",
                    "text_entities": [{"type": "plain", "text": "Test 2"}],
                },
            ],
        }
        self.update: Update = Update(
            update_id=1,
            message=Message(
                message_id=1,
                date=datetime.now(),
                chat=chat,
                text="",
                document=Document(
                    "1",
                    "1",
                    "history.json",
                    "application/json",
                    50 * 1024,
                ),
            ),
        )
        self.context: AsyncMock = AsyncMock()
        self.context.bot.send_message = AsyncMock()
        return_file = MagicMock()
        return_file.file_id = "1"
        return_file.file_unique_id = "1"
        return_file.file_size = 50 * 1024
        return_file.download_to_memory = AsyncMock(
            side_effect=lambda f: f.write(json.dumps(self.history).encode("utf-8"))
        )
        self.context.bot.get_file = AsyncMock(return_value=return_file)

    @patch(
        "bot.responses.bot_messages",
        {
            "history_empty": "History is empty.",
            "history_too_big": "History is too big.",
            "history_invalid": "History is invalid.",
            "history_upload_success": "History uploaded successfully.",
        },
    )
    @patch("bot.responses.batch_embed_messages")
    @patch("bot.responses.store_multiple_messages_to_db")
    @patch("bot.responses.batch_upload_vectors")
    async def test_history(
        self,
        mock_batch_upload_vectors: MagicMock,
        mock_store_multiple_messages_to_db: MagicMock,
        mock_batch_embed_messages: MagicMock,
    ) -> None:
        mock_batch_embed_messages.return_value = [
            [
                [0.1, 0.2],
                [0.2, 0.3],
            ],
        ]
        await history(self.update, self.context)
        self.context.bot.send_message.assert_awaited_once_with(
            chat_id=12345,
            text="History uploaded successfully.",
        )
