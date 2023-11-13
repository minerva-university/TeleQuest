import unittest
from unittest.mock import patch, MagicMock
from telegram import Message
from database import store_message_to_db
from pymongo.collection import Collection


class TestStoreMessageToDb(unittest.TestCase):
    @patch("database.db")
    @patch("telegram.Message")
    def test_store_new_message(
        self, mock_message: MagicMock, mock_db: MagicMock
    ) -> None:
        # Mocking the message object
        mock_message.from_user.to_json.return_value = '{"id": 123, "name": "Test User"}'
        mock_message.chat.title = "Test Chat"
        mock_message.reply_to_message = None
        mock_message.date = "2021-01-01"
        mock_message.message_id = 1

        # Mocking the database behavior
        mock_db.active_groups.find_one.return_value = None
        mock_db.active_groups.insert_one.return_value = MagicMock()
        update_one_return = MagicMock(
            acknowledged=True, matched_count=1, modified_count=1
        )
        mock_db.active_groups.update_one.return_value = update_one_return

        # Call the function with the mock message
        result = store_message_to_db(chat_id=12345, msg=mock_message)
        self.assertTrue(result)
