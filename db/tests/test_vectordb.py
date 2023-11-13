import unittest
from unittest.mock import patch, MagicMock
from vectordb import batch_upload_vectors, query, delete, upload_vectors


class TestVectorDB(unittest.TestCase):
    @patch("vectordb.pinecone.Index")
    def test_upload_vectors(self, mock_index):
        # Arrange
        mock_embeddings = [{"id": "1", "values": [0.1, 0.2], "metadata": {}}]
        mock_index.upsert = MagicMock()

        # Act
        upload_vectors(mock_index, mock_embeddings)

        # Assert
        mock_index.upsert.assert_called_once_with(vectors=mock_embeddings)

    @patch("vectordb.init_pinecone", return_value=MagicMock())
    @patch("vectordb.upload_vectors")
    def test_batch_upload_vectors(self, mock_upload_vectors, mock_init_pinecone):
        # Arrange
        mock_embeddings = [{"id": "1", "values": [0.1, 0.2], "metadata": {}}] * 250
        mock_index = MagicMock()

        # Act
        batch_upload_vectors(mock_index, mock_embeddings)

        # Assert
        self.assertEqual(mock_upload_vectors.call_count, 3)
        mock_init_pinecone.assert_not_called()

    @patch("vectordb.init_pinecone", return_value=MagicMock())
    @patch("vectordb.pinecone.Index")
    def test_query(self, mock_index, mock_init_pinecone):
        # Arrange
        mock_query_vector = [0.1, 0.2]
        mock_index.query.return_value = {"matches": [], "total": 0, "namespace": "test"}

        # Act
        result = query(mock_index, mock_query_vector, top_k=5)

        # Assert
        self.assertEqual(result, {"matches": [], "total": 0, "namespace": "test"})
        mock_init_pinecone.assert_not_called()

    @patch("vectordb.init_pinecone", return_value=MagicMock())
    @patch("vectordb.pinecone")
    def test_delete(self, mock_pinecone, mock_init_pinecone):
        # Arrange
        index_name = "test_index"

        # Act
        delete(index_name)

        # Assert
        mock_pinecone.delete_index.assert_called_once_with(name=index_name)
        mock_init_pinecone.assert_not_called()
