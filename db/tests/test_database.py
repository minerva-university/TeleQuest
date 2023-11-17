import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch
from telegram import Chat, Message, User
from typing import List
from db.database import store_multiple_messages_to_db, store_message_to_db
from db.db_types import AddMessageResult, SerializedMessage


class TestDatabase(unittest.TestCase):
    def setUp(self) -> None:
        self.chat_id = 12345
        self.user = User(id=123, first_name="Test", is_bot=False)
        self.chat = Chat(id=self.chat_id, type="group", title="Test Group")
        self.message = Message(
            message_id=1,
            date=datetime.now(),
            from_user=self.user,
            chat=self.chat,
            text="Test message",
        )
        self.serialized_message = SerializedMessage(self.message)

    @patch("db.database.db")
    def test_store_message_to_db_new(self, mock_db: MagicMock) -> None:
        mock_db.active_groups.find_one.side_effect = [None, None]
        mock_db.active_groups.insert_one.return_value = MagicMock()
        mock_db.active_groups.update_one.return_value = MagicMock(
            acknowledged=True, matched_count=1, modified_count=1
        )

        result = store_message_to_db(self.chat_id, self.serialized_message)
        self.assertEqual(result, AddMessageResult.SUCCESS)

    @patch("db.database.db")
    def test_store_message_to_db_existing(self, mock_db: MagicMock) -> None:
        mock_db.active_groups.find_one.side_effect = [True, True]

        result = store_message_to_db(self.chat_id, self.serialized_message)
        self.assertEqual(result, AddMessageResult.EXISTING)

    @patch("db.database.db")
    def test_store_message_to_db_failure(self, mock_db: MagicMock) -> None:
        mock_db.active_groups.find_one.side_effect = [None, None]
        mock_db.active_groups.insert_one.return_value = MagicMock()
        mock_db.active_groups.update_one.return_value = MagicMock(acknowledged=False)

        result = store_message_to_db(self.chat_id, self.serialized_message)
        self.assertEqual(result, AddMessageResult.FAILURE)

    @patch("db.database.db")
    def test_store_message_to_db_new_group(self, mock_db: MagicMock) -> None:
        mock_db.active_groups.find_one.return_value = None
        mock_db.active_groups.insert_one.return_value = MagicMock()
        mock_db.active_groups.update_one.return_value = MagicMock(
            acknowledged=True, matched_count=1, modified_count=1
        )

        result = store_message_to_db(self.chat_id, self.serialized_message)
        self.assertEqual(result, AddMessageResult.SUCCESS)

    @patch("db.database.db")
    def test_store_message_to_db_existing_message(self, mock_db: MagicMock) -> None:
        mock_db.active_groups.find_one.return_value = {
            "chat_id": self.chat_id,
            "group_name": self.chat.title,
            "categories": [],
            "messages": {self.message.message_id: self.message.to_dict()},
        }

        result = store_message_to_db(self.chat_id, self.serialized_message)
        self.assertEqual(result, AddMessageResult.EXISTING)


class TestStoreMessagesToDB(unittest.TestCase):
    def setUp(self) -> None:
        self.chat_id = 12345
        self.user = User(id=123, first_name="Test", is_bot=False)
        self.chat = Chat(id=self.chat_id, type="group", title="Test Group")
        self.message_1 = Message(
            message_id=1,
            date=datetime.now(),
            from_user=self.user,
            chat=self.chat,
            text="Test message 1",
        )
        self.message_2 = Message(
            message_id=2,
            date=datetime.now(),
            from_user=self.user,
            chat=self.chat,
            text="Test message 2",
        )
        self.serialized_messages = [
            SerializedMessage(self.message_1),
            SerializedMessage(self.message_2),
        ]

    @patch("db.database.db")
    def test_store_multiple_messages_to_db(self, mock_db: MagicMock) -> None:
        mock_db.active_groups.find_one.side_effect = [None, None]
        mock_db.active_groups.insert_one.return_value = MagicMock()
        mock_db.active_groups.update_one.return_value = MagicMock(
            acknowledged=True, matched_count=1, modified_count=1
        )

        result = store_multiple_messages_to_db(self.chat_id, self.serialized_messages)
        self.assertEqual(result, AddMessageResult.SUCCESS)
