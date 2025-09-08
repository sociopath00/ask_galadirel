from qdrant_client import QdrantClient

from src.index import embedding_and_indexing
import config


# Setup Qdrant client
client = QdrantClient(
    url=config.QDRANT_URL,
    api_key=config.QDRANT_API_KEY,
    timeout=120.0  # increase timeout for large inserts
)

# embedding_and_indexing(client, config.DATA_DIR, config.COLLECTION_NAME, config.CHUNK_SIZE, config.CHUNK_OVERLAP)

