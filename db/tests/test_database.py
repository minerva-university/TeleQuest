import unittest
from unittest.mock import patch, MagicMock
from db.database import store_message_to_db, client, db
from db.db_types import AddMessageResult
from telegram import Message, User, Chat
from datetime import datetime


class TestDatabase(unittest.TestCase):
    def setUp(self) -> None:
        self.chat_id = 12345
        self.user = User(id=123, first_name="Test", is_bot=False)
        self.chat = Chat(id=self.chat_id, type="group", title="Test Group")
        self.message = Message(
            message_id=1,
            date=datetime.now(),  # Use the current datetime
            from_user=self.user,
            chat=self.chat,
            text="Test message",
        )

    @patch("db.database.db")
    def test_store_message_to_db_new(self, mock_db: MagicMock) -> None:
        # Setup for a scenario where the message is new (not existing in the DB)
        mock_db.active_groups.find_one.side_effect = [None, None]
        mock_db.active_groups.insert_one.return_value = MagicMock()
        mock_db.active_groups.update_one.return_value = MagicMock(
            acknowledged=True, matched_count=1, modified_count=1
        )

        result = store_message_to_db(self.chat_id, self.message)
        self.assertEqual(result, AddMessageResult.SUCCESS)

    @patch("db.database.db")
    def test_store_message_to_db_existing(self, mock_db: MagicMock) -> None:
        # Setup for a scenario where the message already exists
        mock_db.active_groups.find_one.side_effect = [True, True]

        result = store_message_to_db(self.chat_id, self.message)
        self.assertEqual(result, AddMessageResult.EXISTING)

    @patch("db.database.db")
    def test_store_message_to_db_failure(self, mock_db: MagicMock) -> None:
        # Setup for a scenario where storing the message fails
        mock_db.active_groups.find_one.side_effect = [None, None]
        mock_db.active_groups.insert_one.return_value = MagicMock()
        mock_db.active_groups.update_one.return_value = MagicMock(acknowledged=False)

        result = store_message_to_db(self.chat_id, self.message)
        self.assertEqual(result, AddMessageResult.FAILURE)
