import unittest
from unittest.mock import patch, MagicMock
import vectordb


class TestVectorDB(unittest.TestCase):
    @patch("vectordb.pinecone.Index")
    def test_batch_upload_vectors(self, mock_index):
        # Arrange
        mock_embeddings = [{"id": "1", "values": [0.1, 0.2], "metadata": {}}] * 250
        vectordb.upload_vectors = MagicMock()

        # Act
        vectordb.batch_upload_vectors(mock_index, mock_embeddings)

        # Assert
        self.assertEqual(vectordb.upload_vectors.call_count, 3)

    @patch("vectordb.pinecone.Index")
    def test_query(self, mock_index):
        # Arrange
        mock_query_vector = [0.1, 0.2]
        mock_index.query.return_value = {"matches": [], "total": 0, "namespace": "test"}

        # Act
        result = vectordb.query(mock_index, mock_query_vector, top_k=5)

        # Assert
        self.assertEqual(result, {"matches": [], "total": 0, "namespace": "test"})

    @patch("vectordb.pinecone")
    def test_delete(self, mock_pinecone):
        # Arrange
        index_name = "test_index"

        # Act
        vectordb.delete(index_name)

        # Assert
        mock_pinecone.delete_index.assert_called_once_with(name=index_name)
