import json
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Update, Message, Chat, Document, User
from datetime import datetime
from bot.responses import start, help, history, handle_message
from datetime import datetime
from typing import Optional, Any


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
    async def test_handle_edited_message(
        self, mock_store_message_to_db: AsyncMock
    ) -> None:
        # Create a Chat object
        chat = Chat(id=12345, type="private", title="Test Chat")

        # Create an edited Message object
        edited_message = Message(
            message_id=1,
            date=datetime.now(),
            chat=chat,
            text="Edited Test",
            from_user=User(id=123, first_name="TestUser", is_bot=False),
        )

        # Create an Update object with the edited message
        update = Update(
            update_id=1,
            edited_message=edited_message,
        )

        # Call the handle_message function with the edited message
        await handle_message(update, self.context)

        # Check if store_message_to_db was called at least once
        self.assertTrue(
            mock_store_message_to_db.called, "store_message_to_db was not called"
        )

        # Extract the actual arguments used in the call to store_message_to_db
        args, _ = mock_store_message_to_db.call_args

        # Verify the chat_id argument
        self.assertEqual(
            args[0], 12345, "Incorrect chat_id passed to store_message_to_db"
        )

        # Verify attributes of the SerializedMessage object
        actual_serialized_message = args[1]
        self.assertEqual(
            actual_serialized_message.id,
            edited_message.message_id,
            "Incorrect message ID",
        )
        self.assertEqual(
            actual_serialized_message.text,
            edited_message.text,
            "Incorrect message text",
        )
        if edited_message.from_user is not None:
            self.assertEqual(
                actual_serialized_message.from_user["id"],
                edited_message.from_user.id,
                "Incorrect user ID",
            )
            self.assertEqual(
                actual_serialized_message.from_user["first_name"],
                edited_message.from_user.first_name,
                "Incorrect user first name",
            )
        self.assertEqual(
            actual_serialized_message.date,
            edited_message.date,
            "Incorrect message date",
        )
        self.assertIsNone(
            actual_serialized_message.reply_to_message, "Incorrect reply_to_message"
        )
        self.assertEqual(
            actual_serialized_message.chat_title,
            edited_message.chat.title,
            "Incorrect chat title",
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


class TestHandleMessage(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.user = User(id=123, first_name="TestUser", is_bot=False)
        self.chat = Chat(id=12345, type="private", first_name="TestUser")
        self.context = MagicMock()
        self.context.bot.send_message = AsyncMock()

    def create_message(
        self,
        text: Optional[str],
        user: Optional[User] = None,
        chat: Optional[Chat] = None,
        **kwargs: Any
    ) -> Message:
        return Message(
            message_id=1,
            date=datetime.now(),
            chat=chat or self.chat,
            text=text,
            from_user=user or self.user,
            **kwargs
        )

    @patch("bot.responses.store_message_to_db", return_value=True)
    @patch("bot.responses.upload_vectors")
    async def test_message_with_no_text(
        self, mock_store_message: MagicMock, mock_upload: MagicMock
    ) -> None:
        update = Update(update_id=1, message=self.create_message(None, user=self.user))
        await handle_message(update, self.context)
        self.context.bot.send_message.assert_not_called()

    @patch("bot.responses.store_message_to_db", return_value=True)
    @patch("bot.responses.upload_vectors")
    async def test_message_with_no_command_and_no_reply(
        self, mock_store_message: MagicMock, mock_upload: MagicMock
    ) -> None:
        text = "Hello, how are you?"
        update = Update(update_id=1, message=self.create_message(text, user=self.user))
        await handle_message(update, self.context)
        self.context.bot.send_message.assert_not_called()

    @patch("bot.responses.store_message_to_db", return_value=True)
    @patch("bot.responses.upload_vectors")
    async def test_message_with_media(
        self, mock_store_message: MagicMock, mock_upload: MagicMock
    ) -> None:
        update = Update(
            update_id=1,
            message=self.create_message(None, photo=[MagicMock()], user=self.user),
        )
        await handle_message(update, self.context)
        self.context.bot.send_message.assert_not_called()

    @patch("bot.responses.store_message_to_db", return_value=True)
    @patch("bot.responses.upload_vectors")
    async def test_message_from_a_bot(
        self, mock_store_message: MagicMock, mock_upload: MagicMock
    ) -> None:
        bot_user = User(id=124, first_name="BotUser", is_bot=True)
        update = Update(
            update_id=1, message=self.create_message("Message from bot", user=bot_user)
        )
        await handle_message(update, self.context)
        self.context.bot.send_message.assert_not_called()

    @patch("bot.responses.store_message_to_db", return_value=True)
    @patch("bot.responses.upload_vectors")
    async def test_forwarded_message(
        self, mock_store_message: MagicMock, mock_upload: MagicMock
    ) -> None:
        update = Update(
            update_id=1,
            message=self.create_message(
                "Forwarded message", forward_from=self.user, user=self.user
            ),
        )
        await handle_message(update, self.context)
        self.context.bot.send_message.assert_not_called()

    @patch("bot.responses.store_message_to_db", return_value=True)
    @patch("bot.responses.upload_vectors")
    async def test_message_with_mention_or_hashtag(
        self, mock_store_message: MagicMock, mock_upload: MagicMock
    ) -> None:
        update = Update(
            update_id=1,
            message=self.create_message("Hello @user #test", user=self.user),
        )
        await handle_message(update, self.context)
        self.context.bot.send_message.assert_not_called()

    @patch("bot.responses.store_message_to_db", return_value=True)
    @patch("bot.responses.upload_vectors")
    async def test_replying_to_previous_bot_message(
        self, mock_store_message: MagicMock, mock_upload: MagicMock
    ) -> None:
        original_message = self.create_message("Original message", user=self.user)
        update = Update(
            update_id=1,
            message=self.create_message(
                "Replying to bot message",
                reply_to_message=original_message,
                user=self.user,
            ),
        )
        await handle_message(update, self.context)
        self.context.bot.send_message.assert_not_called()
