import unittest
from db_types import (
    GroupChat,
    PCEmbeddingMetadata,
    PCEmbeddingData,
    PCQueryResult,
    PCQueryResults,
    AddMessageResult,
)


class TestDbTypes(unittest.TestCase):
    def test_group_chat_type(self) -> None:
        # Create a mock GroupChat instance
        group_chat: GroupChat = GroupChat(
            chat_id=12345,
            group_name="Test Group",
            categories=["category1", "category2"],
            messages=None,  # Assuming Collection[TMessage] is a complex type to mock
        )
        self.assertIsInstance(group_chat, dict)

    def test_pc_embedding_metadata_type(self) -> None:
        pc_embedding_metadata: PCEmbeddingMetadata = PCEmbeddingMetadata(
            category="test_category"
        )
        self.assertIsInstance(pc_embedding_metadata, dict)

    def test_pc_embedding_data_type(self) -> None:
        pc_embedding_data: PCEmbeddingData = PCEmbeddingData(
            id="data1", values=[0.1, 0.2, 0.3], metadata=None
        )
        self.assertIsInstance(pc_embedding_data, dict)

    def test_pc_query_result_type(self) -> None:
        pc_query_result: PCQueryResult = PCQueryResult(
            id="result1", score=0.8, values=[0.1, 0.2, 0.3], metadata=None
        )
        self.assertIsInstance(pc_query_result, dict)

    def test_pc_query_results_type(self) -> None:
        pc_query_results: PCQueryResults = PCQueryResults(
            matches=[], total=10, namespace="namespace1"
        )
        self.assertIsInstance(pc_query_results, dict)

    def test_add_message_result_type(self) -> None:
        # Check that all expected members are present in AddMessageResult
        self.assertTrue(AddMessageResult.SUCCESS in AddMessageResult)
        self.assertTrue(AddMessageResult.FAILURE in AddMessageResult)
        self.assertTrue(AddMessageResult.EXISTING in AddMessageResult)

        # Check that members are of the correct enum type
        self.assertIsInstance(AddMessageResult.SUCCESS, AddMessageResult)
        self.assertIsInstance(AddMessageResult.FAILURE, AddMessageResult)
        self.assertIsInstance(AddMessageResult.EXISTING, AddMessageResult)
