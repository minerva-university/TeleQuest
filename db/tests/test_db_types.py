import unittest
import json
from bot.telegram_types import TMessage
from db.db_types import (
    GroupChat,
    PCEmbeddingMetadata,
    PCEmbeddingData,
    PCQueryResult,
    PCQueryResults,
    AddMessageResult,
    SerializedMessage,
)
from datetime import datetime
from telegram import Message, Chat, User


class TestDbTypes(unittest.TestCase):
    def test_group_chat_type(self) -> None:
        # Create a mock GroupChat instance without including the optional 'messages' field
        group_chat: GroupChat = GroupChat(
            chat_id=12345,
            group_name="Test Group",
            categories=["category1", "category2"]
            # 'messages' field is omitted
        )
        self.assertIsInstance(group_chat, dict)

    def test_pc_embedding_metadata_type(self) -> None:
        pc_embedding_metadata: PCEmbeddingMetadata = PCEmbeddingMetadata(
            category="test_category",
            chat_id=12345,
        )
        self.assertIsInstance(pc_embedding_metadata, dict)

    def test_pc_embedding_data_type(self) -> None:
        # Providing valid values for all fields including 'metadata'
        metadata: PCEmbeddingMetadata = PCEmbeddingMetadata(
            category="test_category", chat_id=23456
        )
        pc_embedding_data: PCEmbeddingData = PCEmbeddingData(
            id="data1", values=[0.1, 0.2, 0.3], metadata=metadata
        )
        self.assertIsInstance(pc_embedding_data, dict)

    def test_pc_query_result_type(self) -> None:
        # Providing valid values for all fields including 'metadata'
        metadata: PCEmbeddingMetadata = PCEmbeddingMetadata(
            category="test_category", chat_id=23456
        )
        pc_query_result: PCQueryResult = PCQueryResult(
            id="result1", score=0.8, values=[0.1, 0.2, 0.3], metadata=metadata
        )
        self.assertIsInstance(pc_query_result, dict)

    def test_pc_query_results_type(self) -> None:
        pc_query_results: PCQueryResults = PCQueryResults(
            matches=[], total=10, namespace="namespace1"
        )
        self.assertIsInstance(pc_query_results, dict)

    def test_add_message_result_type(self) -> None:
        self.assertTrue(AddMessageResult.SUCCESS in AddMessageResult)
        self.assertTrue(AddMessageResult.FAILURE in AddMessageResult)
        self.assertTrue(AddMessageResult.EXISTING in AddMessageResult)
        self.assertTrue(AddMessageResult.UPDATED in AddMessageResult)

        self.assertIsInstance(AddMessageResult.SUCCESS, AddMessageResult)
        self.assertIsInstance(AddMessageResult.FAILURE, AddMessageResult)
        self.assertIsInstance(AddMessageResult.EXISTING, AddMessageResult)
        self.assertIsInstance(AddMessageResult.UPDATED, AddMessageResult)


class TestSerializedMessage(unittest.TestCase):
    def setUp(self) -> None:
        self.user = User(id=123, first_name="Test", is_bot=False)
        self.chat = Chat(id=12345, type="group", title="Test Group")
        self.message = Message(
            message_id=1,
            date=datetime.now(),
            from_user=self.user,
            chat=self.chat,
            text="Test message",
        )
        self.serialized_message = SerializedMessage(self.message)

    def test_serialized_message_init(self) -> None:
        self.assertEqual(self.serialized_message.id, self.message.message_id)
        self.assertEqual(
            self.serialized_message.from_user, json.loads(self.user.to_json())
        )
        self.assertEqual(self.serialized_message.date, self.message.date)
        self.assertEqual(self.serialized_message.reply_to_message, None)
        self.assertEqual(self.serialized_message.text, self.message.text)
        self.assertEqual(self.serialized_message.photo, ())
        self.assertIsNone(self.serialized_message.video)
        self.assertIsNone(self.serialized_message.voice)
        self.assertEqual(self.serialized_message.chat_title, self.chat.title)

    def test_get_serialized_without_id(self) -> None:
        serialized_without_id = self.serialized_message.get_as_tmessage()
        expected_result: TMessage = {
            "id": self.message.message_id,
            "from_user": json.loads(self.user.to_json()),
            "date": self.message.date,
            "reply_to_message": None,
            "text": self.message.text,
            "chat_title": self.chat.title,
        }
        self.assertEqual(serialized_without_id, expected_result)

    def test_get_id(self) -> None:
        self.assertEqual(self.serialized_message.get_id(), self.message.message_id)
