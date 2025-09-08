from qdrant_client import QdrantClient

from src.index import embedding_and_indexing
from src.retrieval import retrieve_documents
from src.generate import generate_answer
import config


query = "Can you tell me the origin of the Ring?"

# Setup Qdrant client
client = QdrantClient(
    url=config.QDRANT_URL,
    api_key=config.QDRANT_API_KEY,
    timeout=120.0  # increase timeout for large inserts
)

# Generate vector embedding and store it in Qdrant DB
# embedding_and_indexing(client=client, 
#                        data_dir=config.DATA_DIR, 
#                        collection_name=config.COLLECTION_NAME, 
#                        chunk_size=config.CHUNK_SIZE, 
#                        chunk_overlap=config.CHUNK_OVERLAP)

# Retrieve the results from Qdrant DB
results = retrieve_documents(client=client, 
                             query=query, 
                             collection_name=config.COLLECTION_NAME, 
                             k=3)

# Generate the answer
answer = generate_answer(query=query,
                         results=results)

print(f"Frodo: {query}")
print(f"Galadriel: {answer}")