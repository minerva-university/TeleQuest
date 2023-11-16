import unittest
from unittest.mock import patch, MagicMock

from db.vectordb import batch_upload_vectors, query, delete, upload_vectors
from db.db_types import PCEmbeddingData, PCEmbeddingMetadata
from typing import List


class TestVectorDB(unittest.TestCase):
    @patch("vectordb.pinecone.Index")
    def test_upload_vectors(self, mock_index: MagicMock) -> None:
        # Arrange
        metadata: PCEmbeddingMetadata = {"category": "test_category"}
        mock_embeddings: List[PCEmbeddingData] = [
            PCEmbeddingData(id="1", values=[0.1, 0.2], metadata=metadata)
        ]
        mock_index.upsert = MagicMock()

        # Act
        upload_vectors(mock_index, mock_embeddings)

        # Assert
        mock_index.upsert.assert_called_once_with(vectors=mock_embeddings)

    @patch("vectordb.init_pinecone", return_value=MagicMock())
    @patch("vectordb.upload_vectors")
    def test_batch_upload_vectors(
        self, mock_upload_vectors: MagicMock, mock_init_pinecone: MagicMock
    ) -> None:
        # Arrange
        metadata: PCEmbeddingMetadata = {"category": "test_category"}
        mock_embeddings: List[PCEmbeddingData] = [
            PCEmbeddingData(id="1", values=[0.1, 0.2], metadata=metadata)
        ] * 250
        mock_index = MagicMock()

        # Act
        batch_upload_vectors(mock_index, mock_embeddings)

        # Assert
        self.assertEqual(mock_upload_vectors.call_count, 3)
        mock_init_pinecone.assert_not_called()

    @patch("vectordb.init_pinecone", return_value=MagicMock())
    @patch("vectordb.pinecone.Index")
    def test_query(self, mock_index: MagicMock, mock_init_pinecone: MagicMock) -> None:
        # Arrange
        mock_query_vector: List[float] = [0.1, 0.2]
        mock_index.query.return_value = {"matches": [], "total": 0, "namespace": "test"}

        # Act
        result = query(mock_index, mock_query_vector, top_k=5)

        # Assert
        self.assertEqual(result, {"matches": [], "total": 0, "namespace": "test"})
        mock_init_pinecone.assert_not_called()

    @patch("vectordb.init_pinecone", return_value=MagicMock())
    @patch("vectordb.pinecone")
    def test_delete(
        self, mock_pinecone: MagicMock, mock_init_pinecone: MagicMock
    ) -> None:
        # Arrange
        index_name: str = "test_index"

        # Act
        delete(index_name)

        # Assert
        mock_pinecone.delete_index.assert_called_once_with(name=index_name)
        mock_init_pinecone.assert_not_called()
