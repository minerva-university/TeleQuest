import unittest
from unittest.mock import patch, MagicMock
from telegram import Message
from database import store_message_to_db, AddMessageResult
from typing import Any


class TestStoreMessageToDb(unittest.TestCase):
    @patch("database.db")
    @patch("telegram.Message")
    def test_store_new_message(
        self, mock_message: MagicMock, mock_db: MagicMock
    ) -> None:
        # Mock setup for a new message
        mock_message.configure_mock(
            **{
                "from_user.to_json.return_value": '{"id": 123, "name": "Test User"}',
                "chat.title": "Test Chat",
                "reply_to_message": None,
                "date": "2021-01-01",
                "message_id": 1,
                "text": "Hello",
                "photo": None,
                "video": None,
                "voice": None,
            }
        )
        mock_db.active_groups.find_one.return_value = None
        update_one_return: MagicMock = MagicMock(
            acknowledged=True, matched_count=1, modified_count=1
        )
        mock_db.active_groups.update_one.return_value = update_one_return

        # Act
        result: AddMessageResult = store_message_to_db(chat_id=12345, msg=mock_message)

        # Assert
        self.assertEqual(result, AddMessageResult.SUCCESS)

    @patch("database.db")
    @patch("telegram.Message")
    def test_store_existing_message(
        self, mock_message: MagicMock, mock_db: MagicMock
    ) -> None:
        # Mock setup for an existing message
        mock_message.configure_mock(
            **{
                "message_id": 1,
                "chat.title": "Test Chat",
                "from_user.to_json.return_value": '{"id": 123, "name": "Test User"}',
                "date": "2021-01-01",
                "reply_to_message": None,
            }
        )
        mock_db.active_groups.find_one.side_effect = [
            True,  # First call for checking group chat existence
            True,  # Second call for checking message existence
        ]

        # Act
        result: AddMessageResult = store_message_to_db(chat_id=12345, msg=mock_message)

        # Assert
        self.assertEqual(result, AddMessageResult.EXISTING)

    @patch("database.db")
    @patch("telegram.Message")
    def test_store_message_failure(
        self, mock_message: MagicMock, mock_db: MagicMock
    ) -> None:
        # Mock setup for failure scenario
        mock_message.configure_mock(
            **{
                "message_id": 1,
                "chat.title": "Test Chat",
                "from_user.to_json.return_value": '{"id": 123, "name": "Test User"}',
                "date": "2021-01-01",
                "reply_to_message": None,
            }
        )
        mock_db.active_groups.find_one.return_value = None
        update_one_return: MagicMock = MagicMock(
            acknowledged=False, matched_count=0, modified_count=0
        )
        mock_db.active_groups.update_one.return_value = update_one_return

        # Act
        result: AddMessageResult = store_message_to_db(chat_id=12345, msg=mock_message)

        # Assert
        self.assertEqual(result, AddMessageResult.FAILURE)
