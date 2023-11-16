import unittest
from unittest.mock import patch, MagicMock
from db.vectordb import batch_upload_vectors, upload_vectors, query, delete
from db.db_types import PCEmbeddingData, PCEmbeddingMetadata, PCQueryResults
import pinecone


class TestVectorDB(unittest.TestCase):
    @patch("db.vectordb.pinecone.Index")
    def test_upload_vectors(self, mock_index: MagicMock) -> None:
        # Arrange
        metadata: PCEmbeddingMetadata = {"category": "test_category"}
        mock_embeddings: list[PCEmbeddingData] = [
            PCEmbeddingData(id="1", values=[0.1, 0.2], metadata=metadata)
        ]
        mock_index.upsert = MagicMock()

        # Act
        upload_vectors(mock_index, mock_embeddings)

        # Assert
        mock_index.upsert.assert_called_once_with(vectors=mock_embeddings)

    @patch("db.vectordb.init_pinecone", return_value=MagicMock())
    @patch("db.vectordb.upload_vectors")
    def test_batch_upload_vectors(
        self, mock_upload_vectors: MagicMock, mock_init_pinecone: MagicMock
    ) -> None:
        # Arrange
        metadata: PCEmbeddingMetadata = {"category": "test_category"}
        mock_embeddings: list[PCEmbeddingData] = [
            PCEmbeddingData(id="1", values=[0.1, 0.2], metadata=metadata)
        ] * 250
        mock_index = MagicMock()

        # Act
        batch_upload_vectors(mock_index, mock_embeddings)

        # Assert
        self.assertEqual(mock_upload_vectors.call_count, 3)
        mock_init_pinecone.assert_not_called()

    @patch("db.vectordb.pinecone.Index")
    def test_upload_vectors(self, mock_index_class: MagicMock) -> None:
        # Mock the pinecone.Index instance
        mock_index = mock_index_class.return_value
        mock_index.upsert = MagicMock()

        # Arrange
        metadata: PCEmbeddingMetadata = {"category": "test_category"}
        mock_embeddings: list[PCEmbeddingData] = [
            PCEmbeddingData(id="1", values=[0.1, 0.2], metadata=metadata)
        ]

        # Act
        upload_vectors(mock_index, mock_embeddings)

        # Assert
        mock_index.upsert.assert_called_once_with(vectors=mock_embeddings)

    @patch("db.vectordb.pinecone.Index")
    def test_query(self, mock_index: MagicMock) -> None:
        mock_index.query.return_value = {"matches": [], "total": 0, "namespace": "test"}
        result: PCQueryResults = query(mock_index, [0.1, 0.2])
        self.assertIsInstance(result, dict)

    @patch("db.vectordb.pinecone")
    def test_delete(self, mock_pinecone: MagicMock) -> None:
        delete("test_index")
        mock_pinecone.delete_index.assert_called_once_with(name="test_index")
