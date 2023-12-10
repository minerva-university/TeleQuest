import unittest
from unittest.mock import patch, MagicMock
from db.vectordb import (
    batch_upload_vectors,
    upload_vectors,
    query,
    delete,
    init_pinecone,
)
from db.db_types import PCEmbeddingData, PCEmbeddingMetadata, PCQueryResults


class TestVectorDB(unittest.TestCase):
    @patch("db.vectordb.pinecone.Index")
    def test_upload_vectors(self, mock_index_class: MagicMock) -> None:
        metadata: PCEmbeddingMetadata = PCEmbeddingMetadata(
            category="test_category", chat_id=12345
        )
        mock_embeddings: list[PCEmbeddingData] = [
            PCEmbeddingData(id="1", values=[0.1, 0.2], metadata=metadata)
        ]
        mock_index = mock_index_class.return_value
        mock_index.upsert = MagicMock()

        upload_vectors(mock_embeddings, mock_index)
        mock_index.upsert.assert_called_once_with(vectors=mock_embeddings)

    @patch("db.vectordb.init_pinecone", return_value=MagicMock())
    @patch("db.vectordb.upload_vectors")
    def test_batch_upload_vectors(
        self, mock_upload_vectors: MagicMock, mock_init_pinecone: MagicMock
    ) -> None:
        metadata: PCEmbeddingMetadata = PCEmbeddingMetadata(
            category="test_category", chat_id=12345
        )
        mock_embeddings: list[PCEmbeddingData] = [
            PCEmbeddingData(id="1", values=[0.1, 0.2], metadata=metadata)
        ] * 250
        mock_index = MagicMock()

        batch_upload_vectors(mock_embeddings, mock_index)
        self.assertEqual(mock_upload_vectors.call_count, 3)
        mock_init_pinecone.assert_not_called()

    @patch("db.vectordb.pinecone.Index")
    def test_query(self, mock_index_class: MagicMock) -> None:
        mock_response = {"matches": [], "total": 0, "namespace": "test"}
        mock_index = mock_index_class.return_value
        mock_index.query.return_value = mock_response

        result = query(12345, [0.1, 0.2], 5, mock_index)
        self.assertIsInstance(result, dict)
        self.assertEqual(result, mock_response)
        mock_index.query.assert_called_once_with(
            vector=[0.1, 0.2], top_k=5, filter={"chat_id": {"$eq": 12345}}
        )

    @patch("db.vectordb.pinecone")
    def test_delete(self, mock_pinecone: MagicMock) -> None:
        delete("test_index")
        mock_pinecone.delete_index.assert_called_once_with(name="test_index")

    @patch("db.vectordb.os.getenv")
    @patch("db.vectordb.pinecone")
    def test_init_pinecone(
        self, mock_pinecone: MagicMock, mock_getenv: MagicMock
    ) -> None:
        mock_getenv.return_value = "TEST"
        self.assertIsNone(init_pinecone())

        mock_getenv.return_value = "PROD"
        mock_pinecone.init = MagicMock()
        mock_pinecone.Index.return_value = MagicMock()
        mock_pinecone.list_indexes.return_value = ["test_index"]

        self.assertIsNotNone(init_pinecone())
        mock_pinecone.init.assert_called()
